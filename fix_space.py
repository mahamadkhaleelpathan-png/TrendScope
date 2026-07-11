t = open("main.py","r",encoding="utf-8").read()
t = t.replace("tk.Label(center_panel, text=" + chr(34) + "Deep Filter", "        tk.Label(center_panel, text=" + chr(34) + "Deep Filter")
open("main.py","w",encoding="utf-8").write(t)
print("FIXED")
