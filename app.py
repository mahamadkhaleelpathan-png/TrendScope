from flask import Flask, jsonify, send_file, request
from datetime import datetime, timedelta
from urllib.parse import quote
from synapse.components.get_news import NewsScraper
from synapse.pipelines.supervisor import run_weekly_pipeline
from synapse.config.domain_feeds import DOMAIN_RSS_FEEDS
import glob, os, json, re, csv, io

app = Flask(__name__)
DOMAINS = {
    "Artificial Intelligence (AI)": {"Machine Learning": "machine learning", "LLMs": "LLM OR GPT OR Claude", "Robotics": "robotics", "AI Ethics": "AI ethics"},
    "Technology": {"Software & Apps": "software development OR apps", "Internet Trends": "internet trends", "IT": "cloud computing OR servers"},
    "Business & Startups": {"Startups": "startups OR founders", "Venture Capital": "venture capital", "Corporate": "corporate earnings"},
    "Finance & Stock Market": {"Stocks": "stock market OR wall street", "Banking": "banking OR interest rates", "Economy": "global economy"},
    "Health & Fitness": {"Medical": "medical research", "Mental Health": "mental health", "Fitness": "fitness OR workouts"},
    "Education & Careers": {"Universities": "universities OR college", "EdTech": "online courses OR edtech", "Jobs": "job market"},
    "Entertainment": {"Movies/TV": "movies OR netflix", "Music": "music industry", "Celebs": "celebrities"},
    "Sports": {"Cricket": "cricket OR IPL", "Football": "football OR soccer", "NBA": "basketball OR NBA"},
    "World News": {"Elections": "elections OR government", "Geopolitics": "geopolitics OR UN", "Diplomacy": "diplomacy"},
    "Science & Space": {"Space": "NASA OR SpaceX", "Physics": "physics OR quantum", "Climate": "climate science"},
    "Cybersecurity": {"Breaches": "data breach", "Malware": "malware OR ransomware", "Privacy": "digital privacy"},
    "Gaming": {"PC/Console": "xbox OR playstation", "Mobile": "mobile games", "Esports": "esports"},
    "Mobile & Gadgets": {"Phones": "iphone OR android", "Laptops": "laptops OR hardware", "Smart Home": "smart home gadgets"},
    "Cryptocurrency": {"Bitcoin": "bitcoin OR ethereum", "Web3": "web3 OR NFTs", "Regulation": "crypto regulation"},
    "Environment": {"Warming": "global warming", "Energy": "solar OR wind energy", "Wildlife": "wildlife conservation"},
    "Travel & Tourism": {"Destinations": "travel destinations", "Airlines": "airlines", "Hotels": "airbnb OR hotels"},
    "Food & Lifestyle": {"Food": "recipes OR cooking", "Trends": "food trends OR diets", "Wellness": "lifestyle OR wellness"},
    "Automobiles": {"EVs": "tesla OR electric vehicles", "Launches": "new cars", "Racing": "formula 1"},
    "War & Conflicts": {"Conflicts": "war OR military", "Defense": "defense technology", "Tensions": "sanctions OR borders"},
    "Social Media": {"TikTok/IG": "tiktok OR instagram", "X/Twitter": "X platform OR twitter", "Influencers": "influencers OR viral"},
    "Fashion & Beauty": {"Trends": "fashion trends OR seasonal trends", "Beauty": "skincare OR makeup OR beauty products", "Luxury": "luxury brands OR designer fashion"},
    "Politics & Government": {"Elections": "elections OR voting OR polls", "Policy": "policy OR legislation OR reform", "Diplomacy": "diplomacy OR foreign relations OR treaties"},
    "Real Estate & Property": {"Housing Market": "housing market OR home prices OR real estate", "Commercial": "commercial real estate OR office space", "Mortgages": "mortgage rates OR home loans OR refinancing"},
    "Music": {"New Releases": "new albums OR music releases OR singles", "Concerts": "concerts OR music festivals OR touring", "Industry": "music industry OR streaming OR record labels"},
    "Art & Design": {"Contemporary Art": "contemporary art OR modern art OR galleries", "Design Trends": "design trends OR graphic design OR interior design", "Exhibitions": "art exhibitions OR museums OR biennials"},
}
BOOKMARKS_FILE = "data/bookmarks.json"

def _load_bookmarks():
    if not os.path.exists(BOOKMARKS_FILE):
        return []
    with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_bookmarks(bookmarks):
    os.makedirs("data", exist_ok=True)
    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, indent=2, ensure_ascii=False)

def _fetch_articles(domain, sub, days, q):
    base = DOMAINS.get(domain, {}).get(sub, "")
    query = q if q else (base if base else sub if sub else domain)
    feeds = []
    if domain in DOMAIN_RSS_FEEDS:
        feeds.extend(DOMAIN_RSS_FEEDS[domain])
    feeds.append("https://news.google.com/rss/search?q=" + quote(query) + "&hl=en-US&gl=US&ceid=US:en")
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    scraper = NewsScraper(feeds=feeds)
    result = []
    for a in scraper.extract():
        ad = a.get("date", "")
        if ad and ad >= cutoff:
            a["date_group"] = ad
            result.append(a)
    return result

@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route("/api/domains")
def api_domains():
    return jsonify({d: list(DOMAINS[d].keys()) for d in DOMAINS})

