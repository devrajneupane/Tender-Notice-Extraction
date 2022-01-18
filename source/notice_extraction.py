import cv2
import os
import fitz
import matplotlib.pyplot as plt
# print()

THRESH_VALUE=100
TUNING_FACTOR=0.001
MIN_WIDTH=100   #minimum width of the reactangle to be extracted
MIN_HEIGHT=100  #minimum height of the reactangle to be extracted
# MAX_ASPECT_RATIO=3
MAX_WIDTH=6000    #maximum width of the reactangle to be extracted
MAX_HEIGHT=6000     #maximum height of the reactangle to be extracted

def extract_notice():

   try:
      os.mkdir("./Notices/")
   except FileExistsError:
      pass

   try:
      newspaper_collection=os.listdir("./Images/")
   except FileNotFoundError:
      print("Image folder not found ")
      exit()
   no_of_newspapers=len(newspaper_collection)
   newspaper_count=0
   for newspaper in newspaper_collection:
      newspaper_count+=1
      output_path="./Notices/"+newspaper+"/"
      try:
         os.mkdir(output_path)
      except FileExistsError:
         pass
      print("Processing Newspaper: %s ===================[%s/%s]"%(newspaper,newspaper_count,no_of_newspapers))
      newspaper_pages=os.listdir("./Images/"+newspaper+"/")
      count=0
      page_count=0
      for page in newspaper_pages:
         page_count+=1
         img=cv2.imread("./Images/"+newspaper+"/"+page)
         #convert RGB to grayscale
         img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   


         
         #BINARY_INV thresholding so that the rectangles are white and background is black
         ret, thresh = cv2.threshold(img_gray,THRESH_VALUE, 255, cv2.THRESH_BINARY_INV)   
         

         # canny=cv2.Canny(thresh,30,200)   #Edge detection
         contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
         print("\t==>Extracting Notice from page [%s/%s]"%(page_count,len(newspaper_pages)))
         for contour in contours:
               poly=cv2.approxPolyDP(contour, TUNING_FACTOR*cv2.arcLength(contour, True), True)
               x,y,w,h=cv2.boundingRect(contour)
               if len(poly)==4 and w>=MIN_WIDTH and h>=MIN_HEIGHT and w<=MAX_WIDTH and h<=MAX_HEIGHT:
                  count+=1
                  # cv2.drawContours(img,contour,-1,(0,255,0),10)
                  #cropping only the rectangle containing the notice
                  # cv2.drawContours(img,[contour],0,(0,255,0),3)
                  cropped_image=img[y:y+h,x:x+w]        
                  
                  cv2.imwrite(output_path+"notice"+str(count)+".jpg", cropped_image)
      #    plt.imshow(img[:,:,::-1],cmap="viridis")
      #    plt.imshow(thresh[:,::-1],cmap="gray")
      #    plt.axis('off')
      #    plt.tight_layout()
      #    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
      #    mng=plt.get_current_fig_manager()
      #    mng.full_screen_toggle()
      #    plt.show()
      #    # break
      # break
         # os.remove("./Images/"+newspaper+"/"+page)
      # os.rmdir("./Images/"+newspaper)
   # os.rmdir("./Images/")
