# TrendScope

**TrendScope** is an intelligent, real-time news aggregation platform built for **Pace Techfeast '26**. It combines a Flask-based web dashboard with an Android app to deliver trending news across **25 domains** with offline support, translation, and PDF export.

## Features

- **25 Domains & 85+ Sub-Topics** - AI, Cybersecurity, Sports, Crypto, Food, and more
- **Real-Time Trending Feed** - Instantly loads top stories from multiple domains
- **Advanced Search & Filtering** - Domain, sub-topic, keyword, date range, and sort options
- **PDF Report Generation** - Export filtered news to a formatted PDF
- **Dark/Light Theme Toggle** - Seamless theme switching with persistence
- **Offline Reading** - Download articles with images for offline access
- **Multi-Language Translation** - Translate articles to 11 Indian languages (bn, gu, hi, kn, ml, mr, pa, ta, te, ur)
- **Zero API Keys Required** - Powered by public RSS feeds (no API key needed)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask, feedparser, fpdf2 |
| Android | Kotlin, Room, Coil, OkHttp, ViewModel, LiveData, WorkManager, DataStore |
| Frontend | HTML5, CSS3 (CSS Variables), Vanilla JavaScript |
| Icons | Iconify (Lucide Icons) |
| Fonts | Inter, Playfair Display |

## Project Structure

```
TrendScope/
├── android/TrendScope/          # Android app (Kotlin)
│   └── app/src/main/
│       ├── java/com/trendscope/app/
│       │   ├── MainActivity.kt         # Main activity with tabs, search, theme
│       │   ├── ArticleActivity.kt      # Article detail with download/translate
│       │   ├── ArticleAdapter.kt       # RecyclerView adapter with headers
│       │   ├── CategoryActivity.kt     # Category browsing
│       │   ├── CategoryAdapter.kt      # Category grid adapter
│       │   ├── data/                   # Room DB, Article entity, DAO, ImageCache
│       │   ├── network/                # RSS parsing, API providers, domain feeds
│       │   └── translate/              # Translation manager
│       └── res/                        # Layouts, drawables, strings (11 languages)
│
├── synapse/                     # Python news aggregation pipeline
│   ├── components/get_news.py   # RSS feed scraper
│   ├── config/domain_feeds.py   # 25 domain RSS feed URLs
│   └── pipelines/supervisor.py  # Deduplication pipeline
│
├── templates/index.html         # Flask web frontend
├── app.py                       # Flask web dashboard
├── apk/TrendScope-v3.1.0-release.apk   # Pre-built Android APK
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment variables template
```

## Getting Started

### Python Backend (Web Dashboard)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mahamadkhaleelpathan-png/ai-news.git
   cd ai-news
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application:**
   ```bash
   python app.py
   ```

5. **Open in browser:** Navigate to http://localhost:5000

### Android App

#### Prerequisites
- Android Studio Hedgehog (2023.1.1) or later
- JDK 17
- Android SDK 34

#### Build Steps

1. **Open the project:**
   ```
   File -> Open -> android/TrendScope
   ```

2. **Set up keystore (for release builds):**
   Create a keystore or use the existing one:
   ```bash
   cd android/TrendScope/app
   keytool -genkey -v -keystore release.keystore -alias trendscope -keyalg RSA -keysize 2048 -validity 10000
   ```

3. **Set environment variables (or add to gradle.properties):**
   ```bash
   $env:KEYSTORE_STORE_PASSWORD="your_password"
   $env:KEYSTORE_KEY_PASSWORD="your_password"
   ```

4. **Build release APK:**
   ```bash
   cd android/TrendScope
   ./gradlew assembleRelease
   ```

5. **APK location:** `app/build/outputs/apk/release/app-release.apk`

#### Environment Variables (Android)
| Variable | Description | Default |
|----------|-------------|---------|
| KEYSTORE_PATH | Path to keystore file | release.keystore |
| KEYSTORE_STORE_PASSWORD | Keystore store password | (from gradle.properties) |
| KEYSTORE_KEY_ALIAS | Key alias | trendscope |
| KEYSTORE_KEY_PASSWORD | Key password | (from gradle.properties) |
| GNEWS_API_KEY | GNews API key (optional) | (from gradle.properties) |
| NEWSAPI_KEY | NewsData API key (optional) | (from gradle.properties) |

#### Debug Build (no signing required)
```bash
./gradlew assembleDebug
# APK at: app/build/outputs/apk/debug/app-debug.apk
```

## Download APK

You can download the latest APK directly:
- **Direct download:** `https://raw.githubusercontent.com/mahamadkhaleelpathan-png/ai-news/main/apk/TrendScope-v3.1.0-release.apk`
- Or from the GitHub Releases page

## API Keys

This app works **without any API keys** — all news comes from public RSS feeds. However, if you want additional news sources:

1. Copy `.env.example` to `.env`
2. Get free API keys from:
   - [GNews](https://gnews.io/) (free tier: 100 requests/day)
   - [NewsData](https://newsdata.io/) (free tier: 200 requests/day)
3. Add them to your `.env` file

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
