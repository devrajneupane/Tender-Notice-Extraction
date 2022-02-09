import cv2
import os
from pathlib import Path
import multiprocessing as mp

THRESH_VALUE = 100
TUNING_FACTOR = 0.01   #default 0.001
MIN_WIDTH = 100  # minimum width of the reactangle to be extracted
MIN_HEIGHT = 100  # minimum height of the reactangle to be extracted
# MAX_ASPECT_RATIO=3
MAX_WIDTH = 6000  # maximum width of the reactangle to be extracted
MAX_HEIGHT = 6000  # maximum height of the reactangle to be extracted
CPU_COUNT=mp.cpu_count()

var_count=1
def page_to_notice(path, newspaper, page, output_path, count, page_count,no_of_newspaper_pages):
   input_path = path.parent.joinpath("Images")
   open_img=str( input_path.joinpath(newspaper, page))
   img = cv2.imread(open_img)
   # convert RGB to grayscale
   img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   # BINARY_INV thresholding so that the rectangles are white and background is black
   ret, thresh = cv2.threshold(img_gray, THRESH_VALUE, 255, cv2.THRESH_BINARY_INV)

   contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX)
   print("\t==>Extracting Notice from page [%s/%s]" % (page_count, no_of_newspaper_pages))
   contour_subimage=list()
   for contour in contours:
      poly = cv2.approxPolyDP(contour, TUNING_FACTOR * cv2.arcLength(contour, False), False)
      x, y, w, h = cv2.boundingRect(contour)
      if len(poly)==4 and w >= MIN_WIDTH and h >= MIN_HEIGHT and w <= MAX_WIDTH and h <= MAX_HEIGHT:
         contour_subimage.append(contour)
   i=0
   for contour_subimage_ in contour_subimage:
      nested=False
      x,y,w,h = cv2.boundingRect(contour_subimage_)
      for j in range(len(contour_subimage)):
         if i==j:
            continue
         x_o, y_o, w_o, h_o = cv2.boundingRect(contour_subimage[j])
         TOLORENCE=20
         if (abs(x_o-x)<=TOLORENCE or abs(x_o<x+w)<=TOLORENCE or abs(y_o-y)<=TOLORENCE or abs(y_o-y+h)<=TOLORENCE):
            nested=True
            break
      
      if not nested:
         count =count+1
         # cropped_image = img[y: y + h, x: x + w]
         cv2.drawContours(img, contour_subimage, -1, (0,0,224), 10)
         cv2.putText(img, "x= "+str(x)+" and y= "+str(y), (x,y-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
         filename = str(output_path.joinpath(page.split(".")[0] +"_id_"+str(count) + '.png'))
         # cv2.imwrite(filename, cropped_image)
   
      i=i+1
   cv2.imwrite(filename, img)

def extract_notice():
   path = Path(__file__).parent
   notice_path = path.parent.joinpath("subimage")

   if not notice_path.exists():
      os.mkdir(notice_path)

   try:
      newspaper_collection = os.listdir(path.parent.joinpath("Images"))

   except FileNotFoundError:
      print("Image folder not found ")
      exit()

   no_of_newspapers = len(newspaper_collection)
   newspaper_count = 0

   all_newspaper_images=[]
   for newspaper in newspaper_collection:
      newspaper_count += 1
      print(f"Processing Newspaper: {newspaper} ===================[{newspaper_count}/{no_of_newspapers}]")
      newspaper_path = path.parent.joinpath("Images", newspaper)
      newspaper_pages = sorted(os.listdir(newspaper_path))
      
      for page in newspaper_pages:
         all_newspaper_images.append([page,newspaper])

   processs=[]
   CPU_USED=0  
   count = 0
   page_count = 0
   for page,newspaper in all_newspaper_images:     
 
      output_path = path.parent.joinpath("subimage", newspaper)

      if not path.parent.joinpath(output_path).exists():
         os.mkdir(output_path)
      page_count += 1
      CPU_USED+=1                    
      if CPU_USED<=CPU_COUNT: 
         process=mp.Process(target=page_to_notice, args=(path,newspaper, page, output_path, count, page_count,len(all_newspaper_images)))
         processs.append(process)
         print("starting process : %s" % process)
      if CPU_USED==CPU_COUNT or page_count==len(all_newspaper_images):
         for process in processs:
            process.start()
         for process in processs:
            process.join()
            process.terminate()
         processs=[]
         CPU_USED=0
         print("One iteration completed")

         
         


if __name__ == "__main__":
   extract_notice()
