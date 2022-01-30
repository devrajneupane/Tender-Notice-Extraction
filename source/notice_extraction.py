import cv2
import os
from pathlib import Path

THRESH_VALUE = 100
TUNING_FACTOR = 0.0001
MIN_WIDTH = 100  # minimum width of the reactangle to be extracted
MIN_HEIGHT = 100  # minimum height of the reactangle to be extracted
# MAX_ASPECT_RATIO=3
MAX_WIDTH = 6000  # maximum width of the reactangle to be extracted
MAX_HEIGHT = 6000  # maximum height of the reactangle to be extracted


def extract_notice():
   path = Path(__file__).parent
   notice_path = path.parent.joinpath("Notices")

   if not notice_path.exists():
      os.mkdir(notice_path)

   try:
      newspaper_collection = os.listdir(path.parent.joinpath("Images"))

   except FileNotFoundError:
      print("Image folder not found ")
      exit()

   no_of_newspapers = len(newspaper_collection)
   newspaper_count = 0

   for newspaper in newspaper_collection:
      newspaper_count += 1
      output_path = path.parent.joinpath("Notices", newspaper)

      if not path.parent.joinpath(output_path).exists():
         os.mkdir(output_path)

      print(f"Processing Newspaper: {newspaper} ===================[{newspaper_count}/{no_of_newspapers}]")
      newspaper_path = path.parent.joinpath("Images", newspaper)
      newspaper_pages = os.listdir(newspaper_path)
      count = 0
      page_count = 0
      for page in newspaper_pages:
         page_count += 1
         img = cv2.imread(str(newspaper_path.joinpath(page)))
         # convert RGB to grayscale
         img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

         # BINARY_INV thresholding so that the rectangles are white and background is black
         ret, thresh = cv2.threshold(img_gray, THRESH_VALUE, 255, cv2.THRESH_BINARY_INV)

         # canny=cv2.Canny(thresh,30,200)   #Edge detection
         contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
         print("\t==>Extracting Notice from page [%s/%s]" % (page_count, len(newspaper_pages)))
         for contour in contours:
            poly = cv2.approxPolyDP(contour, TUNING_FACTOR * cv2.arcLength(contour, True), True)
            x, y, w, h = cv2.boundingRect(contour)
            if len(poly) == 4 and w >= MIN_WIDTH and h >= MIN_HEIGHT and w <= MAX_WIDTH and h <= MAX_HEIGHT:
               count += 1
               cropped_image = img[y: y + h, x: x + w]
               filename = str(output_path.joinpath(page.split(".")[0] + "_" + str(count) + '.png'))
               cv2.imwrite(filename, cropped_image)


if __name__ == "__main__":
   extract_notice()
