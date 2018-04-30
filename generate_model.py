import os
from PIL import Image
import sklearn.cross_validation as cross_validation
from sklearn.cross_validation import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
import numpy as np
import time

t = time.time()
labellist = []
train_data = []
for c in 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890':
    for img_name in os.listdir('./traindata/' + c):
        img = Image.open('./traindata/' + c + '/' + img_name)
        img = img.resize((30, 50))
        labellist.append(c)
        x, y = img.size
        # print(x, y)
        # pixeldata = img.load()
        data = []
        for i in range(x):
            for j in range(y):

                if img.getpixel((i, j))[0] < 40:
                    data.append(1)
                else:
                    data.append(0)
        train_data.append(data)
testlabel = []

test_data = []
for img_name in os.listdir('./traindata/_test/'):
    testlabel.append(img_name.split('_')[0])
    img = Image.open('./traindata/_test/' + img_name)
    img = img.resize((30, 50))
    x, y = img.size
    data = []
    for i in range(x):
        for j in range(y):

            if img.getpixel((i, j))[0] < 40:
                data.append(1)
            else:
                data.append(0)
    test_data.append(data)

# KNN
# print(labellist)
train_data = np.array(train_data)
test_data = np.array(test_data)
labellist = np.array(labellist)
X_train, X_test, y_train, y_test = train_test_split(train_data, labellist, test_size=0.01, random_state=0)
np.save('model_data.npy',X_train)
np.save('model_label.npy',y_train)
# pca = PCA(n_components=0.7, whiten=True)
# X_train = pca.fit_transform(X_train)
# X_test = pca.transform(X_test)
#
#
# neighbors = KNeighborsClassifier(n_neighbors=3)
# neighbors.fit(X_train, y_train)
# pre = neighbors.predict(X_test)

# train_data = np.array(train_data)
# test_data = np.array(test_data)
# pca = PCA(n_components=0.7, whiten=True)
# train_data = pca.fit_transform(train_data)
# test_data = pca.transform(test_data)
# neighbors = KNeighborsClassifier(n_neighbors=4)
# neighbors.fit(train_data, labellist)
# pre = neighbors.predict(test_data)

print(pre)
print(y_test)
acc = float((pre == y_test).sum()) / len(y_test)
print(u'准确率：%f,花费时间：%.2fs' % (acc, time.time() - t))
