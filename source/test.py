import fitz
h=list()
w=list()
doc = fitz.open("./source/file.pdf")
for i in range(len(doc)):
    for img in doc.getPageImageList(i):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        
        h.append(pix.height)
        w.append(pix.width)
        print("height , width = ", pix.height, pix.width)
        if pix.n < 5:       # this is GRAY or RGB
            pix.writePNG("p%s-%s.png" % (i, xref))
        else:               # CMYK: convert to RGB first
            pix1 = fitz.Pixmap(fitz.csRGB, pix)
            pix1.writePNG("p%s-%s.png" % (i, xref))
            pix1 = None
        pix = None
print("max_height = ", max(h))
print("min_height = ", min(h))
print("max_width = ", max(w))
print("min_width = ", min(w))