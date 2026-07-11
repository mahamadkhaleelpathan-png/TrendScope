def show_articles(box, log_fn, articles):
    box.config(state="normal")
    box.delete("1.0", "end")
    for a in articles[:50]:
        tt = a.get("title", "No Title")
        cc = a.get("content", "")
        if len(cc) > 120:
            cc = cc[:120]
        uu = a.get("url", "")
        box.insert("end", tt + "\n", "title")
        box.insert("end", cc + "...\n")
        box.insert("end", uu + "\n", "link")
        box.insert("end", "\n")
    box.config(state="disabled")
    log_fn("Showing articles.", "#22c55e")
