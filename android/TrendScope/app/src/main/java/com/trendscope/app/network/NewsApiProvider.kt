package com.trendscope.app.network

import android.util.Log
import com.trendscope.app.BuildConfig
import com.trendscope.app.data.Article
import kotlinx.coroutines.*
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withPermit
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONArray
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.TimeUnit

object NewsApiProvider {
    private const val TAG = "NewsApiProvider"
    private const val MAX_ARTICLES = 200
    private const val RSS_PARALLELISM = 8
    private const val RSS_FETCH_TIMEOUT_MS = 25_000L

    private val client = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(20, TimeUnit.SECONDS)
        .followRedirects(true)
        .build()

    fun fetchArticles(): List<Article> {
        val gnewsKey = try { BuildConfig.GNEWS_API_KEY } catch (e: Exception) { "" }
        if (gnewsKey.isNotEmpty()) {
            Log.d(TAG, "Attempting GNews API...")
            try {
                val articles = fetchFromGNews(gnewsKey)
                if (articles.isNotEmpty()) {
                    Log.i(TAG, "GNews returned ${articles.size} articles")
                    return deduplicate(articles)
                }
                Log.w(TAG, "GNews returned 0 articles")
            } catch (e: Exception) {
                Log.e(TAG, "GNews API failed", e)
            }
        } else {
            Log.d(TAG, "GNews API key not configured, skipping")
        }

        val newsApiKey = try { BuildConfig.NEWSAPI_KEY } catch (e: Exception) { "" }
        if (newsApiKey.isNotEmpty()) {
            Log.d(TAG, "Attempting NewsAPI...")
            try {
                val articles = fetchFromNewsApi(newsApiKey)
                if (articles.isNotEmpty()) {
                    Log.i(TAG, "NewsAPI returned ${articles.size} articles")
                    return deduplicate(articles)
                }
                Log.w(TAG, "NewsAPI returned 0 articles")
            } catch (e: Exception) {
                Log.e(TAG, "NewsAPI failed", e)
            }
        } else {
            Log.d(TAG, "NewsAPI key not configured, skipping")
        }

        Log.i(TAG, "Falling back to concurrent RSS feeds")
        val result = fetchRssConcurrent()
        Log.i(TAG, "RSS total: ${result.size} unique articles")
        return result
    }

    private fun fetchRssConcurrent(): List<Article> {
        val allArticles = Collections.synchronizedList(mutableListOf<Article>())
        val feedUrls = mutableListOf<Triple<String, String, String>>()
        for ((category, urls) in DomainFeeds.FEEDS) {
            for (url in urls) {
                val sourceName = try {
                    java.net.URL(url).host.replace("www.", "")
                } catch (e: Exception) { url }
                feedUrls.add(Triple(url, category, sourceName))
            }
        }
        Log.d(TAG, "Fetching ${feedUrls.size} RSS feeds in parallel (${RSS_PARALLELISM} at a time)")

        val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
        val semaphore = Semaphore(RSS_PARALLELISM)
        val jobs = feedUrls.map { (url, category, sourceName) ->
            scope.async {
                semaphore.withPermit {
                    try {
                        val articles = withTimeout(RSS_FETCH_TIMEOUT_MS) {
                            RssParser.fetchAndParse(url, category, sourceName)
                        }
                        Log.d(TAG, "RSS OK [$sourceName]: ${articles.size} articles")
                        articles
                    } catch (e: TimeoutCancellationException) {
                        Log.w(TAG, "RSS TIMEOUT [$sourceName]: $url")
                        emptyList()
                    } catch (e: Exception) {
                        Log.e(TAG, "RSS FAIL [$sourceName]: $url", e)
                        emptyList()
                    }
                }
            }
        }

        var completed = 0
        val total = jobs.size
        runBlocking {
            for (deferred in jobs) {
                try {
                    val articles = deferred.await()
                    for (article in articles) {
                        if (allArticles.none { it.link == article.link }) {
                            allArticles.add(article)
                        }
                    }
                    if (allArticles.size >= MAX_ARTICLES) {
                        Log.i(TAG, "Reached max articles ($MAX_ARTICLES), cancelling remaining feeds")
                        break
                    }
                } catch (e: Exception) {
                    Log.w(TAG, "RSS job failed", e)
                } finally {
                    completed++
                }
            }
        }
        scope.cancel()

        Log.i(TAG, "RSS: $completed/$total feeds processed, ${allArticles.size} unique articles")
        return deduplicate(allArticles.take(MAX_ARTICLES))
    }

