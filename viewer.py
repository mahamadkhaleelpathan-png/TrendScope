import os
import subprocess

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "data")


def _clean(text):
    if not text:
        return ""
    return text.encode("latin-1", "replace").decode("latin-1")


def generate_news_pdf(articles, domain="", subtopic=""):
    from fpdf import FPDF

    os.makedirs(DATA_DIR, exist_ok=True)

    class NewsPDF(FPDF):
        def header(self):
            if self.page_no() > 1:
                self.set_font("Helvetica", "I", 8)
                self.set_text_color(100, 100, 100)
                self.cell(0, 8, _clean(f"TrendScope Digest - {domain or 'All'} > {subtopic or 'All'}"), align="C")
                self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    pdf = NewsPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(25, 35, 75)
    pdf.cell(0, 12, "TrendScope News Digest", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(100, 100, 120)
    label = _clean(f"{domain}" + (f" > {subtopic}" if subtopic else ""))
    pdf.cell(0, 8, label, align="C", new_x="LMARGIN", new_y="NEXT")
    from datetime import datetime
    pdf.cell(0, 8, datetime.now().strftime("%B %d, %Y"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    for i, a in enumerate(articles[:50], 1):
        title = _clean(a.get("title", "No Title"))
        author = _clean(a.get("author", ""))
        date = _clean(a.get("date", ""))
        content = _clean(a.get("content", ""))
        url = a.get("url", "")

        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(25, 35, 75)
        pdf.multi_cell(0, 7, f"{i}. {title}")
        pdf.ln(1)

        meta = ""
        if author:
            meta += f"Source: {author}"
        if date:
            meta += f"  |  Date: {date}"
        if meta:
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(100, 100, 120)
            pdf.cell(0, 5, meta, new_x="LMARGIN", new_y="NEXT")

        if content:
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 5.5, content[:500] + ("..." if len(content) > 500 else ""))
            pdf.ln(1)

        if url:
            safe_url = url.encode("ascii", "replace").decode("ascii")
            pdf.set_font("Helvetica", "U", 9)
            pdf.set_text_color(80, 80, 200)
            pdf.cell(0, 5, safe_url, link=safe_url, new_x="LMARGIN", new_y="NEXT")

        pdf.set_draw_color(200, 210, 230)
        pdf.line(pdf.l_margin, pdf.get_y() + 3, pdf.w - pdf.r_margin, pdf.get_y() + 3)
        pdf.ln(6)

    path = os.path.join(DATA_DIR, "news_digest.pdf")
    pdf.output(path)
    return path


def show_articles(box, log_fn, articles):
    box.config(state="normal")
    box.delete("1.0", "end")
    urls = []
    for a in articles[:50]:
        tt = a.get("title", "No Title")
        cc = a.get("content", "")
        if len(cc) > 120:
            cc = cc[:120]
        uu = a.get("url", "")
        box.insert("end", tt + "\n", "title")
        box.insert("end", cc + "...\n")
        if uu:
            box.insert("end", "Read More\n", "link")
            urls.append(uu)
        else:
            urls.append("")
        box.insert("end", "\n")
    box.config(state="disabled")

    def on_link_click(event):
        index = box.index(f"@{event.x},{event.y}")
        tags = box.tag_names(index)
        if "link" in tags:
            line = int(index.split(".")[0])
            link_count = 0
            for i in range(1, line + 1):
                line_idx = box.index(f"{i}.0")
                line_end = box.index(f"{i}.end")
                text = box.get(line_idx, line_end).strip()
                if text == "Read More":
                    link_count += 1
            if 0 < link_count <= len(urls) and urls[link_count - 1]:
                subprocess.Popen(["xdg-open", urls[link_count - 1]])

    box.tag_bind("link", "<Button-1>", on_link_click)
    box.tag_configure("link", foreground="#60a5fa", underline=True)
    log_fn("Showing articles. Click 'Read More' to open.", "#22c55e")
