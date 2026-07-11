import json, os
# ========== FIX 1: Clean app.py (no BOM, no encoding issues) ==========
app_code = '''from flask import Flask, jsonify, send_file, request
from datetime import datetime, timedelta
from urllib.parse import quote
from synapse.components.get_news import NewsScraper
from synapse.pipelines.supervisor import run_weekly_pipeline
import glob, os
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
    "Social Media": {"TikTok/IG": "tiktok OR instagram", "X/Twitter": "X platform OR twitter", "Influencers": "influencers OR viral"}
}
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
    base = DOMAINS.get(domain, {}).get(sub, "")
    query = q if q else (base if base else sub if sub else domain)
    url = "https://news.google.com/rss/search?q=" + quote(query) + "&hl=en-US&gl=US&ceid=US:en"
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, days + 1)]
    scraper = NewsScraper(feeds=[url])
    result = []
    for d in dates:
        for a in scraper.extract(d):
            a["date_group"] = d
            result.append(a)
    return jsonify(result)
@app.route("/api/generate-pdf")
def api_pdf():
    domain = request.args.get("domain", "")
    sub = request.args.get("subtopic", "")
    days = int(request.args.get("days", "7"))
    q = request.args.get("search", "")
    base = DOMAINS.get(domain, {}).get(sub, "")
    query = q if q else (base if base else sub if sub else domain)
    url = "https://news.google.com/rss/search?q=" + quote(query) + "&hl=en-US&gl=US&ceid=US:en"
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, days + 1)]
    arts = run_weekly_pipeline(dates=dates, feeds=[url])
    return jsonify({"status": "ok", "count": len(arts) if arts else 0})
@app.route("/api/latest-pdf")
def api_latest_pdf():
    pdfs = glob.glob("data/**/*.pdf", recursive=True)
    if not pdfs:
        return jsonify({"error": "none"}), 404
    return send_file(max(pdfs, key=os.path.getctime))
if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://localhost:5000")
    app.run(debug=False, port=5000)
'''
with open("app.py", "w", encoding="utf-8", newline="\n") as f:
    f.write(app_code)
