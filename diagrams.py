from PIL import Image, ImageDraw, ImageFont
import os

FONT = "C:\\Windows\\Fonts\\arial.ttf"
FONT_BOLD = "C:\\Windows\\Fonts\\arialbd.ttf"
W = 720
H = 400
BG = (248, 249, 252)
BLUE = (41, 98, 255)
DARK = (30, 35, 55)
GREEN = (0, 180, 80)
ORANGE = (255, 150, 30)
RED = (220, 50, 50)
GRAY = (160, 170, 190)
LIGHT_BLUE = (220, 235, 255)
LIGHT_GREEN = (220, 250, 230)
LIGHT_ORANGE = (255, 240, 220)

def make_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT, size)
    except:
        return ImageFont.load_default()

def box(d, x, y, w, h, fill, text, font, text_color=(255,255,255)):
    d.rounded_rectangle([x, y, x+w, y+h], radius=8, fill=fill)
    bbox = d.textbbox((0,0), text, font=font)
    tw = bbox[2]-bbox[0]
    th = bbox[3]-bbox[1]
    d.text((x + w//2 - tw//2, y + h//2 - th//2), text, fill=text_color, font=font)

def arrow(d, x1, y1, x2, y2, color=GRAY):
    d.line([(x1, y1), (x2, y2)], fill=color, width=2)
    mx, my = (x1+x2)//2, (y1+y2)//2
    dx, dy = x2-x1, y2-y1
    length = (dx*dx+dy*dy)**0.5
    if length == 0: return
    ux, uy = dx/length, dy/length
    p1 = (mx - 8*ux + 4*uy, my - 8*uy - 4*ux)
    p2 = (mx - 8*ux - 4*uy, my - 8*uy + 4*ux)
    d.polygon([(mx, my), p1, p2], fill=color)

def label(d, x, y, text, font, color=(100,100,120)):
    bbox = d.textbbox((0,0), text, font=font)
    tw = bbox[2]-bbox[0]
    d.text((x - tw//2, y), text, fill=color, font=font)

# Setup
os.makedirs("diagrams", exist_ok=True)

# === 1. SYSTEM ARCHITECTURE ===
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
f10 = make_font(10)
f11 = make_font(11)
f12 = make_font(12, True)
f14 = make_font(14, True)

# Layer 1: Users
box(d, 60, 20, 180, 45, BLUE, "Web Browser", f14)
box(d, 270, 20, 180, 45, BLUE, "Android App", f14)
box(d, 480, 20, 180, 45, BLUE, "Desktop (Tkinter)", f14)
label(d, 150, 72, "(Flask SPA)", make_font(9), GRAY)
label(d, 360, 72, "(Native Kotlin)", make_font(9), GRAY)
label(d, 570, 72, "(Python GUI)", make_font(9), GRAY)
d.text((10, 35), "Users", fill=DARK, font=f12)

# Layer 2: API/Network
box(d, 160, 115, 400, 45, DARK, "REST API + RSS Aggregation Engine", f14)
label(d, 360, 167, "(Flask Backend - app.py)", make_font(9), GRAY)
arrow(d, 150, 65, 300, 115, GRAY)
arrow(d, 360, 65, 360, 115, GRAY)
arrow(d, 570, 65, 420, 115, GRAY)

# Layer 3: Data Sources
box(d, 100, 210, 170, 45, GREEN, "Google News RSS", f12)
box(d, 310, 210, 130, 45, GREEN, "RSS Feeds", f12)
box(d, 470, 210, 160, 45, GREEN, "Domain Feeds", f12)
arrow(d, 360, 160, 360, 210, GRAY)

# Layer 4: Storage
box(d, 130, 300, 160, 50, ORANGE, "Room DB (SQLite)", f12)
box(d, 430, 300, 160, 50, ORANGE, "PDF Reports (fpdf2)", f12)
arrow(d, 210, 255, 210, 300, GRAY)
arrow(d, 510, 255, 510, 300, GRAY)

# Layer 5: Output
box(d, 60, 370, 150, 40, RED, "JSON / CSV Export", f11, DARK)
box(d, 290, 370, 140, 40, RED, "PDF Download", f11, DARK)
box(d, 510, 370, 150, 40, RED, "Bookmark API", f11, DARK)
arrow(d, 210, 350, 135, 370, GRAY)
arrow(d, 360, 350, 360, 370, GRAY)
arrow(d, 510, 350, 585, 370, GRAY)

img.save("diagrams/system_architecture.png")

# === 2. ANDROID APP ARCHITECTURE ===
img2 = Image.new("RGB", (W, H), BG)
d2 = ImageDraw.Draw(img2)

# Title
d2.text((10, 10), "Android App Architecture", fill=DARK, font=f14)

# Layer 1: UI
box(d2, 50, 40, 620, 50, DARK, "Presentation Layer", f12)
box(d2, 80, 100, 130, 35, BLUE, "MainActivity", f11)
box(d2, 230, 100, 140, 35, BLUE, "ArticleActivity", f11)
box(d2, 390, 100, 120, 35, BLUE, "CategoryActivity", f11)
box(d2, 530, 100, 110, 35, BLUE, "Adapters", f11)
arrow(d2, 360, 90, 360, 145, GRAY)

# Layer 2: ViewModel / Logic
box(d2, 100, 155, 520, 40, GREEN, "Application Logic Layer", f12)
box(d2, 120, 205, 140, 30, GREEN, "TranslationManager", f10, DARK)
box(d2, 290, 205, 140, 30, GREEN, "RssParser", f10, DARK)
box(d2, 460, 205, 120, 30, GREEN, "DomainFeeds", f10, DARK)
arrow(d2, 360, 145, 360, 200, GRAY)

# Layer 3: Data
box(d2, 100, 260, 520, 40, ORANGE, "Data Layer", f12)
box(d2, 120, 312, 140, 30, ORANGE, "Room Database", f10, DARK)
box(d2, 290, 312, 130, 30, ORANGE, "ArticleDao", f10, DARK)
box(d2, 450, 312, 140, 30, ORANGE, "Article Entity", f10, DARK)
arrow(d2, 360, 245, 360, 310, GRAY)

# Layer 4: External
box(d2, 100, 365, 520, 30, RED, "External: MyMemory API / LibreTranslate / RSS Feeds", f11, DARK)
arrow(d2, 360, 350, 360, 365, GRAY)

img2.save("diagrams/android_architecture.png")

# === 3. DATA FLOW FROM RSS TO UI ===
img3 = Image.new("RGB", (W, H), BG)
d3 = ImageDraw.Draw(img3)
d3.text((10, 10), "Data Pipeline: RSS Feed to Article Display", fill=DARK, font=f14)

nodes = [
    (50, 60, 160, 50, BLUE, "RSS Fetch", "OkHttp / Feeds"),
    (290, 60, 200, 50, BLUE, "XmlPullParser", "Parse XML"),
    (560, 60, 120, 50, BLUE, "Article", "Entity created"),
    (120, 180, 200, 50, GREEN, "Room Database", "Insert Article"),
    (400, 180, 200, 50, GREEN, "Room Query", "getAllArticles()"),
    (200, 290, 300, 50, ORANGE, "RecyclerView Adapter", "bindArticle()"),
    (200, 365, 300, 40, RED, "User Sees Article", "Title, Desc, Image, Favicon"),
]
for x, y, w, h, color, t, sub in nodes:
    box(d3, x, y, w, h, color, t, f12, (255,255,255))
    d3.text((x+w//2-30, y+h+2), sub, fill=GRAY, font=make_font(8))

# Arrows
arrow(d3, 130, 110, 210, 140)
arrow(d3, 390, 110, 390, 140)
arrow(d3, 620, 110, 620, 140)
arrow(d3, 220, 230, 220, 290)
arrow(d3, 500, 230, 500, 290)
arrow(d3, 350, 340, 350, 365)

img3.save("diagrams/data_flow.png")

# === 4. TRANSLATION FLOW ===
img4 = Image.new("RGB", (W, H), BG)
d4 = ImageDraw.Draw(img4)
d4.text((10, 10), "Translation Flow: English to Indian Languages", fill=DARK, font=f14)

box(d4, 250, 45, 200, 40, DARK, "User selects language", f12, (255,255,255))
arrow(d4, 350, 85, 350, 115, GRAY)

box(d4, 100, 115, 160, 45, BLUE, "MyMemory API", f12, (255,255,255))
box(d4, 460, 115, 160, 45, ORANGE, "LibreTranslate", f12, (255,255,255))
label(d4, 180, 167, "Primary (no API key)", make_font(8), GRAY)
label(d4, 540, 167, "Fallback", make_font(8), GRAY)

# Branch
d4.line([(350, 110), (180, 115)], fill=GRAY, width=2)
d4.line([(350, 110), (540, 115)], fill=GRAY, width=2)
# Arrow from primary down
arrow(d4, 180, 160, 180, 195, GRAY)
# Arrow from fallback down
arrow(d4, 540, 160, 540, 195, GRAY)

box(d4, 100, 200, 160, 40, GREEN, "Cached in Room DB", f11, DARK)
box(d4, 460, 200, 160, 40, GREEN, "Cached in Room DB", f11, DARK)
d4.line([(165, 240), (260, 240)], fill=GRAY, width=1)

box(d4, 260, 240, 200, 40, DARK, "updateTranslation()", f12, (255,255,255))
arrow(d4, 360, 280, 360, 310, GRAY)

box(d4, 200, 310, 320, 40, RED, "Adapter displays translated text", f12, DARK)

img4.save("diagrams/translation_flow.png")

print("All diagrams generated in diagrams/")
