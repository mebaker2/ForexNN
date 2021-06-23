import sys
import csv
import numpy as np
import random
import time
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras import backend as K

#heres where we define our model
#this is all random as i will not be sharing my configuration for my NN and is up to you to find an optimal config
inputs = keras.Input(shape=(9,))
dense = layers.Dense(710, activation="relu")
x = dense(inputs)
x = layers.Dense(420, activation="sigmoid")(x)
x = layers.Dense(710, activation="softmax")(x)
x = layers.Dense(69, activation="tanh")(x)
x = layers.Dense(6, activation="softplus")(x)
x = layers.Dense(9, activation="selu")(x)
outputs = layers.Dense(1)(x)

#make sure to insert the file name that we are pulling data from
dataPoints=[]
with open(fileName, 'r') as readFrom:
    reader=csv.reader(readFrom.readlines())
    for line in reader:
        dataPoints.append(line)

#slice up our data into training and testData
x_train=[]
x_test=[]
y_train=[]
y_test=[]
count=0
random.shuffle(dataPoints)
for row in dataPoints:
    #change this number to properly spit your data into training and testing data, a 80/20 or 85/15 split is normal
    if count<240:
        x_train.append(row[0:9])
        y_train.append(row[10])
    else:
        x_test.append(row[0:9])
        y_test.append(row[10])
    count+=1

x_train=np.asarray(x_train).astype(float)
x_test=np.asarray(x_test).astype(float)
y_train=np.asarray(y_train).astype(float)
y_test=np.asarray(y_test).astype(float)

model = keras.Model(inputs=inputs, outputs=outputs, name="Forex_NN")
#fill in  with additional arguments like optimizer accuracy and loss
model.compile()
#feel free to try any other arguments with fit as well, some basic ones to play with are batch_size and epochs and maybe validation_split
history = model.fit(x_train, y_train)

#checks the models acuracy and saves it aginst our test data
test_scores = model.evaluate(x_test, y_test, verbose=2)
print("Test loss:", test_scores[0])
print("Test accuracy:", test_scores[1])

model.save("Forex_NN model")
