# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import os
import cv2
# import tensorflow as tf
# from tensorflow import keras
import fitz
import image_extraction
import notice_extraction
import ocr
import filter_notices
import timeit
import time

def main():
    # get pdf from websites and store in /Newspaper folder
    # read pdf form Newspapers folder
    # convert pdf to jpg
    start_time=time.time()
    image_extraction.extract_image()
    # extract notices from jpg
    notice_extraction.extract_notice()
  
    # filter_notices.applyCNN()
    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    print(f"Time Elapsed: {elapsed}")
    # print("Total elapsed time: ",end-start)
    
    # ocr.tender_filter()
    # fetch and check the notices using the model
    # publish the notices on the website

    pass


if __name__ == "__main__":
    main()
