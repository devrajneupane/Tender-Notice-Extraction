import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import cv2
import tensorflow as tf
from tensorflow import keras
from model import get_model

def applyCNN():
    dirList = os.listdir("./Notices/")
    for dir in dirList:
        fileList = os.listdir("./Notices/"+dir+"/")
        for file in fileList:
            img = tf.keras.utils.load_img(f"./Notices/{dir}/{file}", grayscale=False, color_mode="grayscale", target_size=(224, 224,1))
            img = np.array(img, dtype=np.float32)
            img = img.reshape(1, 224, 224, 1)
            img = img / 255.0
            # print(img.shape)
            model = get_model()
            pred = model.predict(img)
            # print(pred)
            if pred[0][0] < pred[0][1]:
                print("Notice is for Tender")
                print(f"{dir}/{file}")

if __name__ == '__main__':
    applyCNN()