print("app.py: written cleanly (no BOM)")
# ========== FIX 2: Rebuild index.html ==========
DM = {
    "Artificial Intelligence (AI)": {"Machine Learning": "machine learning", "LLMs & GPT": "LLM OR GPT", "Robotics": "robotics", "Computer Vision": "computer vision", "Generative AI": "generative AI", "AI Ethics": "AI ethics OR bias"},
    "Technology": {"Software & Apps": "software OR apps", "Internet Trends": "internet trends", "Cloud Computing": "cloud computing OR AWS OR Azure", "Semiconductors": "chips OR semiconductors", "5G & 6G": "5G OR 6G technology"},
    "Sports": {"Cricket": "cricket OR IPL", "Football/Soccer": "football OR soccer", "NBA & Basketball": "basketball OR NBA", "Tennis": "tennis", "Formula 1": "formula 1 OR F1", "Esports": "esports"},
    "Business": {"Startups": "startups OR founders", "Venture Capital": "venture capital", "Layoffs & Jobs": "layoffs OR hiring", "Mergers & Acquisitions": "mergers OR acquisitions", "Remote Work": "remote work"},
    "Finance": {"Stock Market": "stock market", "Banking": "banking", "FinTech": "fintech", "Interest Rates": "interest rates OR RBI OR federal reserve", "Real Estate": "real estate"},
    "Health": {"Medical Research": "medical research", "Fitness": "fitness", "Mental Health": "mental health", "Pharma & Drugs": "pharmaceuticals OR new drugs", "Healthcare Tech": "healthcare technology"},
    "Science": {"Space (NASA/SpaceX)": "NASA OR SpaceX", "Physics": "physics", "Biology": "biology OR genetics", "Climate Science": "climate science", "Archaeology": "archaeology"},
    "Cybersecurity": {"Data Breaches": "data breach", "Malware & Ransomware": "malware OR ransomware", "AI in Security": "AI cybersecurity", "Privacy Laws": "privacy laws OR GDPR"},
    "Gaming": {"PC & Console": "xbox OR playstation OR PC gaming", "Mobile Games": "mobile games", "Game Dev": "game development OR Unreal Engine", "VR/AR Gaming": "virtual reality gaming"},
    "Crypto": {"Bitcoin & Ethereum": "bitcoin OR ethereum", "Web3 & NFTs": "web3 OR NFTs", "DeFi": "decentralized finance", "Crypto Regulations": "crypto regulations OR SEC crypto"},
    "Entertainment": {"Movies & Netflix": "movies OR netflix", "Music": "music industry", "Streaming Wars": "streaming wars OR Disney+", "Celebrities": "celebrities OR pop culture", "Anime & K-Pop": "anime OR K-pop"},
    "World News": {"Elections": "elections", "Geopolitics": "geopolitics", "UN & Summits": "United Nations OR global summit", "Protests": "protests OR strikes"},
    "Education": {"Universities": "universities OR college", "EdTech": "online courses OR edtech", "AI in Education": "AI in education", "Exams & Results": "exams OR competitive tests"},
    "Travel": {"Destinations": "travel destinations", "Airlines": "airlines", "Budget Travel": "budget travel", "Luxury Travel": "luxury travel"},
    "Food": {"Recipes & Cooking": "recipes OR cooking", "Food Trends": "food trends", "Restaurants": "restaurants OR fine dining", "Sustainability": "sustainable food"},
    "Automobiles": {"EVs & Tesla": "tesla OR electric vehicles", "New Car Launches": "new car launches", "Self-Driving": "autonomous OR self-driving cars", "Auto Market": "automobile market"},
    "War & Conflicts": {"Global Conflicts": "war OR military conflict", "Defense Tech": "defense technology", "NATO & Alliances": "NATO OR military alliances"},
    "Environment": {"Global Warming": "global warming", "Green Energy": "solar OR wind energy", "Conservation": "wildlife conservation", "Extreme Weather": "extreme weather OR climate disaster"},
    "Social Media": {"TikTok & Instagram": "tiktok OR instagram", "X (Twitter)": "X platform OR twitter", "YouTube": "YouTube trends", "Influencers": "influencers OR creators"}
}
DI = {
    "Artificial Intelligence (AI)": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&h=340&fit=crop",
    "Technology": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=340&fit=crop",
    "Sports": "https://images.unsplash.com/photo-1461896836934-bd45ea8ba7e2?w=600&h=340&fit=crop",
    "Business": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&h=340&fit=crop",
    "Finance": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600&h=340&fit=crop",
    "Health": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=600&h=340&fit=crop",
    "Science": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600&h=340&fit=crop",
    "Cybersecurity": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600&h=340&fit=crop",
    "Gaming": "https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=600&h=340&fit=crop",
    "Crypto": "https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=600&h=340&fit=crop",
    "Entertainment": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600&h=340&fit=crop",
    "World News": "https://images.unsplash.com/photo-1504711434969-e33886168d6c?w=600&h=340&fit=crop",
    "Education": "https://images.unsplash.com/photo-1523050854058-8df90110c476?w=600&h=340&fit=crop",
    "Travel": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600&h=340&fit=crop",
    "Food": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=340&fit=crop",
    "Automobiles": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&h=340&fit=crop",
    "War & Conflicts": "https://images.unsplash.com/photo-1543342574-701859b23c8c?w=600&h=340&fit=crop",
    "Environment": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&h=340&fit=crop",
    "Social Media": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=600&h=340&fit=crop"
}
dm_json = json.dumps(DM)
di_json = json.dumps(DI)
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>TrendScope</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<script src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,system-ui,sans-serif;background:#F8F6F2;color:#1A1A1A;line-height:1.6}
a{color:inherit;text-decoration:none}
::-webkit-scrollbar{width:6px}::-webkit-scrollbar-thumb{background:#ccc;border-radius:6px}
.ticker{height:36px;background:#C8A96A;color:#fff;display:flex;align-items:center;overflow:hidden;font-size:13px;font-weight:600}
.ticker-label{background:rgba(0,0,0,.15);padding:0 16px;height:100%;display:flex;align-items:center;gap:6px;flex-shrink:0;font-size:11px;letter-spacing:.5px;text-transform:uppercase}
.ticker-track{display:flex;animation:scroll 40s linear infinite;white-space:nowrap}
.ticker-track span{padding:0 32px}
@keyframes scroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.header{height:56px;border-bottom:1px solid #E5E5E5;background:#FFF;display:flex;align-items:center;padding:0 24px;position:sticky;top:0;z-index:100}
.logo{font-family:Playfair Display,serif;font-size:22px;font-weight:700;letter-spacing:-.5px;color:#1A1A1A}.logo b{color:#C8A96A}
.main{display:flex;min-height:calc(100vh - 56px - 36px)}
.sidebar-l{width:220px;border-right:1px solid #E5E5E5;background:#FFF;padding:12px 0;flex-shrink:0;overflow-y:auto}
.sb-title{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#999;padding:8px 16px 6px}
.sb-item{display:flex;align-items:center;gap:10px;padding:9px 16px;font-size:13px;color:#555;cursor:pointer;transition:all .2s;border-radius:7px;margin:0 8px}
.sb-item:hover{background:#F0EDE8;color:#1A1A1A}
.sb-item.active{background:rgba(200,169,106,.12);color:#C8A96A;font-weight:600}
.content{flex:1;padding:20px 24px;overflow-y:auto}
.controls{background:#FFF;border:1px solid #E5E5E5;border-radius:12px;padding:16px 20px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.ctrl-row{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.ctrl-row:last-child{margin-bottom:0}
.ctrl-grp{display:flex;flex-direction:column;gap:4px}
.ctrl-label{font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#999}
.ctrl-in{padding:7px 10px;border:1px solid #E5E5E5;border-radius:8px;background:#fff;color:#1A1A1A;font-size:13px;outline:none;transition:all .2s}
.ctrl-in:focus{border-color:#C8A96A;box-shadow:0 0 0 3px rgba(200,169,106,.08)}
.search-box{position:relative;flex:1}
.search-box .iconify{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:#999;font-size:15px;pointer-events:none}
.search-box .ctrl-in{padding-left:36px;width:100%}
.search-hint{font-size:10px;color:#bbb;margin-top:3px}
.ctrl-spacer{flex:1}
.chips{display:flex;gap:5px}
.chip{padding:6px 12px;border-radius:6px;font-size:12px;font-weight:600;border:1px solid #E5E5E5;color:#555;cursor:pointer;background:none;transition:all .2s}
.chip:hover{border-color:#C8A96A;color:#1A1A1A}
.chip.active{background:#C8A96A;color:#fff;border-color:#C8A96A}
.btn-gen{padding:7px 18px;border-radius:8px;font-size:13px;font-weight:600;background:#C8A96A;color:#fff;cursor:pointer;display:flex;align-items:center;gap:6px;border:none;transition:all .2s;white-space:nowrap}
.btn-gen:hover{background:#b89858;transform:translateY(-1px);box-shadow:0 4px 12px rgba(200,169,106,.25)}
.btn-dl{padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;border:1px solid #E5E5E5;color:#555;cursor:pointer;display:flex;align-items:center;gap:6px;background:none;transition:all .2s;white-space:nowrap}
.btn-dl:hover{border-color:#C8A96A;color:#C8A96A}
.day-hdr{display:flex;align-items:center;gap:10px;margin:24px 0 12px;padding-bottom:8px;border-bottom:2px solid #E5E5E5}
.day-hdr:first-child{margin-top:0}
.day-hdr h2{font-family:Playfair Display,serif;font-size:18px;font-weight:700;color:#1A1A1A}
.day-hdr .cnt{margin-left:auto;font-size:12px;color:#999}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin-bottom:24px}
.card{background:#FFF;border:1px solid #E5E5E5;border-radius:10px;overflow:hidden;transition:all .3s;cursor:pointer}
.card:hover{transform:translateY(-3px);box-shadow:0 4px 16px rgba(0,0,0,.08);border-color:#C8A96A}
.card-img{width:100%;height:170px;position:relative;overflow:hidden;background:linear-gradient(135deg,#E8E4DD,#D5D0C8)}
.card-img img{width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0;z-index:1}
.card-img .fb{position:absolute;top:0;left:0;width:100%;height:100%;z-index:0}
.card-img .ft{position:absolute;bottom:0;left:0;right:0;padding:10px 14px;background:linear-gradient(transparent,rgba(0,0,0,.5));color:#fff;font-size:11px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;z-index:2}
.card-body{padding:14px 16px 16px}
.card-dom{font-size:10px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:#C8A96A;margin-bottom:5px}
.card-title{font-family:Playfair Display,serif;font-size:16px;font-weight:600;line-height:1.4;margin-bottom:6px;color:#1A1A1A;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card-desc{font-size:12.5px;color:#555;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:10px}
.card-meta{font-size:11px;color:#999;display:flex;justify-content:space-between;align-items:center}
.card-meta .rd{color:#3A7CA5;font-weight:600;font-size:12px}
.sidebar-r{width:260px;border-left:1px solid #E5E5E5;background:#FFF;padding:14px;flex-shrink:0;overflow-y:auto}
.rs-title{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#999;margin-bottom:10px;display:flex;align-items:center;gap:6px}
.live-dot{width:6px;height:6px;border-radius:50%;background:#E74C3C;animation:pulse 1.5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.log{max-height:calc(100vh - 120px);overflow-y:auto}
.log-entry{display:flex;gap:8px;padding:5px 0;font-size:11.5px;color:#555;border-bottom:1px solid #ECECEA}
.log-time{font-family:monospace;font-size:10px;color:#999;flex-shrink:0;min-width:40px}
.log-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;margin-top:5px}
.dot-ok{background:#27AE60}.dot-info{background:#3A7CA5}.dot-warn{background:#C8A96A}.dot-err{background:#E74C3C}
.loading{text-align:center;padding:40px;color:#C8A96A;font-size:14px}
.spinner{width:30px;height:30px;border:3px solid #E5E5E5;border-top-color:#C8A96A;border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 12px}
@keyframes spin{to{transform:rotate(360deg)}}
.tr-tag{display:inline-block;font-size:9px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:#fff;background:#C8A96A;padding:3px 8px;border-radius:4px;margin-bottom:6px}
.back-btn{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:#C8A96A;font-weight:600;cursor:pointer;margin-bottom:16px;padding:6px 12px;border-radius:6px;border:1px solid #E5E5E5;background:#fff;transition:all .2s}
.back-btn:hover{background:#F0EDE8;border-color:#C8A96A}
.welcome{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:50px 20px;text-align:center}
.welcome h2{font-family:Playfair Display,serif;font-size:24px;color:#1A1A1A;margin-bottom:8px}
.welcome p{color:#888;font-size:14px;max-width:420px;margin-bottom:24px}
.quick-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;width:100%;max-width:480px}
.quick-btn{padding:14px 8px;border-radius:8px;border:1px solid #E5E5E5;background:#fff;font-size:13px;font-weight:600;color:#555;cursor:pointer;transition:all .2s;text-align:center}
.quick-btn:hover{border-color:#C8A96A;color:#C8A96A;background:rgba(200,169,106,.05);transform:translateY(-1px)}
.quick-btn span{display:block;font-size:10px;color:#aaa;font-weight:400;margin-top:3px}
.retry-btn{margin-top:24px;padding:10px 24px;border-radius:8px;border:none;background:#C8A96A;color:#fff;font-size:13px;font-weight:600;cursor:pointer;transition:all .2s}
.retry-btn:hover{background:#b89858}
.trending-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.trending-hdr h2{font-family:Playfair Display,serif;font-size:22px;font-weight:700;color:#1A1A1A}
.trending-sub{font-size:13px;color:#888;margin-bottom:20px}
.qb{display:inline-block;background:rgba(200,169,106,.1);color:#C8A96A;font-size:11px;font-weight:600;padding:4px 10px;border-radius:5px;margin-bottom:16px;border:1px solid rgba(200,169,106,.2)}
</style>
</head>
<body>
<div class="ticker"><div class="ticker-label">TRENDING</div><div class="ticker-track" id="tk"></div></div>
<header class="header"><a href="#" class="logo">Trend<b>Scope</b></a></header>
<div class="main">
<aside class="sidebar-l"><div class="sb-title">Domains</div><div id="sb"></div></aside>
<main class="content" id="ct">
<div class="controls">
<div class="ctrl-row">
<div class="ctrl-grp"><label class="ctrl-label">Domain</label><select class="ctrl-in" id="dm"></select></div>
<div class="ctrl-grp"><label class="ctrl-label">Sub-Topic</label><select class="ctrl-in" id="st"><option value="">Select domain first</option></select></div>
<div class="ctrl-grp"><label class="ctrl-label">Range</label><div class="chips"><button class="chip" data-d="1" onclick="setD(1)">1D</button><button class="chip active" data-d="7" onclick="setD(7)">7D</button><button class="chip" data-d="30" onclick="setD(30)">30D</button></div></div>
<div class="ctrl-spacer"></div>
<button class="btn-gen" onclick="go()"><span class="iconify" data-icon="lucide:sparkles"></span> Generate</button>
<button class="btn-dl" onclick="dl()"><span class="iconify" data-icon="lucide:download"></span> PDF</button>
</div>
<div class="ctrl-row">
<div class="search-box"><span class="iconify" data-icon="lucide:search"></span><input class="ctrl-in" id="sr" placeholder="Search specifically... e.g. Ram Charan, GPT-5, Free Fire"></div>
</div>
<div class="search-hint" id="hint">Tip: Search text takes priority over sub-topic for accurate results</div>
</div>
<div id="nc"></div>
</main>
<aside class="sidebar-r"><div class="rs-title"><span class="live-dot"></span> Live Activity</div><div class="log" id="lg"></div></aside>
</div>
<script>
var DM=__DM__;var DI=__DI__;var curD=null;var days=7;
function esc(s){return(s||"").replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
function gi(a,d){var u=a.image_url||a.image||"";if(u&&u.length>10&&u.indexOf("http")===0)return{s:u,f:false};return{s:DI[d]||"https://images.unsplash.com/photo-1504711434969-e33886168d6c?w=600&h=340&fit=crop",f:true}}
function ih(a,d){var x=gi(a,d);var h='<div class="card-img">';if(x.f){h+='<img class="fb" src="'+esc(x.s)+'"><div class="ft">'+esc(d||"News")+'</div>'}else{h+='<img src="'+esc(x.s)+'" onerror="this.parentElement.innerHTML=\'<img class=fb src='+String.fromCharCode(39)+esc(DI[d]||"")+String.fromCharCode(39)+'><div class=ft>'+esc(d||"News")+'</div>\'">'}return h+'</div>'}
document.getElementById("nc").addEventListener("click",function(e){var c=e.target.closest(".card");if(c&&c.dataset.url){e.preventDefault();window.open(c.dataset.url,"_blank")}});
document.getElementById("sr").addEventListener("keydown",function(e){if(e.key==="Enter")go()});
function init(){var sb=document.getElementById("sb");var dm=document.getElementById("dm");var h="";var k=Object.keys(DM);for(var i=0;i<k.length;i++){var d=k[i];h+='<div class="sb-item" data-domain="'+esc(d)+'">'+esc(d)+'</div>';dm.innerHTML+='<option value="'+esc(d)+'">'+esc(d)+'</option>'}sb.innerHTML=h;sb.addEventListener("click",function(e){var it=e.target.closest(".sb-item");if(it)sel(it,it.dataset.domain)});dm.onchange=function(){var o=dm.options[dm.selectedIndex];sel({classList:{add:function(){}}},o.value);var its=sb.querySelectorAll(".sb-item");for(var i=0;i<its.length;i++){its[i].classList.remove("active");if(its[i].dataset.domain===o.value)its[i].classList.add("active")}};document.getElementById("st").onchange=function(){uh()};document.getElementById("sr").oninput=function(){uh()};var tk=document.getElementById("tk");var tt="AI Models - IPL 2025 - Crypto Surge - SpaceX Launch - Cyber Attacks - Tesla EV - Apple WWDC - Formula 1";var sp=tt.split(" - ").map(function(t){return"<span>"+t+"</span>"}).join("");tk.innerHTML=sp+sp;log("info","Loaded "+k.length+" domains");showW();loadT()}
function uh(){var s=document.getElementById("sr").value.trim();var st=document.getElementById("st").options[document.getElementById("st").selectedIndex].text;var h=document.getElementById("hint");if(s){h.textContent='Query: "'+s+'" (search takes priority)';h.style.color="#C8A96A"}else if(st&&st!=="Select domain first"){h.textContent='Query: "'+st+'" sub-topic';h.style.color="#999"}else{h.textContent="Tip: Search text takes priority over sub-topic for accurate results";h.style.color="#bbb"}}
function showW(){document.getElementById("nc").innerHTML='<div class="welcome"><h2>Welcome to TrendScope</h2><p>Select a domain, pick a sub-topic, then search to find exactly what you need.</p><div class="quick-grid"><div class="quick-btn" data-qd="Artificial Intelligence (AI)" data-qs="LLMs & GPT" data-sr="GPT-5">AI & LLMs<span>Latest models</span></div><div class="quick-btn" data-qd="Technology" data-qs="Software & Apps" data-sr="">Tech<span>Apps & Software</span></div><div class="quick-btn" data-qd="Sports" data-qs="Cricket" data-sr="IPL final">Cricket<span>IPL & matches</span></div><div class="quick-btn" data-qd="Crypto" data-qs="Bitcoin & Ethereum" data-sr="">Crypto<span>Bitcoin & ETH</span></div><div class="quick-btn" data-qd="Science" data-qs="Space (NASA/SpaceX)" data-sr="Starship">Space<span>NASA & SpaceX</span></div><div class="quick-btn" data-qd="Business" data-qs="Startups" data-sr="">Startups<span>Funding & news</span></div></div><button class="retry-btn" id="retryBtn">Load Trending News</button></div>';document.getElementById("retryBtn").addEventListener("click",loadT);document.getElementById("nc").addEventListener("click",function hn(e){var b=e.target.closest(".quick-btn");if(b){qGo(b.dataset.qd,b.dataset.qs,b.dataset.sr||"");document.getElementById("nc").removeEventListener("click",hn)}})}
function qGo(d,s,r){document.getElementById("dm").value=d;document.getElementById("sr").value=r;curD=d;var its=document.querySelectorAll(".sb-item");for(var i=0;i<its.length;i++){its[i].classList.remove("active");if(its[i].dataset.domain===d)its[i].classList.add("active")}pSub(d);document.getElementById("st").value=s;go()}
function pSub(d){var st=document.getElementById("st");var s=DM[d];st.innerHTML="";if(s){var k=Object.keys(s);for(var i=0;i<k.length;i++)st.innerHTML+='<option value="'+esc(s[k[i]])+'">'+esc(k[i])+'</option>'}}
function sel(el,d){curD=d;var its=document.querySelectorAll(".sb-item");for(var i=0;i<its.length;i++)its[i].classList.remove("active");if(el&&el.classList)el.classList.add("active");document.getElementById("dm").value=d;pSub(d);log("ok","Domain: "+d+" ("+Object.keys(DM[d]).length+" sub-topics)");uh()}
function bQ(){var sv=document.getElementById("st").value;var s=document.getElementById("sr").value.trim();if(s)return s;if(sv)return sv;return ""}
function loadT(){var nc=document.getElementById("nc");nc.innerHTML='<div class="loading"><div class="spinner"></div>Fetching trending news...</div>';log("info","Loading trending...");var ds=["Artificial Intelligence (AI)","Technology","Sports","Business","Finance","Crypto","Entertainment","Science","Cybersecurity"];var al=[];var dn=0;for(var i=0;i<ds.length;i++){(function(d,x){setTimeout(function(){fetch("/api/news?domain="+encodeURIComponent(d)+"&subtopic=&days=1").then(function(r){if(!r.ok)throw new Error("HTTP "+r.status);return r.json()}).then(function(data){if(Array.isArray(data)&&data.length>0){var it=data.slice(0,2);for(var j=0;j<it.length;j++)it[j]._domain=d;al=al.concat(it)}dn++;log("ok",d+": "+(Array.isArray(data)?data.length:0));if(dn===ds.length)fT(al)}).catch(function(){dn++;log("err",d+": failed");if(dn===ds.length)fT(al)})},x*400)})(ds[i],i)}}
function fT(al){if(al.length===0){log("warn","No trending news");showW();return}log("ok","Total: "+al.length+" trending");var h='<div class="trending-hdr"><h2>&#128293; Trending Now</h2><button class="back-btn" style="margin:0" id="refBtn">Refresh</button></div><p class="trending-sub">Top stories from all domains. Pick a domain to dive deeper.</p><div class="grid">';for(var i=0;i<al.length;i++){var a=al[i];var dc=(a.content||"").substring(0,120);if(dc.length>=120)dc+="...";h+='<div class="card" data-url="'+esc(a.url||"")+'">'+ih(a,a._domain)+'<div class="card-body"><div class="tr-tag">'+esc(a._domain||"")+'</div><div class="card-title">'+esc(a.title||"")+'</div><div class="card-desc">'+esc(dc)+'</div><div class="card-meta"><span>'+esc(a.author||"News")+'</span><span class="rd">Read &#8594;</span></div></div></div>'}h+='</div>';document.getElementById("nc").innerHTML=h;document.getElementById("refBtn").addEventListener("click",loadT)}
function setD(n){days=n;var ch=document.querySelectorAll(".chip");for(var i=0;i<ch.length;i++)ch[i].classList.toggle("active",parseInt(ch[i].dataset.d)===n);if(curD)go()}
function log(t,m){var lg=document.getElementById("lg");var n=new Date();var tm=n.getHours().toString().padStart(2,"0")+":"+n.getMinutes().toString().padStart(2,"0");var d=t==="ok"?"dot-ok":t==="err"?"dot-err":t==="warn"?"dot-warn":"dot-info";lg.innerHTML='<div class="log-entry"><span class="log-time">'+tm+'</span><span class="log-dot '+d+'"></span><span>'+m+'</span></div>'+lg.innerHTML}
function go(){if(!curD){log("err","Select a domain first");return}var q=bQ();if(!q){log("err","Pick a sub-topic or type a search");return}log("warn",'Searching: "'+q+'" in '+curD);document.getElementById("nc").innerHTML='<div class="loading"><div class="spinner"></div>Loading...</div>';fetch("/api/news?domain="+encodeURIComponent(curD)+"&subtopic="+encodeURIComponent(q)+"&days="+days).then(function(r){if(!r.ok)throw new Error("HTTP "+r.status);return r.json()}).then(function(data){ren(data,q);log("ok","Found "+data.length+' articles for "'+q+'"')}).catch(function(e){log("err","Failed: "+e.message);showW()})}
function ren(data,q){if(!data||data.length===0){document.getElementById("nc").innerHTML='<div class="back-btn" id="bb">Back to Trending</div><div class="qb">Searched: "'+esc(q)+'" in '+esc(curD)+'</div><div class="welcome"><h2>No articles found</h2><p>Try different keywords or a broader sub-topic.</p></div>';document.getElementById("bb").addEventListener("click",loadT);return}var gr={};for(var i=0;i<data.length;i++){var d=data[i].date_group;if(!gr[d])gr[d]=[];gr[d].push(data[i])}var h='<div class="back-btn" id="bb">Back to Trending</div><div class="qb">Searched: "'+esc(q)+'" in '+esc(curD)+'</div>';var dt=Object.keys(gr).sort().reverse();for(var i=0;i<dt.length;i++){var d=dt[i];var p=d.split("-");var l=new Date(p[0],p[1]-1,p[2]).toLocaleDateString("en-US",{weekday:"long",month:"long",day:"numeric"});h+='<div class="day-hdr"><h2>'+l+'</h2><span class="cnt">'+gr[d].length+' articles</span></div><div class="grid">';for(var j=0;j<gr[d].length;j++){var a=gr[d][j];var dc=(a.content||"").substring(0,150);if(dc.length>=150)dc+="...";h+='<div class="card" data-url="'+esc(a.url||"")+'">'+ih(a,curD)+'<div class="card-body"><div class="card-dom">'+esc(curD)+'</div><div class="card-title">'+esc(a.title||"")+'</div><div class="card-desc">'+esc(dc)+'</div><div class="card-meta"><span>'+esc(a.author||"News")+'</span><span class="rd">Read &#8594;</span></div></div></div>'}h+='</div>';document.getElementById("nc").innerHTML=h;document.getElementById("bb").addEventListener("click",loadT)}
function dl(){if(!curD){log("err","Select a domain first");return}var q=bQ();if(!q){log("err","Pick a sub-topic or type a search");return}log("warn",'Generating PDF for "'+q+'"...');fetch("/api/generate-pdf?domain="+encodeURIComponent(curD)+"&subtopic="+encodeURIComponent(q)+"&days="+days).then(function(r){return r.json()}).then(function(d){log("ok","PDF done! "+d.count+" articles");window.open("/api/latest-pdf","_blank")}).catch(function(){log("err","PDF error")})}
init();
</script>
</body></html>""".replace("__DM__", dm_json).replace("__DI__", di_json)
os.makedirs("templates", exist_ok=True)
with open("templates/index.html", "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
# ========== VERIFY ==========
with open("app.py", "rb") as f:
    bom = f.read(3)
has_bom = bom == b"\xef\xbb\xbf"
print("app.py: BOM " + ("FOUND (BAD)" if has_bom else "CLEAN (GOOD)"))
with open("templates/index.html", "r", encoding="utf-8") as f:
    content = f.read()
dm_count = content.count("sb-item")
has_dm = "var DM=" in content
size = len(content)
print("index.html: " + str(size) + " bytes")
print("var DM found: " + str(has_dm))
print("Domain items: " + str(dm_count))
if not has_bom and has_dm and dm_count >= 19 and size > 10000:
    print("\n=== ALL CHECKS PASSED - READY TO RUN ===")
else:
    print("\n=== SOMETHING WRONG ===")
    if has_bom: print("  - app.py has BOM!")
    if not has_dm: print("  - DM variable missing!")
    if dm_count < 19: print("  - Only " + str(dm_count) + " domains found!")
