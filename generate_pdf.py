from fpdf import FPDF
import os

class TrendScopePDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, "TrendScope - Project Documentation", align="C")
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(25, 35, 75)
        self.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(25, 35, 75)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(60, 60, 80)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(80, 80, 100)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        x = self.l_margin
        y = self.get_y()
        self.set_xy(x, y)
        self.cell(5, 5.5, "-")
        self.set_xy(x + 5, y)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 5, 5.5, text)

    def code_block(self, code, label=""):
        if label:
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(100, 100, 120)
            self.cell(0, 6, label, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Courier", "", 7.5)
        self.set_text_color(20, 60, 100)
        self.set_fill_color(240, 243, 250)
        self.set_draw_color(200, 210, 230)
        lines = code.split("\n")
        block_h = min(len(lines), 60) * 4 + 4
        start_y = self.get_y()
        if start_y + block_h > self.h - 25:
            self.add_page()
            start_y = self.get_y()
        cw = self.w - self.l_margin - self.r_margin
        self.rect(self.l_margin, start_y, cw, block_h)
        for i, line in enumerate(lines):
            if i >= 60:
                self.set_xy(self.l_margin + 2, self.get_y())
                self.multi_cell(cw - 4, 4, "... (truncated)")
                break
            if self.get_y() > start_y + block_h - 4:
                break
            self.set_xy(self.l_margin + 2, self.get_y())
            self.multi_cell(cw - 4, 4, line)
        self.set_y(start_y + block_h + 4)

    def key_value(self, key, value):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 30, 30)
        kw = self.get_string_width(key + ": ") + 2
        self.cell(kw, 5.5, key + ": ")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, value)

    def add_diagram(self, path, caption=""):
        if os.path.exists(path):
            iw = self.w - self.l_margin - self.r_margin
            ih = iw * 0.56
            if self.get_y() + ih > self.h - 25:
                self.add_page()
            self.image(path, x=self.l_margin, w=iw, h=ih)
            if caption:
                self.set_font("Helvetica", "I", 9)
                self.set_text_color(100, 100, 120)
                self.cell(0, 6, caption, align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(4)

pdf = TrendScopePDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Title page
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(25, 35, 75)
pdf.ln(50)
pdf.cell(0, 15, "TrendScope", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 16)
pdf.set_text_color(80, 80, 120)
pdf.cell(0, 10, "Complete Project Documentation", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_font("Helvetica", "I", 11)
pdf.set_text_color(120, 120, 140)
pdf.cell(0, 8, "Pace Techfeast '26", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.cell(0, 8, "July 2026", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(30)

# Table of Contents
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(25, 35, 75)
pdf.cell(0, 10, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
toc_items = [
    "1. Project Overview",
    "2. Project Structure",
    "3. Python Web Application (Flask)",
    "4. Python Desktop Application (Tkinter)",
    "5. Android Native Application (TrendScope)",
    "6. Android Architecture & Components",
    "7. Translation System",
    "8. RSS News Aggregation",
    "9. Setup & Installation",
    "10. API Reference",
]
for item in toc_items:
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(10, 7, "")
    pdf.cell(0, 7, item, new_x="LMARGIN", new_y="NEXT")

# ================ SECTION 1: OVERVIEW ================
pdf.add_page()
pdf.section_title("1. Project Overview")
pdf.body_text(
    "TrendScope is an intelligent, real-time news aggregation platform designed to cut through the noise. "
    "It allows users to instantly fetch, filter, and read trending news across 25 unique domains and 85+ sub-topics "
    "from a clean, elegant interface. The project includes three distinct interfaces:"
)
pdf.bullet("Python Web Dashboard (Flask) - Browser-based interface with dark/light mode, PDF export, and live activity logs")
pdf.bullet("Python Desktop App (Tkinter) - Native Windows GUI with domain/sub-topic selection and article viewer")
pdf.bullet("Android Native App (TrendScope) - Full-featured mobile app with 24 categories, emoji icons, favicons, "
           "on-device translation for 10 Indian languages, day-based article grouping, and bookmark support")
pdf.ln(3)
pdf.body_text(
    "All interfaces share a common RSS-based news aggregation engine powered by Google News RSS feeds and "
    "public news sources across 25 domains including AI, Technology, Sports, Finance, Health, Science, "
    "Cybersecurity, Gaming, Crypto, Entertainment, World News, and more."
)

pdf.add_diagram("diagrams/system_architecture.png", "Figure 1: System Architecture - Users, Backend, Storage & Output")

# ================ SECTION 2: PROJECT STRUCTURE ================
pdf.add_page()
pdf.section_title("2. Project Structure")
pdf.code_block("""pace_tech-feast--main/
+-- app.py                    # Flask backend - API routes, RSS parsing, PDF gen
+-- main.py                   # Tkinter desktop GUI application
+-- launcher.py               # Flask + Cloudflare tunnel launcher
+-- viewer.py                 # Article display helper for Tkinter
+-- pdf_opener.py             # HTML-based PDF viewer
+-- clean_layout.py           # Generates templates/index.html
+-- build_data.py             # Generates _data.json (domains + images)
+-- build_html.py             # Full HTML/CSS/JS generator (653 lines)
+-- requirements.txt          # Python dependencies
+-- README.md                 # Project documentation
+-- TODO.md                   # Task list
+-- templates/
|   +-- index.html            # Single-page web app (generated)
+-- synapse/
|   +-- components/
|   |   +-- get_news.py       # NewsScraper class - RSS fetching + parsing
|   +-- config/
|   |   +-- domain_feeds.py   # DOMAIN_RSS_FEEDS - 25 domain RSS URLs
|   +-- pipelines/
|       +-- supervisor.py     # run_weekly_pipeline - orchestration
+-- android/
    +-- TrendScope/
        +-- build.gradle.kts
        +-- settings.gradle.kts
        +-- app/
            +-- build.gradle.kts
            +-- release.keystore
            +-- src/main/
                +-- AndroidManifest.xml
                +-- java/com/trendscope/app/
                |   +-- MainActivity.kt
                |   +-- ArticleActivity.kt
                |   +-- ArticleAdapter.kt
                |   +-- CategoryActivity.kt
                |   +-- CategoryAdapter.kt
                |   +-- data/
                |   |   +-- Article.kt, ArticleDao.kt, AppDatabase.kt
                |   +-- network/
                |   |   +-- DomainFeeds.kt, RssParser.kt
                |   +-- translate/
                |       +-- TranslationManager.kt
                +-- res/
                    +-- drawable/, layout/, menu/, mipmap-*/
                    +-- values/ (10 Indian languages + English)""", "Directory Tree")

# ================ SECTION 3: PYTHON WEB APP ================
pdf.add_page()
pdf.section_title("3. Python Web Application (Flask)")
pdf.body_text(
    "The Flask web backend serves as the primary API server for the web dashboard. It provides RESTful endpoints "
    "for fetching news, generating PDF reports, managing bookmarks, and exporting data. The frontend is a single-page "
    "HTML application generated by build_html.py / clean_layout.py."
)
pdf.sub_title("Key Features")
pdf.bullet("25 domains with 85+ sub-topics for granular news filtering")
pdf.bullet("Real-time RSS feed fetching with date-range filtering (1/7/30 days)")
pdf.bullet("Advanced search combining domain, sub-topic, custom query, and time range")
pdf.bullet("PDF report generation with fpdf2")
pdf.bullet("Trending words extraction across top news domains")
pdf.bullet("Bookmark management with CRUD API")
pdf.bullet("Export to JSON and CSV formats")
pdf.bullet("Live activity log showing fetch progress and errors")
pdf.bullet("Dark/Light theme toggle with localStorage persistence")
pdf.bullet("Frequent categories quick-access panel")
pdf.ln(2)
pdf.sub_title("API Routes")
pdf.code_block("""GET  /                         Serves the SPA frontend (templates/index.html)
GET  /api/domains               Returns dict of domains -> [subtopics]
GET  /api/news                  Fetch articles: ?domain=&subtopic=&days=&search=
GET  /api/trending              Extract top trending words from recent articles
GET  /api/generate-pdf          Generate PDF report for given filters
GET  /api/latest-pdf            Download the most recently generated PDF
GET  /api/frequent-categories   Returns 10 most-used category shortcuts
GET  /api/export/json           Export articles as JSON download
GET  /api/export/csv            Export articles as CSV download
POST /api/bookmarks             Save a bookmark (JSON body)
GET  /api/bookmarks             List all bookmarks
DELETE /api/bookmarks           Remove a bookmark (?url=)""", "Flask Routes")
pdf.ln(2)

pdf.sub_title("News Fetching Architecture")
pdf.body_text(
    "The _fetch_articles() function builds a query from the selected domain and sub-topic, constructs RSS feed URLs "
    "(combining domain-specific feeds from DOMAIN_RSS_FEEDS with a Google News RSS search URL), and uses the "
    "NewsScraper class to parse articles. Results are filtered by the cutoff date (1/7/30 days)."
)

# ================ SECTION 4: TKINTER APP ================
pdf.add_page()
pdf.section_title("4. Python Desktop Application (Tkinter)")
pdf.body_text(
    "The Tkinter-based desktop GUI (main.py) mirrors the web app functionality with a native Windows interface. "
    "It provides the same domain/sub-topic browsing, article fetching, and PDF report generation."
)
pdf.sub_title("TrendScopeUI Class")
pdf.code_block("""+-- TrendScopeUI
    +-- __init__()          Window setup (1050x680, dark theme)
    +-- build_ui()          Constructs all widgets
    |   +-- Header: title, subtitle, theme controls
    |   +-- Trending bar: horizontal scroll of word clouds
    |   +-- Domain listbox (left panel)
    |   +-- Sub-topic listbox (center-top)
    |   +-- Date range radio buttons (1/7/30 days)
    |   +-- Search entry with placeholder
    |   +-- Generate PDF / Open Latest buttons
    |   +-- Article viewer text box (rich text)
    |   +-- Live activity log (right sidebar)
    +-- on_main_select()    Populates sub-topics for selected domain
    +-- on_sub_select()     Stores selected sub-topic
    +-- start_generation()  Fetches articles + generates PDF
    +-- open_latest_pdf()   Opens latest PDF via pdf_opener.py
    +-- add_log()           Appends timestamped log messages""", "Desktop Application Architecture")

pdf.ln(2)
pdf.sub_title("Color Theme")
pdf.code_block("""Background (dark)    #0f172a (Slate 900)
Panel background     #1e293b (Slate 800)
Accent               #8b5cf6 (Violet 500)
Text main            #f1f5f9 (Slate 100)
Text subtle          #94a3b8 (Slate 400)
Success              #22c55e (Green 500)
Danger               #ef4444 (Red 500)""", "Color Palette")

# ================ SECTION 5: ANDROID APP ================
pdf.add_page()
pdf.section_title("5. Android Native Application (TrendScope)")
pdf.body_text(
    "TrendScope for Android is a fully native Kotlin application targeting API 26+ with a modern Material Design "
    "interface. It provides the complete news aggregation experience on mobile with additional native features "
    "including on-device translation, domain favicons, emoji category icons, and bookmarks."
)
pdf.sub_title("Build Configuration")
pdf.code_block("""Plugins:      Android Application, Kotlin Android, KAPT, Kotlin Serialization
compileSdk:   34
targetSdk:    34
minSdk:       26
versionCode:  3
versionName:  3.0.0
Java:         JDK 17
Signing:      release.keystore
ProGuard:     minifyEnabled = true
View Binding: enabled""", "build.gradle.kts Summary")

pdf.sub_title("Dependencies")
pdf.code_block("""androidx.core:core-ktx:1.12.0              App compat
com.google.android.material:material:1.11.0  Material Design
androidx.room:room-runtime:2.6.1             Room Database
androidx.room:room-compiler:2.6.1 (kapt)     Room annotation processor
com.squareup.okhttp3:okhttp:4.12.0            HTTP client
org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3
io.coil-kt:coil:2.5.0                         Image loading
androidx.lifecycle:lifecycle-*:2.7.0          Lifecycle components""", "Key Dependencies")

pdf.add_diagram("diagrams/android_architecture.png", "Figure 2: Android App Architecture - Layered Design")

# ================ SECTION 6: ANDROID COMPONENTS ================
pdf.add_page()
pdf.section_title("6. Android Architecture & Components")

pdf.sub_title("Activities (4 screens)")
pdf.body_text("The app uses a standard single-Activity architecture with 3 activities:")
pdf.ln(1)
pdf.sub_sub_title("MainActivity.kt (289 lines)")
pdf.body_text(
    "The primary activity with three tabs: Categories (grid of 24 emoji-coded categories), All News "
    "(chronological article list with day headers), and Bookmarks (saved articles). Includes a toolbar "
    "with language selector menu, search functionality, and RSS feed refresh. Manages batch article "
    "translation and persistent language preference via SharedPreferences."
)
pdf.sub_sub_title("CategoryActivity.kt (76 lines)")
pdf.body_text(
    "Opened when a category card is tapped. Displays all articles filtered by the selected category. "
    "Supports swipe-to-refresh and passes the selected language for translation display."
)
pdf.sub_sub_title("ArticleActivity.kt (143 lines)")
pdf.body_text(
    "Full article detail view showing title, source, date, content, and image. Features include "
    "bookmark toggle (heart icon), share via Android intent, 'Open Original' button loading the "
    "source URL in browser, and translated content display when a non-English language is active."
)

pdf.sub_title("Data Layer")
pdf.sub_sub_title("Article.kt (Room Entity)")
pdf.code_block("""@Entity(tableName = "articles")
data class Article(
    @PrimaryKey val link: String,
    val title: String,
    val description: String,
    val content: String = "",
    val pubDate: String,
    val imageUrl: String = "",
    val source: String,
    val category: String,
    val isBookmarked: Boolean = false,
    val fetchedAt: Long = System.currentTimeMillis(),
    val pubDateMillis: Long = 0L,
    val translatedTitle: String = "",
    val translatedDescription: String = "",
    val translatedContent: String = "",
    val translateLang: String = ""
)""", "Article Entity")
pdf.ln(1)

pdf.sub_sub_title("ArticleDao.kt")
pdf.code_block("""Key queries:
- getAllArticles()           -> All articles ordered by date
- getArticlesByCategory()    -> Filtered by category
- getBookmarks()             -> Bookmarked articles only
- searchArticles(query)      -> Full-text search (title, desc, translations)
- insertArticles()           -> Batch insert with REPLACE strategy
- updateTranslation()        -> Update translated text + language code
- toggleBookmark()           -> Toggle bookmark status
- getArticlesNotInLang()     -> Articles needing translation
- getCount()                 -> Total article count""", "DAO Operations")

pdf.sub_sub_title("AppDatabase.kt")
pdf.code_block("""@Database(entities = [Article::class], version = 3)
TrendScope database singleton with destructive migration fallback.""", "Database")

pdf.sub_title("View Layer")
pdf.sub_sub_title("ArticleAdapter.kt (164 lines)")
pdf.body_text(
    "RecyclerView adapter that groups articles into sections with day headers "
    "(Today, Yesterday, This Week, This Month, Earlier/Monthly). Each article card displays: "
    "domain favicon, title (translated when language active), source, date, description preview, "
    "and thumbnail image. Uses coroutine-based image loading via raw HTTP connections."
)
pdf.sub_sub_title("CategoryAdapter.kt (48 lines)")
pdf.body_text(
    "Grid adapter (2 columns) displaying 24 category cards. Each card shows the category emoji "
    "and name with a randomly colored background from a curated palette."
)

# ================ SECTION 7: TRANSLATION ================
pdf.add_page()
pdf.section_title("7. Translation System")
pdf.body_text(
    "The Android app provides cloud-based translation across 10 Indian languages. "
    "The system uses a primary API with automatic fallback for reliability."
)
pdf.sub_title("Supported Languages")
pdf.code_block("""Code  Language       Native Name      Type
hi    Hindi         Hindi            Full
bn    Bengali       Bangla           Full
te    Telugu        Telugu           Full
ta    Tamil         Tamil            Full
mr    Marathi       Marathi          Full
gu    Gujarati      Gujarati         Full
kn    Kannada       Kannada          Full
ml    Malayalam     Malayalam        Full
pa    Punjabi       Punjabi          Full
ur    Urdu          Urdu             Full""", "10 Indian Languages")
pdf.ln(2)

pdf.sub_title("Architecture")
pdf.body_text(
    "TranslationManager is a singleton object that provides a suspend function for translation. "
    "It uses a two-tier API strategy:"
)
pdf.bullet("Primary: MyMemory API (api.mymemory.translated.net) - generous free tier, no API key required")
pdf.bullet("Fallback: LibreTranslate (libretranslate.com/translate) - open-source, used when MyMemory fails")
pdf.ln(2)

pdf.add_diagram("diagrams/translation_flow.png", "Figure 3: Translation Pipeline - API Call Flow")

pdf.sub_title("Translation Flow")
pdf.code_block("""User selects language
    -> setLanguage(code) called
    -> Switch to All News tab
    -> translateAllArticles(targetLang) launched
    -> getArticlesNotInLang() from Room
    -> For each article (sequentially, 600ms gap):
        -> translate(title) via MyMemory -> LibreTranslate fallback
        -> 400ms delay
        -> translate(description)
        -> 400ms delay
        -> translate(content)
        -> updateTranslation() in Room DB
    -> refreshCurrentView() loads translated articles
    -> New ArticleAdapter displays translated text""", "Sequential Translation Pipeline")
pdf.ln(2)

pdf.sub_title("UI String Resources")
pdf.body_text(
    "All UI strings (tabs, buttons, status messages) are provided in all 10 Indian languages plus English. "
    "The app uses Android's locale-based resource resolution with values-{lang}/strings.xml files."
)
pdf.code_block("""Strings include: app_name, tab_categories, tab_all_news, tab_bookmarks,
search_hint, today, yesterday, this_week, this_month, earlier,
open_original, no_bookmarks, bookmarked, removed_bookmark,
select_language, language, status_starting, status_fetching,
status_translating, status_translating_count, translation_complete,
translation_partial, loading_articles""", "21 String Resources per Language")

# ================ SECTION 8: RSS NEWS AGGREGATION ================
pdf.add_page()
pdf.section_title("8. RSS News Aggregation")

pdf.sub_title("24 Categories")
pdf.code_block("""Category                       Icon
Artificial Intelligence       AI
Technology                    TC
Sports                        SP
Finance                       FN
Health & Fitness              HF
Education & Careers           ED
Entertainment                 EN
Business & Startups           BS
World News                    WN
Science & Space               SS
Cybersecurity                 CS
Gaming                        GM
Mobile & Gadgets              MG
Cryptocurrency                CR
Environment                   EV
Travel & Tourism              TR
Food & Lifestyle              FL
Automobiles                   AU
War & Conflicts               WC
Social Media                  SM
Fashion & Beauty              FB
Politics & Government         PG
Real Estate & Property        RE
Music                         MU""", "Category Index with Emoji Icons")

pdf.sub_title("RssParser.kt (186 lines)")
pdf.body_text(
    "The RSS parser uses Android's XmlPullParser to parse RSS 2.0 and Atom feeds from multiple sources. Key features:"
)
pdf.bullet("Parses title, link, description, pubDate, and image from <enclosure>, <media:content>, or <img> tags")
pdf.bullet("Date formatting from multiple RSS date formats to 'MMM dd, yyyy HH:mm' display format")
pdf.bullet("pubDateMillis computed for day-based grouping (Today/Yesterday/This Week/This Month)")
pdf.bullet("Batch fetching across all 24 categories with per-article callback")
pdf.bullet("HTML tag stripping from description text")
pdf.bullet("Per-source RSS feed URLs defined in DomainFeeds.FEEDS map")

pdf.add_diagram("diagrams/data_flow.png", "Figure 4: Data Pipeline - RSS Feed to Article Display")

pdf.sub_title("Domain Favicons")
pdf.body_text(
    "Each article in the list displays a small favicon next to the source name, loaded from "
    "Google's favicon service: https://www.google.com/s2/favicons?domain=DOMAIN&sz=64. "
    "The DomainFeeds object maps source names to domains via getFaviconUrl()."
)

# ================ SECTION 9: SETUP ================
pdf.add_page()
pdf.section_title("9. Setup & Installation")

pdf.sub_title("Python Web App")
pdf.code_block("""# Prerequisites: Python 3.8+
python -m venv .venv
.venv\\Scripts\\Activate  # Windows
pip install -r requirements.txt
python clean_layout.py     # Generate frontend
python app.py              # Run -> http://localhost:5000""", "Python Setup")
pdf.ln(2)

pdf.sub_title("Android App")
pdf.code_block("""# Prerequisites: JDK 17, Android SDK 34
cd android/TrendScope
gradlew assembleRelease
# Output: app/build/outputs/apk/release/app-release.apk
# Signing: release.keystore (PASSWORD_REMOVED)
# APK Size: ~2.4 MB""", "Android Build")
pdf.ln(2)

pdf.sub_title("Build Outputs")
pdf.code_block("""Python Web App:  http://localhost:5000
Python Desktop:  python main.py (Tkinter GUI)
Android APK:     android/TrendScope/app/build/outputs/apk/release/app-release.apk
APK Size:        2.4 MB (minified + ProGuard)
PDF Reports:     data/*.pdf (generated via web UI)""", "Artifacts")

# ================ SECTION 10: API REFERENCE ================
pdf.add_page()
pdf.section_title("10. API Reference")

pdf.sub_title("Flask API Endpoints")
pdf.code_block("""GET /api/domains
  Returns: {domain_name: [subtopic1, subtopic2, ...]}

GET /api/news?domain=&subtopic=&days=&search=
  Returns: [{title, author, url, date, content, image_url}]

GET /api/trending?domain=
  Returns: [{word, count}] - top 25 trending words

GET /api/generate-pdf?domain=&subtopic=&days=&search=
  Returns: {status, count}

GET /api/latest-pdf
  Returns: PDF file download

GET /api/frequent-categories
  Returns: [{domain, subtopic, label}]

GET /api/bookmarks              List all bookmarks
POST /api/bookmarks             Save bookmark (JSON body)
DELETE /api/bookmarks?url=      Remove bookmark

GET /api/export/json             Export as JSON file
GET /api/export/csv              Export as CSV file""", "Full API Reference")

pdf.ln(2)
pdf.sub_title("Article JSON Schema")
pdf.code_block("""{
  "title":      "Article Title",
  "author":     "Source Name",
  "url":        "https://example.com/article",
  "date":       "2026-07-07",
  "content":    "Full article body text...",
  "image_url":  "https://example.com/image.jpg"
}""", "Article Format")

pdf.ln(5)
pdf.set_font("Helvetica", "I", 10)
pdf.set_text_color(100, 100, 120)
pdf.cell(0, 8, "End of Documentation", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, "Generated July 2026 | TrendScope v3.0.0 | Pace Techfeast '26", align="C")

output_path = os.path.join(os.path.dirname(__file__), "TrendScope_Project_Documentation.pdf")
pdf.output(output_path)
print(f"PDF generated: {output_path}")
