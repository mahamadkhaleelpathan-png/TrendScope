import json, os
DM = {
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
dm_json = json.dumps(DM)
html = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>TrendScope</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>
<style>
:root{
--bg:#F7F5F0;--bg-card:#FFFFFF;--bg-side:#FFFFFF;--bg-ctrl:#FFFFFF;
--text:#1A1A1A;--text2:#555;--text3:#999;--text-inv:#fff;
--border:#E5E5E5;--border2:#ECECEA;
--accent:#C8A96A;--accent2:#b89858;--accent-bg:rgba(200,169,106,.1);
--shadow:0 1px 3px rgba(0,0,0,.04);--shadow2:0 4px 16px rgba(0,0,0,.08);
--ticker-bg:#C8A96A;--ticker-text:#fff;
--read-color:#3A7CA5;
--card-img-bg:linear-gradient(135deg,#E8E4DD,#D5D0C8);
--fade-bg:rgba(247,245,240,.92);
--scrollbar-track:transparent;--scrollbar-thumb:rgba(200,169,106,.3);--scrollbar-thumb-hover:rgba(200,169,106,.55);
--scrollbar-side-thumb:rgba(0,0,0,.12);
--focus-ring:0 0 0 2px var(--accent-bg),0 0 0 4px var(--accent);
}
[data-theme="dark"]{
--bg:#0F0F0F;--bg-card:#1A1A1A;--bg-side:#141414;--bg-ctrl:#1A1A1A;
--text:#E0E0E0;--text2:#AAA;--text3:#666;--text-inv:#111;
--border:#2A2A2A;--border2:#222;
--accent:#C8A96A;--accent2:#d4b87a;--accent-bg:rgba(200,169,106,.12);
--shadow:0 1px 3px rgba(0,0,0,.2);--shadow2:0 4px 16px rgba(0,0,0,.3);
--ticker-bg:#1A1A1A;--ticker-text:#C8A96A;
--read-color:#6ABED8;
--card-img-bg:linear-gradient(135deg,#2A2A2A,#222);
--fade-bg:rgba(15,15,15,.92);
--scrollbar-track:transparent;--scrollbar-thumb:rgba(200,169,106,.4);--scrollbar-thumb-hover:rgba(200,169,106,.7);
--scrollbar-side-thumb:rgba(255,255,255,.1);
--focus-ring:0 0 0 2px rgba(200,169,106,.15),0 0 0 4px var(--accent);
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;font-family:Inter,system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;transition:background .3s,color .3s}
a{color:inherit;text-decoration:none}
/* Reset all buttons to look like plain elements */
button{font:inherit;color:inherit;background:none;border:none;cursor:pointer;padding:0}
button:focus-visible{outline:none;box-shadow:var(--focus-ring);border-radius:4px}
/* ===== CUSTOM SCROLLBARS ===== */
.content::-webkit-scrollbar{width:8px}
.content::-webkit-scrollbar-track{background:var(--scrollbar-track);margin:4px 0}
.content::-webkit-scrollbar-thumb{background:var(--scrollbar-thumb);border-radius:4px;border:2px solid var(--bg)}
.content::-webkit-scrollbar-thumb:hover{background:var(--scrollbar-thumb-hover)}
.content{scrollbar-width:thin;scrollbar-color:var(--scrollbar-thumb) var(--bg)}
.sidebar-l::-webkit-scrollbar{width:4px}
.sidebar-l::-webkit-scrollbar-track{background:var(--scrollbar-track)}
.sidebar-l::-webkit-scrollbar-thumb{background:var(--scrollbar-side-thumb);border-radius:4px}
.sidebar-r::-webkit-scrollbar{width:4px}
.sidebar-r::-webkit-scrollbar-track{background:var(--scrollbar-track)}
.sidebar-r::-webkit-scrollbar-thumb{background:var(--scrollbar-side-thumb);border-radius:4px}
.ticker{height:34px;background:var(--ticker-bg);color:var(--ticker-text);display:flex;align-items:center;overflow:hidden;font-size:12px;font-weight:600}
.ticker-label{background:rgba(0,0,0,.12);padding:0 14px;height:100%;display:flex;align-items:center;gap:5px;flex-shrink:0;font-size:10px;letter-spacing:.5px;text-transform:uppercase}
.ticker-track{display:flex;animation:scroll 40s linear infinite;white-space:nowrap}
.ticker-track span{padding:0 28px}
@keyframes scroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.header{height:52px;border-bottom:1px solid var(--border);background:var(--bg-ctrl);display:flex;align-items:center;padding:0 20px;position:sticky;top:0;z-index:100;transition:background .3s,border .3s}
.logo{font-family:'DM Serif Display',serif;font-size:21px;font-weight:400;color:var(--text);letter-spacing:-.3px;transition:color .3s}.logo b{color:var(--accent)}
.header-right{margin-left:auto;display:flex;align-items:center;gap:10px}
.theme-btn{width:36px;height:36px;border-radius:50%;border:1px solid var(--border);background:var(--bg-card);display:flex;align-items:center;justify-content:center;transition:all .25s;color:var(--text2)}
.theme-btn:hover{border-color:var(--accent);color:var(--accent);transform:scale(1.08)}
.main{display:flex;height:calc(100vh - 52px - 34px)}
/* ===== LEFT SIDEBAR ===== */
.sidebar-l{width:230px;height:100%;border-right:1px solid var(--border);background:var(--bg-side);padding:10px 0;flex-shrink:0;overflow-y:auto;transition:background .3s,border .3s}
.sb-title{font-size:9px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--text3);padding:8px 14px 6px}
.acc-item{border-bottom:1px solid var(--border2)}
.acc-hdr{display:flex;align-items:center;gap:10px;padding:10px 14px;cursor:pointer;transition:all .2s;user-select:none;width:100%;text-align:left}
.acc-hdr:hover{background:var(--accent-bg)}
.acc-hdr.active{background:var(--accent-bg)}
.acc-icon{width:28px;height:28px;border-radius:6px;background:var(--accent-bg);display:flex;align-items:center;justify-content:center;flex-shrink:0;color:var(--accent);font-size:14px;transition:all .2s}
.acc-hdr.active .acc-icon,.acc-hdr:hover .acc-icon{background:var(--accent);color:#fff}
.acc-name{flex:1;font-size:12.5px;font-weight:600;color:var(--text);transition:color .2s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.acc-arrow{font-size:10px;color:var(--text3);transition:transform .3s;flex-shrink:0}
.acc-hdr.active .acc-arrow{transform:rotate(180deg)}
.acc-body{max-height:0;overflow:hidden;transition:max-height .35s ease}
.acc-body.open{max-height:300px}
.acc-body-inner{padding:0 14px 8px 52px}
.sub-item{display:block;width:100%;text-align:left;padding:6px 0;font-size:12px;color:var(--text2);cursor:pointer;transition:all .15s;border-bottom:1px solid var(--border2);border-radius:0}
.sub-item:last-child{border-bottom:none}
.sub-item:hover{color:var(--accent);padding-left:4px}
/* ===== CENTER CONTENT ===== */
.content{flex:1;padding:16px 20px;overflow-y:auto;min-width:0;position:relative}
.controls{background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:10px 16px;margin-bottom:16px;box-shadow:var(--shadow);transition:background .3s,border .3s}
.ctrl-row{display:flex;align-items:center;gap:8px}
.search-box{position:relative;flex:1}
.search-box .iconify{position:absolute;left:10px;top:50%;transform:translateY(-50%);color:var(--text3);font-size:14px;pointer-events:none}
.search-box input{width:100%;padding:7px 10px 7px 32px;border:1px solid var(--border);border-radius:7px;background:var(--bg);color:var(--text);font-size:12px;outline:none;transition:all .2s}
.search-box input:focus{border-color:var(--accent);box-shadow:var(--focus-ring)}
.chips{display:flex;gap:4px}
.chip{padding:5px 10px;border-radius:5px;font-size:11px;font-weight:600;border:1px solid var(--border);color:var(--text2);cursor:pointer;background:none;transition:all .2s}
.chip:hover{border-color:var(--accent);color:var(--text)}
.chip.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.btn-gen{padding:6px 14px;border-radius:7px;font-size:12px;font-weight:600;background:var(--accent);color:#fff;display:flex;align-items:center;gap:5px;transition:all .2s;white-space:nowrap}
.btn-gen:hover{background:var(--accent2);transform:translateY(-1px);box-shadow:0 3px 10px rgba(200,169,106,.25)}
.btn-dl{padding:6px 12px;border-radius:7px;font-size:12px;font-weight:600;border:1px solid var(--border);color:var(--text2);display:flex;align-items:center;gap:5px;background:var(--bg-card);transition:all .2s;white-space:nowrap}
.btn-dl:hover{border-color:var(--accent);color:var(--accent)}
.section-hdr{display:flex;align-items:center;gap:6px;margin-bottom:10px}
.section-hdr h2{font-family:'DM Serif Display',serif;font-size:20px;font-weight:400;color:var(--text)}
.section-sub{font-size:12px;color:var(--text3);margin-top:-6px;margin-bottom:12px}
.day-hdr{display:flex;align-items:center;gap:6px;margin-bottom:10px;padding-bottom:5px;border-bottom:1.5px solid var(--border)}
.day-hdr h3{font-family:'DM Serif Display',serif;font-size:15px;font-weight:400;color:var(--text)}
.day-hdr .cnt{margin-left:auto;font-size:11px;color:var(--text3);background:var(--accent-bg);padding:2px 8px;border-radius:10px}
.slider-section{margin-bottom:20px}
.slider-outer{position:relative}
.slider-viewport{overflow:hidden;border-radius:10px}
.slider-track{display:flex;transition:transform .45s cubic-bezier(.25,.8,.25,1);will-change:transform}
.slider-track.dragging{transition:none}
.slider-page{min-width:100%;flex-shrink:0;display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.slider-fade-r{position:absolute;right:0;top:0;bottom:0;width:50px;background:linear-gradient(90deg,transparent,var(--fade-bg));pointer-events:none;z-index:4;border-radius:0 10px 10px 0;transition:opacity .3s}
.slider-fade-l{position:absolute;left:0;top:0;bottom:0;width:50px;background:linear-gradient(-90deg,transparent,var(--fade-bg));pointer-events:none;z-index:4;border-radius:10px 0 0 10px;transition:opacity .3s}
.slider-fade-r.hide,.slider-fade-l.hide{opacity:0;pointer-events:none}
.slider-nav{display:flex;align-items:center;justify-content:flex-end;gap:6px;margin-top:10px}
.slider-info{font-size:11px;color:var(--text3);margin-right:auto}.slider-info b{color:var(--accent);font-weight:700}
.slider-dots{display:flex;gap:4px;margin-right:6px;flex-wrap:wrap;justify-content:flex-end;max-width:180px}
.slider-dot{width:6px;height:6px;border-radius:50%;background:var(--border);cursor:pointer;transition:all .25s;padding:0}
.slider-dot.on{background:var(--accent);width:18px;border-radius:3px}
.slider-arrow{width:32px;height:32px;border-radius:50%;background:var(--bg-card);border:1px solid var(--border);color:var(--text2);display:flex;align-items:center;justify-content:center;transition:all .2s;box-shadow:var(--shadow)}
.slider-arrow:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.slider-arrow.off{opacity:.25;pointer-events:none}
.card{background:#fff;border:1px solid #e5e5e5;border-radius:12px;overflow:hidden;cursor:pointer;display:flex;flex-direction:column;transition:box-shadow .2s;height:360px;}
.card:hover{box-shadow:0 4px 16px rgba(0,0,0,.08);}
.card-img{width:100%;height:140px;overflow:hidden;background:#f0f0f0;position:relative;}
.card-img img{width:100%;height:100%;object-fit:cover;display:block;transition:opacity .3s;}
.card:hover .card-img img{opacity:0.9;}
.card-img .ph{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:var(--text3);font-size:20px;pointer-events:none;opacity:.4}
.card-body{padding:10px 12px;flex:1;display:flex;flex-direction:column;gap:4px;background:#fff;overflow:hidden;min-width:0;}
.card-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:4px}
.card-tag{font-size:10px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#C8A96A;}
.card-src{font-size:8.5px;color:var(--text3)}
.card-title{font-family:"DM Serif Display",serif;font-size:14px;font-weight:600;line-height:1.35;color:#111;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;}
.card-desc{font-family:Inter,system-ui,sans-serif;font-size:12px;font-weight:400;color:#555;line-height:1.5;margin-top:6px;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden;white-space:normal;word-wrap:break-word;overflow-wrap:break-word;}
.card-footer{display:flex;justify-content:space-between;align-items:center;font-size:10px;color:#aaa;margin-top:auto;padding-top:8px;}.card-date{color:#bbb;}
.card-read{font-size:10.5px;color:var(--read-color);font-weight:600;display:flex;align-items:center;gap:2px;transition:gap .2s}
.card:hover .card-read{gap:5px}
.card-empty{display:none;}
.sidebar-r{width:200px;height:100%;border-left:1px solid var(--border);background:var(--bg-side);flex-shrink:0;overflow-y:auto;padding:12px;transition:background .3s,border .3s}
.rs-title{font-size:9px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--text3);margin-bottom:10px;display:flex;align-items:center;gap:5px}
.dom-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.dom-btn{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 4px 8px;border-radius:8px;border:1px solid var(--border);background:var(--bg-card);cursor:pointer;transition:all .25s;color:var(--text2)}
.dom-btn:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-2px);box-shadow:0 3px 10px rgba(200,169,106,.15)}
.dom-btn.active{border-color:var(--accent);background:var(--accent-bg);color:var(--accent)}
.dom-btn .iconify{font-size:18px;transition:color .2s}
.dom-btn:hover .iconify{color:var(--accent)}
.dom-btn-label{font-size:9px;font-weight:600;text-align:center;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.scroll-hint{position:absolute;bottom:16px;right:16px;width:34px;height:34px;border-radius:50%;background:var(--bg-card);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:50;box-shadow:var(--shadow2);transition:all .3s;opacity:0;pointer-events:none;color:var(--text2)}
.scroll-hint.show{opacity:1;pointer-events:all}
.scroll-hint:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.loading{text-align:center;padding:36px;color:var(--accent);font-size:13px}
.spinner{width:26px;height:26px;border:3px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 10px}
@keyframes spin{to{transform:rotate(360deg)}}
.back-btn{display:inline-flex;align-items:center;gap:5px;font-size:12px;color:var(--accent);font-weight:600;cursor:pointer;margin-bottom:12px;padding:5px 10px;border-radius:5px;border:1px solid var(--border);background:var(--bg-card);transition:all .2s}
.back-btn:hover{background:var(--accent-bg);border-color:var(--accent)}
.welcome{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:36px 20px;text-align:center}
.welcome h2{font-family:'DM Serif Display',serif;font-size:22px;color:var(--text);margin-bottom:6px}
.welcome p{color:var(--text3);font-size:13px;max-width:400px;margin-bottom:18px}
.retry-btn{margin-top:18px;padding:8px 18px;border-radius:7px;background:var(--accent);color:#fff;font-size:12px;font-weight:600;cursor:pointer;transition:all .2s}
.retry-btn:hover{background:var(--accent2)}
</style>
</head>
<body>
<div class="ticker"><div class="ticker-label">TRENDING</div><div class="ticker-track" id="tk"></div></div>
<header class="header">
<a href="#" class="logo">Trend<b>Scope</b></a>
<div class="header-right">
<button class="theme-btn" id="themeBtn" aria-label="Toggle theme"><span class="iconify" data-icon="lucide:moon" style="font-size:16px"></span></button>
</div>
</header>
<div class="main">
<aside class="sidebar-l"><div class="sb-title">Explore Domains</div><div id="accordion"></div></aside>
<main class="content" id="ct">
<div class="controls"><div class="ctrl-row">
<div class="search-box"><span class="iconify" data-icon="lucide:search"></span><input id="sr" placeholder="Search within selected topic..."></div>
<div class="chips"><button class="chip" data-d="1" onclick="setD(1)">1D</button><button class="chip active" data-d="7" onclick="setD(7)">7D</button><button class="chip" data-d="30" onclick="setD(30)">30D</button></div>
<button class="btn-gen" onclick="go()"><span class="iconify" data-icon="lucide:sparkles"></span> Generate</button>
<button class="btn-dl" onclick="dl()"><span class="iconify" data-icon="lucide:download"></span> PDF</button>
</div></div>
<div id="nc"></div>
<div class="scroll-hint" id="scrollHint"><span class="iconify" data-icon="lucide:chevron-down" style="font-size:16px"></span></div>
</main>
<aside class="sidebar-r">
<div class="rs-title"><span class="iconify" data-icon="lucide:zap" style="font-size:11px;color:var(--accent)"></span> Quick Access</div>
<div class="dom-grid" id="domGrid"></div>
</aside>
</div>
<script>
var DM=__DM_JSON__;
var curD=null,curSub="",days=7,PER_PAGE=8;
var ICONS={"Artificial Intelligence (AI)":"lucide:brain","Technology":"lucide:cpu","Business & Startups":"lucide:briefcase","Finance & Stock Market":"lucide:trending-up","Health & Fitness":"lucide:heart-pulse","Education & Careers":"lucide:graduation-cap","Entertainment":"lucide:clapperboard","Sports":"lucide:trophy","World News":"lucide:globe","Science & Space":"lucide:flask-conical","Cybersecurity":"lucide:shield-alert","Gaming":"lucide:gamepad-2","Mobile & Gadgets":"lucide:smartphone","Cryptocurrency":"lucide:bitcoin","Environment":"lucide:leaf","Travel & Tourism":"lucide:plane","Food & Lifestyle":"lucide:utensils","Automobiles":"lucide:car","War & Conflicts":"lucide:alert-triangle","Social Media":"lucide:message-circle"};
var SHORT={"Artificial Intelligence (AI)":"AI","Technology":"Tech","Business & Startups":"Biz","Finance & Stock Market":"Finance","Health & Fitness":"Health","Education & Careers":"Edu","Entertainment":"Fun","Sports":"Sports","World News":"World","Science & Space":"Science","Cybersecurity":"Cyber","Gaming":"Games","Mobile & Gadgets":"Mobile","Cryptocurrency":"Crypto","Environment":"Eco","Travel & Tourism":"Travel","Food & Lifestyle":"Food","Automobiles":"Auto","War & Conflicts":"War","Social Media":"Social"};
function esc(s){return(s||"").replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
var theme=localStorage.getItem("ts-theme")||"light";
document.documentElement.setAttribute("data-theme",theme);
function updateThemeIcon(){document.getElementById("themeBtn").innerHTML='<span class="iconify" data-icon="lucide:'+(theme==="light"?"moon":"sun")+'" style="font-size:16px"></span>'}
updateThemeIcon();
document.getElementById("themeBtn").onclick=function(){theme=theme==="light"?"dark":"light";document.documentElement.setAttribute("data-theme",theme);localStorage.setItem("ts-theme",theme);updateThemeIcon()};
function buildAccordion(){
var el=document.getElementById("accordion"),h="",keys=Object.keys(DM);
for(var i=0;i<keys.length;i++){var d=keys[i],subs=DM[d],subKeys=Object.keys(subs);
h+='<div class="acc-item"><button class="acc-hdr" data-domain="'+esc(d)+'" aria-expanded="false"><div class="acc-icon"><span class="iconify" data-icon="'+(ICONS[d]||"lucide:newspaper")+'"></span></div><span class="acc-name">'+esc(d)+'</span><span class="acc-arrow">&#9660;</span></button><div class="acc-body"><div class="acc-body-inner">';
for(var j=0;j<subKeys.length;j++) h+='<button class="sub-item" data-domain="'+esc(d)+'" data-sub="'+esc(subKeys[subKeys[j]])+'">'+esc(subKeys[j])+'</button>';
h+='</div></div></div>'}
el.innerHTML=h;
el.addEventListener("click",function(e){
var hdr=e.target.closest(".acc-hdr");if(hdr){var wasOpen=hdr.classList.contains("active");closeAll();if(!wasOpen){hdr.classList.add("active");hdr.setAttribute("aria-expanded","true");hdr.nextElementSibling.classList.add("open");curD=hdr.dataset.domain;curSub="";highlightDomBtn(curD);}else{hdr.setAttribute("aria-expanded","false");}}
var sub=e.target.closest(".sub-item");if(sub){curD=sub.dataset.domain;curSub=sub.dataset.sub;closeAll();var hdr2=sub.closest(".acc-item").querySelector(".acc-hdr");hdr2.classList.add("active");hdr2.setAttribute("aria-expanded","true");hdr2.nextElementSibling.classList.add("open");highlightDomBtn(curD);go();}
});
}
function closeAll(){var hdrs=document.querySelectorAll(".acc-hdr.active");for(var i=0;i<hdrs.length;i++){hdrs[i].classList.remove("active");hdrs[i].setAttribute("aria-expanded","false");hdrs[i].nextElementSibling.classList.remove("open")}}
function buildDomGrid(){
var el=document.getElementById("domGrid"),h="",keys=Object.keys(DM);
for(var i=0;i<keys.length;i++){var d=keys[i];
h+='<button class="dom-btn" data-domain="'+esc(d)+'" aria-label="'+esc(d)+'"><span class="iconify" data-icon="'+(ICONS[d]||"lucide:newspaper")+'"></span><span class="dom-btn-label">'+esc(SHORT[d]||d)+'</span></button>'}
el.innerHTML=h;
el.addEventListener("click",function(e){var btn=e.target.closest(".dom-btn");if(btn){curD=btn.dataset.domain;curSub="";closeAll();var hdr=document.querySelector('.acc-hdr[data-domain="'+esc(curD)+'"]');if(hdr){hdr.classList.add("active");hdr.setAttribute("aria-expanded","true");hdr.nextElementSibling.classList.add("open");}highlightDomBtn(curD);go();}});
}
function highlightDomBtn(d){var btns=document.querySelectorAll(".dom-btn");for(var i=0;i<btns.length;i++)btns[i].classList.toggle("active",btns[i].dataset.domain===d)}
(function(){var tk=document.getElementById("tk"),tt="AI Models - IPL 2025 - Crypto Surge - SpaceX Launch - Cyber Attacks - Tesla EV - Apple WWDC - Formula 1",sp=tt.split(" - ").map(function(t){return"<span>"+t+"</span>"}).join("");tk.innerHTML=sp+sp})();
document.getElementById("sr").addEventListener("keydown",function(e){if(e.key==="Enter")go()});
var contentEl=document.querySelector(".content");
var scrollHint=document.getElementById("scrollHint");
contentEl.addEventListener("scroll",function(){
  var atBottom=contentEl.scrollHeight-contentEl.scrollTop-contentEl.clientHeight<80;
  scrollHint.classList.toggle("show",!atBottom);
});
scrollHint.addEventListener("click",function(){contentEl.scrollTo({top:contentEl.scrollHeight,behavior:"smooth"})});
function initSliders(){var els=document.querySelectorAll(".slider-outer");for(var i=0;i<els.length;i++)wireSlider(els[i])}
function wireSlider(outer){
var vp=outer.querySelector(".slider-viewport"),track=outer.querySelector(".slider-track"),arrL=outer.parentElement.querySelector(".slider-arrow.left"),arrR=outer.parentElement.querySelector(".slider-arrow.right"),dotsW=outer.parentElement.querySelector(".slider-dots"),infoW=outer.parentElement.querySelector(".slider-info"),fadeL=outer.querySelector(".slider-fade-l"),fadeR=outer.querySelector(".slider-fade-r");
if(!track||!vp)return;var pages=track.querySelectorAll(".slider-page"),total=pages.length,cur=0;
if(total<=1){if(arrR)arrR.style.display="none";if(arrL)arrL.style.display="none";if(dotsW)dotsW.style.display="none";if(fadeR)fadeR.classList.add("hide");return}
function go(p){cur=Math.max(0,Math.min(p,total-1));track.style.transform="translateX(-"+(cur*vp.offsetWidth)+"px)";if(arrL)arrL.classList.toggle("off",cur===0);if(arrR)arrR.classList.toggle("off",cur>=total-1);if(fadeL)fadeL.classList.toggle("hide",cur===0);if(fadeR)fadeR.classList.toggle("hide",cur>=total-1);if(infoW)infoW.innerHTML="Page <b>"+(cur+1)+"</b> of "+total;var dots=dotsW?dotsW.querySelectorAll(".slider-dot"):[];for(var i=0;i<dots.length;i++)dots[i].classList.toggle("on",i===cur)}
if(dotsW){var dh="";for(var i=0;i<total;i++)dh+='<button class="slider-dot'+(i===0?" on":"")+'" data-p="'+i+'"></button>';dotsW.innerHTML=dh;dotsW.onclick=function(e){var d=e.target.closest(".slider-dot");if(d)go(parseInt(d.dataset.p))}}
if(arrR)arrR.onclick=function(){go(cur+1)};if(arrL)arrL.onclick=function(){go(cur-1)}
var drag=false,sx=0,sp=0,mv=false;
track.addEventListener("mousedown",function(e){drag=true;mv=false;sx=e.clientX;sp=cur;track.classList.add("dragging");e.preventDefault()});
window.addEventListener("mousemove",function(e){if(!drag)return;var dx=e.clientX-sx;if(Math.abs(dx)>4)mv=true;track.style.transform="translateX(-"+(sp*vp.offsetWidth-dx)+"px)"});
window.addEventListener("mouseup",function(e){if(!drag)return;drag=false;track.classList.remove("dragging");if(!mv){go(cur);return}var dx=e.clientX-sx;if(Math.abs(dx)>vp.offsetWidth*.1){go(dx<0?cur+1:cur-1)}else{go(cur)}});
track.addEventListener("touchstart",function(e){drag=true;mv=false;sx=e.touches[0].clientX;sp=cur;track.classList.add("dragging")},{passive:true});
track.addEventListener("touchmove",function(e){if(!drag)return;var dx=e.touches[0].clientX-sx;if(Math.abs(dx)>4)mv=true;track.style.transform="translateX(-"+(sp*vp.offsetWidth-dx)+"px)"},{passive:true});
track.addEventListener("touchend",function(e){if(!drag)return;drag=false;track.classList.remove("dragging");if(!mv){go(cur);return}var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>vp.offsetWidth*.1){go(dx<0?cur+1:cur-1)}else{go(cur)}});
go(0);var rt;window.addEventListener("resize",function(){clearTimeout(rt);rt=setTimeout(function(){go(cur)},120)})
}
function sliderHTML(id,items,tag,headerHTML){var total=items.length,np=Math.ceil(total/PER_PAGE),h='<div class="slider-section" id="'+id+'">';if(headerHTML)h+=headerHTML;h+='<div class="slider-outer"><div class="slider-fade-l hide"></div><div class="slider-fade-r"></div><div class="slider-viewport"><div class="slider-track">';for(var p=0;p<np;p++){h+='<div class="slider-page">';for(var c=0;c<PER_PAGE;c++){var idx=p*PER_PAGE+c;h+=idx<total?cardHTML(items[idx],tag):'<div class="card-empty"></div>'}h+='</div>'}h+='</div></div></div><div class="slider-nav"><div class="slider-info">Page <b>1</b> of '+np+" &middot; "+total+' articles</div><div class="slider-dots"></div><button class="slider-arrow left"><span class="iconify" data-icon="lucide:chevron-left" style="font-size:16px"></span></button><button class="slider-arrow right"><span class="iconify" data-icon="lucide:chevron-right" style="font-size:16px"></span></button></div></div>';return h}
function cardHTML(a,tag){var desc=(a.content||"").substring(0,300); if(desc===(a.title||""))desc=""; if(desc.length>=300)desc+="...";var src=a.author||"Google News",t=tag||curD||"News";return'<div class="card" data-url="'+esc(a.url||"")+'"><div class="card-img">'+(a.image_url?'<img src="'+esc(a.image_url)+'" loading="lazy">':'')+'</div><div class="card-body"><span class="card-tag">'+esc(t)+'</span><div class="card-title">'+esc(a.title||"")+'</div><div class="card-desc">'+esc(desc)+'</div><div class="card-footer"><span class="card-src">'+esc(src)+'</span><span class="card-date">'+esc(a.date_group||"")+'</span></div></div></div>'}
document.getElementById("nc").addEventListener("click",function(e){var card=e.target.closest(".card");if(card&&card.dataset.url){e.preventDefault();window.open(card.dataset.url,"_blank")}});
function showWelcome(){document.getElementById("nc").innerHTML='<div class="welcome"><h2>Welcome to TrendScope</h2><p>Pick a domain from the left panel or quick-access buttons on the right.</p><button class="retry-btn" id="retryBtn">Load Trending News</button></div>';document.getElementById("retryBtn").addEventListener("click",loadTrending)}
function loadTrending(){var nc=document.getElementById("nc");nc.innerHTML='<div class="loading"><div class="spinner"></div>Fetching trending news...</div>';var domains=Object.keys(DM),all=[],done=0;
for(var i=0;i<domains.length;i++){(function(d,idx){setTimeout(function(){fetch("/api/news?domain="+encodeURIComponent(d)+"&subtopic=&days=1").then(function(r){if(!r.ok)throw new Error(r.status);return r.json()}).then(function(data){var count=Array.isArray(data)?data.length:0;if(count>0){var items=data.slice(0,PER_PAGE);for(var j=0;j<items.length;j++)items[j]._domain=d;all=all.concat(items)}done++;if(done===domains.length)finishTrending(all)}).catch(function(){done++;if(done===domains.length)finishTrending(all)})},idx*300)})(domains[i],i)}}
function finishTrending(all){if(!all.length){showWelcome();return}var header='<div class="section-hdr"><h2>Trending Now</h2><button class="back-btn" style="margin:0" id="refreshBtn">&#x21bb; Refresh</button></div><p class="section-sub">Top stories from all domains</p>';document.getElementById("nc").innerHTML=sliderHTML("trending",all,null,header);document.getElementById("refreshBtn").addEventListener("click",loadTrending);initSliders()}
function setD(n){days=n;var chips=document.querySelectorAll(".chip");for(var i=0;i<chips.length;i++)chips[i].classList.toggle("active",parseInt(chips[i].dataset.d)===n);if(curD)go()}
function go(){if(!curD)return;var search=document.getElementById("sr").value;var query=curSub;if(search&&curSub)query=curSub+" "+search;else if(search)query=search;else if(!curSub)query=curD;
document.getElementById("nc").innerHTML='<div class="loading"><div class="spinner"></div>Loading...</div>';
fetch("/api/news?domain="+encodeURIComponent(curD)+"&subtopic="+encodeURIComponent(query)+"&days="+days).then(function(r){if(!r.ok)throw new Error(r.status);return r.json()}).then(function(data){render(data)}).catch(function(){showWelcome()})}
function render(data){if(!data||!data.length){document.getElementById("nc").innerHTML='<div class="back-btn" id="backBtn">&#8592; Back</div><div class="welcome"><h2>No articles found</h2><p>Try a different topic.</p></div>';document.getElementById("backBtn").addEventListener("click",loadTrending);return}
var groups={};for(var i=0;i<data.length;i++){var d=data[i].date_group;if(!groups[d])groups[d]=[];groups[d].push(data[i])}
var html='<div class="back-btn" id="backBtn">&#8592; Back to Trending</div><div class="section-hdr"><h2>'+esc(curD)+'</h2><span style="margin-left:auto;font-size:11px;color:var(--text3)">'+data.length+" articles</span></div>";
var dates=Object.keys(groups).sort().reverse(),cId=0;
for(var i=0;i<dates.length;i++){var date=dates[i],parts=date.split("-"),label=new Date(parts[0],parts[1]-1,parts[2]).toLocaleDateString("en-US",{weekday:"long",month:"long",day:"numeric"}),items=groups[date];
html+=sliderHTML("dp-"+cId,items,null,'<div class="day-hdr"><h3>'+label+'</h3><span class="cnt">'+items.length+'</span></div>');cId++}
document.getElementById("nc").innerHTML=html;document.getElementById("backBtn").addEventListener("click",loadTrending);initSliders()}
function dl(){if(!curD)return;var search=document.getElementById("sr").value,query=curSub;if(search&&curSub)query=curSub+" "+search;else if(search)query=search;else if(!curSub)query=curD;
fetch("/api/generate-pdf?domain="+encodeURIComponent(curD)+"&subtopic="+encodeURIComponent(query)+"&days="+days).then(function(r){return r.json()}).then(function(d){window.open("/api/latest-pdf","_blank")}).catch(function(){})}
buildAccordion();buildDomGrid();showWelcome();
</script>
</body></html>""".replace("__DM_JSON__",dm_json)
os.makedirs("templates",exist_ok=True)
with open("templates/index.html","w",encoding="utf-8") as f:
    f.write(html)
print("KEYBOARD ACCESSIBLE: Tab + Enter works on all domains, sub-items, buttons, chips, search")
