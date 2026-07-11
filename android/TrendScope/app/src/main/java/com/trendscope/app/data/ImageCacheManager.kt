package com.trendscope.app.data

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Log
import okhttp3.OkHttpClient
import okhttp3.Request
import java.io.File
import java.io.FileOutputStream
import java.security.MessageDigest
import java.util.concurrent.TimeUnit

object ImageCacheManager {
    private const val TAG = "ImageCacheManager"
    private const val CACHE_DIR = "offline_images"
    private const val TIMEOUT_SECONDS = 10L

    private val client = OkHttpClient.Builder()
        .connectTimeout(TIMEOUT_SECONDS, TimeUnit.SECONDS)
        .readTimeout(TIMEOUT_SECONDS, TimeUnit.SECONDS)
        .followRedirects(true)
        .build()

    private fun getCacheDir(context: Context): File {
        val dir = File(context.filesDir, CACHE_DIR)
        if (!dir.exists()) {
            dir.mkdirs()
        }
        return dir
    }

    private fun hashUrl(url: String): String {
        val digest = MessageDigest.getInstance("MD5")
        val bytes = digest.digest(url.toByteArray())
        return bytes.joinToString("") { "%02x".format(it) } + ".jpg"
    }

    fun getLocalPath(context: Context, url: String): String {
        val file = File(getCacheDir(context), hashUrl(url))
        return if (file.exists()) file.absolutePath else ""
    }

    fun cacheImage(context: Context, imageUrl: String): String {
        if (imageUrl.isEmpty()) return ""
        val cached = getLocalPath(context, imageUrl)
        if (cached.isNotEmpty()) {
            Log.d(TAG, "Image already cached: $imageUrl")
            return cached
        }
        try {
            val request = Request.Builder().url(imageUrl)
                .header("User-Agent", "TrendScope/1.0").build()
            val response = client.newCall(request).execute()
            if (!response.isSuccessful) {
                Log.w(TAG, "Failed to download image: HTTP ${response.code} for $imageUrl")
                return ""
            }
            val input = response.body?.byteStream() ?: return ""
            val file = File(getCacheDir(context), hashUrl(imageUrl))
            FileOutputStream(file).use { output ->
                input.copyTo(output)
            }
            input.close()
            Log.d(TAG, "Cached image: $imageUrl -> ${file.absolutePath}")
            return file.absolutePath
        } catch (e: Exception) {
            Log.e(TAG, "Failed to cache image: $imageUrl", e)
            return ""
        }
    }

    fun loadBitmap(localPath: String): Bitmap? {
        if (localPath.isEmpty()) return null
        val file = File(localPath)
        if (!file.exists()) return null
        return try {
            BitmapFactory.decodeFile(localPath)
        } catch (e: Exception) {
            Log.e(TAG, "Failed to load bitmap from $localPath", e)
            null
        }
    }

    fun deleteCachedImage(localPath: String) {
        if (localPath.isEmpty()) return
        try {
            val file = File(localPath)
            if (file.exists()) {
                file.delete()
                Log.d(TAG, "Deleted cached image: $localPath")
            }
        } catch (e: Exception) {
            Log.e(TAG, "Failed to delete cached image: $localPath", e)
        }
    }
}
