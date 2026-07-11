package com.trendscope.app.network

import android.util.Log
import com.trendscope.app.data.Article
import okhttp3.OkHttpClient
import okhttp3.Request
import org.xmlpull.v1.XmlPullParser
import org.xmlpull.v1.XmlPullParserFactory
import java.io.StringReader
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.TimeUnit

object RssParser {
    private const val TAG = "RssParser"
    private val client = OkHttpClient.Builder()
        .connectTimeout(8, TimeUnit.SECONDS)
        .readTimeout(10, TimeUnit.SECONDS)
        .followRedirects(true)
        .build()

    fun fetchAndParse(feedUrl: String, category: String, sourceName: String): List<Article> {
        return try {
            val request = Request.Builder().url(feedUrl).header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36").build()
            val response = client.newCall(request).execute()
            if (!response.isSuccessful) {
                Log.w(TAG, "HTTP ${response.code} for $feedUrl")
                return emptyList()
            }
            val xml = response.body?.string()
            if (xml.isNullOrEmpty()) {
                Log.w(TAG, "Empty body from $feedUrl")
                return emptyList()
            }
            val articles = parseRssXml(xml, category, sourceName)
            Log.d(TAG, "$sourceName: ${articles.size} articles")
            articles
        } catch (e: Exception) {
            Log.e(TAG, "Failed to fetch $feedUrl", e)
            emptyList()
        }
    }

    private fun parseRssXml(xml: String, category: String, sourceName: String): List<Article> {
        val articles = mutableListOf<Article>()
        try {
            val factory = XmlPullParserFactory.newInstance()
            val parser = factory.newPullParser()
            parser.setInput(StringReader(xml))

            var eventType = parser.eventType
            var title = ""
            var link = ""
            var description = ""
            var pubDate = ""
            var author = ""
            var inItem = false
            var currentTag = ""

            while (eventType != XmlPullParser.END_DOCUMENT) {
                when (eventType) {
                    XmlPullParser.START_TAG -> {
                        currentTag = parser.name
                        if (parser.name == "item" || parser.name == "entry") {
                            inItem = true
                            title = ""; link = ""; description = ""; pubDate = ""; author = ""
                        }
                        if (inItem && (currentTag == "link")) {
                            val href = parser.getAttributeValue(null, "href")
                            if (href != null && link.isEmpty()) {
                                link = href
                            }
                        }
                    }
                    XmlPullParser.TEXT -> {
                        val text = parser.text?.trim() ?: ""
                        when {
                            inItem && currentTag == "title" && title.isEmpty() -> title = text
                            inItem && currentTag == "link" && link.isEmpty() -> {
                                val attrLink = parser.getAttributeValue(null, "href")
                                if (link.isEmpty()) {
                                    link = attrLink ?: text
                                }
                            }
                            inItem && (currentTag == "description" || currentTag == "summary" || currentTag == "content") && description.isEmpty() -> {
                                description = text
                            }
                            inItem && (currentTag == "pubDate" || currentTag == "published" || currentTag == "updated") && pubDate.isEmpty() -> {
                                pubDate = text
                            }
                            inItem && (currentTag == "author" || currentTag == "dc:creator" || currentTag == "creator") && author.isEmpty() -> {
                                author = text
                            }
                        }
                    }
                    XmlPullParser.END_TAG -> {
                        if (parser.name == "item" || parser.name == "entry") {
                            inItem = false
                            if (link.isNotEmpty() && title.isNotEmpty()) {
                                val imgUrl = extractImageUrl(description)
                                val cleanDesc = description
                                    .replace(Regex("<[^>]*>"), "")
                                    .take(300)
                                val formattedDate = formatDate(pubDate)
                                val dateMillis = parseDateToMillis(pubDate)
                                articles.add(Article(
                                    link = link,
                                    title = title,
                                    description = cleanDesc,
                                    pubDate = formattedDate,
                                    imageUrl = imgUrl,
                                    source = sourceName,
                                    category = category,
                                    author = author,
                                    pubDateMillis = dateMillis
                                ))
                            } else if (title.isNotEmpty() && link.isEmpty()) {
                                Log.w(TAG, "$sourceName: skipped article '$title' - no link")
                            }
                        }
                    }
                }
                eventType = parser.next()
            }
        } catch (e: Exception) {
            Log.e(TAG, "parseRssXml failed for $sourceName", e)
        }
        if (articles.isEmpty()) {
            Log.w(TAG, "$sourceName: 0 articles parsed from ${xml.length} bytes")
        }
        return articles
    }

    private fun extractImageUrl(html: String): String {
        val regex = Regex("""<img[^>]+src=["']([^"']+)["']""", RegexOption.IGNORE_CASE)
        val match = regex.find(html)
        if (match != null) {
            var url = match.groupValues[1]
            if (url.startsWith("//")) url = "https:$url"
            return url
        }
        val mediaRegex = Regex("""<media:content[^>]+url=["']([^"']+)["']""", RegexOption.IGNORE_CASE)
        val mediaMatch = mediaRegex.find(html)
        return mediaMatch?.groupValues?.get(1) ?: ""
    }

    private fun formatDate(dateStr: String): String {
        if (dateStr.isEmpty()) return ""
        val patterns = listOf(
            "EEE, dd MMM yyyy HH:mm:ss Z",
            "EEE, dd MMM yyyy HH:mm:ss zzz",
            "yyyy-MM-dd'T'HH:mm:ssXXX",
            "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
            "yyyy-MM-dd'T'HH:mm:ssZ",
            "yyyy-MM-dd'T'HH:mm:ss'Z'",
            "yyyy-MM-dd HH:mm:ss",
            "yyyy-MM-dd",
            "EEE, dd MMM yyyy HH:mm:ss 'GMT'",
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
        val cleaned = dateStr.replace(Regex("\\s+"), " ").trim()
        return cleaned.take(30)
    }

    fun parseDateToMillis(dateStr: String): Long {
        if (dateStr.isEmpty()) return System.currentTimeMillis()
        val patterns = listOf(
            "EEE, dd MMM yyyy HH:mm:ss Z",
            "EEE, dd MMM yyyy HH:mm:ss zzz",
            "yyyy-MM-dd'T'HH:mm:ssXXX",
            "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
            "yyyy-MM-dd'T'HH:mm:ssZ",
            "yyyy-MM-dd'T'HH:mm:ss'Z'",
            "yyyy-MM-dd HH:mm:ss",
            "yyyy-MM-dd",
            "EEE, dd MMM yyyy HH:mm:ss 'GMT'",
        )
        for (pattern in patterns) {
            try {
                val sdf = SimpleDateFormat(pattern, Locale.US)
                sdf.timeZone = TimeZone.getTimeZone("UTC")
                val date = sdf.parse(dateStr)
                if (date != null) return date.time
            } catch (_: Exception) { }
        }
        return System.currentTimeMillis()
    }

    private fun extractDomain(url: String): String {
        return try {
            val javaUrl = java.net.URL(url)
            javaUrl.host.replace("www.", "")
        } catch (e: Exception) {
            url
        }
    }

    fun fetchAllFeeds(onProgress: (String, String) -> Unit, onArticle: (Article) -> Unit) {
        for ((category, urls) in DomainFeeds.FEEDS) {
            for (url in urls) {
                val sourceName = extractDomain(url)
                onProgress(category, sourceName)
                val articles = fetchAndParse(url, category, sourceName)
                articles.forEach { onArticle(it) }
            }
        }
    }
}
