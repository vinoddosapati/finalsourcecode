import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Activation, Dropout
from matplotlib import pyplot as plt

print("data loading train...")

data_tr = np.loadtxt('.\\savedata\\all_tr.csv', delimiter=',',
                     dtype=int)
print("data loading eval...")
data_cv = np.loadtxt('.\\savedata\\all_cv.csv', delimiter=',',
                     dtype=int)

train_data = data_tr[:, :-1].astype(np.float32)
train_data = tf.reshape(train_data, [-1, 45, 45, 1])
train_labels = data_tr[:, -1].astype(np.int32)

eval_data = data_cv[:, :-1].astype(np.float32)
eval_data = tf.reshape(eval_data, [-1, 45, 45, 1])
eval_labels = data_cv[:, -1].astype(np.int32)
print("data load DONE...")

# input layer shape
input_shape = (45, 45, 1)

model = Sequential()
# conv1 and pool1
model.add(Conv2D(42, kernel_size=(4, 4), input_shape=input_shape))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
# conv2 and pool2
model.add(Conv2D(42, kernel_size=(4, 4)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

# full connected dense
model.add(Flatten())
model.add(Dense(972, activation=tf.nn.relu))
model.add(Dropout(0.2))
model.add(Dense(240, activation=tf.nn.relu))
model.add(Dropout(0.2))
# 34 output predicts
model.add(Dense(34, activation=tf.nn.softmax))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')

print("training model.....")
model.fit(x=train_data, y=train_labels, batch_size=250, epochs=1, shuffle=True, validation_data=(eval_data, eval_labels))
print("training model DONE.....")

# save model
model.save('seq_model_new.model')