@app.route("/api/news")
def api_news():
    domain = request.args.get("domain", "")
    sub = request.args.get("subtopic", "")
    days = int(request.args.get("days", "7"))
    q = request.args.get("search", "")
    return jsonify(_fetch_articles(domain, sub, days, q))

@app.route("/api/generate-pdf")
def api_pdf():
    domain = request.args.get("domain", "")
    sub = request.args.get("subtopic", "")
    days = int(request.args.get("days", "7"))
    q = request.args.get("search", "")
    base = DOMAINS.get(domain, {}).get(sub, "")
    query = q if q else (base if base else sub if sub else domain)
    feeds = []
    if domain in DOMAIN_RSS_FEEDS:
        feeds.extend(DOMAIN_RSS_FEEDS[domain])
    feeds.append("https://news.google.com/rss/search?q=" + quote(query) + "&hl=en-US&gl=US&ceid=US:en")
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, days)]
    arts = run_weekly_pipeline(dates=dates, feeds=feeds)
    return jsonify({"status": "ok", "count": len(arts) if arts else 0})

@app.route("/api/frequent-categories")
def api_frequent():
    return jsonify([
        {"domain": "Artificial Intelligence (AI)", "subtopic": "LLMs", "label": "AI & LLMs"},
        {"domain": "Technology", "subtopic": "Software & Apps", "label": "Tech Apps"},
        {"domain": "Sports", "subtopic": "Cricket", "label": "Cricket / IPL"},
        {"domain": "Cryptocurrency", "subtopic": "Bitcoin", "label": "Bitcoin & Crypto"},
        {"domain": "Science & Space", "subtopic": "Space", "label": "Space / NASA"},
        {"domain": "Business & Startups", "subtopic": "Startups", "label": "Startups"},
        {"domain": "Entertainment", "subtopic": "Movies/TV", "label": "Movies & TV"},
        {"domain": "Cybersecurity", "subtopic": "Malware", "label": "Cyber Security"},
        {"domain": "World News", "subtopic": "Geopolitics", "label": "World Politics"},
        {"domain": "Mobile & Gadgets", "subtopic": "Phones", "label": "Phones & Gadgets"},
    ])

@app.route("/api/latest-pdf")
def api_latest_pdf():
    pdfs = glob.glob("data/**/*.pdf", recursive=True)
    if not pdfs:
        return jsonify({"error": "none"}), 404
    return send_file(max(pdfs, key=os.path.getctime))

@app.route("/api/bookmarks", methods=["GET", "POST", "DELETE"])
def api_bookmarks():
    if request.method == "GET":
        bm = _load_bookmarks()
        return jsonify(bm)

    if request.method == "POST":
        data = request.get_json(force=True, silent=True) or {}
        if not data.get("url"):
            return jsonify({"error": "url required"}), 400
        bm = _load_bookmarks()
        exists = any(b.get("url") == data["url"] for b in bm)
        if not exists:
            bm.append({
                "title": data.get("title", ""),
                "url": data["url"],
                "author": data.get("author", ""),
                "content": data.get("content", ""),
                "image_url": data.get("image_url", ""),
                "domain": data.get("domain", ""),
                "date": data.get("date", ""),
                "saved_at": datetime.now().isoformat(),
            })
            _save_bookmarks(bm)
        return jsonify({"status": "saved", "count": len(bm)})

    if request.method == "DELETE":
        url = request.args.get("url", "")
        if not url:
            return jsonify({"error": "url required"}), 400
        bm = _load_bookmarks()
        bm = [b for b in bm if b.get("url") != url]
        _save_bookmarks(bm)
        return jsonify({"status": "removed", "count": len(bm)})

@app.route("/api/trending")
def api_trending():
    seen = set()
    words = {}
    domain = request.args.get("domain", "")
    test_domains = [domain] if domain else list(DOMAINS.keys())[:6]
    for d in test_domains:
        try:
            arts = _fetch_articles(d, "", 1, "")
            for a in arts:
                t = a.get("title", "")
                if t in seen:
                    continue
                seen.add(t)
                for w in re.findall(r"[A-Za-z]{4,}", t):
                    wl = w.lower()
                    if wl not in ("that", "with", "this", "from", "have", "been", "will", "what", "they", "into", "over", "more", "than", "also", "after", "about", "their", "latest", "would", "could", "should", "first", "after", "still", "other", "which", "these", "those", "there"):
                        words[wl] = words.get(wl, 0) + 1
        except Exception:
            continue
    top = sorted(words.items(), key=lambda x: -x[1])[:25]
    return jsonify([{"word": w, "count": c} for w, c in top])

@app.route("/api/export/<fmt>")
def api_export(fmt):
    domain = request.args.get("domain", "")
    sub = request.args.get("subtopic", "")
    days = int(request.args.get("days", "7"))
    q = request.args.get("search", "")
    arts = _fetch_articles(domain, sub, days, q)

    if fmt == "json":
        path = "data/export.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(arts, f, indent=2, ensure_ascii=False)
        return send_file(path, as_attachment=True, download_name="articles.json")

    if fmt == "csv":
        si = io.StringIO()
        w = csv.writer(si)
        w.writerow(["title", "author", "url", "date", "content"])
        for a in arts:
            w.writerow([a.get("title", ""), a.get("author", ""), a.get("url", ""), a.get("date", ""), a.get("content", "")])
        mem = io.BytesIO(si.getvalue().encode("utf-8"))
        return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="articles.csv")

    return jsonify({"error": "unsupported format"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
