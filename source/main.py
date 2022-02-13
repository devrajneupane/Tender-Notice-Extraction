import datetime
import sys
import time
import image_extraction
import notice_extraction
import get_resources
import filter_notices
import ocr
from pathlib import Path
import os
from datetime import date
from sql import sql_initialize, sql_query_date
import googledrive

def main():
    path = Path(__file__).parent
    sql_initialize()
    start_time = time.time()
    #Clean Unwanted Folders
    ocr.clean_folders()
    
    dat=date.today().strftime("%Y-%m-%d")
    temp=sql_query_date()

    #If the current date is present in the database then terminate the program
    if temp:
        temp=temp[0].strftime("%Y-%m-%d")
        if temp==dat:
            print("#######--SQL DATABASE ALREADY UPDATED--#######")
            return
    
    # get pdf from websites and store in /Newspaper folder
    get_resources.get_resource()

    # read pdf form Newspapers folder
    # convert pdf to jpg
    image_extraction.extract_image()

    # extract rectangular notices from jpg
    notice_extraction.extract_notice()

    #Apply Xception model to detect if the image looks like tender
    filter_notices.applyCNN()

    #Apply OCR to the extracted notices to detect if the notice is tender
    ocr.tender_filter()

    googledrive.upload_to_google_drive()

    #Clean Unwanted Folders
    ocr.clean_folders()

    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    print(f"Time Elapsed: {elapsed}")



if __name__ == "__main__":
    main()