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


def applyCNN():
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

