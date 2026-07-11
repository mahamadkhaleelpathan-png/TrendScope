import json
data = json.load(open("_data.json", encoding="utf-8"))
DM = data["dm"]
DI = data["di"]
def esc(s):
    s = s or ""
    s = s.replace("&", "&amp;")
    s = s.replace('"', "&quot;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    return s
def get_img(article, domain):
    u = article.get("image_url", "") or article.get("image", "")
    if u and len(u) > 10 and u.startswith("http"):
        return u, False
    fallback = DI.get(domain, "https://images.unsplash.com/photo-1504711434969-e33886168d6c?w=800&h=400&fit=crop")
    return fallback, True
def slide_html(article, domain):
    img, is_fb = get_img(article, domain)
    desc = (article.get("content", "") or "")[:140]
    if len(desc) >= 140:
        desc += "..."
    author = article.get("author", "News")
    url = article.get("url", "#")
    h = '<div class="cs">'
    if is_fb:
        h += '<div class="cs-img" style="background:url(' + esc(img) + ') center/cover">'
        h += '<div class="cs-fb">' + esc(domain) + '</div></div>'
    else:
        h += '<div class="cs-img"><img src="' + esc(img) + '"></div>'
    h += '<div class="cs-body">'
    h += '<div class="cs-tag">' + esc(domain) + '</div>'
    h += '<h3 class="cs-title">' + esc(article.get("title", "")) + '</h3>'
    h += '<p class="cs-desc">' + esc(desc) + '</p>'
    h += '<div class="cs-meta"><span>' + esc(author) + '</span>'
    h += '<a href="' + esc(url) + '" target="_blank">Read &#8594;</a></div>'
    h += '</div></div>'
    return h
css = """
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,system-ui,sans-serif;background:#F8F6F2;color:#1A1A1A;line-height:1.6}
a{color:inherit;text-decoration:none}
::-webkit-scrollbar{width:6px}::-webkit-scrollbar-thumb{background:#ccc;border-radius:6px}
.ticker{height:36px;background:#C8A96A;color:#fff;display:flex;align-items:center;overflow:hidden;font-size:13px;font-weight:600}
.ticker-label{background:rgba(0,0,0,.15);padding:0 16px;height:100%;display:flex;align-items:center;gap:6px;flex-shrink:0;font-size:11px;letter-spacing:.5px;text-transform:uppercase}
.ticker-track{display:flex;animation:scroll 40s linear infinite;white-space:nowrap}
.ticker-track span{padding:0 32px}
@keyframes scroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.header{height:56px;border-bottom:1px solid #E5E5E5E5;background:#FFF;display:flex;align-items:center;padding:0 24px;position:sticky;top:0;z-index:100}
.logo{font-family:Playfair Display,serif;font-size:22px;font-weight:700;letter-spacing:-.5px;color:#1A1A1A}.logo b{color:#C8A96A}
.main{display:flex;min-height:calc(100vh - 56px - 36px)}
.sidebar-l{width:220px;border-right:1px solid #E5E5E5E5;background:#FFF;padding:12px 0;flex-shrink:0;overflow-y:auto}
.sb-title{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#999;padding:8px 16px 6px}
.sb-item{display:flex;align-items:center;gap:10px;padding:9px 16px;font-size:13px;color:#555;cursor:pointer;transition:all .2s;border-radius:7px;margin:0 8px}
.sb-item:hover{background:#F0EDE8;color:#1A1A1A}
.sb-item.active{background:rgba(200,169,106,.12);color:#C8A96A;font-weight:600}
.content{flex:1;padding:20px 24px;overflow-y:auto}
.controls{background:#FFF;border:1px solid #E5E5E5E;border-radius:12px;padding:16px 20px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.ctrl-row{display:flex;align-items:center;gap:10px;margin-bottom:12px}
.ctrl-row:last-child{margin-bottom:0}
.ctrl-grp{display:flex;flex-direction:column;gap:4px}
.ctrl-label{font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#999}
.ctrl-in{padding:7px 10px;border:1px solid #E5E5E5E;border-radius:8px;background:#fff;color:#1A1A1A;font-size:13px;outline:none;transition:all .2s}
.ctrl-in:focus{border-color:#C8A96A;box-shadow:0 0 0 3px rgba(200,169,106,.08)}
.search-box{position:relative;flex:1}
.search-box .iconify{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:#999;font-size:15px;pointer-events:none}
.search-box .ctrl-in{padding-left:36px;width:100%}
.ctrl-spacer{flex:1}
.chips{display:flex;gap:5px}
.chip{padding:6px 12px;border-radius:6px;font-size:12px;font-weight:600;border:1px solid #E5E5E5E5;color:#555;cursor:pointer;background:none;transition:all .2s}
.chip:hover{border-color:#C8A96A;color:#1A1A1A}
.chip.active{background:#C8A96A;color:#fff;border-color:#C8A96A}
.btn-gen{padding:7px 18px;border-radius:8px;font-size:13px;font-weight:600;background:#C8A96A;color:#fff;cursor:pointer;display:flex;align-items:center;gap:6px;border:none;transition:all .2s;white-space:nowrap}
.btn-gen:hover{background:#b89858;transform:translateY(-1px);box-shadow:0 4px 12px rgba(200,169,106,.25)}
.btn-dl{padding:7px 14px;border-radius:8px;font-size:13px;font-weight:600;border:1px solid #E5E5E5E5;color:#555;cursor:pointer;display:flex;align-items:center;gap:6px;background:none;transition:all .2s;white-space:nowrap}
.btn-dl:hover{border-color:#C8A96A;color:#C8A96A}
.sidebar-r{width:260px;border-left:1px solid #E5E5E5E5;background:#FFF;padding:14px;flex-shrink:0;overflow-y:auto}
.rs-title{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#999;margin-bottom:10px;display:flex;align-items:center;gap:6px}
.live-dot{width:6px;height:6px;border-radius:50%;background:#E74C3C;animation:pulse 1.5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.log{max-height:calc(100vh - 120px);overflow-y:auto}
.log-entry{display:flex;gap:8px;padding:5px 0;font-size:11.5px;color:#555;border-bottom:1px solid #ECECEA}
.log-time{font-family:monospace;font-size:10px;color:#999;flex-shrink:0;min-width:40px}
.log-dot{width:5px;height:5px;border-radius:50%;flex-shrink:0;margin-top:5px}
.dot-ok{background:#27AE60}.dot-info{background:#3A7CA5}.dot-warn{background:#C8A96A}.dot-err{background:#E74C3C}
.loading{text-align:center;padding:40px;color:#C8A96A;font-size:14px}
.spinner{width:30px;height:30px;border:3px solid #E5E5E5E5;border-top-color:#C8A96A;border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 12px}
@keyframes spin{to{transform:rotate(360deg)}}
.back-btn{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:#C8A96A;font-weight:600;cursor:pointer;margin-bottom:16px;padding:6px 12px;border-radius:6px;border:1px solid #E5E5E5E5;background:#fff;transition:all .2s}
.back-btn:hover{background:#F0EDE8;border-color:#C8A96A}
.welcome{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:50px 20px;text-align:center}
.welcome h2{font-family:Playfair Display,serif;font-size:24px;color:#1A1A1A;margin-bottom:8px}
.welcome p{color:#888;font-size:14px;max-width:420px;margin-bottom:24px}
.quick-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;width:100%;max-width:480px}
.quick-btn{padding:14px 8px;border-radius:8px;border:1px solid #E5E5E5E5;background:#fff;font-size:13px;font-weight:600;color:#555;cursor:pointer;transition:all .2s;text-align:center}
.quick-btn:hover{border-color:#C8A96A;color:#C8A96A;background:rgba(200,169,106,.05);transform:translateY(-1px)}
.quick-btn span{display:block;font-size:10px;color:#aaa;font-weight:400;margin-top:3px}
.retry-btn{margin-top:24px;padding:10px 24px;border-radius:8px;border:none;background:#C8A96A;color:#fff;font-size:13px;font-weight:600;cursor:pointer;transition:all .2s}
.retry-btn:hover{background:#b89858}
.qb{display:inline-block;background:rgba(200,169,106,.1);color:#C8A96A;font-size:11px;font-weight:600;padding:4px 10px;border-radius:5px;margin-bottom:16px;border:1px solid rgba(200,169,106,.2)}
.freq{padding:14px 0 4px;border-top:1px solid #ECECEA;margin-top:8px}.freq-title{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:#999;margin-bottom:10px;display:flex;align-items:center;gap:6px}.freq-chip{display:inline-block;padding:5px 10px;margin:3px;border-radius:5px;font-size:11px;font-weight:600;background:#F0EDE8;color:#555;cursor:pointer;transition:all .2s;border:none}.freq-chip:hover{background:#C8A96A;color:#fff}
.thdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.thdr h2{font-family:Playfair Display,serif;font-size:22px;font-weight:700;color:#1A1A1A}
.tsub{font-size:13px;color:#888;margin-bottom:20px}
.carousel{position:relative;margin-bottom:24px;background:#FFF;border:1px solid #E5E5E5E5;border-radius:14px;overflow:hidden}
.c-track{display:flex;transition:transform .45s cubic-bezier(.4,0,.2,1)}
.cs{min-width:100%;display:flex;height:420px}
.cs-img{width:55%;height:100%;position:relative;overflow:hidden;background:linear-gradient(135deg,#E8E4DD,#D5D0C8)}
.cs-img img{width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0}
.cs-fb{position:absolute;bottom:0;left:0;right:0;padding:14px;background:linear-gradient(transparent,rgba(0,0,0,.55));color:#fff;font-size:12px;font-weight:600;letter-spacing:.5px;text-transform:uppercase}
.cs-body{width:45%;padding:28px;display:flex;flex-direction:column;justify-content:center}
.cs-tag{display:inline-block;font-size:9px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:#fff;background:#C8A96A;padding:3px 10px;border-radius:4px;margin-bottom:10px;width:fit-content}
.cs-title{font-family:Playfair Display,serif;font-size:20px;font-weight:700;line-height:1.35;color:#1A1A1A;margin-bottom:10px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.cs-desc{font-size:13px;color:#666;line-height:1.55;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:16px;flex:1}
.cs-meta{font-size:11px;color:#999;display:flex;justify-content:space-between;align-items:center;padding-top:12px;border-top:1px solid #ECECEA}
.cs-meta a{color:#3A7CA5;font-weight:600;font-size:12px}
.c-arr{position:absolute;top:50%;transform:translateY(-50%);width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.92);border:1px solid #E5E5E5E5;font-size:22px;cursor:pointer;z-index:5;display:flex;align-items:center;justify-content:center;color:#555;transition:all .2s;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.c-arr:hover{background:#C8A96A;color:#fff;border-color:#C8A96A}
.c-arr.l{left:12px}
.c-arr.r{right:12px}
.c-dots{text-align:center;padding:14px 0}
.c-dots .dot{display:inline-block;width:8px;height:8px;border-radius:8px;background:#ddd;margin:0 4px;cursor:pointer;transition:all .3s}
.c-dots .dot.active{background:#C8A96A;width:24px;border-radius:4px}
.c-counter{font-size:12px;color:#999;text-align:center;margin-top:4px}
.day-hdr{display:flex;align-items:center;gap:10px;margin:24px 0 12px;padding-bottom:8px;border-bottom:2px solid #E5E5E5E5}
.day-hdr h2{font-family:Playfair Display,serif;font-size:18px;font-weight:700;color:#1A1A1A}
.day-hdr .cnt{margin-left:auto;font-size:12px;color:#999}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);z-index:200;justify-content:center;align-items:center}
.modal.show{display:flex}
.modal-content{background:#fff;border-radius:16px;max-width:800px;width:90%;max-height:85vh;overflow-y:auto;padding:32px;box-shadow:0 20px 60px rgba(0,0,0,.2);position:relative}
.modal-close{position:absolute;top:16px;right:16px;width:32px;height:32px;border-radius:50%;border:none;background:#F0EDE8;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#555;transition:all .2s}
.modal-close:hover{background:#E74C3C;color:#fff}
.modal-img{width:100%;height:280px;object-fit:cover;border-radius:10px;margin-bottom:16px}
.modal-tag{display:inline-block;font-size:9px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:#fff;background:#C8A96A;padding:3px 10px;border-radius:4px;margin-bottom:10px}
.modal h2{font-family:Playfair Display,serif;font-size:24px;font-weight:700;color:#1A1A1A;margin-bottom:8px}
.modal-meta{font-size:12px;color:#999;margin-bottom:16px;display:flex;gap:16px}
.modal-body{font-size:15px;line-height:1.7;color:#333;white-space:pre-wrap}
.modal-actions{display:flex;gap:8px;margin-top:16px;padding-top:16px;border-top:1px solid #ECECEA}
.bm-btn{padding:6px 12px;border-radius:6px;font-size:12px;font-weight:600;border:1px solid #E5E5E5E5;cursor:pointer;background:#fff;color:#555;transition:all .2s;display:flex;align-items:center;gap:4px}
.bm-btn:hover{border-color:#C8A96A;color:#C8A96A}
.bm-btn.saved{background:rgba(200,169,106,.12);border-color:#C8A96A;color:#C8A96A}
.trending-list{padding:10px 0}.t-word{display:inline-block;padding:4px 10px;margin:3px;border-radius:12px;font-size:11px;font-weight:600;background:#F0EDE8;color:#555;cursor:pointer;transition:all .2s;border:none}.t-word:hover{background:#C8A96A;color:#fff}
.bm-item{display:flex;gap:12px;padding:10px 0;border-bottom:1px solid #ECECEA;cursor:pointer;transition:all .2s;align-items:flex-start}.bm-item:hover{background:#F8F6F2;margin:0 -8px;padding:10px 8px;border-radius:8px}
.bm-item img{width:48px;height:48px;border-radius:6px;object-fit:cover;flex-shrink:0;background:#E8E4DD}
.bm-item .bm-info{flex:1;min-width:0}.bm-item .bm-title{font-size:13px;font-weight:600;color:#1A1A1A;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.bm-item .bm-meta{font-size:10px;color:#999;margin-top:4px}
.bm-del{font-size:16px;color:#ccc;cursor:pointer;padding:4px;flex-shrink:0;background:none;border:none;transition:all .2s}.bm-del:hover{color:#E74C3C}
.exp-btn{font-size:11px;padding:4px 10px}
"""
js = """
var curD=null;
var days=7;
var sIdx=0;
var sTotal=0;
function esc(s) {
    s = s || "";
    s = s.replace(/&/g, "&amp;");
    s = s.replace(/"/g, "&quot;");
    s = s.replace(/</g, "&lt;");
    s = s.replace(/>/g, "&gt;");
    return s;
}
function getImg(a, d) {
    var u = a.image_url || a.image || "";
    if (u && u.length > 10 && u.indexOf("http") === 0) return u;
    return DI[d] || "https://images.unsplash.com/photo-1504711434969-e33886168d6c?w=800&h=400&fit=crop";
}
function makeSlide(a, d) {
    var img = getImg(a, d);
    var desc = (a.content || "").substring(0, 140);
    if (desc.length >= 140) desc += "...";
    var author = a.author || "News";
    var url = a.url || "#";
    var h = '<div class="cs">';
    if (img === getImg(a, d)) {
        h += '<div class="cs-img" style="background:url(' + esc(img) + ') center/cover"><div class="cs-fb">' + esc(d) + '</div></div>';
    } else {
        h += '<div class="cs-img"><img src="' + esc(img) + '"></div>';
    }
    h += '<div class="cs-body">';
    h += '<div class="cs-tag">' + esc(d) + '</div>';
    h += '<h3 class="cs-title">' + esc(a.title || "") + '</h3>';
    h += '<p class="cs-desc">' + esc(desc) + '</p>';
    h += '<div class="cs-meta"><span>' + esc(author) + '</span><div>';
    h += '<button class="bm-btn" onclick="event.stopPropagation();toggleBookmark(this,' + "'" + esc(url) + "','" + esc(a.title || "") + "','" + esc(author) + "','" + esc(desc) + "','" + esc(img) + "','" + esc(d) + "','" + esc(a.date || "") + "'" + ')" title="Bookmark">&#9733;</button>';
    h += '<button class="bm-btn" onclick="event.stopPropagation();openArticle(' + "'" + esc(url) + "','" + esc(a.title || "") + "','" + esc(author) + "','" + esc(a.content || "") + "','" + esc(img) + "','" + esc(d) + "','" + esc(a.date || "") + "'" + ')">Read</button></div></div>';
    h += '</div></div></div>';
    return h;
}
function slideBy(n) {
    sIdx += n;
    if (sIdx < 0) sIdx = sTotal - 1;
    if (sIdx >= sTotal) sIdx = 0;
    updateCarousel();
}
function updateCarousel() {
    var t = document.getElementById("cT");
    if (t) t.style.transform = "translateX(-" + (sIdx * 100) + "%)";
    var ds = document.querySelectorAll(".c-dots .dot");
    for (var i = 0; i < ds.length; i++) {
        ds[i].classList.toggle("active", i === sIdx);
    }
    var c = document.getElementById("cCt");
    if (c) c.textContent = (sIdx + 1) + " / " + sTotal;
    log("info", "Slide " + (sIdx + 1) + " of " + sTotal);
}
function goToSlide(i) {
    sIdx = i;
    updateCarousel();
}
function buildCarousel(articles, domain) {
    sTotal = articles.length;
    sIdx = 0;
    var t = document.getElementById("cT");
    var d = document.getElementById("cD");
    var h = "";
    for (var i = 0; i < articles.length; i++) {
        h += makeSlide(articles[i], domain);
    }
    t.innerHTML = h;
    var dots = "";
    for (var i = 0; i < articles.length; i++) {
        var cls = (i === 0) ? " active" : "";
        dots += '<span class="dot' + cls + '" onclick="goToSlide(' + i + ')"></span>';
    }
    d.innerHTML = dots;
    updateCarousel();
}
document.getElementById("nc").addEventListener("click", function(e) {
    var c = e.target.closest(".cs-title");
    if (c) {
        var slide = c.closest(".cs");
        if (slide) {
            var url = slide.querySelector("a[href]");
            if (url) { e.preventDefault(); window.open(url.href, "_blank"); }
        }
    }
});
document.addEventListener("keydown", function(e) {
    if (e.key === "ArrowLeft") slideBy(-1);
    if (e.key === "ArrowRight") slideBy(1);
});
document.getElementById("sr").addEventListener("keydown", function(e) {
    if (e.key === "Enter") go();
});
function init() {
    var sb = document.getElementById("sb");
    var dm = document.getElementById("dm");
    var h = "";
    var k = Object.keys(DM);
    for (var i = 0; i < k.length; i++) {
        var d = k[i];
        h += '<div class="sb-item" data-domain="' + esc(d) + '">' + esc(d) + '</div>';
        dm.innerHTML += '<option value="' + esc(d) + '">' + esc(d) + '</option>';
    }
    sb.innerHTML = h;
    sb.addEventListener("click", function(e) {
        var it = e.target.closest(".sb-item");
        if (it) selectDomain(it, it.dataset.domain);
    });
    dm.onchange = function () {
        var o = dm.options[dm.selectedIndex];
        selectDomain({ classList: { add: function () {} } }, o.value);
        var items = sb.querySelectorAll(".sb-item");
        for (var i = 0; i < items.length; i++) {
            items[i].classList.remove("active");
            if (items[i].dataset.domain === o.value) items[i].classList.add("active");
        }
    };
    var tk = document.getElementById("tk");
    var tt = "AI Models - IPL 2025 - Crypto Surge - SpaceX Launch - Cyber Attacks - Tesla EV - Apple WWDC - Formula 1";
    var sp = tt.split(" - ").map(function (t) { return "<span>" + t + "</span>"; }).join("");
    tk.innerHTML = sp + sp;
    log("info", "Loaded " + k.length + " domains");
    showWelcome();
    loadTrending();
    loadFrequent();
}
function showWelcome() {
    document.getElementById("nc").innerHTML = '<div class="welcome"><h2>Welcome to TrendScope</h2><p>Select a domain, pick a sub-topic, then search.</p><div class="quick-grid">';
    var quickBtns = [
        ["Artificial Intelligence (AI)", "LLMs", "GPT-5", "AI & LLMs", "Latest models"],
        ["Technology", "Software & Apps", "", "Tech", "Apps & Software"],
        ["Sports", "Cricket", "IPL final", "Cricket", "IPL & matches"],
        ["Cryptocurrency", "Bitcoin", "", "Crypto", "Bitcoin & ETH"],
        ["Science & Space", "Space", "Starship", "Space", "NASA & SpaceX"],
        ["Business & Startups", "Startups", "", "Startups", "Funding & news"]
    ];
    for (var i = 0; i < quickBtns.length; i++) {
        var q = quickBtns[i];
        h += '<div class="quick-btn" data-qd="' + esc(q[0]) + '" data-qs="' + esc(q[1]) + '" data-sr="' + esc(q[2]) + '">' + q[3] + '<span>' + q[4] + '</span></div>';
    }
    h += '</div><button class="retry-btn" id="retryBtn">Load Trending News</button></div>';
    document.getElementById("retryBtn").addEventListener("click", loadTrending);
    document.getElementById("nc").addEventListener("click", function (e) {
        var btn = e.target.closest(".quick-btn");
        if (btn) {
            quickGo(btn.dataset.qd, btn.dataset.qs, btn.dataset.sr || "");
            document.getElementById("nc").removeEventListener("click", arguments.callee);
        }
    });
}
function quickGo(d, s, r) {
    document.getElementById("dm").value = d;
    document.getElementById("sr").value = r;
    curD = d;
    var items = document.querySelectorAll(".sb-item");
    for (var i = 0; i < items.length; i++) {
        items[i].classList.remove("active");
        if (items[i].dataset.domain === d) items[i].classList.add("active");
    }
    populateSubs(d);
    document.getElementById("st").value = s;
    go();
}
function populateSubs(d) {
    var st = document.getElementById("st");
    var s = DM[d];
    st.innerHTML = "";
    if (s) {
        var k = Object.keys(s);
        for (var i = 0; i < k.length; i++) {
            st.innerHTML += '<option value="' + esc(s[k[i]]) + '">' + esc(k[i]) + '</option>';
        }
    }
}
function selectDomain(el, d) {
    curD = d;
    var items = document.querySelectorAll(".sb-item");
    for (var i = 0; i < items.length; i++) items[i].classList.remove("active");
    if (el && el.classList) el.classList.add("active");
    document.getElementById("dm").value = d;
    populateSubs(d);
    log("ok", "Domain: " + d + " (" + Object.keys(DM[d]).length + " sub-topics)");
}
function loadFrequent() {
    fetch("/api/frequent-categories")
        .then(function (r) { return r.json(); })
        .then(function (data) {
            var fc = document.getElementById("fc");
            var h = "";
            for (var i = 0; i < data.length; i++) {
                h += '<button class="freq-chip" data-qd="' + esc(data[i].domain) + '" data-qs="' + esc(data[i].subtopic) + '">' + esc(data[i].label) + '</button>';
            }
            fc.innerHTML = h;
            fc.addEventListener("click", function (e) {
                var chip = e.target.closest(".freq-chip");
                if (chip) {
                    selectDomain(null, chip.dataset.qd);
                    populateSubs(chip.dataset.qd);
                    document.getElementById("st").value = chip.dataset.qs;
                    document.getElementById("sr").value = "";
                    go();
                }
            });
        })
        .catch(function () {});
}
function buildQuery() {
    var subVal = document.getElementById("st").value;
    var search = document.getElementById("sr").value.trim();
    if (search) return search;
    if (subVal) return subVal;
    return "";
}
function loadTrending() {
    var nc = document.getElementById("nc");
    nc.innerHTML = '<div class="loading"><div class="spinner"></div>Fetching trending...</div>';
    log("info", "Loading trending...");
    var domains = [
        "Artificial Intelligence (AI)", "Technology", "Sports", "Business & Startups", "Finance & Stock Market", "Cryptocurrency", "Entertainment", "Science & Space", "Cybersecurity"
    ];
    var all = [];
    var done = 0;
    for (var i = 0; i < domains.length; i++) {
        (function (d, x) {
            setTimeout(function () {
                fetch("/api/news?domain=" + encodeURIComponent(d) + "&subtopic=&days=" + days)
                    .then(function (r) {
                        if (!r.ok) throw new Error("HTTP " + r.status);
                        return r.json();
                    })
                    .then(function (data) {
                        if (Array.isArray(data) && data.length > 0) {
                            var it = data.slice(0, 3);
                            for (var j = 0; j < it.length; j++) it[j]._domain = d;
                            all = all.concat(it);
                        }
                        done++;
                        log("ok", d + ": " + (Array.isArray(data) ? data.length : 0));
                        if (done === domains.length) finishTrending(all);
                    })
                    .catch (function () {
                        done++;
                        log("err", d + ": failed");
                        if (done === domains.length) finishTrending(all);
                    });
            }, x * 400);
        })(domains[i], i);
    }
}
function finishTrending(all) {
    if (all.length === 0) {
        log("warn", "No trending news");
        showWelcome();
        return;
    }
    log("ok", "Total: " + all.length + " trending");
    var h = '<div class="thdr"><h2>&#128293; Trending Now</h2><button class="back-btn" style="margin:0" id="refBtn">Refresh</button></div>';
    h += '<p class="tsub">Swipe or use arrows to browse. Click a card to read.</p>';
    h += '<div class="carousel"><button class="c-arr l" onclick="slideBy(-1)">&#8249;</button>';
    h += '<div class="c-track" id="cT"></div>';
    h += '<button class="c-arr r" onclick="slideBy(1)">&#8250;</button></div>';
    h += '<div class="c-dots" id="cD"></div>';
    h += '<div class="c-counter" id="cCt"></div>';
    document.getElementById("nc").innerHTML = h;
    buildCarousel(all, "trending");
    document.getElementById("refBtn").addEventListener("click", loadTrending);
}
function setDays(n) {
    days = n;
    var ch = document.querySelectorAll(".chip");
    for (var i = 0; i < ch.length; i++) {
        ch[i].classList.toggle("active", parseInt(ch[i].dataset.d) === n);
    }
    if (curD) go();
}
function log(type, msg) {
    var lg = document.getElementById("lg");
    var n = new Date();
    var tm = n.getHours().toString().padStart(2, "0") + ":" + n.getMinutes().toString().padStart(2, "0");
    var dot = type === "ok" ? "dot-ok" : type === "err" ? "dot-err" : type === "warn" ? "dot-warn" : "dot-info";
    lg.innerHTML = '<div class="log-entry"><span class="log-time">' + tm + '</span><span class="log-dot ' + dot + '"></span><span>' + msg + '</span></div>' + lg.innerHTML;
}
function go() {
    if (!curD) { log("err", "Select a domain first"); return; }
    var q = buildQuery();
    if (!q) { log("err", "Pick a sub-topic or search"); return; }
    log("warn", "Searching: \"" + q + "\" in " + curD);
    document.getElementById("nc").innerHTML = '<div class="loading"><div class="spinner"></div>Loading...</div>';
    fetch("/api/news?domain=" + encodeURIComponent(curD) + "&subtopic=" + encodeURIComponent(q) + "&days=" + days)
        .then(function (r) {
            if (!r.ok) throw new Error("HTTP " + r.status);
            return r.json();
        })
        .then(function (data) {
            renderResults(data, q);
            log("ok", "Found " + data.length + " articles");
        })
        .catch (function (e) {
            log("err", "Failed: " + e.message);
            showWelcome();
        });
}
function renderResults(data, q) {
    if (!data || data.length === 0) {
        document.getElementById("nc").innerHTML = '<div class="back-btn" id="bb">Back to Trending</div><div class="qb">Searched: "' + esc(q) + '" in "' + esc(curD) + '"</div><div class="welcome"><h2>No articles found</h2><p>Try different keywords.</p></div>';
        document.getElementById("bb").addEventListener("click", loadTrending);
        return;
    }
    var h = '<div class="back-btn" id="bb">Back to Trending</div>';
    h += '<div class="qb">Searched: "' + esc(q) + '" in "' + esc(curD) + '"</div>';
    h += '<div class="carousel"><button class="c-arr l" onclick="slideBy(-1)">&#8249;</button>';
    h += '<div class="c-track" id="cT"></div>';
    h += '<button class="c-arr r" onclick="slideBy(1)">&#8250;</button></div>';
    h += '<div class="c-dots" id="cD"></div>';
    h += '<div class="c-counter" id="cCt"></div>';
    document.getElementById("nc").innerHTML = h;
    buildCarousel(data, curD);
    document.getElementById("bb").addEventListener("click", loadTrending);
}
function downloadPDF() {
    if (!curD) { log("err", "Select a domain first"); return; }
    var q = buildQuery();
    if (!q) { log("err", "Pick a sub-topic or search"); return; }
    log("warn", "Generating PDF...");
    fetch("/api/generate-pdf?domain=" + encodeURIComponent(curD) + "&subtopic=" + encodeURIComponent(q) + "&days=" + days)
        .then(function (r) { return r.json(); })
        .then(function (d) {
            log("ok", "PDF done! " + d.count + " articles");
            window.open("/api/latest-pdf", "_blank");
        })
        .catch(function () { log("err", "PDF error"); });
}
var bookmarksCache = null;
function openArticle(url, title, author, content, img, domain, date) {
    var m = document.getElementById("modal");
    var imgHtml = img && img.indexOf("http") === 0 ? '<img class="modal-img" src="' + esc(img) + '" alt="">' : "";
    var s = content.substring(0, 5000);
    m.innerHTML = '<div class="modal-content"><button class="modal-close" onclick="closeModal()">&times;</button>' +
        imgHtml +
        '<div class="modal-tag">' + esc(domain) + '</div>' +
        '<h2>' + esc(title) + '</h2>' +
        '<div class="modal-meta"><span>' + esc(author) + '</span><span>' + esc(date) + '</span></div>' +
        '<div class="modal-body">' + esc(s) + '</div>' +
        '<div class="modal-actions">' +
        '<button class="bm-btn" id="modalBmBtn" onclick="toggleBookmark(this,' + "'" + esc(url) + "','" + esc(title) + "','" + esc(author) + "','" + esc(s.substring(0,200)) + "','" + esc(img) + "','" + esc(domain) + "','" + esc(date) + "'" + ')">&#9733; Bookmark</button>' +
        '<a href="' + esc(url) + '" target="_blank" class="bm-btn">Open Original</a>' +
        '</div></div>';
    m.classList.add("show");
    document.body.style.overflow = "hidden";
    m.addEventListener("click", function(e) { if (e.target === m) closeModal(); });
    document.addEventListener("keydown", modalKeydown);
    // check if already bookmarked
    fetch("/api/bookmarks").then(function(r) { return r.json(); }).then(function(bm) {
        var exists = bm.some(function(b) { return b.url === url; });
        if (exists) document.getElementById("modalBmBtn").classList.add("saved");
    }).catch(function() {});
}
function closeModal() {
    var m = document.getElementById("modal");
    m.classList.remove("show");
    m.innerHTML = "";
    document.body.style.overflow = "";
    document.removeEventListener("keydown", modalKeydown);
}
function modalKeydown(e) { if (e.key === "Escape") closeModal(); }
function toggleBookmark(btn, url, title, author, content, img, domain, date) {
    var saved = btn.classList.contains("saved");
    if (saved) {
        fetch("/api/bookmarks?url=" + encodeURIComponent(url), { method: "DELETE" })
            .then(function(r) { return r.json(); })
            .then(function(d) {
                btn.classList.remove("saved");
                btn.textContent = btn.textContent.replace("Bookmarked", "Bookmark");
                log("ok", "Bookmark removed");
                if (document.getElementById("bmSection") && document.getElementById("bmSection").style.display !== "none") loadBookmarks();
            }).catch(function() {});
    } else {
        fetch("/api/bookmarks", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({url: url, title: title, author: author, content: content, image_url: img, domain: domain, date: date})
        }).then(function(r) { return r.json(); })
        .then(function(d) {
            btn.classList.add("saved");
            btn.textContent = btn.textContent.replace("Bookmark", "Bookmarked");
            log("ok", "Bookmark saved");
            if (document.getElementById("bmSection") && document.getElementById("bmSection").style.display !== "none") loadBookmarks();
        }).catch(function() {});
    }
}
function loadBookmarks() {
    fetch("/api/bookmarks").then(function(r) { return r.json(); }).then(function(data) {
        bookmarksCache = data;
        var nc = document.getElementById("nc");
        var h = '<div class="back-btn" onclick="showHome()">Back to Home</div>';
        h += '<div class="thdr"><h2>&#128278; Saved Bookmarks (' + data.length + ')</h2></div>';
        if (data.length === 0) {
            h += '<div class="welcome"><h2>No bookmarks yet</h2><p>Click the &#9733; star on any article to save it.</p></div>';
        } else {
            for (var i = 0; i < data.length; i++) {
                var b = data[i];
                var img = b.image_url && b.image_url.indexOf("http") === 0 ? b.image_url : "";
                h += '<div class="bm-item" onclick="openArticle(' + "'" + esc(b.url) + "','" + esc(b.title) + "','" + esc(b.author) + "','" + esc(b.content || "") + "','" + esc(b.image_url || "") + "','" + esc(b.domain || "") + "','" + esc(b.date || "") + "'" + ')">';
                h += img ? '<img src="' + esc(img) + '">' : '<div style="width:48px;height:48px;border-radius:6px;background:#E8E4DD;flex-shrink:0"></div>';
                h += '<div class="bm-info"><div class="bm-title">' + esc(b.title) + '</div><div class="bm-meta">' + esc(b.author) + ' &middot; ' + esc(b.domain) + '</div></div>';
                h += '<button class="bm-del" onclick="event.stopPropagation();deleteBookmark(\'' + esc(b.url) + '\', this)">&times;</button></div>';
            }
        }
        nc.innerHTML = h;
    }).catch(function() { log("err", "Failed to load bookmarks"); });
}
function deleteBookmark(url, el) {
    fetch("/api/bookmarks?url=" + encodeURIComponent(url), { method: "DELETE" })
        .then(function(r) { return r.json(); })
        .then(function() {
            var item = el.closest(".bm-item");
            if (item) item.remove();
            log("ok", "Bookmark removed");
        }).catch(function() {});
}
function showBookmarks() { loadBookmarks(); }
function showHome() {
    curD = null;
    showWelcome();
    loadTrending();
}
function exportCSV() {
    if (!curD) { log("err", "Select a domain first"); return; }
    var q = buildQuery();
    if (!q) { log("err", "Pick a sub-topic or search"); return; }
    window.open("/api/export/csv?domain=" + encodeURIComponent(curD) + "&subtopic=" + encodeURIComponent(q) + "&days=" + days, "_blank");
    log("ok", "CSV download started");
}
function exportJSON() {
    if (!curD) { log("err", "Select a domain first"); return; }
    var q = buildQuery();
    if (!q) { log("err", "Pick a sub-topic or search"); return; }
    window.open("/api/export/json?domain=" + encodeURIComponent(curD) + "&subtopic=" + encodeURIComponent(q) + "&days=" + days, "_blank");
    log("ok", "JSON download started");
}
function loadTrendingWords() {
    fetch("/api/trending?domain=")
        .then(function(r) { return r.json(); })
        .then(function(data) {
            var el = document.getElementById("tw");
            if (!el) return;
            var h = "";
            for (var i = 0; i < Math.min(data.length, 20); i++) {
                h += '<button class="t-word" onclick="quickSearch(\'' + esc(data[i].word) + '\')">' + esc(data[i].word) + '</button>';
            }
            el.innerHTML = h;
        }).catch(function() {});
}
function quickSearch(term) {
    document.getElementById("sr").value = term;
    if (document.getElementById("dm").value) {
        curD = document.getElementById("dm").value;
        go();
    } else {
        log("warn", "Select a domain first, then search");
    }
}
init();
loadTrendingWords();
"""
body = '<div class="ticker"><div class="ticker-label">TRENDING</div><div class="ticker-track" id="tk"></div></div>';
body += '<header class="header"><a href="#" class="logo">Trend<b>Scope</b></a></header>';
body += '<div class="main">';
body += '<aside class="sidebar-l"><div class="sb-title">Domains</div><div id="sb"></div></aside>';
body += '<main class="content" id="ct"><div class="controls">';
body += '<div class="ctrl-row">';
body += '<div class="ctrl-grp"><label class="ctrl-label">Domain</label><select class="ctrl-in" id="dm"></select></div>';
body += '<div class="ctrl-grp"><label class="ctrl-label">Sub-Topic</label><select class="ctrl-in" id="st"><option value="">Select domain first</option></select></div>';
body += '<div class="ctrl-grp"><label class="ctrl-label">Range</label><div class="chips"><button class="chip" data-d="1" onclick="setDays(1)">1D</button><button class="chip active" data-d="7" onclick="setDays(7)">7D</button><button class="chip" data-d="30" onclick="setDays(30)">30D</button><button class="chip" data-d="90" onclick="setDays(90)">90D</button><button class="chip" data-d="180" onclick="setDays(180)">6M</button></div></div>';
body += '<div class="ctrl-spacer"></div>';
body += '<button class="btn-gen" onclick="go()"><span class="iconify" data-icon="lucide:sparkles"></span> Generate</button>';
body += '<button class="btn-dl" onclick="downloadPDF()"><span class="iconify" data-icon="lucide:download"></span> PDF</button>';
body += '<button class="btn-dl exp-btn" onclick="exportCSV()">CSV</button>';
body += '<button class="btn-dl exp-btn" onclick="exportJSON()">JSON</button>';
body += '</div>';
body += '<div class="ctrl-row"><div class="search-box"><span class="iconify" data-icon="lucide:search"></span><input class="ctrl-in" id="sr" placeholder="Search... e.g. Ram Charan, Free Fire, GPT-5"></div></div>';
body += '<div class="search-hint" id="hint">Tip: Search text takes priority for accurate results</div></div>';
body += '<div id="nc"></div></main>';
body += '<aside class="sidebar-r"><div class="rs-title"><span class="live-dot"></span> Live Activity</div><div class="log" id="lg"></div><div class="trending-list"><div class="freq-title">&#128200; Trending Words</div><div id="tw"></div></div><div class="freq"><div class="freq-title">Popular Categories</div><div id="fc"></div></div><div style="padding-top:8px"><div class="rs-title" style="cursor:pointer" onclick="showBookmarks()">&#128278; Bookmarks</div></div></aside>';
body += '</div>';
body += '<div class="modal" id="modal"></div>';
body += '<script src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>';
body += '<style>' + css + '</style>';
body += '<script>var DM=' + json.dumps(DM) + ';var DI=' + json.dumps(DI) + ';' + js + '</script>';
body += '</body></html>';
import os
os.makedirs("templates", exist_ok=True)
with open("templates/index.html", "w", encoding="utf-8", newline="\n") as f:
    f.write(body)
size = len(body)
actual = len(DM)
print("index.html: " + str(size) + " bytes")
print("Domains in data: " + str(actual))
if actual >= 25:
    print("SUCCESS! All " + str(actual) + " domains verified!")
else:
    print("WARNING: Only " + str(actual) + " domains found - something went wrong!")
