# 最邻近差值 位于ImageEnhance.py文件 第25行
# 双线性插值 位于ImageEnhance.py文件 第33行
#图片缩小的坐标变换为Y=(X+0.5)*W0/W-0.5,Y为原始图像中的浮点数坐标,X为缩小后图像中的整数坐标,其中W0为原始图像宽度,W为缩小后图像宽度
#图片放大的坐标变换为Y=(X+0.5)*(W0-1)/W-0.5,Y为原始图像中的浮点数坐标,X为缩小后图像中的整数坐标,其中W0为原始图像宽度,W为缩小后图像宽度
import fire
import numpy as np
import cv2.cv2 as cv2
#获取图片
def GetImage(path):
    img = cv2.imread(path)
    return img
#将图片写入文件
def WriteImage(path, img):
    cv2.imwrite(path, img)
#最邻近差值
def Nearest(img, height, width):
    #获取图片的高度、宽度、通道数
    img_height, img_width, img_channels = img.shape
    #创建一个空白图片
    img_new = np.zeros((height, width, img_channels), dtype=np.uint8)
    #遍历新图片的每一个像素点
    for i in range(height):
        for j in range(width):
            #计算新图片中的像素点在原图片中的坐标
            img_new[i, j] = img[int(i * img_height / height), int(j * img_width / width)]
    return img_new
#双线性差值
def Bilinear(img, height, width):
    #获取图片的高度、宽度、通道数
    img_height, img_width, img_channels = img.shape
    #创建一个空白图片
    img_new = np.zeros((height, width, img_channels), dtype=np.uint8)
    #判断是否为放大或缩小
    if height > img_height:
        #放大
        for i in range(height):
            for j in range(width):
                #计算新图片中的像素点在原图片中的坐标
                x = (i + 0.5) * (img_height - 1) / height - 0.5
                y = (j + 0.5) * (img_width - 1) / width - 0.5
                #计算原图片中的坐标的整数部分和小数部分
                x1 = int(x)
                x2 = x1 + 1
                y1 = int(y)
                y2 = y1 + 1
                #计算新图片中的像素点在原图片中的坐标
                x1 = 0 if x1 < 0 else x1
                x2 = img_height - 1 if x2 >= img_height else x2
                y1 = 0 if y1 < 0 else y1
                y2 = img_width - 1 if y2 >= img_width else y2
                #计算新图片中的像素点的值
                img_new[i, j] = (x2 - x) * (y2 - y) * img[x1, y1] + (x - x1) * (y2 - y) * img[x2, y1] + (x2 - x) * (y - y1) * img[x1, y2] + (x - x1) * (y - y1) * img[x2, y2]
    else:
        #缩小
        for i in range(height):
            for j in range(width):
                #计算新图片中的像素点在原图片中的坐标
                x = (i + 0.5) * img_height / height - 0.5
                y = (j + 0.5) * img_width / width - 0.5
                #计算原图片中的坐标的整数部分和小数部分
                x1 = int(x)
                x2 = x1 + 1
                y1 = int(y)
                y2 = y1 + 1
                #计算新图片中的像素点在原图片中的坐标
                x1 = 0 if x1 < 0 else x1
                x2 = img_height - 1 if x2 >= img_height else x2
                y1 = 0 if y1 < 0 else y1
                y2 = img_width - 1 if y2 >= img_width else y2
                #计算新图片中的像素点的值
                img_new[i, j] = (x2 - x) * (y2 - y) * img[x1, y1] + (x - x1) * (y2 - y) * img[x2, y1] + (x2 - x) * (y - y1) * img[x1, y2] + (x - x1) * (y - y1) * img[x2, y2]
    return img_new
#图像增强
def ImageEnhance(path, outpath, height, width, algorithm):
    img = GetImage(path)
    if algorithm == 'nearest':
        # 最近邻插值
        img_new = Nearest(img, height, width)
    elif algorithm == 'bilinear':
        # 双线性插值
        img_new = Bilinear(img, height, width)
    WriteImage(outpath, img_new)
if __name__ == '__main__':
    fire.Fire(ImageEnhance)

