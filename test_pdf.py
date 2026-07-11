import glob
pdfs = glob.glob("data/*.pdf")
print("Found PDFs:", len(pdfs))
if pdfs:
    print(pdfs)
pdfs2 = glob.glob("data/**/*.pdf", recursive=True)
print("Found with subfolders:", len(pdfs2))
if pdfs2:
    print(pdfs2)
