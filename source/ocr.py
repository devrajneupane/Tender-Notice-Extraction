import os
import sys
import cv2
from pathlib import Path
import pytesseract as tess
from dotenv import dotenv_values
import multiprocessing as mp
from sql import sql_insert, sql_initialize
import shutil

CPU_COUNT=mp.cpu_count()
dic=None

path = Path(sys.path[0])
if sys.platform == "win32":
    tesseract_exec = dotenv_values(path.joinpath(".env"))["TESSERACT_EXECUTABLE"]
    tess.pytesseract.tesseract_cmd = tesseract_exec


# print(dic[3]=="bids")

def clean_folders():
    try:
        shutil.rmtree(path.parent.joinpath("Newspapers"))
    except OSError as e:
        pass
    try:
        shutil.rmtree(path.parent.joinpath("Images"))
    except OSError as e:
        pass
    try:
        shutil.rmtree(path.parent.joinpath("Notices"))
    except OSError as e:
       pass
    try:
        shutil.rmtree(path.parent.joinpath("notNotices"))
    except OSError as e:
        pass
    try:
        shutil.rmtree(path.parent.joinpath("notTender"))
    except OSError as e:
        pass
    try:
        shutil.rmtree(path.parent.joinpath("subimage"))
    except OSError as e:
        pass


def is_tender(folder,img):
    """
    img in grayscale format for better performance
    """
    global dic
    image = cv2.imread("./Notices/" + folder + "/" + img, 0)
    strike = 0
    text = tess.image_to_data(image, lang="eng+nep", timeout=240)
    for x, b in enumerate(text.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                b[11] = b[11].lower()
                s1 = set(dic)
                s2 = set(b)
                res = s1.intersection(s2)
                if len(res) != 0:
                    strike += 1
                    print("\t\tStrike word: ", res)
    date=folder[-10:]
    YMD=date.split("-")
    if strike >=1:

        try:
            os.mkdir(path.parent.joinpath("Tender/{}".format(date)))
            
        except FileExistsError:
            pass
        try:
            os.mkdir(path.parent.joinpath("Tender/{}/{}".format(date,folder[:-11])))
        except FileExistsError:
            pass
        
        cv2.imwrite(f"./Tender/{date}/{folder[:-11]}/{img}", image)
        sql_insert(img.split("_id_")[1].split('.')[0],date,folder[:-11], img.split("_pg_")[1].split("_id")[0], img)
        print(f"\t\t==> {img} is Tender")
    else:
        try:
            os.mkdir(path.parent.joinpath("notTender/{}".format(date)))
            
        except FileExistsError:
            pass
        try:
            os.mkdir(path.parent.joinpath("notTender/{}/{}".format(date,folder[:-11])))
        except FileExistsError:
            pass
        cv2.imwrite(f"./notTender/{date}/{folder[:-11]}/{img}", image)
        print(f"\t\t==> {img} is not Tender")


def tender_filter():
    global dic
    try:
        with open(path.parent.joinpath("dict.txt"), "r", encoding="utf-8") as dicx:
            try:
                os.mkdir(path.parent.joinpath("Tender"))
                

            except FileExistsError:
                pass
            try:
                os.mkdir(path.parent.joinpath("notTender"))
                

            except FileExistsError:
                pass

            # print(dicx.read())
            dic = dicx.read().lower().splitlines()

    except FileNotFoundError:
        print("dict.txt not found")
        exit()

    folder_list = os.listdir(path.parent.joinpath("Notices/"))
    folder_count = 0
    sql_initialize()
    for folder in folder_list:
        folder_count += 1
        print(f"Processing Newspaper: {folder}=====================[{folder_count}/{len(folder_list)}]")
        img_list = os.listdir("./Notices/" + folder + "/")
        image_count = 0
        CPU_USED = 0
        processs=[]
        for img in img_list:
            image_count += 1
            print(f"\t==> Processing {img} for tender [{image_count}/{len(img_list)}]")
            CPU_USED+=1                 
            if CPU_USED<=CPU_COUNT: 
                process=mp.Process(target=is_tender, args=(folder,img))
                processs.append(process)
                print("starting process : %s" % process)
                # pool.apply_async(page_to_image,args=(page, output_path,newspaper,i,page_count))
            if CPU_USED==CPU_COUNT or image_count==len(img_list):
                for process in processs:
                    process.start()
                for process in processs:
                    process.join()
                    process.terminate()
                processs=[]
                CPU_USED=0
                print("One iteration completed")
    
    clean_folders()

            
                # os.remove(f"./Notices/{folder}/{img}")
    #         os.remove(path="./Notices/"+folder+"/"+img)
    #     os.rmdir("./Notices/"+folder)
    # os.rmdir("./Notices")


def tender_filter1():
    
    sql_initialize()
    folder_list = os.listdir(path.parent.joinpath("Notices/"))
    folder_count = 0
    for folder in folder_list:
        folder_count += 1
        print(f"Processing Newspaper: {folder}=====================[{folder_count}/{len(folder_list)}]")
        img_list = os.listdir("./Notices/" + folder + "/")
        image_count = 0
        for img in img_list:
            image_count += 1
            print(f"\t==> Processing {img} for tender [{image_count}/{len(img_list)}]")
            is_tender(folder, img)
            
                # os.remove(f"./Notices/{folder}/{img}")
    #         os.remove(path="./Notices/"+folder+"/"+img)
    #     os.rmdir("./Notices/"+folder)
    # os.rmdir("./Notices")



if __name__ == "__main__":
    tender_filter()
