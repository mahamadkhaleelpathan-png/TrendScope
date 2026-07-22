def open_pdf():
    import os, subprocess, tkinter.messagebox as mb

    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(PROJECT_DIR, "data")

    try:
        if not os.path.exists(DATA_DIR):
            mb.showinfo("No PDF", "No PDF files found!")
            return
        pdfs = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith('.pdf')]
        if not pdfs:
            mb.showinfo("No PDF", "No PDF files found!")
            return
        latest = max(pdfs, key=os.path.getctime)
        subprocess.Popen(["xdg-open", latest])
    except Exception as e:
        mb.showerror("Error", str(e))
