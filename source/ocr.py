import pytesseract as tess
import cv2
import matplotlib.pyplot as plt
import os


dicx=open("dict.txt","r")
dic=dicx.read().lower().splitlines()
dicx.close()

def ocr(img):
        text=tess.image_to_data(img,lang="eng+nep",timeout=100)
        return text

img_list=os.listdir("./Notices/")

for i in img_list:    
    strike=0
    image=cv2.imread("./Notices/"+i,0)
    # _,thresh=cv2.threshold(image,100,255,cv2.THRESH_BINARY_INV)
    # plt.imshow(image,cmap="gray")
    # plt.axis('off')
    # plt.tight_layout()
    # plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    # mng=plt.get_current_fig_manager()
    # mng.full_screen_toggle()
    # plt.show()
    text=ocr(image)
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
        print (f"{i} is a tender")
    else:
        print (f"{i} is not a tender")

