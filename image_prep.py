import cv2
import os

def createFilelist(mydir):
    Filelist=[]
    for root,dirs,files in os.walk(mydir): 
        for name in files:
            fullname=os.path.join(root,name)
            Filelist.append(fullname)
    return Filelist


myFilelist=createFilelist(r"D:\Programming\Python\Tender-Notice-Extraction\Datasets\0")

for img_dr in myFilelist[0:len(myFilelist)//2]:
    img=cv2.imread(img_dr)
    print(img.shape)

