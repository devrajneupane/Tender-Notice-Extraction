import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
from random import shuffle
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from ResNet import ResidualUnit
from Inception import InceptionUnit
from Xception import XceptionUnit

def get_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Conv2D(4, 7, strides = 2, input_shape = [224, 224, 1], padding = "same", use_bias = False))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Activation("relu"))
    model.add(keras.layers.MaxPool2D(pool_size=3, strides=2, padding = "same"))
    model.add(ResidualUnit(3, strides = 2))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(10, activation = "relu"))
    model.add(keras.layers.Dense(2, activation = "softmax"))

    model.load_weights("model.h5")
    return model

if __name__ == '__main__':
    get_model()



