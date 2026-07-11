t = open("main.py","r",encoding="utf-8").read()
old = "tk.Label(center_panel, text=" + chr(34) + "Deep Filter"
new = "        tk.Label(center_panel, text=" + chr(34) + "Deep Filter"
t = t.replace(old, new)
old2 = "self.lang_combo = ttk.Combobox"
new2 = "        self.lang_combo = ttk.Combobox"
t = t.replace(old2, new2)
open("main.py","w",encoding="utf-8").write(t)
print("FIXED")
