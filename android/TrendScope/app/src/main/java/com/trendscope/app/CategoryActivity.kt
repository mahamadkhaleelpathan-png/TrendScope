package com.trendscope.app

import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.trendscope.app.data.AppDatabase
import com.trendscope.app.data.Article
import com.trendscope.app.databinding.ActivityCategoryBinding
import com.trendscope.app.network.DomainFeeds
import com.trendscope.app.network.RssParser
import kotlinx.coroutines.*

class CategoryActivity : AppCompatActivity() {
    private lateinit var binding: ActivityCategoryBinding
    private lateinit var db: AppDatabase
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    private var articles = mutableListOf<Article>()
    private var currentLang = ""
    private var currentSourceLang = "auto"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCategoryBinding.inflate(layoutInflater)
        setContentView(binding.root)

        db = AppDatabase.getInstance(this)

        val category = intent.getStringExtra("category") ?: return
        currentLang = intent.getStringExtra("lang") ?: ""
        currentSourceLang = intent.getStringExtra("sourceLang") ?: "auto"
        binding.toolbar.title = category
        binding.toolbar.setNavigationOnClickListener { finish() }

        binding.rvArticles.layoutManager = LinearLayoutManager(this)
        loadArticles(category)
        binding.swipeRefresh.setOnRefreshListener { loadArticles(category) }
    }

    private fun loadArticles(category: String) {
        binding.progressBar.visibility = android.view.View.VISIBLE
        articles.clear()

        scope.launch {
            withContext(Dispatchers.IO) {
                val feeds = DomainFeeds.getFeedsForCategory(category)
                for (url in feeds) {
                    val sourceName = url.replace("www.", "").let {
                        try { java.net.URL(it).host } catch (e: Exception) { it }
                    }
                    try {
                        val parsed = RssParser.fetchAndParse(url, category, sourceName)
                        articles.addAll(parsed)
                        Log.d("CategoryActivity", "$sourceName: ${parsed.size} articles")
                    } catch (e: Exception) {
                        Log.e("CategoryActivity", "Failed to fetch $url", e)
                    }
                }
                try {
                    db.articleDao().insertArticles(articles)
                    Log.d("CategoryActivity", "Saved ${articles.size} articles to DB for category: $category")
                } catch (e: Exception) {
                    Log.e("CategoryActivity", "Failed to save articles to DB", e)
                }
            }
            binding.progressBar.visibility = android.view.View.GONE
            binding.swipeRefresh.isRefreshing = false
            binding.rvArticles.adapter = ArticleAdapter(
                articles = articles.sortedByDescending { it.pubDateMillis },
                onClick = { article ->
                    val intent = android.content.Intent(this@CategoryActivity, ArticleActivity::class.java)
                    intent.putExtra("link", article.link)
                    intent.putExtra("title", article.title)
                    intent.putExtra("description", article.description)
                    intent.putExtra("content", article.content)
                    intent.putExtra("pubDate", article.pubDate)
                    intent.putExtra("imageUrl", article.imageUrl)
                    intent.putExtra("source", article.source)
                    intent.putExtra("category", article.category)
                    intent.putExtra("author", article.author)
                    intent.putExtra("lang", currentLang)
                    intent.putExtra("sourceLang", currentSourceLang)
                    startActivity(intent)
                },
                currentLang = currentLang
            )
            Toast.makeText(this@CategoryActivity, getString(R.string.loading_articles, articles.size), Toast.LENGTH_SHORT).show()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
