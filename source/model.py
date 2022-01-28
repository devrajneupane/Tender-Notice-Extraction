import os
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split
from sklearn import metrics

from Inception import InceptionUnit
from ResNet import ResidualUnit
from Xception import XceptionUnit

def ResNet():
    model_resnet = keras.models.Sequential()
    model_resnet.add(keras.layers.Conv2D(4, 7, strides = 2, input_shape = [224, 224, 1], padding = "same", use_bias = False))
    model_resnet.add(keras.layers.BatchNormalization())
    model_resnet.add(keras.layers.Activation("relu"))
    model_resnet.add(keras.layers.MaxPool2D(pool_size=3, strides=2, padding = "same"))
    prev_filters = 4
    for filters in [8, 8, 16, 16]:
        strides = 1 if filters == prev_filters else 2
        model_resnet.add(ResidualUnit(filters, strides = strides))
        prev_filters = filters
    model_resnet.add(keras.layers.GlobalAveragePooling2D())
    model_resnet.add(keras.layers.Flatten())
    model_resnet.add(keras.layers.Dropout(0.4))
    model_resnet.add(keras.layers.Dense(2, activation = "relu"))
    model_resnet.add(keras.layers.Dense(1, activation = "sigmoid"))

    return model_resnet

def GoogleNet():
    model_googlenet = keras.models.Sequential()
    model_googlenet.add(keras.layers.Conv2D(8, 7, strides = 2, input_shape = [224, 224, 1], padding = "same", use_bias = False))
    model_googlenet.add(keras.layers.BatchNormalization())
    model_googlenet.add(keras.layers.Activation("relu"))
    model_googlenet.add(keras.layers.MaxPool2D(pool_size=3, strides=2, padding = "same"))
    model_googlenet.add(InceptionUnit())
    model_googlenet.add(keras.layers.MaxPool2D(pool_size=3, strides=2, padding = "same"))
    model_googlenet.add(InceptionUnit())
    model_googlenet.add(InceptionUnit())
    model_googlenet.add(InceptionUnit())
    model_googlenet.add(keras.layers.MaxPool2D(pool_size=3, strides=2, padding = "same"))
    model_googlenet.add(InceptionUnit())
    model_googlenet.add(keras.layers.GlobalAveragePooling2D())
    model_googlenet.add(keras.layers.Flatten())
    model_googlenet.add(keras.layers.Dropout(0.4))
    model_googlenet.add(keras.layers.Dense(2, activation = "relu"))
    model_googlenet.add(keras.layers.Dense(1, activation = "sigmoid"))

    return model_googlenet

def Xception():
    model_xception = keras.models.Sequential()
    model_xception.add(keras.layers.Conv2D(8, 7, strides = 2, input_shape = [224, 224, 1], padding = "same", use_bias = False))
    model_xception.add(keras.layers.BatchNormalization())
    model_xception.add(keras.layers.Activation("relu"))
    model_xception.add(XceptionUnit(8, isEntryExit=True))
    # model_xception.add(XceptionUnit(8, isEntryExit=True))
    model_xception.add(XceptionUnit(16))
    model_xception.add(XceptionUnit(16))
    model_xception.add(XceptionUnit(16))
    # model_xception.add(XceptionUnit(16))
    model_xception.add(XceptionUnit(8, isEntryExit=True))
    model_xception.add(keras.layers.SeparableConv2D(8, 3, padding = "same"))
    model_xception.add(keras.layers.BatchNormalization())
    model_xception.add(keras.layers.Activation("relu"))
    model_xception.add(keras.layers.Flatten())
    model_xception.add(keras.layers.Dropout(0.4))
    model_xception.add(keras.layers.Dense(2, activation = "relu"))
    model_xception.add(keras.layers.Dense(1, activation = "sigmoid"))

    return model_xception

def model_check():
    datasets = np.load('D:\Programming\Python\Tender-Notice-Extraction\source\models\datasets.npy', allow_pickle=True)
    np.random.shuffle(datasets)
    X = []
    y = []
    for ele in datasets:
        X.append(ele[0])
        y.append(ele[1])
    X = np.array(X)
    y = np.array(y)


    X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, y_train_full, test_size=0.2, random_state=42) 

    model1 = ResNet()
    model2 = GoogleNet()
    model3 = Xception()

    all_model = [model1, model2, model3]

    model = model1
    early_stopping_cb = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
    optimizer = keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, decay=0.001)
    model.compile(loss=tf.keras.losses.CategoricalCrossentropy(), optimizer=optimizer, metrics=["accuracy"])

    history = model.fit(X_train, y_train,
                                epochs=2,
                                validation_data=(X_valid, y_valid),
                                callbacks=[early_stopping_cb])  

    model.evaluate(X_test, y_test)

    # get training chart 
    plt.plot(history.history['accuracy'], "-")
    plt.plot(history.history['val_accuracy'], ":")
    plt.title('ResNet Accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['Training', 'Validiation'], loc='upper left')
    plt.grid(True)
    plt.show()

    #plot loss
    plt.plot(history.history['loss'], "-")
    plt.plot(history.history['val_loss'], ":")
    plt.title('ResNet Loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['Training', 'Validiation'], loc='upper left')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    model_check()

