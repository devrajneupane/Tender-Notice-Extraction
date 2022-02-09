import time
import image_extraction
import notice_extraction
from get_resources import get_resource
import filter_notices
import ocr
from datetime import date
from sql import sql_initialize, sql_query_date


def main():
    start_time = time.time()
    sql_initialize()
    # get pdf from websites and store in /Newspaper folder
    dat=date.today().strftime("%Y-%m-%d")
    temp=sql_query_date()
    if not temp:
        temp=temp[0].strftime("%Y-%m-%d")
        if temp==dat:
            print("bye bye")
            return
    

    get_resource()
    # read pdf form Newspapers folder
    # convert pdf to jpg
    image_extraction.extract_image()
    # extract notices from jpg
    notice_extraction.extract_notice()

    filter_notices.applyCNN()
    ocr.tender_filter()
    elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    print(f"Time Elapsed: {elapsed}")
    # print("Total elapsed time: ",end-start)

    # ocr.tender_filter()
    # fetch and check the notices using the model
    # publish the notices on the website


if __name__ == "__main__":
    main()