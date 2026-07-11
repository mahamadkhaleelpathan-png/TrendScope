t = open("templates/index.html","r",encoding="utf-8").read()
q = chr(39)
bad = " onerror=" + q + "this.style.display=" + q + q + q + " " + q + "}" + q + ">"
good = ""
t = t.replace(bad, good)
open("templates/index.html","w",encoding="utf-8").write(t)
print("FIXED")
