import os
import sys
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
from model import ResNet, GoogleNet, Xception


datasets = np.load('D:\Programming\Python\Tender-Notice-Extraction\source\models\datasets.npy', allow_pickle=True)
np.random.shuffle(datasets)
X = []
y = []
for ele in datasets:
    X.append(ele[0])
    y.append(ele[1])
X = np.array(X)
y = np.array(y)

early_stopping_cb = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
epoch = 20
f = 3

# remove all checkpoints if it exists
# try:
#     os.remove("D:\Programming\Python\Tender-Notice-Extraction\source\models\checkpoint_resnet.h5")
# except:
#     pass
# try:
#     os.remove("D:\Programming\Python\Tender-Notice-Extraction\source\models\checkpoint_googlenet.h5")
# except:
#     pass
# try:
#     os.remove("D:\Programming\Python\Tender-Notice-Extraction\source\models\checkpoint_xception.h5")
# except:
#     pass

files = os.listdir("../models")
for file in files:
    if file.startswith("checkpoint"):
        os.remove(os.path.join(sys.path[0]), "models" ,file)

X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.2, random_state=f)
X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, y_train_full, test_size=0.2, random_state=f)

model_resnet = ResNet()
model_googlenet = GoogleNet()
model_xception = Xception()


model_resnet.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])
model_googlenet.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])
model_xception.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])

print("\n\nTraining ResNet\n\n")
checkpoint_cb_resnet = keras.callbacks.ModelCheckpoint(filepath='D:\Programming\Python\Tender-Notice-Extraction\source\models\checkpoint_resnet.h5', save_best_only=True)
history_resnet = model_resnet.fit(X_train, y_train, epochs = epoch, validation_data = (X_valid, y_valid), callbacks = [checkpoint_cb_resnet], batch_size = 16)
model_resnet = keras.models.load_model('D:\Programming\Python\Tender-Notice-Extraction\source\models\checkpoint_resnet.h5', custom_objects={'ResidualUnit': ResidualUnit})
model_resnet.save('D:\Programming\Python\Tender-Notice-Extraction\source\models\model_resnet_' + str(f) + '.h5')

print("\n\nTraining GoogleNet\n\n")
checkpoint_cb_googlenet = keras.callbacks.ModelCheckpoint(filepath='D:\Programming\Python\Tender-Notice-Extraction\source\models\checkpoint_googlenet.h5', save_best_only=True)
history_googlenet = model_googlenet.fit(X_train, y_train, epochs = epoch, validation_data = (X_valid, y_valid), callbacks = [checkpoint_cb_googlenet], batch_size = 16)
model_googlenet = keras.models.load_model('D:\Programming\Python\Tender-Notice-Extraction\source\models\checkpoint_googlenet.h5', custom_objects={'InceptionUnit': InceptionUnit})
model_googlenet.save('D:\Programming\Python\Tender-Notice-Extraction\source\models\model_googlenet_' + str(f) + '.h5')

print("\n\nTraining Xception\n\n")
checkpoint_cb_xception = keras.callbacks.ModelCheckpoint(filepath='D:\Programming\Python\Tender-Notice-Extraction\source\models\checkpoint_xception.h5', save_best_only=True)
history_xception = model_xception.fit(X_train, y_train, epochs = epoch, validation_data = (X_valid, y_valid), callbacks = [checkpoint_cb_xception], batch_size = 16)
model_xception = keras.models.load_model('D:\Programming\Python\Tender-Notice-Extraction\source\models\checkpoint_xception.h5', custom_objects={'XceptionUnit': XceptionUnit})
model_xception.save('D:\Programming\Python\Tender-Notice-Extraction\source\models\model_xception_' + str(f) + '.h5')

print("\n\nEvaluating ResNet\n\n")
model_resnet.evaluate(X_test, y_test)
print("\n\nEvaluating GoogleNet\n\n")
model_googlenet.evaluate(X_test, y_test)
print("\n\nEvaluating Xception\n\n")
model_xception.evaluate(X_test, y_test)


# get training chart

plt.plot(history_resnet.history['accuracy'], "-")
plt.plot(history_resnet.history['val_accuracy'], ":")
plt.title('ResNet Accuracy'+str(f))
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='lower right')
plt.grid(True)
plt.savefig('D:\Programming\Python\Tender-Notice-Extraction\img\\resnet_accuracy_' + str(f) + '.png')
plt.clf()

plt.plot(history_googlenet.history['accuracy'], "-")
plt.plot(history_googlenet.history['val_accuracy'], ":")
plt.title('GoogleNet Accuracy' + str(f))
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='lower right')
plt.grid(True)
plt.savefig('D:\Programming\Python\Tender-Notice-Extraction\img\googlenet_accuracy_' + str(f) + '.png')
plt.clf()

plt.plot(history_xception.history['accuracy'], "-")
plt.plot(history_xception.history['val_accuracy'], ":")
plt.title('Xception Accuracy'  + str(f))
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='lower right')
plt.grid(True)
plt.savefig('D:\Programming\Python\Tender-Notice-Extraction\img\\xception_accuracy_' + str(f) + '.png')
plt.clf()

plt.plot(history_resnet.history['loss'], "-")
plt.plot(history_resnet.history['val_loss'], ":")
plt.title('ResNet Loss'  + str(f))
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.grid(True)
plt.savefig('D:\Programming\Python\Tender-Notice-Extraction\img\\resnet_loss_' + str(f) + '.png')
plt.clf()

plt.plot(history_googlenet.history['loss'], "-")
plt.plot(history_googlenet.history['val_loss'], ":")
plt.title('GoogleNet Loss' + str(f))
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.grid(True)
plt.savefig('D:\Programming\Python\Tender-Notice-Extraction\img\googlenet_loss_' + str(f) + '.png')
plt.clf()



plt.plot(history_xception.history['loss'], "-")
plt.plot(history_xception.history['val_loss'], ":")
plt.title('Xception Loss' + str(f))
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.grid(True)
plt.savefig('D:\Programming\Python\Tender-Notice-Extraction\img\\xception_loss_' + str(f) + '.png')
plt.clf()
   



