import os
import fitz
try:
    os.mkdir("./Newspapers/")
except FileExistsError:
    pass

try:
    os.mkdir("./Images")
except FileExistsError:
    pass

newspapers=os.listdir("./Newspapers/")
for newspaper in newspapers:
    if newspaper.endswith(".pdf"):
        doc = fitz.open(os.path.join("./Newspapers/",newspaper))  
        try:
            output_path="./Images/"+newspaper[:-4]+"/"
            os.mkdir(output_path)
        except FileExistsError:
            pass          
        for i in range (0,doc.page_count):
            page=doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(5,5))
            output = "page"+str(i)+".jpg"
            pix.save((output_path+output))
        doc.close()