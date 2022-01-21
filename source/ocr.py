import pytesseract as tess
tess.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import cv2
import matplotlib.pyplot as plt
import os
print("helo")
try:
    dicx=open("dict.txt","r", encoding="utf-8")
except FileNotFoundError:
    print("dict.txt not found")
    exit()
# print(dicx.read())
dic=dicx.read().lower().splitlines()
dicx.close()
# print(dic[3]=="bids")
def is_notice(img):
    """ 
    img in grayscale format for better performance
    """
    strike = 0
    text=tess.image_to_data(img,lang="eng+nep",timeout=100)
    for x,b in enumerate(text.splitlines()):
        if x !=0:
            b=b.split()
            if len(b)==12:
                b[11]=b[11].lower()
                s1=set(dic)
                s2=set(b)
                res=s1.intersection(s2)
                if (len(res) !=0):
                    strike+=1
    if strike>=1:
        return True
    else:
        return False

if __name__ == '__main__':
    path = r"D:\Programming\Python\Tender-Notice-Extraction\Notices\1"
    imdir = os.listdir(path)
    for i in imdir:
        fp = path + f"\{i}"
        res = is_notice(cv2.imread(fp,0))
        print(fp, res)