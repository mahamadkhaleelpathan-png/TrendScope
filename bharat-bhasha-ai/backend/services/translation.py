import requests
import json
import hashlib
import os

class TranslationService:
    def __init__(self):
        self.cache_dir = os.path.join(os.path.dirname(__file__), "..", "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.api_key = os.getenv("GOOGLE_TRANSLATE_KEY", "")

    def _cache_key(self, text, source, target):
        raw = f"{text}:{source}:{target}"
        return hashlib.md5(raw.encode()).hexdigest()

    def _get_cached(self, key):
        path = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return None

    def _set_cache(self, key, data):
        path = os.path.join(self.cache_dir, f"{key}.json")
        with open(path, "w") as f:
            json.dump(data, f)

    def translate(self, text, source_lang, target_lang):
        if not text or source_lang == target_lang:
            return {"translated_text": text, "confidence": 1.0, "source": "identity"}

        key = self._cache_key(text, source_lang, target_lang)
        cached = self._get_cached(key)
        if cached:
            return cached

        result = self._translate_libretranslate(text, source_lang, target_lang)
        if result:
            self._set_cache(key, result)
            return result

        result = self._translate_google_free(text, source_lang, target_lang)
        if result:
            self._set_cache(key, result)
            return result

        return {"translated_text": text, "confidence": 0.0, "source": "failed"}

    def _translate_libretranslate(self, text, source, target):
        try:
            resp = requests.post(
                "https://libretranslate.com/translate",
                json={"q": text, "source": source, "target": target, "format": "text"},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                return {"translated_text": data.get("translatedText", text), "confidence": 0.85, "source": "libre"}
        except:
            pass
        return None

    def _translate_google_free(self, text, source, target):
        try:
            url = "https://translate.googleapis.com/translate_a/single"
            params = {"client": "gtx", "sl": source, "tl": target, "dt": "t", "q": text}
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                translated = "".join(part[0] for part in data[0] if part[0])
                conf = min(0.95, float(data[0][0][1]) if len(data[0]) > 0 and len(data[0][0]) > 1 and data[0][0][1] else 0.9)
                return {"translated_text": translated, "confidence": conf, "source": "google"}
        except:
            pass
        return None

    def detect_language(self, text):
        if not text:
            return "en"
        try:
            resp = requests.post(
                "https://libretranslate.com/detect",
                json={"q": text},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    return data[0].get("language", "en")
        except:
            pass
        try:
            url = "https://translate.googleapis.com/translate_a/single"
            params = {"client": "gtx", "sl": "auto", "tl": "en", "dt": "t", "q": text[:100]}
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                return resp.json()[2]
        except:
            pass
        return "en"
