t = open("main.py","r",encoding="utf-8").read()
q = chr(34)
lang_dict = "LANGUAGES = {"
lang_dict += chr(34) + "English" + chr(34) + ": " + chr(34) + "hl=en-US&gl=US&ceid=US:en" + chr(34) + ", "
lang_dict += chr(34) + "Hindi" + chr(34) + ": " + chr(34) + "hl=hi&gl=IN&ceid=IN:hi" + chr(34) + ", "
lang_dict += chr(34) + "Telugu" + chr(34) + ": " + chr(34) + "hl=te&gl=IN&ceid=IN:te" + chr(34) + ", "
lang_dict += chr(34) + "Tamil" + chr(34) + ": " + chr(34) + "hl=ta&gl=IN&ceid=IN:ta" + chr(34) + ", "
lang_dict += chr(34) + "Malayalam" + chr(34) + ": " + chr(34) + "hl=ml&gl=IN&ceid=IN:ml" + chr(34) + ", "
lang_dict += chr(34) + "Bengali" + chr(34) + ": " + chr(34) + "hl=bn&gl=IN&ceid=IN:bn" + chr(34) + ", "
lang_dict += chr(34) + "Kannada" + chr(34) + ": " + chr(34) + "hl=kn&gl=IN&ceid=IN:kn" + chr(34) + ", "
lang_dict += chr(34) + "Marathi" + chr(34) + ": " + chr(34) + "hl=mr&gl=IN&ceid=IN:mr" + chr(34)
lang_dict += "}"
t = t.replace("BG_DARK = " + chr(34) + "#0f172a" + chr(34), lang_dict + "\n\nBG_DARK = " + chr(34) + "#0f172a" + chr(34))
ui_label = "tk.Label(center_panel, text=" + chr(34) + "Language:" + chr(34) + ", font=(" + chr(34) + "Helvetica" + chr(34) + ", 10), bg=BG_PANEL, fg=TEXT_MAIN).pack(anchor=" + chr(34) + "w" + chr(34) + ", padx=20)"
ui_box = "self.lang_combo = ttk.Combobox(center_panel, values=list(LANGUAGES.keys()), state=" + chr(34) + "readonly" + chr(34) + ", font=(" + chr(34) + "Helvetica" + chr(34) + ", 11))\nself.lang_combo.pack(fill=" + chr(34) + "x" + chr(34) + ", padx=20, pady=(0, 15))\nself.lang_combo.set(" + chr(34) + "English" + chr(34) + ")"
t = t.replace("tk.Label(center_panel, text=" + chr(34) + "Deep Filter", ui_label + "\n" + ui_box + "\n        tk.Label(center_panel, text=" + chr(34) + "Deep Filter")
old_url = "https://news.google.com/rss/search?q=" + "{quote(query)}" + "&hl=en-US&gl=US&ceid=US:en"
new_url = "https://news.google.com/rss/search?q=" + "{quote(query)}" + "&{LANGUAGES.get(self.lang_combo.get(), " + chr(34) + "hl=en-US&gl=US&ceid=US:en" + chr(34) + ")}"
t = t.replace(old_url, new_url)
open("main.py","w",encoding="utf-8").write(t)
print("DONE")
