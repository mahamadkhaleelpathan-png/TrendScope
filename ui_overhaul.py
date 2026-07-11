import json, os
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
.header{height:56px;border-bottom:1px solid #E5E5E5;background:#FFFFFF;display:flex;align-items:center;padding:0 24px;position:sticky;top:0;z-index:100}
.logo{font-family:Playfair Display,serif;font-size:22px;font-weight:700;letter-spacing:-.5px;color:#1A1A1A}.logo b{color:#C8A96A}
.main{display:flex;min-height:calc(100vh - 56px - 36px)}
.sidebar-l{width:220px;border-right:1px solid #E5E5E5;background:#FFFFFF;padding:12px 0;flex-shrink:0;overflow-y:auto}
.sb-title{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#999;padding:8px 16px 6px}
.sb-item{display:flex;align-items:center;gap:10px;padding:9px 16px;font-size:13px;color:#555;cursor:pointer;transition:all .2s;border-radius:7px;margin:0 8px}
.sb-item:hover{background:#F0EDE8;color:#1A1A1A}
.sb-item.active{background:rgba(200,169,106,.1);color:#C8A96A;font-weight:600}
.content{flex:1;padding:20px 24px;overflow-y:auto}
.controls{background:#FFFFFF;border:1px solid #E5E5E5;border-radius:10px;padding:16px 20px;margin-bottom:20px;display:flex;align-items:flex-end;gap:12px;flex-wrap:wrap;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.ctrl-grp{display:flex;flex-direction:column;gap:5px}
.ctrl-grp.grow{flex:1;min-width:200px}
.ctrl-label{font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#999}
.ctrl-in{padding:8px 12px;border:1px solid #E5E5E5;border-radius:8px;background:#fff;color:#1A1A1A;font-size:13px;outline:none;transition:all .2s}
.ctrl-in:focus{border-color:#C8A96A;box-shadow:0 0 0 3px rgba(200,169,106,.08)}
.chips{display:flex;gap:6px}
.chip{padding:6px 14px;border-radius:6px;font-size:12px;font-weight:600;border:1px solid #E5E5E5;color:#555;cursor:pointer;background:none;transition:all .2s}
.chip:hover{border-color:#C8A96A;color:#1A1A1A}
.chip.active{background:#C8A96A;color:#fff;border-color:#C8A96A}
.btn-gen{padding:9px 20px;border-radius:8px;font-size:13px;font-weight:600;background:#C8A96A;color:#fff;cursor:pointer;display:flex;align-items:center;gap:6px;border:none;transition:all .2s}
.btn-gen:hover{background:#b89858;transform:translateY(-1px);box-shadow:0 4px 12px rgba(200,169,106,.25)}
.btn-dl{padding:9px 16px;border-radius:8px;font-size:13px;font-weight:600;border:1px solid #E5E5E5;color:#555;cursor:pointer;display:flex;align-items:center;gap:6px;background:none;transition:all .2s}
.btn-dl:hover{border-color:#C8A96A;color:#C8A96A}
.day-hdr{display:flex;align-items:center;gap:10px;margin:24px 0 12px;padding-bottom:8px;border-bottom:2px solid #E5E5E5}
.day-hdr:first-child{margin-top:0}
.day-hdr h2{font-family:Playfair Display,serif;font-size:18px;font-weight:700;color:#1A1A1A}
.day-hdr .cnt{margin-left:auto;font-size:12px;color:#999}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin-bottom:24px}
.card{background:#FFFFFF;border:1px solid #E5E5E5;border-radius:10px;overflow:hidden;transition:all .3s;cursor:pointer}
.card:hover{transform:translateY(-3px);box-shadow:0 4px 16px rgba(0,0,0,.08);border-color:#C8A96A}
.card img{width:100%;height:170px;object-fit:cover;background:#F0EDE8;display:block}
.card-body{padding:14px 16px 16px}
.card-dom{font-size:10px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:#C8A96A;margin-bottom:5px}
.card-title{font-family:Playfair Display,serif;font-size:16px;font-weight:600;line-height:1.4;margin-bottom:6px;color:#1A1A1A;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card-desc{font-size:12.5px;color:#555;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:10px}
.card-meta{font-size:11px;color:#999;display:flex;justify-content:space-between;align-items:center}
.card-meta a{color:#3A7CA5;font-weight:600}
.card-meta a:hover{text-decoration:underline}
.sidebar-r{width:260px;border-left:1px solid #E5E5E5;background:#FFFFFF;padding:14px;flex-shrink:0;overflow-y:auto}
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
.trending-hdr{display:flex;align-items:center;gap:10px;margin-bottom:16px}
.trending-hdr h2{font-family:Playfair Display,serif;font-size:22px;font-weight:700;color:#1A1A1A}
.trending-hdr .fire{font-size:24px}
.trending-sub{font-size:13px;color:#888;margin-bottom:20px}
.back-btn{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:#C8A96A;font-weight:600;cursor:pointer;margin-bottom:16px;padding:6px 12px;border-radius:6px;border:1px solid #E5E5E5;background:#fff;transition:all .2s}
.back-btn:hover{background:#F0EDE8;border-color:#C8A96A}
.no-img{width:100%;height:170px;background:linear-gradient(135deg,#E8E4DD,#D5D0C8);display:flex;align-items:center;justify-content:center;color:#999;font-size:12px}
.tr-tag{display:inline-block;font-size:9px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:#fff;background:#C8A96A;padding:3px 8px;border-radius:4px;margin-bottom:6px}
</style>
</head>
<body>
<div class="ticker"><div class="ticker-label">TRENDING</div><div class="ticker-track" id="tk"></div></div>
<header class="header"><a href="#" class="logo">Trend<b>Scope</b></a></header>
<div class="main">
<aside class="sidebar-l"><div class="sb-title">Domains</div><div id="sb"></div></aside>
<main class="content" id="ct">
<div class="controls">
<div class="ctrl-grp"><label class="ctrl-label">Domain</label><select class="ctrl-in" id="dm"></select></div>
<div class="ctrl-grp grow"><label class="ctrl-label">Sub-Topic</label><input class="ctrl-in" id="st" placeholder="Search anything... e.g. LLMs, IPL, Bitcoin, SpaceX"></div>
<div class="ctrl-grp"><label class="ctrl-label">Range</label><div class="chips"><button class="chip" data-d="1" onclick="setD(1)">1D</button><button class="chip active" data-d="7" onclick="setD(7)">7D</button><button class="chip" data-d="30" onclick="setD(30)">30D</button></div></div>
<button class="btn-gen" onclick="go()"><span class="iconify" data-icon="lucide:sparkles"></span> Generate</button>
<button class="btn-dl" onclick="dl()"><span class="iconify" data-icon="lucide:download"></span> PDF</button>
</div>
<div id="nc"></div>
</main>
<aside class="sidebar-r"><div class="rs-title"><span class="live-dot"></span> Live Activity</div><div class="log" id="lg"></div></aside>
</div>
<script>
var DM = """ + json.dumps(DM) + """;
var curD = null;
var days = 7;
function init() {
    var sb = document.getElementById("sb");
    var dm = document.getElementById("dm");
    var h = "";
    for(var d in DM) {
        h += '<div class="sb-item" onclick="sel(this, this.textContent)">' + d + '</div>';
        dm.innerHTML += '<option value="' + d + '">' + d + '</option>';
    }
    sb.innerHTML = h;
    dm.onchange = function() {
        var opt = dm.options[dm.selectedIndex];
        sel(opt, opt.value);
    };
    var tk = document.getElementById("tk");
    var tt = "AI Models - IPL 2025 - Crypto Surge - SpaceX Launch - Cyber Attacks - Tesla EV - Apple WWDC - Formula 1";
    tk.innerHTML = tt.split(" - ").map(function(t){return '<span>' + t + '</span>';}).join('') + tt.split(" - ").map(function(t){return '<span>' + t + '</span>';}).join('');
    log("info", "System ready");
    loadTrending();
}
function loadTrending() {
    var nc = document.getElementById("nc");
    nc.innerHTML = '<div class="loading"><div class="spinner"></div>Loading trending news...</div>';
    log("info", "Fetching trending news...");
    var domains = ["Artificial Intelligence (AI)", "Technology", "Sports", "Business", "Finance", "Crypto", "Entertainment", "Science", "Cybersecurity"];
    var promises = domains.map(function(d) {
        return fetch("/api/news?domain=" + encodeURIComponent(d) + "&subtopic=&days=1")
            .then(function(r) { return r.json(); })
            .then(function(data) {
                return data.slice(0, 2).map(function(a) { a._domain = d; return a; });
            })
            .catch(function() { return []; });
    });
    Promise.all(promises).then(function(results) {
        var all = [].concat.apply([], results);
        log("ok", "Loaded " + all.length + " trending articles");
        renderTrending(all);
    });
}
function renderTrending(data) {
    if(!data.length) {
        document.getElementById("nc").innerHTML = '<div style="text-align:center;padding:60px 20px;color:#999"><div style="font-size:48px;margin-bottom:12px;opacity:.4"><span class="iconify" data-icon="lucide:search-x"></span></div><h3 style="color:#555;margin-bottom:6px">No trending news found</h3><p style="font-size:13px">Try again later or select a domain.</p></div>';
        return;
    }
    var html = '<div class="trending-hdr"><span class="fire">&#128293;</span><h2>Trending Now</h2></div>';
    html += '<p class="trending-sub">Real-time top stories from across all domains. Click a domain on the left to dive deeper.</p>';
    html += '<div class="grid">';
    data.forEach(function(a) {
        var img = a.image_url || "";
        var desc = (a.content || "").substring(0, 120);
        if(desc.length >= 120) desc += "...";
        var src = a.author || "News";
        html += '<div class="card" onclick="window.open(\'' + (a.url || "#") + '\', \'_blank\')">';
        if(img) {
            html += '<img src="' + img + '" style="object-fit:cover" onerror="this.outerHTML=\'<div class=no-img><span class=iconify data-icon=lucide:image-off style=font-size:28px></span></div>\'">';
        } else {
            html += '<div class="no-img"><span class="iconify" data-icon="lucide:image-off" style="font-size:28px"></span></div>';
        }
        html += '<div class="card-body">';
        html += '<div class="tr-tag">' + (a._domain || "") + '</div>';
        html += '<div class="card-title">' + (a.title || "") + '</div>';
        html += '<div class="card-desc">' + desc + '</div>';
        html += '<div class="card-meta"><span>' + src + '</span><a href="' + (a.url || "#") + '" target="_blank" onclick="event.stopPropagation()">Read &#8594;</a></div>';
        html += '</div></div>';
    });
    html += '</div>';
    document.getElementById("nc").innerHTML = html;
}
function sel(el, d) {
    curD = d;
    document.querySelectorAll(".sb-item").forEach(function(e){e.classList.remove("active")});
    el.classList.add("active");
    document.getElementById("dm").value = d;
    log("ok", "Domain: " + d);
}
function setD(n){days=n;document.querySelectorAll(".chip").forEach(function(c){c.classList.toggle("active",parseInt(c.dataset.d)===n);});if(curD)go();}
function log(type,msg){var lg=document.getElementById("lg");var now=new Date();var t=now.getHours().toString().padStart(2,"0")+":"+now.getMinutes().toString().padStart(2,"0");var dot=type==="ok"?"dot-ok":type==="err"?"dot-err":type==="warn"?"dot-warn":"dot-info";lg.innerHTML='<div class="log-entry"><span class="log-time">'+t+'</span><span class="log-dot '+dot+'"></span><span>'+msg+'</span></div>'+lg.innerHTML;}
function go(){if(!curD){log("err","Select a domain first");return;}var sub=document.getElementById("st").value;log("warn","Fetching "+curD+(sub?" ("+sub+")":"")+"...");document.getElementById("nc").innerHTML='<div class="loading"><div class="spinner"></div>Loading...</div>';fetch("/api/news?domain="+encodeURIComponent(curD)+"&subtopic="+encodeURIComponent(sub)+"&days="+days).then(function(r){return r.json();}).then(function(data){render(data);log("ok","Found "+data.length+" articles");}).catch(function(e){log("err","Fetch failed");document.getElementById("nc").innerHTML='<div style="text-align:center;padding:60px 20px;color:#999"><h3 style="color:#555">Error</h3><p>Failed to fetch news. Check your API.</p></div>';});}
function render(data){
    if(!data.length){
        document.getElementById("nc").innerHTML='<div class="back-btn" onclick="loadTrending()"><span class="iconify" data-icon="lucide:arrow-left"></span> Back to Trending</div><div style="text-align:center;padding:60px 20px;color:#999"><div style="font-size:48px;margin-bottom:12px;opacity:.4"><span class="iconify" data-icon="lucide:search-x"></span></div><h3 style="color:#555">No articles found</h3><p style="font-size:13px">Try a different sub-topic or increase the date range.</p></div>';
        return;
    }
    var groups={};
    data.forEach(function(a){var d=a.date_group;if(!groups[d])groups[d]=[];groups[d].push(a);});
    var html='<div class="back-btn" onclick="loadTrending()"><span class="iconify" data-icon="lucide:arrow-left"></span> Back to Trending</div>';
    var dates=Object.keys(groups).sort().reverse();
    dates.forEach(function(date){var parts=date.split("-");var label=new Date(parts[0],parts[1]-1,parts[2]).toLocaleDateString("en-US",{weekday:"long",month:"long",day:"numeric"});html+='<div class="day-hdr"><h2>'+label+'</h2><span class="cnt">'+groups[date].length+' articles</span></div><div class="grid">';groups[date].forEach(function(a){var img=a.image_url||"";var desc=(a.content||"").substring(0,150);if(desc.length>=150)desc+="...";var src=a.author||"News";html+='<div class="card" onclick="window.open(\''+(a.url||"#")+'\', \'_blank\')">';if(img){html+='<img src="'+img+'" style="object-fit:cover" onerror="this.outerHTML=\'<div class=no-img><span class=iconify data-icon=lucide:image-off style=font-size:28px></span></div>\'">';}else{html+='<div class="no-img"><span class="iconify" data-icon="lucide:image-off" style="font-size:28px"></span></div>';}html+='<div class="card-body"><div class="card-dom">'+curD+'</div><div class="card-title">'+(a.title||"")+'</div><div class="card-desc">'+desc+'</div><div class="card-meta"><span>'+src+'</span><a href="'+(a.url||"#")+'" target="_blank" onclick="event.stopPropagation()">Read &#8594;</a></div></div></div>';});html+='</div>';});
    document.getElementById("nc").innerHTML=html;
}
function dl(){if(!curD){log("err","Select a domain first");return;}var sub=document.getElementById("st").value;log("warn","Generating PDF...");fetch("/api/generate-pdf?domain="+encodeURIComponent(curD)+"&subtopic="+encodeURIComponent(sub)+"&days="+days).then(function(r){return r.json();}).then(function(d){log("ok","PDF done! "+d.count+" articles");window.open("/api/latest-pdf","_blank");}).catch(function(e){log("err","PDF error");});}
init();
</script>
</body></html>"""
os.makedirs("templates", exist_ok=True)
with open("templates/index.html", "w", encoding="utf-8") as file:
    file.write(html)
print("UI OVERHAUL COMPLETE!")
print("- Sub-topic is now a free search input")
print("- Trending news with images loads on startup")
print("- Back to Trending button when viewing specific results")