    private fun fetchFromGNews(apiKey: String): List<Article> {
        val url = "https://gnews.io/api/v4/top-headlines?token=$apiKey&lang=en&max=50"
        Log.d(TAG, "GET $url")
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "TrendScope/1.0")
            .build()
        val response = client.newCall(request).execute()
        val body = response.body?.string() ?: run {
            Log.w(TAG, "GNews: empty body, code=${response.code}")
            return emptyList()
        }
        if (!response.isSuccessful) {
            Log.w(TAG, "GNews: HTTP ${response.code}: ${body.take(200)}")
            return emptyList()
        }
        return parseGNewsResponse(body)
    }

    private fun parseGNewsResponse(jsonStr: String): List<Article> {
        val root = JSONObject(jsonStr)
        val articlesArr = root.optJSONArray("articles") ?: return emptyList()
        val result = mutableListOf<Article>()
        for (i in 0 until articlesArr.length()) {
            try {
                val obj = articlesArr.getJSONObject(i)
                val title = obj.optString("title", "")
                val url = obj.optString("url", "")
                if (title.isEmpty() || url.isEmpty()) continue
                val desc = obj.optString("description", "")
                val image = obj.optString("image", "")
                val source = obj.optJSONObject("source")?.optString("name", "") ?: "GNews"
                val pubDate = obj.optString("publishedAt", "")
                val dateMillis = RssParser.parseDateToMillis(pubDate)
                val formattedDate = formatDate(pubDate)
                result.add(Article(
                    link = url,
                    title = title,
                    description = desc.take(300),
                    pubDate = formattedDate,
                    imageUrl = image,
                    source = if (source.isNotEmpty()) source else "GNews",
                    category = "Top News",
                    pubDateMillis = dateMillis
                ))
            } catch (e: Exception) {
                Log.w(TAG, "Failed to parse GNews article #$i", e)
            }
        }
        return result
    }

    private fun fetchFromNewsApi(apiKey: String): List<Article> {
        val url = "https://newsapi.org/v2/top-headlines?apiKey=$apiKey&language=en&pageSize=50"
        Log.d(TAG, "GET $url")
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "TrendScope/1.0")
            .build()
        val response = client.newCall(request).execute()
        val body = response.body?.string() ?: run {
            Log.w(TAG, "NewsAPI: empty body, code=${response.code}")
            return emptyList()
        }
        if (!response.isSuccessful) {
            Log.w(TAG, "NewsAPI: HTTP ${response.code}: ${body.take(200)}")
            return emptyList()
        }
        return parseNewsApiResponse(body)
    }

    private fun parseNewsApiResponse(jsonStr: String): List<Article> {
        val root = JSONObject(jsonStr)
        val articlesArr = root.optJSONArray("articles") ?: return emptyList()
        val result = mutableListOf<Article>()
        for (i in 0 until articlesArr.length()) {
            try {
                val obj = articlesArr.getJSONObject(i)
                val title = obj.optString("title", "")
                val url = obj.optString("url", "")
                if (title.isEmpty() || url.isEmpty()) continue
                val desc = obj.optString("description", "")
                val image = obj.optString("urlToImage", "")
                val source = obj.optJSONObject("source")?.optString("name", "") ?: ""
                val author = obj.optString("author", "")
                val pubDate = obj.optString("publishedAt", "")
                val dateMillis = RssParser.parseDateToMillis(pubDate)
                val formattedDate = formatDate(pubDate)
                result.add(Article(
                    link = url,
                    title = title,
                    description = desc.take(300),
                    pubDate = formattedDate,
                    imageUrl = image,
                    source = if (source.isNotEmpty()) source else "NewsAPI",
                    category = "Top News",
                    author = author,
                    pubDateMillis = dateMillis
                ))
            } catch (e: Exception) {
                Log.w(TAG, "Failed to parse NewsAPI article #$i", e)
            }
        }
        return result
    }

    private fun formatDate(dateStr: String): String {
        if (dateStr.isEmpty()) return ""
        val patterns = listOf(
            "yyyy-MM-dd'T'HH:mm:ssXXX",
            "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
            "yyyy-MM-dd'T'HH:mm:ss'Z'",
            "yyyy-MM-dd'T'HH:mm:ssZ",
            "EEE, dd MMM yyyy HH:mm:ss Z"
        )
        for (pattern in patterns) {
            try {
                val sdf = SimpleDateFormat(pattern, Locale.US)
                sdf.timeZone = TimeZone.getTimeZone("UTC")
                val date = sdf.parse(dateStr)
                if (date != null) {
                    val outSdf = SimpleDateFormat("MMM dd, yyyy HH:mm", Locale.US)
                    return outSdf.format(date)
                }
            } catch (_: Exception) { }
        }
        return dateStr.take(30)
    }

    private fun deduplicate(articles: List<Article>): List<Article> {
        val seen = mutableSetOf<String>()
        return articles.filter { seen.add(it.link) }
    }
}
