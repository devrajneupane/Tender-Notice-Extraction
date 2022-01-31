import os
import sys
import cv2
from pathlib import Path
import pytesseract as tess
from dotenv import dotenv_values


path = Path(sys.path[0])
# if sys.platform == "win32":
#     tesseract_exec = dotenv_values(path.joinpath(".env"))["TESSERACT_EXECUTABLE"]
#     tess.pytesseract.tesseract_cmd = tesseract_exec

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

# print(dic[3]=="bids")


def is_tender(img):
    """
    img in grayscale format for better performance
    """
    strike = 0
    text = tess.image_to_data(img, lang="eng+nep", timeout=240)
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
    if strike >= 1:
        return True
    else:
        return False



def tender_filter():
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
            image = cv2.imread("./Notices/" + folder + "/" + img, 0)

            if is_tender(image):
                cv2.imwrite(f"./Tender/{img}", image)
                print(f"\t\t==> {img} is Tender")
            else:
                cv2.imwrite(f"./notTender/{img}", image)
                print(f"\t\t==> {img} is not Tender")
                # os.remove(f"./Notices/{folder}/{img}")
    #         os.remove(path="./Notices/"+folder+"/"+img)
    #     os.rmdir("./Notices/"+folder)
    # os.rmdir("./Notices")


if __name__ == "__main__":
    tender_filter()
