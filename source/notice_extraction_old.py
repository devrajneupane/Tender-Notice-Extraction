import cv2
import os
import fitz


MIN_WIDTH=500    #minimum width of the reactangle to be extracted
MIN_HEIGHT=500   #minimum height of the reactangle to be extracted
MAX_WIDTH=6000    #maximum width of the reactangle to be extracted
MAX_HEIGHT=6000     #maximum height of the reactangle to be extracted

try:
   os.mkdir("./Notices/")
except FileExistsError:
   pass


newspaper_collection=os.listdir("./Images/")
for newspaper in newspaper_collection:
   output_path="./Notices/"+newspaper+"/"
   try:
      os.mkdir(output_path)
   except FileExistsError:
      pass
   newspaper_pages=os.listdir("./Images/"+newspaper+"/")
   count=0
   for page in newspaper_pages:
      img=cv2.imread("./Images/"+newspaper+"/"+page)
      #convert RGB to grayscale
      img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   

      
      #BINARY_INV thresholding so that the rectangles are white and background is black
      ret, thresh = cv2.threshold(img_gray,190, 255, cv2.THRESH_BINARY_INV)   
      # canny=cv2.Canny(thresh,30,200)   #Edge detection
      contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      for contour in contours:
            x,y,w,h=cv2.boundingRect(contour)
            if w>=MIN_WIDTH and h>=MIN_HEIGHT and w<=MAX_WIDTH and h<=MAX_HEIGHT:
               count+=1
               # cv2.drawContours(img,contour,-1,(0,255,0),10)
               #cropping only the rectangle containing the notice
               cropped_image=img[y:y+h,x:x+w]               
               cv2.imwrite(output_path+"notice"+str(count)+".jpg", cropped_image)
      # cv2.imshow("contour", cv2.resize(img, (800,600)))
      # cv2.waitKey(0)