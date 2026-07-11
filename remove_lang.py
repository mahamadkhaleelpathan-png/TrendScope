t = open("main.py","r",encoding="utf-8").read()
q = chr(34)
# Remove language label
t = t.replace("tk.Label(center_panel, text=" + q + "Language:" + q + ", font=(" + q + "Helvetica" + q + ", 10), bg=BG_PANEL, fg=TEXT_MAIN).pack(anchor=" + q + "w" + q + ", padx=20)" + "\n        ", "")
# Remove language combobox
t = t.replace("        self.lang_combo = ttk.Combobox(center_panel, values=list(LANGUAGES.keys()), state=" + q + "readonly" + q + ", font=(" + q + "Helvetica" + q + ", 11))\n        self.lang_combo.pack(fill=" + q + "x" + q + ", padx=20, pady=(0, 15))\n        self.lang_combo.set(" + q + "English" + q + ")" + "\n        ", "")
# Remove LANGUAGES dict
lines = t.split("\n")
new_lines = []
skip = False
for line in lines:
    if "LANGUAGES = {" in line:
        skip = True
    if skip and "}" in line and "BG_DARK" not in line:
        skip = False
        continue
    if not skip:
        new_lines.append(line)
t = "\n".join(new_lines)
# Lock URL to English
old_url = "https://news.google.com/rss/search?q=" + "{quote(query)}" + "&{LANGUAGES.get(self.lang_combo.get(), " + q + "hl=en-US&gl=US&ceid=US:en" + q + ")}"
new_url = "https://news.google.com/rss/search?q=" + "{quote(query)}" + "&hl=en-US&gl=US&ceid=US:en"
t = t.replace(old_url, new_url)
# Remove ttk import if not used elsewhere
t = t.replace("from tkinter import ttk\n", "")
open("main.py","w",encoding="utf-8").write(t)
print("DONE")
