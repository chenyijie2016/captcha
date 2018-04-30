import os
from PIL import Image
from matplotlib import pyplot as plt
from ImageProcess import vertical
from sklearn.cluster import KMeans

DIR = './TARGET/'
images = [x for x in os.listdir(DIR)]
print(range(101, 0, -1))
len4 = []
len5 = []


def get_start_x(img_shape):
    for i in range(len(img_shape)):
        if img_shape[i] != 0:
            return i - 1


def get_end_x(img_shape):
    for i in range(len(img_shape) - 1, 0, -1):
        if img_shape[i] != 0:
            return i + 1


g_num = 1


def do_split(img, start, end, parts):
    # image = Image()
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
    pred = KMeans(n_clusters=parts, random_state=9).fit_predict(Data)
    # print(pred)
    global g_num
    for p in range(parts):
        min_x = 300
        max_x = 0
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
        image.resize((30, 50))
        # try:
        #     image.save('./traindata/' + code[p] + '/' + str(g_num) + '.jpg')
        # except :
        #     pass
        g_num += 1

    # plt.scatter(DataX, DataY, marker='o', c=pred)
    # plt.title(img_name.split('_')[0])
    # plt.savefig('./test3/' + code + '.png')
    # plt.clf()





def split_image(img, img_shape, start, end, parts):
    # plt.plot(img_shape[start:end])
    # plt.ylim(0, 50)
    # plt.xlim(0, 200)
    # plt.title(img_name.split('_')[0] + ' width= ' + str(end - begin))
    # plt.savefig('./test2/' + code + '.png')
    # plt.clf()
    do_split(img, 0, 200, parts)


for img_name in images:
    print(images.index(img_name), '/', len(images))
    img = Image.open(DIR + img_name)
    code = img_name.split('_')[0]
    x, y = img.size
    # print(x, y)
    img_shape = vertical(img)

    begin = get_start_x(img_shape)
    end = get_end_x(img_shape)

    img_width = end - begin
    if img_width >= 112:
        split_image(img, img_shape, begin, end, 5)
    else:
        split_image(img, img_shape, begin, end, 4)

    # plt.plot(img_shape)
    # plt.ylim(0, 50)
    # plt.xlim(0, 200)
    # plt.title(img_name.split('_')[0] + ' width= ' + str(end - begin))
    # plt.savefig('./test1/' + code + '.png')
    # plt.clf()
# print(len(len4))
# print(len(len5))
# print(sum(len4) / len(len4))
# print(sum(len5) / len(len5))
#
# for lim in range(105, 115):
#     ok4 = 0
#     ok5 = 0
#     print('lim-=', lim)
#     for i in range(len(len4)):
#         if len4[i] < lim:
#             ok4 += 1
#     print(ok4 / len(len4))
#
#     for i in range(len(len5)):
#         if len5[i] >= lim:
#             ok5 += 1
#     print(ok5 / len(len5))
#
#     print((ok4 + ok5) / (len(len4) + len(len5)))
