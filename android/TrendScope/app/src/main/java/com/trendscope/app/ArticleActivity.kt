package com.trendscope.app

import android.content.Intent
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.view.View
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.trendscope.app.data.AppDatabase
import com.trendscope.app.data.Article
import com.trendscope.app.data.ImageCacheManager
import com.trendscope.app.databinding.ActivityArticleBinding
import com.trendscope.app.translate.TranslationManager
import kotlinx.coroutines.*

class ArticleActivity : AppCompatActivity() {
    private lateinit var binding: ActivityArticleBinding
    private lateinit var db: AppDatabase
    private lateinit var article: Article
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    private var isBookmarked = false
    private var isDownloaded = false
    private var selectedTargetLang = "en"
    private lateinit var langCodes: List<String>
    private var originalTitle = ""
    private var originalContent = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityArticleBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val currentLang = intent.getStringExtra("lang") ?: ""
        article = Article(
            link = intent.getStringExtra("link") ?: return,
            title = intent.getStringExtra("title") ?: "",
            description = intent.getStringExtra("description") ?: "",
            pubDate = intent.getStringExtra("pubDate") ?: "",
            imageUrl = intent.getStringExtra("imageUrl") ?: "",
            source = intent.getStringExtra("source") ?: "",
            category = intent.getStringExtra("category") ?: "",
            content = intent.getStringExtra("content") ?: "",
            author = intent.getStringExtra("author") ?: ""
        )

        db = AppDatabase.getInstance(this)
        selectedTargetLang = if (currentLang.isNotEmpty()) currentLang else "en"

