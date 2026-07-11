def open_pdf():
    import os, webbrowser, glob, tkinter.messagebox as mb
    try:
        pdfs = glob.glob("data/**/*.pdf", recursive=True)
        if not pdfs:
            mb.showinfo("No PDF", "No PDF files found!")
            return
        latest = max(pdfs, key=os.path.getctime)
        path = os.path.abspath(latest).replace(chr(92), "/")
        html = "<html><head><title>Digest</title><style>body{margin:0;background:#0f172a;font-family:sans-serif;display:flex;flex-direction:column;height:100vh}div{background:#1e293b;padding:15px 30px;display:flex;justify-content:space-between;align-items:center}h2{color:#f1f5f9;margin:0}a{background:#8b5cf6;color:white;padding:10px 25px;text-decoration:none;border-radius:8px;font-weight:bold}iframe{flex:1;border:none;width:100%}</style></head><body><div><h2>Synapse Weekly Digest</h2><a href='file:///" + path + "' download>Download PDF</a></div><iframe src='file:///" + path + "'></iframe></body></html>"
        hpath = os.path.join("data", "viewer.html")
        with open(hpath, "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open("file:///" + os.path.abspath(hpath).replace(chr(92), "/"))
    except Exception as e:
        mb.showerror("Error", str(e))
