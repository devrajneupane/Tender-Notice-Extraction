import cv2
import os
from pathlib import Path
import multiprocessing as mp
import sys
from log import Logger

THRESH_VALUE = 100   # Pixel value less than THRESH_VALUE is converted to white
                     # and greater than THRESH_VALUE is converted to black

RECOMPUTE_WIDTH= 1800    #If the width and height of the contour
RECOMPUTE_HEIGHT= 2000   # is greater than RECOMPUTE_WIDTH, RECOMPUTE_HEIGHT
                         # then the contour is recomputed
                         # to search for inner rectangular contour


EPSILON_FACTOR = 0.01   #default 0.01

MIN_WIDTH = 100  # minimum width of the reactangle to be extracted

MIN_HEIGHT = 100  # minimum height of the reactangle to be extracted

MAX_WIDTH = 6000  # maximum width of the reactangle to be extracted

MAX_HEIGHT = 6000  # maximum height of the reactangle to be extracted

#CPU_COUNT returns the no of threads available
#so that we can use all the available threads
#during the execution of the program
CPU_COUNT=mp.cpu_count()


def same_contour(c1,c2):
   if c1.shape != c2.shape:
      return False
   
   row=c1.shape[0]
   count=0
   for j in range (0,row):
      if c1[j][0][0] == c2[j][0][0]:
         count +=1

      if c1[j][0][1] == c2[j][0][1]:
         count +=1

      # print(f"count={count} and row={row}")
      if count==2*row:
         return True

