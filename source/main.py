import time
import image_extraction
import notice_extraction
from get_resources import get_resource
import filter_notices
import ocr
from datetime import date


def main():
    start_time = time.time()
    # get pdf from websites and store in /Newspaper folder
    date=date.today()
    

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