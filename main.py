import os
from pdf_opener import open_pdf
from urllib.parse import quote
from viewer import show_articles, generate_news_pdf
import tkinter as tk
from datetime import datetime, timedelta
from synapse.pipelines.supervisor import run_weekly_pipeline

DOMAINS = {
    "Technology": {"Software & Apps": "software development OR apps", "Internet Trends": "internet trends", "IT": "cloud computing OR servers"},
    "Artificial Intelligence (AI)": {"Machine Learning": "machine learning", "LLMs": "LLM OR GPT OR Claude", "Robotics": "robotics", "AI Ethics": "AI ethics"},
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


BG_DARK = "#0f172a"
BG_PANEL = "#1e293b"
ACCENT = "#8b5cf6"
TEXT_MAIN = "#f1f5f9"
TEXT_SUB = "#94a3b8"
SUCCESS = "#22c55e"
DANGER = "#ef4444"
YELLOW = "#facc15"

class TrendScopeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TrendScope Dashboard")
        self.root.geometry("1050x680")
        self.root.configure(bg=BG_DARK)
        self.selected_main = None
        self.selected_sub = None
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#1e293b", height=55)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="â¬¡ TrendScope", font=("Helvetica", 20, "bold"), bg="#1e293b", fg="white").pack(side="left", padx=20)
        profile_fr = tk.Frame(header, bg="#1e293b")
        profile_fr.pack(side="right", padx=20)
        tk.Label(profile_fr, text="ðŸŸ¢", font=("Helvetica", 10), bg="#1e293b", fg=SUCCESS).pack(side="right")
        tk.Label(profile_fr, text="Admin  |  Premium", font=("Helvetica", 10), bg="#1e293b", fg=TEXT_SUB).pack(side="right", padx=10)

        trend_bar = tk.Frame(self.root, bg="#0f172a", height=40)
        trend_bar.pack(fill="x")
        trend_bar.pack_propagate(False)
        tk.Label(trend_bar, text="ðŸ”¥ Trending:", font=("Helvetica", 10, "bold"), bg="#0f172a", fg=YELLOW).pack(side="left", padx=15)
        for t in ["AI Models", "IPL 2025", "Crypto", "Apple WWDC", "SpaceX", "Cyber Attacks", "Tesla EV"]:
            tk.Label(trend_bar, text=f" {t}", font=("Helvetica", 9), bg="#334155", fg=TEXT_MAIN, padx=8, pady=5).pack(side="left", padx=2)

        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT: Domains (Using a proper Listbox so clicking actually works!)
        left_panel = tk.Frame(body, bg=BG_PANEL, width=230)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)
        tk.Label(left_panel, text="ðŸ“‚ DOMAINS", font=("Helvetica", 10, "bold"), bg=BG_PANEL, fg=TEXT_SUB).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.domain_listbox = tk.Listbox(left_panel, font=("Helvetica", 11), bg="#0f172a", fg=TEXT_MAIN, selectbackground=ACCENT, selectforeground="white", bd=0, highlightthickness=0, highlightcolor=ACCENT, activestyle="none")
        self.domain_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        for domain in DOMAINS.keys():
            self.domain_listbox.insert(tk.END, f"   {domain}")
        self.domain_listbox.bind("<<ListboxSelect>>", self.on_main_select)

        # CENTER: Settings
        center_panel = tk.Frame(body, bg=BG_PANEL)
        center_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(center_panel, text="âš™ï¸ CONFIGURE DIGEST", font=("Helvetica", 12, "bold"), bg=BG_PANEL, fg=TEXT_SUB).pack(anchor="w", padx=20, pady=(15, 10))
        tk.Label(center_panel, text="Sub-Topic:", font=("Helvetica", 10), bg=BG_PANEL, fg=TEXT_MAIN).pack(anchor="w", padx=20)
        
        self.sub_listbox = tk.Listbox(center_panel, height=6, font=("Helvetica", 10), bg="#0f172a", fg=TEXT_MAIN, selectbackground=ACCENT, selectforeground="white", bd=0, highlightthickness=1, highlightcolor=ACCENT)
        self.sub_listbox.pack(fill="x", padx=20, pady=(0, 15))
        self.sub_listbox.bind("<<ListboxSelect>>", self.on_sub_select)
        
        tk.Label(center_panel, text="Deep Filter (Optional):", font=("Helvetica", 10), bg=BG_PANEL, fg=TEXT_MAIN).pack(anchor="w", padx=20)
        self.search_entry = tk.Entry(center_panel, font=("Helvetica", 12), bg="#0f172a", fg=TEXT_MAIN, insertbackground=TEXT_MAIN, bd=0, highlightthickness=1, highlightcolor=ACCENT)
        self.search_entry.pack(fill="x", padx=20, pady=(0, 20))
        self.search_entry.insert(0, "  e.g., IPL, OpenAI, Apple...")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)

        self.gen_btn = tk.Button(center_panel, text="âš¡  GENERATE PDF", font=("Helvetica", 13, "bold"), bg=ACCENT, fg="white", activebackground="#7c3aed", bd=0, pady=15, cursor="hand2", command=self.start_generation)
        btn_row = tk.Frame(center_panel, bg=BG_PANEL)
        btn_row.pack(fill="x", padx=20, pady=(10, 5))
        self.gen_btn = tk.Button(btn_row, text="GENERATE PDF", font=("Helvetica", 11, "bold"), bg=ACCENT, fg="white", bd=0, pady=10, cursor="hand2", command=self.start_generation)
        self.gen_btn.pack(side="left", expand=True, fill="x", padx=(0,2))
        self.pdf_btn = tk.Button(btn_row, text="OPEN PDF", font=("Helvetica", 11, "bold"), bg="#334155", fg="white", bd=0, pady=10, cursor="hand2", command=open_pdf)
        self.pdf_btn.pack(side="left", expand=True, fill="x", padx=(2,2))
        self.dl_btn = tk.Button(btn_row, text="DOWNLOAD PDF", font=("Helvetica", 11, "bold"), bg="#16a34a", fg="white", bd=0, pady=10, cursor="hand2", command=self.download_pdf)
        self.dl_btn.pack(side="right", expand=True, fill="x", padx=(2,0))
        tk.Label(center_panel, text="GENERATED ARTICLES", font=("Helvetica", 10, "bold"), bg=BG_PANEL, fg=TEXT_SUB).pack(anchor="w", padx=20, pady=(10,2))
        self.article_box = tk.Text(center_panel, font=("Helvetica", 9), bg="#0f172a", fg=TEXT_MAIN, bd=0, highlightthickness=1, highlightcolor=ACCENT, state="disabled", wrap="word", cursor="arrow")
        self.article_box.pack(fill="both", expand=True, padx=20, pady=(0,15))
        self.article_box.tag_configure("title", foreground="#60a5fa", font=("Helvetica", 10, "bold"))
        self.article_box.tag_configure("link", foreground="#facc15")

        # RIGHT: Notifications
        right_panel = tk.Frame(body, bg=BG_PANEL, width=280)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        tk.Label(right_panel, text="ðŸ”” LIVE ACTIVITY", font=("Helvetica", 10, "bold"), bg=BG_PANEL, fg=TEXT_SUB).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.log_box = tk.Text(right_panel, font=("Consolas", 9), bg="#0f172a", fg="#4ade80", bd=0, highlightthickness=0, state="disabled", wrap="word")
        self.log_box.pack(fill="both", expand=True, padx=10, pady=5)
        self.add_log("System initialized.", "white")
        self.add_log("Ready to generate.", TEXT_SUB)



    def open_latest_pdf(self):
        import subprocess
        project_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(project_dir, "data")
        if not os.path.exists(data_dir): return
        pdfs = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.pdf')]
        if not pdfs: return
        latest = max(pdfs, key=os.path.getctime)
        subprocess.Popen(["xdg-open", latest])

    def download_pdf(self):
        import shutil, tkinter.filedialog as fd, tkinter.messagebox as mb
        project_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(project_dir, "data")
        if not os.path.exists(data_dir):
            mb.showinfo("No PDF", "Generate a PDF first!")
            return
        pdfs = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.pdf')]
        if not pdfs:
            mb.showinfo("No PDF", "Generate a PDF first!")
            return
        latest = max(pdfs, key=os.path.getctime)
        dest = fd.asksaveasfilename(
            initialdir=os.path.expanduser("~/Downloads"),
            initialfile=os.path.basename(latest),
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save PDF As"
        )
        if dest:
            shutil.copy2(latest, dest)
            self.add_log(f"PDF saved to: {dest}", SUCCESS)
            mb.showinfo("Downloaded", f"PDF saved to:\n{dest}")

    def clear_placeholder(self, event):
        if "e.g.," in self.search_entry.get():
            self.search_entry.delete(0, tk.END)

    def add_log(self, message, color="white"):
        self.log_box.config(state="normal")
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert(tk.END, f"[{time_str}] {message}\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")

    def on_main_select(self, event):
        selection = self.domain_listbox.curselection()
        if selection:
            self.selected_main = self.domain_listbox.get(selection[0]).strip()
            self.sub_listbox.delete(0, tk.END)
            for sub in DOMAINS[self.selected_main].keys():
                self.sub_listbox.insert(tk.END, sub)
            self.add_log(f"Loaded: {self.selected_main}", "#60a5fa")

    def on_sub_select(self, event):
        selection = self.sub_listbox.curselection()
        if selection:
            self.selected_sub = self.sub_listbox.get(selection[0]).strip()
            self.add_log(f"Selected: {self.selected_sub}", "#60a5fa")

    def start_generation(self):
        if not self.selected_main:
            self.add_log("âŒ Please select a domain!", DANGER)
            return
        search = self.search_entry.get().replace("  e.g., IPL, OpenAI, Apple...", "")
        base = DOMAINS[self.selected_main].get(self.selected_sub, "")
        query = search if search else (base if base else self.selected_main)
        feed_url = f"https://news.google.com/rss/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"
        self.gen_btn.config(text="â³ WORKING...", bg="#64748b")
        self.add_log(f"â³ Fetching {self.selected_main}...", YELLOW)
        self.root.update()
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 8)]
        try:
            articles = run_weekly_pipeline(dates=dates, feeds=[feed_url])
            show_articles(self.article_box, self.add_log, articles)
            if articles:
                generate_news_pdf(articles, self.selected_main, self.selected_sub or "")
                self.open_latest_pdf()
                self.add_log(f"PDF generated ({len(articles)} articles)!", SUCCESS)
            else:
                self.add_log("No articles found.", YELLOW)
            self.gen_btn.config(text="âš¡  GENERATE PDF", bg=ACCENT)
        except Exception as e:
            self.add_log(f"âŒ Error: {str(e)[:40]}", DANGER)
            self.gen_btn.config(text="âš¡  GENERATE PDF", bg=ACCENT)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrendScopeUI(root)
    root.mainloop()