        setupToolbar()
        displayArticle()
        setupLanguageSelector()
        checkBookmarkAndDownloadStatus()
        setupListeners()
        loadCachedTranslation()
    }

    private fun setupToolbar() {
        binding.toolbar.title = ""
        binding.toolbar.setNavigationOnClickListener { finish() }
    }

    private fun setupListeners() {
        binding.fabBookmark.setOnClickListener { toggleBookmark() }
        binding.fabShare.setOnClickListener {
            val sendIntent = Intent().apply {
                action = Intent.ACTION_SEND
                putExtra(Intent.EXTRA_TEXT, "${article.title}\n\n${article.link}")
                type = "text/plain"
            }
            startActivity(Intent.createChooser(sendIntent, "Share"))
        }
        binding.fabDownload.setOnClickListener { onDownloadClicked() }
        binding.tvOpenOriginal.setOnClickListener {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(article.link))
            startActivity(intent)
        }
    }

    private fun setupLanguageSelector() {
        langCodes = TranslationManager.getSupportedLanguages()
        val langNames = langCodes.map { TranslationManager.getEnglishName(it) }
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, langNames)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        binding.langSpinner.adapter = adapter

        val defaultIndex = langCodes.indexOf(selectedTargetLang).coerceAtLeast(0)
        binding.langSpinner.setSelection(defaultIndex)

        binding.btnTranslateArticle.setOnClickListener { doTranslate() }
    }

    private fun displayArticle() {
        originalTitle = Html.fromHtml(article.title, Html.FROM_HTML_MODE_COMPACT).toString()
        originalContent = Html.fromHtml(
            if (article.description.isNotEmpty()) article.description else article.content,
            Html.FROM_HTML_MODE_COMPACT
        ).toString()

        binding.tvArticleTitle.text = originalTitle
        binding.tvArticleSource.text = article.source
        binding.tvArticleDate.text = article.pubDate
        binding.tvArticleContent.text = originalContent

        if (article.localImagePath.isNotEmpty()) {
            val bitmap = ImageCacheManager.loadBitmap(article.localImagePath)
            if (bitmap != null) {
                binding.ivArticleImage.visibility = View.VISIBLE
                binding.ivArticleImage.setImageBitmap(bitmap)
                return
            }
        }
        if (article.imageUrl.isNotEmpty()) {
            binding.ivArticleImage.visibility = View.VISIBLE
            Thread {
                try {
                    val conn = java.net.URL(article.imageUrl).openConnection()
                    conn.connectTimeout = 5000
                    val input = conn.getInputStream()
                    val bitmap = BitmapFactory.decodeStream(input)
                    input.close()
                    binding.ivArticleImage.post { binding.ivArticleImage.setImageBitmap(bitmap) }
                } catch (_: Exception) { }
            }.start()
        }
    }

    private fun showOriginal() {
        binding.tvArticleTitle.text = originalTitle
        binding.tvArticleContent.text = originalContent
    }

    private fun doTranslate() {
        val textToTranslate = article.description.ifEmpty { article.content }
        if (textToTranslate.isEmpty()) {
            Toast.makeText(this, "No text to translate", Toast.LENGTH_SHORT).show()
            return
        }

        selectedTargetLang = langCodes[binding.langSpinner.selectedItemPosition]
        binding.progressBar.visibility = View.VISIBLE
        binding.btnTranslateArticle.isEnabled = false
        binding.tvError.visibility = View.GONE

        scope.launch {
            try {
                val effectiveSource = TranslationManager.detectLanguage(textToTranslate)

                val newTitle = if (article.title.isNotEmpty()) {
                    TranslationManager.translate(article.title, effectiveSource, selectedTargetLang)
                } else ""

                delay(400)

                val descText = if (article.description.isNotEmpty()) article.description else article.content
                val newDesc = if (descText.isNotEmpty()) {
                    TranslationManager.translate(descText, effectiveSource, selectedTargetLang)
                } else ""

                delay(400)

                val contentText = if (article.content.isNotEmpty()) article.content else article.description
                val newContent = if (contentText.isNotEmpty()) {
                    TranslationManager.translate(contentText, effectiveSource, selectedTargetLang)
                } else ""

                binding.tvArticleTitle.text = newTitle.ifEmpty { originalTitle }
                binding.tvArticleContent.text = newDesc.ifEmpty { originalContent }

                withContext(Dispatchers.IO) {
                    db.articleDao().updateTranslation(
                        article.link,
                        newTitle,
                        newDesc,
                        newContent,
                        selectedTargetLang,
                        effectiveSource
                    )
                }

                Toast.makeText(this@ArticleActivity,
                    "Translated to ${TranslationManager.getEnglishName(selectedTargetLang)}",
                    Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                showOriginal()
                binding.tvError.text = "Translation failed: ${e.message}"
                binding.tvError.visibility = View.VISIBLE
            }
            binding.progressBar.visibility = View.GONE
            binding.btnTranslateArticle.isEnabled = true
        }
    }

    private fun loadCachedTranslation() {
        scope.launch {
            val dbArticle = withContext(Dispatchers.IO) {
                db.articleDao().getArticleByLink(article.link)
            }
            if (dbArticle != null && dbArticle.translateLang == selectedTargetLang) {
                var loaded = false
                if (dbArticle.translatedTitle.isNotEmpty()) {
                    binding.tvArticleTitle.text = dbArticle.translatedTitle
                    loaded = true
                }
                if (dbArticle.translatedDescription.isNotEmpty()) {
                    binding.tvArticleContent.text = dbArticle.translatedDescription
                    loaded = true
                }
                if (loaded) {
                    binding.langSpinner.setSelection(langCodes.indexOf(selectedTargetLang).coerceAtLeast(0))
                    binding.tvError.visibility = View.GONE
                }
            }
        }
    }

    private fun checkBookmarkAndDownloadStatus() {
        scope.launch {
            val dbArticle = withContext(Dispatchers.IO) {
                db.articleDao().getArticleByLink(article.link)
            }
            if (dbArticle != null) {
                isDownloaded = dbArticle.isDownloaded
                isBookmarked = dbArticle.isBookmarked
                if (dbArticle.localImagePath.isNotEmpty()) {
                    article = article.copy(localImagePath = dbArticle.localImagePath)
                    displayArticle()
                }
                Log.d("ArticleActivity", "Status for '${article.title.take(30)}': bookmarked=$isBookmarked, downloaded=$isDownloaded")
            } else {
                isDownloaded = false
                isBookmarked = false
                Log.d("ArticleActivity", "Article not in DB: ${article.link}")
            }
            updateBookmarkIcon()
            updateDownloadIcon()
        }
    }

    private fun onDownloadClicked() {
        if (isDownloaded) {
            AlertDialog.Builder(this)
                .setTitle(getString(R.string.delete_offline_title))
                .setMessage(getString(R.string.delete_offline_message))
                .setPositiveButton(getString(R.string.delete)) { _, _ -> deleteOfflineArticle() }
                .setNegativeButton(getString(R.string.cancel), null)
                .show()
        } else {
            downloadOfflineArticle()
        }
    }

    private fun downloadOfflineArticle() {
        binding.progressBar.visibility = View.VISIBLE
        binding.fabDownload.isEnabled = false
        Toast.makeText(this, getString(R.string.download_started), Toast.LENGTH_SHORT).show()

        scope.launch {
            try {
                val localImagePath = withContext(Dispatchers.IO) {
                    ImageCacheManager.cacheImage(this@ArticleActivity, article.imageUrl)
                }
                val now = System.currentTimeMillis()
                val saved = withContext(Dispatchers.IO) {
                    val existing = db.articleDao().getArticleByLink(article.link)
                    if (existing != null) {
                        db.articleDao().markDownloaded(article.link, now, localImagePath)
                        existing.copy(isDownloaded = true, downloadedAt = now, localImagePath = localImagePath)
                    } else {
                        val dl = article.copy(
                            isDownloaded = true,
                            downloadedAt = now,
                            localImagePath = localImagePath
                        )
                        db.articleDao().insertArticle(dl)
                        dl
                    }
                }
                isDownloaded = true
                article = saved
                if (localImagePath.isNotEmpty()) {
                    displayArticle()
                }
                Log.d("ArticleActivity", "Download complete: ${article.link}, image=$localImagePath")
                binding.progressBar.visibility = View.GONE
                binding.fabDownload.isEnabled = true
                updateDownloadIcon()
                Toast.makeText(this@ArticleActivity, getString(R.string.download_complete), Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                Log.e("ArticleActivity", "Download failed", e)
                binding.progressBar.visibility = View.GONE
                binding.fabDownload.isEnabled = true
                Toast.makeText(this@ArticleActivity, getString(R.string.download_failed) + ": ${e.message}", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun deleteOfflineArticle() {
        scope.launch {
            try {
                val existing = withContext(Dispatchers.IO) {
                    db.articleDao().getArticleByLink(article.link)
                }
                if (existing != null && existing.localImagePath.isNotEmpty()) {
                    ImageCacheManager.deleteCachedImage(existing.localImagePath)
                }
                withContext(Dispatchers.IO) {
                    db.articleDao().markDeleted(article.link)
                }
                isDownloaded = false
                article = article.copy(localImagePath = "")
                Log.d("ArticleActivity", "Deleted offline copy: ${article.link}")
                updateDownloadIcon()
                Toast.makeText(this@ArticleActivity, getString(R.string.offline_copy_deleted), Toast.LENGTH_SHORT).show()
            } catch (e: Exception) {
                Log.e("ArticleActivity", "Delete failed", e)
                Toast.makeText(this@ArticleActivity, getString(R.string.download_failed) + ": ${e.message}", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun toggleBookmark() {
        val newState = !isBookmarked
        val updated = article.copy(isBookmarked = newState)
        scope.launch {
            withContext(Dispatchers.IO) {
                db.articleDao().insertArticle(updated)
                Log.d("ArticleActivity", "Set bookmarked=$newState for ${article.link}")
            }
            isBookmarked = newState
            updateBookmarkIcon()
            Toast.makeText(this@ArticleActivity,
                if (isBookmarked) getString(R.string.bookmarked) else getString(R.string.removed_bookmark),
                Toast.LENGTH_SHORT).show()
        }
    }

    private fun updateBookmarkIcon() {
        binding.fabBookmark.setImageResource(
            if (isBookmarked) android.R.drawable.btn_star_big_on
            else android.R.drawable.btn_star_big_off
        )
    }

    private fun updateDownloadIcon() {
        binding.fabDownload.setImageResource(
            if (isDownloaded) R.drawable.ic_delete
            else R.drawable.ic_download
        )
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
