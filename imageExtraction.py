import fitz

pdffile = "/media/gamedisk/study_materials/6th semester/minor project/Tender-Notice-extraction-from-E-papers-using-AI-/openCV/test_pdf.pdf"
doc = fitz.open(pdffile)
page = doc.load_page(len(doc))
pix = page.get_pixmap()
output = "outfile.png"
pix.save(output)




