import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
import os
import cv2
import tensorflow as tf
from tensorflow import keras
from Inception import InceptionUnit
from ResNet import ResidualUnit
from Xception import XceptionUnit
from model import ResNet, GoogleNet, Xception
# from model import get_model
try:
    os.mkdir("./Tender")
except FileExistsError:
    pass

try:
    os.mkdir("./notTender")
except FileExistsError:
    pass

def resize(img):
    old_image_width, old_image_height, channels = img.shape
    color = (0,0,0)
    if old_image_width>old_image_height:
        result= np.full((old_image_width,old_image_width, channels), color, dtype=np.uint8)
        yc = (old_image_width-old_image_height)//2
        #temp=result[:, yc:yc+old_image_height,:]
        #print("a",temp.shape)
        result[:, yc:yc+old_image_height,:] = img 
        #return result
    elif old_image_width<old_image_height:
        result= np.full((old_image_height,old_image_height, channels), color, dtype=np.uint8)
        xc = (old_image_height-old_image_width)//2
        #temp= result[xc:xc+old_image_width,:,:]
        #print("b",temp.shape)
        result[xc:xc+old_image_width,:,:] = img 
        #return result
    else:
        result=img
    a=cv2.resize(result,(224,224))
    return a


def applyCNN():
    dirList = os.listdir("./Notices/")
    for dir in dirList:
        fileList = os.listdir("./Notices/"+dir+"/")
        for file in fileList:
            # img = tf.keras.utils.load_img(f"./Notices/{dir}/{file}", grayscale=False, color_mode="grayscale")
            img = cv2.imread(f"./Notices/{dir}/{file}")
            temp=img.copy()
            img = resize(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = np.array(img, dtype=np.float32)
            print(img.shape)
            img = img.reshape(1, 224, 224, 1)
            img = img / 255.0
            model = Xception()
            model = keras.models.load_model('./source/models/model_xception_1.h5', custom_objects={'XceptionUnit': XceptionUnit})
            pred = model.predict(img)
            # print(pred)
            if pred[0][0] < pred[0][1]:
                print("Notice is for Tender")
                print(f"{dir}/{file}")
                cv2.imwrite("./Tender/"+file,temp)
            else:
                print("Notice is not tender")
                print(f"{dir}/{file}")
                cv2.imwrite("./notTender/"+file, temp)




def applyCNN1():
    dirList = os.listdir("./Notices/")
    for dir in dirList:
        fileList = os.listdir("./Notices/"+dir+"/")
        for file in fileList:
            img = tf.keras.utils.load_img(f"./Notices/{dir}/{file}", grayscale=False, color_mode="grayscale")
            
            img = np.array(img, dtype=np.float32)
            temp=img.copy()
            img=cv2.resize(img, (224,224))
            img = img.reshape(1, 224, 224, 1)
            img = img / 255.0
            # print(img.shape)
            model = Xception()
            model = keras.models.load_model('./source/models/model_xception_1.h5', custom_objects={'XceptionUnit': XceptionUnit})
            pred = model.predict(img)
            # print(pred)
            if pred[0][0] < pred[0][1]:
                print("Notice is for Tender")
                print(f"{dir}/{file}")
                cv2.imwrite("./Tender/"+file,temp)
            else:
                print("Notice is not tender")
                print(f"{dir}/{file}")
                cv2.imwrite("./notTender/"+file, temp)

if __name__ == '__main__':
    applyCNN()

