import cv2
import os
from pathlib import Path
import multiprocessing as mp
import numpy as np
import sys
import datetime

from log import Logger

THRESH_VALUE = 100   # Pixel value less than THRESH_VALUE is converted to white
                     # and greater than THRESH_VALUE is converted to black

EPSILON_FACTOR = 0.01   #default 0.01

MIN_WIDTH = 100  # minimum width of the reactangle to be extracted

MIN_HEIGHT = 100  # minimum height of the reactangle to be extracted

MAX_WIDTH = 6000  # maximum width of the reactangle to be extracted

MAX_HEIGHT = 6000  # maximum height of the reactangle to be extracted

#CPU_COUNT returns the no of threads available
#so that we can use all the available threads
#during the execution of the program
CPU_COUNT=mp.cpu_count()

def page_to_notice(path, newspaper, page, output_path,no_of_newspaper_pages):
   """
   Extract rectangular contour from image of each page of PDF
   path= current path of the file
   newspaper= name of the newspaper folder inside the Images folder
   page= name of the image file in the newspaper folder inside Images folder
   output_path= path of the subimage folder
   page_count= no of pages processed
   no_of_newspaper_pages= total no of pages in the newspaper folder
   """
   
   #Read the image of the page
   img = cv2.imread(str(path.parent.joinpath("Images", newspaper, page)))

   # convert RGB to grayscale
   img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   # BINARY_INV thresholding so that the rectangles are white and background is black
   ret, thresh = cv2.threshold(img_gray, THRESH_VALUE, 255, cv2.THRESH_BINARY_INV)

   # Find contours in the image
   contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   print(f"\t==>Extracting Notice from {newspaper[:-11]} page [%s/%s]" % (page.split("_pg_")[1].split(".")[0], no_of_newspaper_pages))

   count=0
   for contour in contours:
      # Find the area of contour
      rect_area = cv2.contourArea(contour)

      # Filter contours based on area
      if  rect_area < MIN_WIDTH * MIN_HEIGHT:
         continue

      #Approximate the contour curve with specified precision ie. EPSILON
      #More infohttps://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#ga0012a5fdaea70b8a9970165d98722b4c
      EPSILON= EPSILON_FACTOR * cv2.arcLength(contour, True)
      poly = cv2.approxPolyDP(contour,EPSILON, True)

      #Coordinates of the rectangular contour
      x, y, w, h = cv2.boundingRect(contour)

      # Filter contours based on width and height and no of sides
      if len(poly)==4 and w >= MIN_WIDTH and h >= MIN_HEIGHT and w <= MAX_WIDTH and h <= MAX_HEIGHT:
         count =count+1

         #Cropping the ROI
         cropped_image = img[y: y + h, x: x + w]
         # cv2.drawContours(img, contour_subimage, -1, (0,0,224), 10)
         # cv2.putText(img, "x= "+str(x)+" and y= "+str(y), (x,y-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
         filename = str(output_path.joinpath(page.split(".")[0] +"_id_"+str(count) + '.png'))
         cv2.imwrite(filename, cropped_image)
   # cv2.imwrite(filename, img)


def extract_notice():
   sys.stdout=Logger()

   print("\n========Extracting rectangular contour=======\n")
   path = Path(__file__).parent
   notice_path = path.parent.joinpath("subimage")

   if not notice_path.exists():
      os.mkdir(notice_path)

   try:
      newspaper_collection = os.listdir(path.parent.joinpath("Images"))
   except FileNotFoundError:
      print(f"==>\n'Images' folder not found in: \n{path.parent}\n")
      exit()

   if len(newspaper_collection)==0:
      print(f"==>\n'Images' folder is empty in: \n{path.parent}\n<==")
      exit()
 
   all_newspaper_images=[]

#Making a list of all the images present in the Images folder
#This is done to make multiprocessing more effictient
   for newspaper in newspaper_collection: 
      newspaper_path = path.parent.joinpath("Images", newspaper)
      newspaper_pages = sorted(os.listdir(newspaper_path))
      if len(newspaper_pages)==0:
         print(f"==>\n{newspaper} folder is empty in: \n{path.parent.joinpath('Images')}\n<==")
         continue
      no_of_newspaper_pages = len(newspaper_pages)
      for page in newspaper_pages:
         all_newspaper_images.append([page,newspaper,no_of_newspaper_pages])

   #Multiprocessing the execution of the program
   processs=[]
   newspaper_count = 0
   CPU_USED=0  
   page_count = 0

   for page,newspaper,no_of_newspaper_pages in all_newspaper_images:   
      newspaper_count += 1  
      print(f"Processing Newspaper: {newspaper} ===================[{newspaper_count}/{len(all_newspaper_images)}]")
      output_path = path.parent.joinpath("subimage", newspaper)

      if not path.parent.joinpath(output_path).exists():
         os.mkdir(output_path)

      page_count += 1
      CPU_USED+=1      #number of processes used so far

      #If the no of processes are less than CPU_COUNT, 
      # continue adding new processes
      if CPU_USED<=CPU_COUNT: 
         process=mp.Process(target=page_to_notice, args=(path,newspaper, page, output_path, no_of_newspaper_pages))
         processs.append(process)

      #If the no of processes are equal tto CPU_COUNT,
      #Or if no further process can be added,
      # then start the execution of the processes
      if CPU_USED==CPU_COUNT or page_count==len(all_newspaper_images):

         #Start the execution of the processes
         for process in processs:
            process.start()
         
         #Wait for the processes to finish
         #This is done to make sure that all the processes are finished
         #before moving to the next newspaper
         #After the processes are finished, it is terminated
         for process in processs:
            process.join()
            process.terminate()
         processs=[]
         CPU_USED=0

if __name__ == "__main__":
   sys.stdout=Logger(str(datetime.datetime.now()))
   extract_notice()
