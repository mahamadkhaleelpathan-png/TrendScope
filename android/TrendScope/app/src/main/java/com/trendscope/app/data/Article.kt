package com.trendscope.app.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "articles")
data class Article(
    @PrimaryKey val link: String,
    val title: String,
    val description: String,
    val content: String = "",
    val pubDate: String,
    val imageUrl: String = "",
    val source: String,
    val category: String,
    val author: String = "",
    val isBookmarked: Boolean = false,
    val isDownloaded: Boolean = false,
    val downloadedAt: Long = 0L,
    val localImagePath: String = "",
    val fetchedAt: Long = System.currentTimeMillis(),
    val pubDateMillis: Long = 0L,
    val translatedTitle: String = "",
    val translatedDescription: String = "",
    val translatedContent: String = "",
    val translateLang: String = "",
    val sourceLang: String = ""
)
