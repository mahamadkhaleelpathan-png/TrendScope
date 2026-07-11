package com.trendscope.app.translate

import android.util.Log
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.net.URLEncoder
import java.util.concurrent.TimeUnit

object TranslationManager {
    private const val TAG = "TranslationManager"
    private val client = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    private val JSON_MEDIA = "application/json; charset=utf-8".toMediaType()

    val ALL_LANGUAGES = listOf(
        "en", "hi", "te", "ta", "kn", "ml", "mr", "bn", "gu", "pa",
        "or", "as", "ur", "sa", "kok", "mni", "ne", "brx", "doi", "mai", "sat", "sd", "ks"
    )

    fun getDisplayName(code: String): String = when (code) {
        "en" -> "English"
        "hi" -> "हिन्दी"
        "bn" -> "বাংলা"
        "te" -> "తెలుగు"
        "ta" -> "தமிழ்"
        "mr" -> "मराठी"
        "gu" -> "ગુજરાતી"
        "kn" -> "ಕನ್ನಡ"
        "ml" -> "മലയാളം"
        "pa" -> "ਪੰਜਾਬੀ"
        "or" -> "ଓଡ଼ିଆ"
        "as" -> "অসমীয়া"
        "ur" -> "اردو"
        "sa" -> "संस्कृतम्"
        "kok" -> "कोंकणी"
        "mni" -> "মীতৈ"
        "ne" -> "नेपाली"
        "brx" -> "बरʼ"
        "doi" -> "डोगरी"
        "mai" -> "मैथिली"
        "sat" -> "ᱥᱟᱱᱛᱟᱲᱤ"
        "sd" -> "سنڌي"
        "ks" -> "कॉशुर"
        else -> "Unknown"
    }

    fun getEnglishName(code: String): String = when (code) {
        "en" -> "English"
        "hi" -> "Hindi"
        "bn" -> "Bengali"
        "te" -> "Telugu"
        "ta" -> "Tamil"
        "mr" -> "Marathi"
        "gu" -> "Gujarati"
        "kn" -> "Kannada"
        "ml" -> "Malayalam"
        "pa" -> "Punjabi"
        "or" -> "Odia"
        "as" -> "Assamese"
        "ur" -> "Urdu"
        "sa" -> "Sanskrit"
        "kok" -> "Konkani"
        "mni" -> "Manipuri"
        "ne" -> "Nepali"
        "brx" -> "Bodo"
        "doi" -> "Dogri"
        "mai" -> "Maithili"
        "sat" -> "Santali"
        "sd" -> "Sindhi"
        "ks" -> "Kashmiri"
        else -> "Unknown"
    }

    fun getSupportedLanguages(): List<String> = ALL_LANGUAGES

    suspend fun detectLanguage(text: String): String {
        if (text.isEmpty()) return "en"
        try {
            val json = JSONObject().apply { put("q", text) }
            val body = json.toString().toRequestBody(JSON_MEDIA)
            val request = Request.Builder()
                .url("https://libretranslate.com/detect")
                .header("User-Agent", "TrendScope/1.0")
                .post(body)
                .build()
            val bodyStr = withContext(Dispatchers.IO) {
                val resp = client.newCall(request).execute()
                resp.body?.string()
            }
            if (bodyStr != null) {
                val arr = JSONArray(bodyStr)
                if (arr.length() > 0) {
                    val lang = arr.getJSONObject(0).optString("language", "")
                    if (lang.isNotEmpty()) {
                        Log.d(TAG, "detectLanguage(Libre): $lang")
                        return lang
                    }
                }
            }
        } catch (e: Exception) {
            Log.w(TAG, "LibreTranslate detect failed", e)
        }
        return detectGoogle(text)
    }

    private suspend fun detectGoogle(text: String): String {
        try {
            val url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q=${URLEncoder.encode(text.take(100), "UTF-8")}"
            val request = Request.Builder().url(url).header("User-Agent", "Mozilla/5.0").build()
            val body = withContext(Dispatchers.IO) {
                val resp = client.newCall(request).execute()
                resp.body?.string()
            }
            if (body != null) {
                val arr = JSONArray(body)
                if (arr.length() > 2) {
                    val detected = arr.optString(2, "")
                    if (detected.isNotEmpty()) {
                        Log.d(TAG, "detectLanguage(Google): $detected")
                        return detected
                    }
                }
            }
        } catch (e: Exception) {
            Log.w(TAG, "Google detect failed", e)
        }
        return "en"
    }