def find_ind(contour,contours,h):

   i=0
   for c in contours:
      # val=cv2.matchShapes(c, contour,1,0.0)
      # if val==0:
      #    break
      # i=i+1
      # print("i=",i)
      # print("c.shape=",c.shape)
      # print("contour.shape=",contour.shape)
      # print("c=",c)
      # print("contour=",contour)

      if c.shape != contour.shape:
         i=i+1
         continue
      
      row=c.shape[0]
      count=0
      for j in range (0,row):
         if c[j][0][0] == contour[j][0][0]:
            count +=1

         if c[j][0][1] == contour[j][0][1]:
            count +=1

      # print(f"count={count} and row={row}")
      if count==2*row:
         # print("index=",i , "hier of i=",h[0][i])
         return i
      else:
         i=i+1
              


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
   sys.stdout=Logger()
   
   #Read the image of the page
   img = cv2.imread(str(path.parent.joinpath("Images", newspaper, page)))

   # convert RGB to grayscale
   img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   # BINARY_INV thresholding so that the rectangles are white and background is black
   ret, thresh = cv2.threshold(img_gray, THRESH_VALUE, 255, cv2.THRESH_BINARY_INV)

   # Find contours in the image
   contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   print(f"\t==>Extracting Notice from {newspaper[:-11]} page [%s/%s]" % (page.split("_pg_")[1].split(".")[0], no_of_newspaper_pages))

   count=0
   


   for contour , hier in zip(contours, hierarchy[0]):

      #Only iterate over the outer contours
      #Hierarchy of a contour is in 
      #[Next, Previous, First_Child, Parent] format
      #For the contour to be outer contour,
      #it should not have parent
      #i.e Parent should be -1
      if not hier[3] == -1:
         continue

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
      if len(poly)==4  and w >= MIN_WIDTH and h >= MIN_HEIGHT and w <= MAX_WIDTH and h <= MAX_HEIGHT:
         count =count+1
         round_complete=0

         if (w>=RECOMPUTE_WIDTH and h>=RECOMPUTE_HEIGHT):
            while (w>=RECOMPUTE_WIDTH and h>=RECOMPUTE_HEIGHT):
               if hier[2] == -1 :
                  break
               hier = hierarchy[0][hier[2]]
               contour=contours[hier[2]]
               x, y, w, h = cv2.boundingRect(contour)
               
            hier=hierarchy[0][find_ind(contour, contours,hierarchy)]
               
            if hier[0] == -1 or hier[1] == -1:
               round_complete+=1
            EPSILON= EPSILON_FACTOR * cv2.arcLength(contour, True)
            poly = cv2.approxPolyDP(contour,EPSILON, True)

            #Coordinates of the rectangular contour
            x, y, w, h = cv2.boundingRect(contour)

            # Filter contours based on width and height and no of sides
            if len(poly)==4  and w >= MIN_WIDTH and h >= MIN_HEIGHT and w <= MAX_WIDTH and h <= MAX_HEIGHT:
               count =count+1
               cropped_image = img[y: y + h, x: x + w]
               filename = str(output_path.joinpath(page.split(".")[0] +"_id_"+str(count) + '.png'))
               cv2.imwrite(filename, cropped_image)
               
               # cv2.drawContours(img, contour, -1, (0,0,224), 10)
               # cv2.putText(img, "x= "+str(x)+" and y= "+str(y)+"hier="+str(hier), (x,y-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
               # print("hir",hier)
               # print("checkpoint 1")
            
            run=True
            org_contour=contour
            while run:
               #Recompute the contour with
               if hier[0] == -1:
                  break
               contour=contours[hier[0]]
               if same_contour(contour, org_contour):
                  break

               EPSILON= EPSILON_FACTOR * cv2.arcLength(contour, True)
               poly = cv2.approxPolyDP(contour,EPSILON, True)

               #Coordinates of the rectangular contour
               x, y, w, h = cv2.boundingRect(contour)

               # Filter contours based on width and height and no of sides
               if len(poly)==4  and w >= MIN_WIDTH and h >= MIN_HEIGHT and w <= MAX_WIDTH and h <= MAX_HEIGHT:
                  count =count+1
                  cropped_image = img[y: y + h, x: x + w]
                  filename = str(output_path.joinpath(page.split(".")[0] +"_id_"+str(count) + '.png'))
                  cv2.imwrite(filename, cropped_image)
                  # cv2.drawContours(img, contour, -1, (0,0,224), 10)
                  # cv2.putText(img, "x= "+str(x)+" and y= "+str(y)+"hier="+str(hier), (x,y-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
                  # print("hir",hier)
                  # print("checkpoint 2")
               hier=hierarchy[0][find_ind(contour, contours,hierarchy)]
               if hier[0] == -1 or hier[1] == -1:
                  round_complete+=1
               if round_complete==2:      #Iterating through all the interior rectangles,
                                          #for the loop to go through all the rectanges
                                          #it must encounter one NEXT = -1 and one PREVIOUS = -1
                  run=False 
                  
         else:
            #Cropping the ROI
            cropped_image = img[y: y + h, x: x + w]
            # cv2.drawContours(img, contour, -1, (0,0,224), 10)
            # cv2.putText(img, "x= "+str(x)+" and y= "+str(y)+"hier="+str(hier), (x,y-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
            filename = str(output_path.joinpath(page.split(".")[0] +"_id_"+str(count) + '.png'))
            cv2.imwrite(filename, cropped_image)
   # cv2.imwrite("filename.png", img)


def page_to_notice1(path, newspaper, page, output_path,no_of_newspaper_pages):
   """
   Extract rectangular contour from image of each page of PDF
   path= current path of the file
   newspaper= name of the newspaper folder inside the Images folder
   page= name of the image file in the newspaper folder inside Images folder
   output_path= path of the subimage folder
   page_count= no of pages processed
   no_of_newspaper_pages= total no of pages in the newspaper folder
   """
   sys.stdout=Logger()
   
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
   for contour ,hr in zip(contours,hierarchy[0]):
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
         # cv2.drawContours(img, contour, -1, (0,0,224), 10)
         # cv2.putText(img, "x= "+str(x)+" and y= "+str(y)+" hr= "+str(hr), (x,y-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (13,7,135), 3)
         filename = str(output_path.joinpath(page.split(".")[0] +"_id_"+str(count)+ '.png'))
         cv2.imwrite(filename, cropped_image)
   # cv2.imwrite(filename, img)


def extract_notice():
   sys.stdout=Logger()
   print("\n========Extracting rectangular contour=======\n")
   path = Path(sys.path[0])
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
   sys.stdout=Logger(datetime.datetime.now())
   extract_notice()
