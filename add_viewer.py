q = chr(34)
t = open("main.py","r",encoding="utf-8").read()
ob = 'self.gen_btn.pack(fill=' + q + 'x' + q + ', padx=20, pady=(10, 0))'
nb = 'btn_row = tk.Frame(center_panel, bg=BG_PANEL)\n'
nb += '        btn_row.pack(fill=' + q + 'x' + q + ', padx=20, pady=(10, 5))\n'
nb += '        self.gen_btn = tk.Button(btn_row, text=' + q + 'GENERATE PDF' + q + ', font=(' + q + 'Helvetica' + q + ', 11, ' + q + 'bold' + q + '), bg=ACCENT, fg=' + q + 'white' + q + ', bd=0, pady=10, cursor=' + q + 'hand2' + q + ', command=self.start_generation)\n'
nb += '        self.gen_btn.pack(side=' + q + 'left' + q + ', expand=True, fill=' + q + 'x' + q + ', padx=(0,5))\n'
nb += '        self.pdf_btn = tk.Button(btn_row, text=' + q + 'OPEN PDF' + q + ', font=(' + q + 'Helvetica' + q + ', 11, ' + q + 'bold' + q + '), bg=' + q + '#334155' + q + ', fg=' + q + 'white' + q + ', bd=0, pady=10, cursor=' + q + 'hand2' + q + ', command=self.open_latest_pdf)\n'
nb += '        self.pdf_btn.pack(side=' + q + 'right' + q + ', expand=True, fill=' + q + 'x' + q + ', padx=(5,0))\n'
nb += '        tk.Label(center_panel, text=' + q + 'GENERATED ARTICLES' + q + ', font=(' + q + 'Helvetica' + q + ', 10, ' + q + 'bold' + q + '), bg=BG_PANEL, fg=TEXT_SUB).pack(anchor=' + q + 'w' + q + ', padx=20, pady=(10,2))\n'
nb += '        self.article_box = tk.Text(center_panel, font=(' + q + 'Helvetica' + q + ', 9), bg=' + q + '#0f172a' + q + ', fg=TEXT_MAIN, bd=0, highlightthickness=1, highlightcolor=ACCENT, state=' + q + 'disabled' + q + ', wrap=' + q + 'word' + q + ', cursor=' + q + 'arrow' + q + ')\n'
nb += '        self.article_box.pack(fill=' + q + 'both' + q + ', expand=True, padx=20, pady=(0,15))\n'
nb += '        self.article_box.tag_configure(' + q + 'title' + q + ', foreground=' + q + '#60a5fa' + q + ', font=(' + q + 'Helvetica' + q + ', 10, ' + q + 'bold' + q + '))\n'
nb += '        self.article_box.tag_configure(' + q + 'link' + q + ', foreground=' + q + '#facc15' + q + ')'
t = t.replace(ob, nb)
old_call = 'run_weekly_pipeline(dates=dates, feeds=[feed_url])'
new_call = 'articles = run_weekly_pipeline(dates=dates, feeds=[feed_url])\n            self.show_articles(articles)'
t = t.replace(old_call, new_call)
fn = '\n    def show_articles(self, articles):\n'
fn += '        self.article_box.config(state=' + q + 'normal' + q + ')\n'
fn += '        self.article_box.delete(' + q + '1.0' + q + ', tk.END)\n'
fn += '        for a in articles[:50]:\n'
fn += '            tt = a.get(' + q + 'title' + q + ',' + q + 'No Title' + q + ')\n'
fn += '            cc = a.get(' + q + 'content' + q + ',' + q + q + ')\n'
fn += '            if len(cc) > 120:\n'
fn += '                cc = cc[:120]\n'
fn += '            uu = a.get(' + q + 'url' + q + ',' + q + q + ')\n'
fn += '            self.article_box.insert(tk.END, tt + ' + q + '\\n' + q + ', ' + q + 'title' + q + ')\n'
fn += '            self.article_box.insert(tk.END, cc + ' + q + '...\n' + q + ')\n'
fn += '            self.article_box.insert(tk.END, uu + ' + q + '\\n' + q + ', ' + q + 'link' + q + ')\n'
fn += '            self.article_box.insert(tk.END, ' + q + '\\n' + q + ')\n'
fn += '        self.article_box.config(state=' + q + 'disabled' + q + ')\n'
fn += '        self.add_log(' + q + 'Showing articles.' + q + ', SUCCESS)\n'
t = t.replace('    def open_latest_pdf(self):', fn + '    def open_latest_pdf(self):')
open("main.py","w",encoding="utf-8").write(t)
print("DONE")
