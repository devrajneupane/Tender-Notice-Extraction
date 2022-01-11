import cv2
import os
import fitz

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
      img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
      ROI_AREA=1000000
      ret, thresh = cv2.threshold(img_gray,190, 255, cv2.THRESH_BINARY_INV)
      canny=cv2.Canny(thresh,30,200)
      contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      for contour in contours:
            x,y,w,h=cv2.boundingRect(contour)
            if cv2.contourArea(contour)>=ROI_AREA:
               count+=1
            #   cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
               cropped_image=img[y:y+h,x:x+w]
               
               cv2.imwrite(output_path+"notice"+str(count)+".jpg", cropped_image)
      # cv2.imshow("before",cv2.resize(img,(800,600)))
      # cv2.waitKey(0)

   

              
# img=cv2.imread("./openCV/outfile2.jpg")
# img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# ROI_AREA=1000000
# ret, thresh = cv2.threshold(img_gray,190, 255, cv2.THRESH_BINARY_INV)
# canny=cv2.Canny(thresh,30,200)
# contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# for contour in contours:
#     x,y,w,h=cv2.boundingRect(contour)
#     if cv2.contourArea(contour)>=ROI_AREA:
#         cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
#         cropped_image=img[y:y+h,x:x+w]
#         cv2.imwrite("notice.jpg", cropped_image)
# cv2.imshow("before",cv2.resize(img,(800,600)))
# cv2.waitKey(0)

