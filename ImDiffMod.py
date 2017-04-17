import cv2
import numpy as np
import os
import CropImage
import ImDiff
from random import randint


def imDiff(im1, im2):

    gray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray1, gray2)
    return diff


def cropPhoto(img):

    # imageYUV = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    imageYUV = cv2.imread(img)
    dimensions = np.shape(imageYUV)
    print(dimensions)
    padding = 5
    maxDim = max(dimensions[0], dimensions[1])
    if dimensions[0] > dimensions[1]:
        imageYUV1 = imageYUV[0:int(dimensions[0]/2) + padding, 0:dimensions[1]]
        imageYUV2 = imageYUV[int((dimensions[0] / 2) - padding):int(dimensions[0]), 0:dimensions[1]]
    else:
        imageYUV1 = imageYUV[0:dimensions[0], 0:int(dimensions[1]/2) + padding]
        imageYUV2 = imageYUV[0:dimensions[0], int((dimensions[1] / 2) - padding):int(dimensions[1])]

    # cropped1 = getRect(imageYUV1)
    # cropped2 = getRect(imageYUV2)
    # dim1 = (np.shape(cropped1))
    # dim2 = (np.shape(cropped2))
    # minw = min(dim1[0], dim2[0])
    # minh = min(dim1[1], dim2[1])
    #
    # print(dim1, dim2)

    # cropped1 = cropped1[0:minw, 0:minh]
    # cropped2 = cropped2[0:minw, 0:minh]

    # minSum = 10000


    # diff = imDiff(cropped1, cropped2)
    # diff = cv2.erode(diff, np.ones(shape=(2, 2), dtype=np.uint8), iterations=1)
    # diff = cv2.erode(diff, np.ones(shape=(2, 2), dtype=np.uint8), iterations=1)
    # diff = cv2.dilate(diff, np.ones(shape=(2, 2), dtype=np.uint8), iterations=1)
    # cv2.imshow('Crop1', cropped1)
    # cv2.imshow('Crop2', cropped2)
    # cv2.imshow('img', bestMatch)
    # cv2.imshow('YUV1', imageYUV1)
    # cv2.imshow('YUV2', imageYUV2)
    # cv2.waitKey()

    return imageYUV1, imageYUV2

def getRect(imageYUV):

    imgY = np.zeros(imageYUV.shape[0:2], np.uint8)
    imgY[:, :] = imageYUV[:, :, 0]
    # blurImg = cv2.GaussianBlur(imgY, ksize=(3, 3), sigmaX=0)
    edges = cv2.Canny(imgY, 100, 300, apertureSize=3)

    im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    maxC = 0
    maxCnt = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > maxC:
            maxC = cv2.contourArea(cnt)
            maxCnt = cnt

    # cv2.drawContours(imageYUV, [maxCnt], 0, (0, 255, 0), 3)
    x, y, w, h = cv2.boundingRect(maxCnt)
    # cv2.rectangle(imageYUV, (x, y), (x+w, y+h), (0, 0, 255), 3)
    imageYUV = imageYUV[y:y+h, x:x+w]
    return imageYUV


def PrcessImage(fileName):
    im1, im2 = cropPhoto(fileName)
    imOut = CropImage.cropImage(im1, im2)
    # im1 = cv2.GaussianBlur(im1, ksize=(3,3), sigmaX=0)
    # kernel = np.ones((3,3),np.float32)/9
    # im1 = cv2.filter2D(im1,-1,kernel)
    # imP, imN = ImDiff.imDiff(im1, imOut)

    return im1[0:im1.shape[0]-8, 0:im1.shape[1]], imOut[0:im1.shape[0]-8, 0:im1.shape[1]]

# if __name__ == '__main__':
#     file = 'D:\\Hocus-Focus\\'
#     for f in os.listdir(file):
#         if str(f) == '0.png':
#             continue
#         # img = cv2.imread(file + str(f))
#         # im1, im2 = cropPhoto(file + str(f))
#         PrcessImage(file + str(f))