    suspend fun translate(text: String, targetLang: String): String {
        return translate(text, "en", targetLang)
    }

    suspend fun translate(text: String, sourceLang: String, targetLang: String): String {
        if (text.isEmpty() || sourceLang == targetLang) return text

        Log.d(TAG, "translate: $sourceLang -> $targetLang, text.length=${text.length}")

        try {
            return translateGoogle(text, sourceLang, targetLang)
        } catch (e: Exception) {
            Log.w(TAG, "Google Translate failed", e)
        }

        try {
            return translateMyMemory(text, sourceLang, targetLang)
        } catch (e: Exception) {
            Log.w(TAG, "MyMemory failed", e)
        }

        try {
            return translateLibre(text, sourceLang, targetLang)
        } catch (e: Exception) {
            Log.w(TAG, "LibreTranslate failed", e)
        }

        val msg = "All backends failed: $sourceLang -> $targetLang"
        Log.e(TAG, msg)
        throw Exception(msg)
    }

    @Throws(Exception::class)
    private suspend fun translateGoogle(text: String, source: String, target: String): String {
        val src = if (source == "auto" || source == "auto") "auto" else source
        val url = "https://translate.googleapis.com/translate_a/single" +
            "?client=gtx&sl=$src&tl=$target&dt=t&q=${URLEncoder.encode(text, "UTF-8")}"
        val request = Request.Builder().url(url)
            .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            .header("Accept", "application/json")
            .build()

        val body = withContext(Dispatchers.IO) {
            val resp = client.newCall(request).execute()
            if (!resp.isSuccessful) throw Exception("Google API returned ${resp.code}")
            resp.body?.string() ?: throw Exception("Google API returned empty body")
        }

        val arr = JSONArray(body)
        val sb = StringBuilder()
        val first = arr.optJSONArray(0)
        if (first != null) {
            for (i in 0 until first.length()) {
                val part = first.optJSONArray(i)
                if (part != null) sb.append(part.optString(0, ""))
            }
        }
        val translated = sb.toString()
        if (translated.isEmpty()) throw Exception("Google Translate returned empty result")
        Log.d(TAG, "translateGoogle OK: ${translated.take(50)}...")
        return translated
    }

    @Throws(Exception::class)
    private suspend fun translateMyMemory(text: String, source: String, target: String): String {
        val url = "https://api.mymemory.translated.net/get" +
            "?q=${URLEncoder.encode(text, "UTF-8")}&langpair=$source|$target"
        val request = Request.Builder().url(url)
            .header("User-Agent", "TrendScope/1.0")
            .build()

        val body = withContext(Dispatchers.IO) {
            val resp = client.newCall(request).execute()
            if (!resp.isSuccessful) throw Exception("MyMemory API returned ${resp.code}")
            resp.body?.string() ?: throw Exception("MyMemory returned empty body")
        }

        val json = JSONObject(body)
        val translated = json.optJSONObject("responseData")?.optString("translatedText", "")
        if (translated.isNullOrEmpty() || translated == text) {
            throw Exception("MyMemory returned no translation")
        }
        Log.d(TAG, "translateMyMemory OK: ${translated.take(50)}...")
        return translated
    }

    @Throws(Exception::class)
    private suspend fun translateLibre(text: String, source: String, target: String): String {
        val json = JSONObject().apply {
            put("q", text); put("source", source); put("target", target); put("format", "text")
        }
        val body = json.toString().toRequestBody(JSON_MEDIA)
        val request = Request.Builder()
            .url("https://libretranslate.com/translate")
            .header("User-Agent", "TrendScope/1.0")
            .post(body)
            .build()

        val respBody = withContext(Dispatchers.IO) {
            val resp = client.newCall(request).execute()
            if (!resp.isSuccessful) throw Exception("LibreTranslate returned ${resp.code}")
            resp.body?.string() ?: throw Exception("LibreTranslate returned empty body")
        }

        val result = JSONObject(respBody)
        val translated = result.optString("translatedText", "")
        if (translated.isEmpty() || translated == text) {
            throw Exception("LibreTranslate returned no translation")
        }
        Log.d(TAG, "translateLibre OK: ${translated.take(50)}...")
        return translated
    }
}
