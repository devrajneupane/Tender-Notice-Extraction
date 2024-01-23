import sys
import time
import datetime
import ocr
from log import Logger
from sql import sql_query_info
from pathlib import Path

sys.stdout = Logger(datetime.datetime.now())


def main():
    start_time = time.time()
    # Clean Unwanted Folders
    ocr.clean_folders()
    today = datetime.datetime.now()
    latest_date_from_database, exist = sql_query_info()

    # If the current date is present in the database then terminate the program
    if latest_date_from_database:
        if today.strftime("%Y-%m-%d") == latest_date_from_database[0].strftime("%Y-%m-%d"):
            if (today.hour < 11) or exist:
                sys.exit("#######--SQL DATABASE ALREADY UPDATED--#######")

    import get_resources
    import filter_notices
    import image_extraction
    import notice_extraction
    # import googledrive

    # get pdf from websites and store in /Newspaper folder
    get_resources.get_resource()

    # read pdf form Newspapers folder
    # convert pdf to jpg
    image_extraction.extract_image()

    # extract rectangular notices from jpg
    notice_extraction.extract_notice()

    # Apply Xception model to detect if the image looks like tender
    filter_notices.applyCNN()

    # Apply OCR to the extracted notices to detect if the notice is tender
    ocr.tender_filter()

    # googledrive.upload_to_google_drive()

    # Clean Unwanted Folders
    ocr.clean_folders()

    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    print(f"Time Elapsed: {elapsed}")


if __name__ == "__main__":
    main()
