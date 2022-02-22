import os
import sys
import shutil
from pathlib import Path
import multiprocessing as mp
import cv2
import numpy as np
import pytesseract as tess
from dotenv import dotenv_values
from sql import sql_insert
from log import Logger

sys.stdout=Logger()

# CPU_COUNT returns the no of threads available
# so that we can use all the available threads
# during the execution of the program
CPU_COUNT = mp.cpu_count()
path = Path(sys.path[0])
website_root_folder = path.parent.parent

dir_lst = os.listdir(path)
if ".env" not in dir_lst:
    print(f"==>\n.env file not found in: \n{path}\n<==")
    exit()
env_path = path.joinpath(".env")

if sys.platform == "win32":
    try:
        tesseract_exec = dotenv_values(env_path)["TESSERACT_EXECUTABLE"]
    except KeyError:
        print("TESSERACT_EXECUTABLE not found in .env file")
        exit()
    tess.pytesseract.tesseract_cmd = tesseract_exec


def remove_duplicate_img():
    """
    This function removes the duplicate images present in the Notices folder
    It simply compares the image matrix of the image
    If the matrix is same, it is removed
    """
    sys.stdout=Logger()
    newspaper_lst = os.listdir(path.parent.joinpath("Notices"))
    for newspaper in newspaper_lst:
        img_lst = os.listdir(path.parent.joinpath("Notices", newspaper))
        for img in img_lst:
            org_img = np.array(cv2.imread(str(path.parent.joinpath("Notices", newspaper, img)), 0))
            for img2 in img_lst:
                if img == img2:
                    continue
                else:
                    dup_img = np.array(cv2.imread(str(path.parent.joinpath("Notices", newspaper, img2)), 0))
                    if not org_img.shape == dup_img.shape:
                        continue
                    if np.array_equal(org_img, dup_img):
                        os.remove(str(path.parent.joinpath("Notices", newspaper, img2)))
                        img_lst.remove(img2)
                        print(f"\t\t==> {img} is same as{img2}, so {img2} is removed")


def clean_folders():
    """
    This function removes the folders which are not required
    Folder removed are:
    1) ./Newspapers
    2) ./Images
    3) ./Notices
    4) ./notNotices
    5) ./notTender
    6) ./subimage
    """
    sys.stdout=Logger()
    dirs = ['Newspapers', 'Images', 'Notices', 'notNotices', 'notTender', 'subimage']

    for directory in dirs:
        tmp_dir = path.parent.joinpath(directory)
        if os.path.exists(tmp_dir):
            try:
                shutil.rmtree(tmp_dir)
            except:
                pass


def is_tender(folder, img, dic):
    """
    Applies OCR to the <img> present in <folder> and
    checks for keyword in the image which is present in dict.txt
    and if found, it moves the image to Tender folder
    """
    sys.stdout=Logger()
    image = cv2.imread(str(path.parent.joinpath("Notices", folder, img)), 0)
    strike = 0
    text = tess.image_to_data(image, lang="eng+nep", timeout=240)
    for x, b in enumerate(text.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                b[11] = b[11].lower()
                s1 = set(dic)
                s2 = set(b)

                # Find the common word between the dictionary and the image
                res = s1.intersection(s2)

                # If the common word is found, strike is incremented
                if len(res) != 0:
                    strike += 1
                    print("\t\tStrike word: ", res)

    date = folder[-10:]

    # If strike is greater than 0, it means that the image is tender
    if strike >= 1:

        try:
            os.mkdir(website_root_folder.joinpath("media", "Tender", date))

        except FileExistsError:
            pass
        try:
            os.mkdir(website_root_folder.joinpath("media", "Tender", date, folder[:-11]))
        except FileExistsError:
            pass

        cv2.imwrite(str(website_root_folder.joinpath("media", "Tender", date, folder[:-11], img)), image)

        # Insert the information regarding tender into the database
        print(f"\t\t==> {img} is Tender")
        sql_insert(img.split("_id_")[1].split('.')[0], date, folder[:-11], img.split("_pg_")[1].split("_id")[0], "Tender/" + date + "/" + folder[:-11] + "/" + img)

    else:
        try:
            os.mkdir(path.parent.joinpath("notTender", date))

        except FileExistsError:
            pass
        try:
            os.mkdir(path.parent.joinpath("notTender", date, folder[:-11]))
        except FileExistsError:
            pass
        cv2.imwrite(str(path.parent.joinpath("notTender", date, folder[:-11], img)), image)
        print(f"\t\t==> {img} is not Tender")


def tender_filter():
    sys.stdout=Logger()
    print("\n========Applying OCR for confirmation=======\n")

    # load the dictionary file
    remove_duplicate_img()

    try:
        dicx = open(path.parent.joinpath("dict.txt"), "r", encoding="utf-8")
    except FileNotFoundError:
        print(f"==>'dict.txt' not found in: \n{path.parent}\n<==")
        exit()

    try:
        os.mkdir(website_root_folder.joinpath("media"))
    except FileExistsError:
        pass

    try:
        os.mkdir(website_root_folder.joinpath("media", "Tender"))
    except FileExistsError:
        pass

    try:
        os.mkdir(path.parent.joinpath("notTender"))
    except FileExistsError:
        pass

    dic = dicx.read().lower().splitlines()

    try:
        folder_list = os.listdir(path.parent.joinpath("Notices"))
    except FileNotFoundError:
        print(f"==>'Notices' folder not found in: \n{path.parent}\n<==")
        exit()

    if len(folder_list) == 0:
        print(f"==>\n'Notices' folder is empty in: \n{path.parent}<==")
        exit()
    folder_count = 0

    for folder in folder_list:
        folder_count += 1
        print(f"Processing Newspaper: {folder}=====================[{folder_count}/{len(folder_list)}]")

        # multiprocessing the execution of the program
        img_list = os.listdir(path.parent.joinpath("Notices", folder))
        if len(img_list) == 0:
            print(f"==>\n'{folder}' folder is empty in: \n{path.parent.joinpath('Notices')}\n<==")
            continue
        image_count = 0
        CPU_USED = 0
        processs = []

        for img in img_list:
            image_count += 1
            print(f"\t==> Processing {img} for tender [{image_count}/{len(img_list)}]")
            CPU_USED += 1  # number of processes used so far

            # If the no of processes are less than CPU_COUNT,
            # continue adding new processes
            if CPU_USED <= CPU_COUNT:
                process = mp.Process(target=is_tender, args=(folder, img, dic))
                processs.append(process)

            # If the no of processes are equal tto CPU_COUNT,
            # Or if no further process can be added,
            # then start the execution of the processes
            if CPU_USED == CPU_COUNT or image_count == len(img_list):

                # Start the execution of the processes
                for process in processs:
                    process.start()

                # Wait for the processes to finish
                # This is done to make sure that all the processes are finished
                # before moving to the next newspaper
                # After the processes are finished, it is terminated
                for process in processs:
                    process.join()
                    process.terminate()
                processs = []
                CPU_USED = 0


if __name__ == "__main__":
    sys.stdout=Logger(datetime.datetime.now())
    tender_filter()
