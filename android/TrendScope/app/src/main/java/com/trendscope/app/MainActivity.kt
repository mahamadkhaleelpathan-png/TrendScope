package com.trendscope.app

import android.app.AlertDialog
import android.app.DatePickerDialog
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import com.google.android.material.tabs.TabLayout
import com.trendscope.app.data.AppDatabase
import com.trendscope.app.data.Article
import com.trendscope.app.databinding.ActivityMainBinding
import com.trendscope.app.network.DomainFeeds
import com.trendscope.app.translate.TranslationManager
import kotlinx.coroutines.*
import java.text.SimpleDateFormat
import java.util.*

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding
    private lateinit var db: AppDatabase
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    private var currentTab = 0
    private var currentLang = ""
    private var currentSourceLang = "auto"
    private lateinit var prefs: SharedPreferences
    private var isSearchActive = false
    private var searchKeyword = ""
    private var searchCategory = ""
    private var searchFromDate = 0L
    private var searchToDate = Long.MAX_VALUE
    private var searchSortNewest = true

    override fun onCreate(savedInstanceState: Bundle?) {
        prefs = getSharedPreferences("trendscope_prefs", MODE_PRIVATE)
        applySavedTheme()
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        db = AppDatabase.getInstance(this)
        currentLang = prefs.getString("selected_lang", "") ?: ""
        currentSourceLang = prefs.getString("source_lang", "auto") ?: "auto"

        setupTabs()
        setupCategoryGrid()
        binding.tabLayout.getTabAt(0)?.select()

        binding.etSearch.setOnEditorActionListener { _, _, _ ->
            searchArticles(binding.etSearch.text.toString())
            true
        }

        binding.toolbar.setOnMenuItemClickListener { item ->
            when (item.itemId) {
                R.id.action_language -> {
                    showTranslationDialog()
                    true
                }
                R.id.action_search -> {
                    showAdvancedSearchDialog()
                    true
                }
                R.id.action_theme -> {
                    toggleTheme()
                    true
                }
                else -> false
            }
        }

        updateOfflineBanner()
    }

    private fun setupTabs() {
        binding.tabLayout.addOnTabSelectedListener(object : TabLayout.OnTabSelectedListener {
            override fun onTabSelected(tab: TabLayout.Tab?) {
                currentTab = tab?.position ?: 0
                when (currentTab) {
                    0 -> showCategories()
                    1 -> showBookmarks()
                    2 -> showOfflineArticles()
                }
            }
            override fun onTabUnselected(tab: TabLayout.Tab?) {}
            override fun onTabReselected(tab: TabLayout.Tab?) {}
        })
    }

    private fun setupCategoryGrid() {
        val categories = DomainFeeds.getAllCategories()
        binding.rvCategories.layoutManager = GridLayoutManager(this, 2)
        binding.rvCategories.adapter = CategoryAdapter(categories) { category ->
            val intent = Intent(this, CategoryActivity::class.java)
            intent.putExtra("category", category)
            intent.putExtra("lang", currentLang)
            intent.putExtra("sourceLang", currentSourceLang)
            startActivity(intent)
        }
    }

    private fun showCategories() {
        binding.rvCategories.visibility = View.VISIBLE
        binding.rvArticles.visibility = View.GONE
        binding.layoutError.visibility = View.GONE
        binding.progressBar.visibility = View.GONE
        binding.tvStatus.visibility = View.GONE
        binding.rvFilterChips.visibility = View.GONE
        binding.tvLastUpdated.visibility = View.GONE
        isSearchActive = false
    }

    private fun showBookmarks() {
        scope.launch {
            try {
                val bookmarks = withContext(Dispatchers.IO) {
                    val result = db.articleDao().getBookmarks()
                    Log.d("MainActivity", "Loaded ${result.size} bookmarks from DB")
                    result
                }
                binding.rvCategories.visibility = View.GONE
                binding.rvArticles.visibility = View.VISIBLE
                binding.layoutError.visibility = View.GONE
                binding.progressBar.visibility = View.GONE
                binding.tvStatus.visibility = View.GONE
                binding.rvFilterChips.visibility = View.GONE
                binding.tvLastUpdated.visibility = View.GONE
                isSearchActive = false
                if (bookmarks.isEmpty()) {
                    Toast.makeText(this@MainActivity, getString(R.string.no_bookmarks), Toast.LENGTH_SHORT).show()
                }
                showArticlesList(bookmarks)
            } catch (e: Exception) {
                Log.e("MainActivity", "Failed to load bookmarks", e)
            }
        }
    }

    private fun showOfflineArticles() {
        scope.launch {
            try {
                val offline = withContext(Dispatchers.IO) {
                    db.articleDao().getDownloadedArticles()
                }
                binding.rvCategories.visibility = View.GONE
                binding.rvArticles.visibility = View.VISIBLE
                binding.layoutError.visibility = View.GONE
                binding.progressBar.visibility = View.GONE
                binding.tvStatus.visibility = View.GONE
                binding.rvFilterChips.visibility = View.GONE
                binding.tvLastUpdated.visibility = View.GONE
                isSearchActive = false
                if (offline.isEmpty()) {
                    Toast.makeText(this@MainActivity, getString(R.string.empty_offline), Toast.LENGTH_SHORT).show()
                }
                showArticlesList(offline)
            } catch (e: Exception) {
                Log.e("MainActivity", "Failed to load offline articles", e)
            }
        }
    }

    private fun showArticlesList(articles: List<Article>) {
        binding.rvArticles.layoutManager = LinearLayoutManager(this)
        binding.rvArticles.adapter = ArticleAdapter(articles, { article ->
            val intent = Intent(this, ArticleActivity::class.java)
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
        }, currentLang)
    }

    private fun searchArticles(query: String) {
        if (query.isBlank()) {
            isSearchActive = false
            refreshCurrentView()
            return
        }
        isSearchActive = true
        searchKeyword = query
        saveSearchQuery(query)
        scope.launch {
            binding.progressBar.visibility = View.VISIBLE
            try {
                val results = withContext(Dispatchers.IO) {
                    db.articleDao().searchArticles(query)
                }
                binding.progressBar.visibility = View.GONE
                binding.rvCategories.visibility = View.GONE
                binding.rvArticles.visibility = View.VISIBLE
                if (results.isEmpty()) {
                    Toast.makeText(this@MainActivity, getString(R.string.no_results), Toast.LENGTH_SHORT).show()
                }
                showArticlesList(results)
            } catch (e: Exception) {
                Log.e("MainActivity", "Search failed", e)
                binding.progressBar.visibility = View.GONE
            }
        }
    }

    private fun showAdvancedSearchDialog() {
        val categories = listOf("") + DomainFeeds.getAllCategories()
        val catNames = listOf(getString(R.string.all_categories)) + DomainFeeds.getAllCategories()
        val catCodes = categories.toTypedArray()
        val catLabels = catNames.toTypedArray()

        val items = mutableListOf<CharSequence>()
        items.add("Keyword: ${searchKeyword.ifEmpty { "(any)" }}")
        items.add("Category: ${if (searchCategory.isEmpty()) "All" else searchCategory}")
        items.add("Sort: ${if (searchSortNewest) "Newest" else "Oldest"}")
        items.add("Set From Date")
        items.add("Set To Date")
        items.add(getString(R.string.search))
        items.add(getString(R.string.clear_filters))
        items.add(getString(R.string.search_history))

        AlertDialog.Builder(this)
            .setTitle(getString(R.string.advanced_search))
            .setItems(items.toTypedArray()) { _, which ->
                when (which) {
                    0 -> showKeywordInputDialog()
                    1 -> showCategoryPickerDialog(catCodes, catLabels)
                    2 -> {
                        searchSortNewest = !searchSortNewest
                        Toast.makeText(this, if (searchSortNewest) "Newest First" else "Oldest First", Toast.LENGTH_SHORT).show()
                    }
                    3 -> showDatePickerDialog(true)
                    4 -> showDatePickerDialog(false)
                    5 -> executeAdvancedSearch()
                    6 -> clearAdvancedFilters()
                    7 -> showSearchHistoryDialog()
                }
            }
            .show()
    }

    private fun showKeywordInputDialog() {
        val input = android.widget.EditText(this)
        input.hint = "Enter keyword"
        input.setText(searchKeyword)
        AlertDialog.Builder(this)
            .setTitle("Search Keyword")
            .setView(input)
            .setPositiveButton("OK") { _, _ ->
                searchKeyword = input.text.toString().trim()
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showCategoryPickerDialog(codes: Array<String>, labels: Array<String>) {
        val currentIndex = codes.indexOfFirst { it == searchCategory }.coerceAtLeast(0)
        AlertDialog.Builder(this)
            .setTitle("Select Category")
            .setSingleChoiceItems(labels, currentIndex) { _, which ->
                searchCategory = codes[which]
            }
            .setPositiveButton("OK", null)
            .show()
    }

    private fun showDatePickerDialog(isFrom: Boolean) {
        val cal = Calendar.getInstance()
        if (!isFrom && searchToDate != Long.MAX_VALUE) {
            cal.timeInMillis = searchToDate
        }
        DatePickerDialog(
            this,
            { _, year, month, day ->
                cal.set(year, month, day, 0, 0, 0)
                if (isFrom) {
                    searchFromDate = cal.timeInMillis
                    Toast.makeText(this, "From: ${SimpleDateFormat("MMM dd, yyyy", Locale.US).format(cal.time)}", Toast.LENGTH_SHORT).show()
                } else {
                    cal.set(Calendar.HOUR_OF_DAY, 23)
                    cal.set(Calendar.MINUTE, 59)
                    cal.set(Calendar.SECOND, 59)
                    searchToDate = cal.timeInMillis
                    Toast.makeText(this, "To: ${SimpleDateFormat("MMM dd, yyyy", Locale.US).format(cal.time)}", Toast.LENGTH_SHORT).show()
                }
            },
            cal.get(Calendar.YEAR),
            cal.get(Calendar.MONTH),
            cal.get(Calendar.DAY_OF_MONTH)
        ).show()
    }

    private fun executeAdvancedSearch() {
        val query = searchKeyword
        if (query.isEmpty() && searchCategory.isEmpty()) {
            isSearchActive = false
            refreshCurrentView()
            return
        }
        isSearchActive = true
        if (query.isNotEmpty()) saveSearchQuery(query)

        scope.launch {
            binding.progressBar.visibility = View.VISIBLE
            try {
                val results = withContext(Dispatchers.IO) {
                    db.articleDao().searchArticlesAdvanced(
                        query = query,
                        category = searchCategory,
                        fromDate = searchFromDate,
                        toDate = searchToDate
                    )
                }
                val sorted = if (searchSortNewest) {
                    results.sortedByDescending { it.pubDateMillis }
                } else {
                    results.sortedBy { it.pubDateMillis }
                }
                binding.progressBar.visibility = View.GONE
                binding.rvCategories.visibility = View.GONE
                binding.rvArticles.visibility = View.VISIBLE
                if (sorted.isEmpty()) {
                    Toast.makeText(this@MainActivity, getString(R.string.no_results), Toast.LENGTH_SHORT).show()
                }
                showArticlesList(sorted)
            } catch (e: Exception) {
                Log.e("MainActivity", "Advanced search failed", e)
                binding.progressBar.visibility = View.GONE
            }
        }
    }

    private fun clearAdvancedFilters() {
        searchKeyword = ""
        searchCategory = ""
        searchFromDate = 0L
        searchToDate = Long.MAX_VALUE
        searchSortNewest = true
        isSearchActive = false
        refreshCurrentView()
        Toast.makeText(this, "Filters cleared", Toast.LENGTH_SHORT).show()
    }

    private fun saveSearchQuery(query: String) {
        val history = getSearchHistory().toMutableList()
        history.remove(query)
        history.add(0, query)
        if (history.size > 20) {
            history.removeAt(history.lastIndex)
        }
        prefs.edit().putString("search_history", history.joinToString("|")).apply()
    }

    private fun getSearchHistory(): List<String> {
        val raw = prefs.getString("search_history", "") ?: ""
        return if (raw.isEmpty()) emptyList() else raw.split("|").filter { it.isNotEmpty() }
    }

    private fun showSearchHistoryDialog() {
        val history = getSearchHistory()
        if (history.isEmpty()) {
            Toast.makeText(this, "No search history", Toast.LENGTH_SHORT).show()
            return
        }
        AlertDialog.Builder(this)
            .setTitle(getString(R.string.search_history))
            .setItems(history.toTypedArray()) { _, which ->
                val query = history[which]
                binding.etSearch.setText(query)
                searchArticles(query)
            }
            .setNeutralButton("Clear All") { _, _ ->
                prefs.edit().remove("search_history").apply()
                Toast.makeText(this, "History cleared", Toast.LENGTH_SHORT).show()
            }
            .show()
    }

    private fun showTranslationDialog() {
        val languages = TranslationManager.getSupportedLanguages()
        val names = languages.map { "${TranslationManager.getEnglishName(it)} (${TranslationManager.getDisplayName(it)})" }

        val srcLabel = if (currentSourceLang == "auto") "Auto Detect"
        else "${TranslationManager.getEnglishName(currentSourceLang)}"
        val tgtLabel = if (currentLang.isEmpty()) "None"
        else "${TranslationManager.getEnglishName(currentLang)}"

        val view = layoutInflater.inflate(android.R.layout.simple_list_item_1, null) as TextView
        view.text = "Translate from: $srcLabel\nTranslate to: $tgtLabel"
        view.setPadding(40, 30, 40, 30)
        view.textSize = 16f

        AlertDialog.Builder(this)
            .setTitle(getString(R.string.select_language))
            .setView(view)
            .setPositiveButton("Change Source") { _, _ ->
                showSourcePicker(languages, names)
            }
            .setNeutralButton("Swap") { _, _ ->
                val temp = currentSourceLang
                currentSourceLang = if (currentLang.isEmpty()) "auto" else currentLang
                currentLang = if (temp == "auto") "" else temp
                prefs.edit().putString("selected_lang", currentLang).apply()
                prefs.edit().putString("source_lang", currentSourceLang).apply()
                if (currentLang.isNotEmpty()) {
                    translateAllArticles(currentLang, currentSourceLang)
                } else {
                    refreshCurrentView()
                }
            }
            .setNegativeButton("Change Target") { _, _ ->
                showTargetPicker(languages, names)
            }
            .show()
    }

    private fun showSourcePicker(languages: List<String>, names: List<String>) {
        val items = mutableListOf("Auto Detect")
        items.addAll(names)
        val codes = mutableListOf("auto")
        codes.addAll(languages)

        AlertDialog.Builder(this)
            .setTitle("Translate FROM:")
            .setItems(items.toTypedArray()) { _, which ->
                currentSourceLang = codes[which]
                prefs.edit().putString("source_lang", currentSourceLang).apply()
                if (currentLang.isNotEmpty()) {
                    translateAllArticles(currentLang, currentSourceLang)
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun showTargetPicker(languages: List<String>, names: List<String>) {
        val items = mutableListOf("None (Show Original)")
        items.addAll(names)
        val codes = mutableListOf("")
        codes.addAll(languages)

        AlertDialog.Builder(this)
            .setTitle("Translate TO:")
            .setItems(items.toTypedArray()) { _, which ->
                setLanguage(codes[which], currentSourceLang)
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun setLanguage(code: String, sourceLang: String = "auto") {
        currentLang = code
        currentSourceLang = sourceLang
        prefs.edit().putString("selected_lang", code).apply()
        prefs.edit().putString("source_lang", sourceLang).apply()
        if (code.isNotEmpty()) {
            translateAllArticles(code, sourceLang)
        } else {
            refreshCurrentView()
        }
    }

    private fun translateAllArticles(targetLang: String, sourceLang: String = "auto") {
        binding.progressBar.visibility = View.VISIBLE
        binding.tvStatus.text = getString(R.string.status_translating)
        binding.tvStatus.visibility = View.VISIBLE

        scope.launch {
            try {
                val toTranslate = withContext(Dispatchers.IO) {
                    db.articleDao().getArticlesNotInLang(targetLang)
                }
                if (toTranslate.isEmpty()) {
                    binding.progressBar.visibility = View.GONE
                    binding.tvStatus.visibility = View.GONE
                    Toast.makeText(this@MainActivity, "All articles already translated", Toast.LENGTH_SHORT).show()
                    return@launch
                }
                translateBatch(toTranslate, targetLang, sourceLang)
            } catch (e: Exception) {
                binding.progressBar.visibility = View.GONE
                binding.tvStatus.visibility = View.GONE
                Toast.makeText(this@MainActivity, "Translation error: ${e.message}", Toast.LENGTH_LONG).show()
            }
        }
    }

    private suspend fun translateBatch(articles: List<Article>, targetLang: String, sourceLang: String = "auto") {
        var count = 0
        val total = articles.size
        var hasError = false
        for (article in articles) {
            count++
            withContext(Dispatchers.Main) {
                binding.tvStatus.text = getString(R.string.status_translating_count, count, total)
            }
            try {
                val effectiveSource = if (sourceLang == "auto") {
                    TranslationManager.detectLanguage(article.title)
                } else sourceLang

                val translatedTitle = TranslationManager.translate(article.title, effectiveSource, targetLang)
                delay(400)
                val translatedDesc = TranslationManager.translate(article.description, effectiveSource, targetLang)
                delay(400)
                val translatedContent = TranslationManager.translate(
                    article.content.ifEmpty { article.description }, effectiveSource, targetLang
                )
                withContext(Dispatchers.IO) {
                    db.articleDao().updateTranslation(
                        article.link, translatedTitle, translatedDesc, translatedContent, targetLang, effectiveSource
                    )
                }
            } catch (e: Exception) {
                hasError = true
            }
            delay(600)
        }
        refreshCurrentView()
        binding.progressBar.visibility = View.GONE
        binding.tvStatus.visibility = View.GONE
        if (hasError) {
            Toast.makeText(this@MainActivity, getString(R.string.translation_partial), Toast.LENGTH_LONG).show()
        } else {
            Toast.makeText(this@MainActivity, getString(R.string.translation_complete), Toast.LENGTH_SHORT).show()
        }
    }

    private fun refreshCurrentView() {
        when (currentTab) {
            1 -> showBookmarks()
            2 -> showOfflineArticles()
        }
    }

    private fun updateOfflineBanner() {
        if (!isNetworkAvailable()) {
            binding.tvOfflineBanner.visibility = View.VISIBLE
        } else {
            binding.tvOfflineBanner.visibility = View.GONE
        }
    }

    private fun isNetworkAvailable(): Boolean {
        val cm = getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val network = cm.activeNetwork ?: return false
        val caps = cm.getNetworkCapabilities(network) ?: return false
        return caps.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
    }

    override fun onResume() {
        super.onResume()
        updateThemeMenuTitle()
    }

    private fun applySavedTheme() {
        val nightMode = prefs.getInt("night_mode", AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM)
        AppCompatDelegate.setDefaultNightMode(nightMode)
    }

    private fun toggleTheme() {
        val currentMode = prefs.getInt("night_mode", AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM)
        val newMode = if (currentMode == AppCompatDelegate.MODE_NIGHT_YES) {
            AppCompatDelegate.MODE_NIGHT_NO
        } else {
            AppCompatDelegate.MODE_NIGHT_YES
        }
        prefs.edit().putInt("night_mode", newMode).apply()
        AppCompatDelegate.setDefaultNightMode(newMode)
    }

    private fun updateThemeMenuTitle() {
        val item = binding.toolbar.menu.findItem(R.id.action_theme)
        val currentMode = prefs.getInt("night_mode", AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM)
        val isDark = currentMode == AppCompatDelegate.MODE_NIGHT_YES ||
                (currentMode == AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM &&
                        (resources.configuration.uiMode and android.content.res.Configuration.UI_MODE_NIGHT_MASK) ==
                                android.content.res.Configuration.UI_MODE_NIGHT_YES)
        item?.title = if (isDark) getString(R.string.light_mode) else getString(R.string.dark_mode)
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
