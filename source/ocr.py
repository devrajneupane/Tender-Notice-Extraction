import pytesseract as tess
import cv2
import matplotlib.pyplot as plt
import os
print()
try:
    dicx=open("dict.txt","r")
except FileNotFoundError:
    print("dict.txt not found")
    exit()
    
dic=dicx.read().lower().splitlines()
dicx.close()

def is_notice(img):
    """ 
    img in grayscale format for better performance
    """
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
