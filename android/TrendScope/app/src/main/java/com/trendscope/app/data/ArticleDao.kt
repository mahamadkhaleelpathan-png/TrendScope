package com.trendscope.app.data

import androidx.room.*

@Dao
interface ArticleDao {
    @Query("SELECT * FROM articles WHERE isBookmarked = 1 ORDER BY pubDateMillis DESC")
    suspend fun getBookmarks(): List<Article>

    @Query("SELECT * FROM articles WHERE category = :category ORDER BY pubDateMillis DESC")
    suspend fun getArticlesByCategory(category: String): List<Article>

    @Query("SELECT * FROM articles ORDER BY pubDateMillis DESC")
    suspend fun getAllArticles(): List<Article>

    @Query("SELECT * FROM articles WHERE link = :link")
    suspend fun getArticleByLink(link: String): Article?

    @Query("SELECT * FROM articles WHERE title LIKE '%' || :query || '%' OR description LIKE '%' || :query || '%' OR translatedTitle LIKE '%' || :query || '%' OR translatedDescription LIKE '%' || :query || '%' ORDER BY pubDateMillis DESC")
    suspend fun searchArticles(query: String): List<Article>

    @Query("SELECT * FROM articles WHERE (title LIKE '%' || :query || '%' OR description LIKE '%' || :query || '%' OR author LIKE '%' || :query || '%') AND (:category IS NULL OR :category = '' OR category = :category) AND pubDateMillis BETWEEN :fromDate AND :toDate ORDER BY pubDateMillis DESC")
    suspend fun searchArticlesAdvanced(query: String, category: String, fromDate: Long, toDate: Long): List<Article>

    @Query("SELECT * FROM articles ORDER BY pubDateMillis ASC LIMIT :limit OFFSET :offset")
    suspend fun getArticlesAsc(limit: Int, offset: Int): List<Article>

    @Query("SELECT * FROM articles ORDER BY pubDateMillis DESC LIMIT :limit OFFSET :offset")
    suspend fun getArticlesDesc(limit: Int, offset: Int): List<Article>

    @Query("SELECT * FROM articles WHERE category = :category ORDER BY pubDateMillis DESC LIMIT :limit OFFSET :offset")
    suspend fun getArticlesByCategoryPaginated(category: String, limit: Int, offset: Int): List<Article>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertArticles(articles: List<Article>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertArticle(article: Article)

    @Delete
    suspend fun deleteArticle(article: Article)

    @Query("UPDATE articles SET isBookmarked = NOT isBookmarked WHERE link = :link")
    suspend fun toggleBookmark(link: String)

    @Query("UPDATE articles SET isBookmarked = 1 WHERE link = :link")
    suspend fun setBookmarked(link: String)

    @Query("UPDATE articles SET isBookmarked = 0 WHERE link = :link")
    suspend fun setUnBookmarked(link: String)

    @Query("SELECT isBookmarked FROM articles WHERE link = :link")
    suspend fun isBookmarked(link: String): Boolean?

    @Query("DELETE FROM articles")
    suspend fun clearAll()

    @Query("SELECT DISTINCT category FROM articles ORDER BY category")
    suspend fun getCategories(): List<String>

    @Query("SELECT COUNT(*) FROM articles")
    suspend fun getCount(): Int

    @Query("SELECT COUNT(*) FROM articles WHERE category = :category")
    suspend fun getCountByCategory(category: String): Int

    @Query("SELECT MAX(pubDateMillis) FROM articles")
    suspend fun getLatestPubDateMillis(): Long?

    @Query("UPDATE articles SET translatedTitle = :title, translatedDescription = :desc, translatedContent = :content, translateLang = :lang, sourceLang = :sourceLang WHERE link = :link")
    suspend fun updateTranslation(link: String, title: String, desc: String, content: String, lang: String, sourceLang: String = "en")

    @Query("SELECT * FROM articles WHERE translateLang != :lang OR translateLang IS NULL ORDER BY pubDateMillis DESC")
    suspend fun getArticlesNotInLang(lang: String): List<Article>

    @Query("SELECT * FROM articles ORDER BY pubDateMillis DESC")
    suspend fun getAllArticlesUnlimited(): List<Article>

    @Query("SELECT link FROM articles WHERE isBookmarked = 1")
    suspend fun getBookmarkedLinks(): List<String>

    @Query("SELECT * FROM articles WHERE isDownloaded = 1 ORDER BY downloadedAt DESC")
    suspend fun getDownloadedArticles(): List<Article>

    @Query("SELECT * FROM articles WHERE isDownloaded = 1 AND (title LIKE '%' || :query || '%' OR description LIKE '%' || :query || '%' OR source LIKE '%' || :query || '%') ORDER BY downloadedAt DESC")
    suspend fun searchDownloadedArticles(query: String): List<Article>

    @Query("SELECT isDownloaded FROM articles WHERE link = :link")
    suspend fun isDownloaded(link: String): Boolean?

    @Query("UPDATE articles SET isDownloaded = 1, downloadedAt = :timestamp, localImagePath = :imagePath WHERE link = :link")
    suspend fun markDownloaded(link: String, timestamp: Long, imagePath: String)

    @Query("UPDATE articles SET isDownloaded = 0, downloadedAt = 0, localImagePath = '' WHERE link = :link")
    suspend fun markDeleted(link: String)

    @Query("SELECT COUNT(*) FROM articles WHERE isDownloaded = 1")
    suspend fun getDownloadedCount(): Int

    @Query("SELECT link FROM articles WHERE isDownloaded = 1")
    suspend fun getDownloadedLinks(): List<String>
}
