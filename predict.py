import numpy as np
from PIL import Image
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from ImageProcess import vertical
from sklearn.cluster import KMeans
import os
import logging
import time

# 加载模型文件

# 数据集，每个向量为30*50=1500维， 每个维度上只有0/1两种情况
train_x = np.load('model_data.npy')
# 标注集，缺少部分字母
train_y = np.load('model_label.npy')

# 主成分分析，处理后会变成28维的数据
pca = PCA(n_components=0.7, whiten=True)
train_x = pca.fit_transform(train_x)

# KNN
neighbors = KNeighborsClassifier(n_neighbors=3)
neighbors.fit(train_x, train_y)

# 测试文件所在的目录
dir = './TARGET/'


def get_start_x(img_shape):
    """
    获取图片投影的开始点
    :param img_shape:
    :return:
    """
    for i in range(len(img_shape)):
        if img_shape[i] != 0:
            return i - 1


def get_end_x(img_shape):
    """
    获取图片投影的结束点
    :param img_shape:
    :return:
    """
    for i in range(len(img_shape) - 1, 0, -1):
        if img_shape[i] != 0:
            return i + 1


def do_split(img, start, end, parts):
    """
    图片分割，利用图片投影确定的开始和结束点确定分割起止的坐标
    :param img:
    :param start:
    :param end:
    :param parts: 划分字符数
    :return:
    """

    pixeldata = img.load()
    DataX = []
    DataY = []
    Data = []
    for x in range(start, end):
        for y in range(50):
            if pixeldata[x, y] < 40:
                DataX.append(x)
                DataY.append(50 - y)
                Data.append((x, y))

    # 利用KMeans聚类进行划分
    pred = KMeans(n_clusters=parts, random_state=5).fit_predict(Data)

    # 取出每个聚类的形状，保存成图片
    preresult = []
    for p in range(parts):
        min_x = 300
        max_x = 0
        # 确定起止点
        for i in range(len(DataX)):
            if pred[i] == p:
                if min_x > DataX[i]:
                    min_x = DataX[i]

                if DataX[i] > max_x:
                    max_x = DataX[i]

        image = Image.new('RGB', (max_x - min_x + 1, 50), (255, 255, 255))
        for i in range(len(DataX)):
            if pred[i] == p:
                image.putpixel((DataX[i] - min_x, 50 - DataY[i]), (0, 0, 0))
        image = image.resize((30, 50))
        # 由于聚类划分具有随机性，利用该字符出现的最小x值确定其在整个图片中排布顺序
        preresult.append((min_x, image))
    # 如上进行排序
    preresult = sorted(preresult, key=lambda x: x[0])
    result = [x[1] for x in preresult]

    return result


def convert_img_to_vector(img):
    """
    将图片转换为向量
    :param img:
    :return:
    """
    x, y = img.size

    data = []
    for i in range(x):
        for j in range(y):

            if img.getpixel((i, j))[0] < 40:
                data.append(1)
            else:
                data.append(0)
    return data


def predict(image_name):
    """
    进行预测
    :param image_name:
    :return:
    """
    img = Image.open(dir + image_name)
    code = image_name.split('_')[0]
    print('Source: ', code, end='')
    # 向量化
    img_shape = vertical(img)

    begin = get_start_x(img_shape)
    end = get_end_x(img_shape)
    img_width = end - begin

    # 如果字符区域宽度大于112则认为有5个字符，否则有认为有4个
    # 此数据根据统计分析得出，总体准确率约89%
    if img_width >= 112:
        res = do_split(img, begin, end, 5)
    else:
        res = do_split(img, begin, end, 4)

    # 构建测试集
    test = []
    for r in res:
        test.append(convert_img_to_vector(r))

    test = np.array(test)
    # 主成分
    test = pca.transform(test)

    # 预测
    pre = neighbors.predict(test)

    # 结果
    pre = ''.join(pre)
    print(' Predict: ', pre)
    if pre == code:
        return 1
    else:
        return -1


if __name__ == '__main__':
    accept = 0
    total = 0

    for i in os.listdir(dir):
        total += 1
        if predict(i) == 1:
            accept += 1

    print('准确率{:.6f}'.format(accept / total))
