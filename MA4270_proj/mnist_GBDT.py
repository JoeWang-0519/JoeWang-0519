# MNIST PROBLEM (Chinese mnist)
# ADABOOST, GBDT, XGBOOST
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
#import tensorflow.examples.tutorial.mnist.input_data as input_data

#read data from MNIST
#filename1 = '/Users/wangjiangyi/Downloads/archive/MNIST_DATA'
mnist = tf.keras.datasets.mnist
(train_images,train_labels),(test_images,test_labels) = mnist.load_data()

#the size of training set and test set
print(train_images.shape,train_labels.shape)
print(test_images.shape,test_labels.shape)

'''
#1. Visualize the dataset with image
#a)
n = 3
m = 3
for i in range(n):
    for j in range(m):
        plt.subplot(n, m, i*n+j+1)
        index = i*n+j
        img_arr = train_images[index]
        img = Image.fromarray(img_arr)
        plt.title(train_labels[index])
        plt.imshow(img, cmap='Greys')

plt.show()

#b)

a = 20
im = Image.new('L', (28 * a, 28 * a))  # genrate a BIG PICTURE to visualize a^2 pictures

labels = []
images = []

for i in range(a**2):  # pick a^2 consecutive integers
    img = train_images[i]
    label = train_labels[i]
    pil_img = Image.fromarray(np.uint8(img))  #transformation
    labels.append(label)
    images.append(pil_img)

# get a^2 pictures in ONE BIG picutre
for k in range(a, a*(a+1), a):
    for j in range(10000):
        if j < a:
            im.paste(images[j], (j * 28, 28 * (int(k / a) - 1)))
        elif j < k:
            im.paste(images[j], ((j - k + a) * 28, 28 * (int(k / a) - 1)))

im.show()  # visualization
print(labels)

#2. Visulaize the dataset with Array

sample_index = 8

print('Label of the training sample: ',train_labels[sample_index])
for i in range(28):
    for j in range(28):
        if train_images[sample_index][i][j]:
            print('0 ', end='')
        else:
            print('1 ', end='')
    print('')

'''
# Pre-processing of dataset
# 1.Normalization
train_images_norm = train_images/255.0
test_images_norm = test_images/255.0
#print(train_images_norm[0])


# 2.flatten -> flat_train_image_norm has the size: (60000,784)
flat_train_images_norm = []
flat_test_images_norm = []
k=0

for item in train_images_norm:
    flat_train_images_norm.append(np.reshape(item,784))


for item in test_images_norm:
    flat_test_images_norm.append(np.reshape(item,784))

# 3.extract binary-class dataset
class1=8
class2=2

bi_train_images=[]
bi_train_labels=[]
bi_test_images=[]
bi_test_labels=[]

# construct the training sample for binary case
count=0
for image, label in zip(flat_train_images_norm,train_labels):
    if count<6000:
        if label in [class1,class2]:
            bi_train_images.append(image)
            bi_train_labels.append(label)
        count+=1

for image, label in zip(flat_test_images_norm,test_labels):
    if label in [class1,class2]:
        bi_test_images.append(image)
        bi_test_labels.append(label)

# 3.learning process
# a) multi-class case
'''
gbdt = GradientBoostingClassifier(loss='deviance', learning_rate=.2, n_estimators=50, subsample=.8
                                  , min_samples_split=2, min_samples_leaf=2, max_depth=4
                                  , init=None, random_state=None, max_features=None
                                  , verbose=0, max_leaf_nodes=None, warm_start=False
                                  )
gbdt.fit(flat_train_images_norm[:50000], train_labels[:50000])

test_pred = gbdt.predict(flat_test_images_norm)
train_pred = gbdt.predict(flat_train_images_norm)
test_err=0
train_err=0

for i in range(test_pred.shape[0]):
    if test_pred[i] == test_labels[i]:
        continue
    else:
        test_err+=1

for i in range(train_pred.shape[0]):
    if train_pred[i] == train_labels[i]:
        continue
    else:
        train_err+=1

print("testing error is: ",test_err/test_pred.shape[0])
print("training error is: ", train_err/train_pred.shape[0])

'''


print(bi_train_labels[0])

# binary-class
gbdt1 = GradientBoostingClassifier(loss='exponential', learning_rate=1, n_estimators=5, subsample=1
                                  , min_samples_split=2, min_samples_leaf=2, max_depth=2
                                  , init=None, random_state=None, max_features=None
                                  , verbose=0, max_leaf_nodes=None, warm_start=False
                                  )
gbdt1.fit(bi_train_images, bi_train_labels)

bi_test_pred = gbdt1.predict(bi_test_images)
bi_train_pred = gbdt1.predict(bi_train_images)
bi_test_err = 0
bi_train_err = 0


print(bi_test_pred.shape)
print(bi_train_pred.shape)

for i in range(bi_test_pred.shape[0]):
    if bi_test_pred[i] == bi_test_labels[i]:
        continue
    else:
        bi_test_err+=1

for i in range(bi_train_pred.shape[0]):
    if bi_train_pred[i] == bi_train_labels[i]:
        continue
    else:
        bi_train_err+=1

print("testing error is: ",bi_test_err/bi_test_pred.shape[0])
print("training error is: ", bi_train_err/bi_train_pred.shape[0])


