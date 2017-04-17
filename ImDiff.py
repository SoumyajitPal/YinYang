import cv2
import numpy as np
import CropImage
from random import randint


def imDiff(im1, im2):

    # im1 = im1[0:im1.shape[0]-8, 0:im1.shape[1]]
    # im2 = im2[0:im2.shape[0]-8, 0:im2.shape[1]]

    imGray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    imGray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    print(im1.shape, im2.shape)
    im = cv2.absdiff(imGray1, imGray2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    thresh = cv2.erode(im, kernel, iterations=3)
    thresh = cv2.erode(thresh, kernel, iterations=3)
    ret, thresh = cv2.threshold(im, 127,255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    # finalIm = thresh
    thresh = cv2.dilate(thresh, kernel, iterations=2)
    # thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    img2, contours,hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_KCOS )
    # finalIm = cv2.erode(finalIm, kernel=np.ones(shape=(3, 3), dtype=np.uint8))
    contours = [cc for cc in contours if 10 < cv2.contourArea(cc) < 15000]
    '''for c in contours:    
        x,y,w,h = cv2.boundingRect(c)
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])'''
    #cv2.circle(im, (cX, cY), 2, (255, 0, 2), 3)
    #cv2.rectangle(im, (cX, cY), (cX+w, cY+h), (0, 255, 0), 2)
    colors = []
    for i in range(50):
        colors.append((randint(0,255), randint(0,255), randint(0,255)))
    # finalIm = cv2.cvtColor(im1, cv2.COLOR_GRAY2BGR)
    # testEllipse = ((100, 50), (20, 100), 90)
    # cv2.ellipse(im2, testEllipse, (0,0,255), 3)
    # cv2.circle(im2, (50, 118), 2, (255,0,0))
    # cv2.circle(im2, (100, 100), 2, (255,0,0))
    for i, cnt in enumerate(contours):
        try:
            # ellipse = cv2.fitEllipse(cnt)
            # if ellipse[0][0] < 0  or ellipse[0][0] > im.shape[1] or ellipse[0][1] < 0 or ellipse[0][1] > im.shape[0]:
                # continue
            # cv2.ellipse(im1, ellipse, colors[i], 1)
            # cv2.ellipse(im2, ellipse, colors[i], 1)
            cv2.drawContours(im1, [cnt], 0, colors[i], 1)
            cv2.drawContours(im2, [cnt], 0, colors[i], 1)
        except cv2.error:
            continue
        # cv2.drawContours(im1, [cnt], 0, colors[i], 2)
        # cv2.drawContours(im2, [cnt], 0, colors[i], 2)
    # cv2.drawContours(finalIm, contours, -1, (0,255,0), 2)
    # cv2.imwrite('p441.png', im1)
    # cv2.imwrite('p442.png', im2)
    cv2.imshow('diff', thresh)
    # cv2.waitKey()
    # cv2.imwrite("difference.png", finalIm)
    return im1, im2

if __name__ == '__main__':

    Folder = 'C:\\Users\\soumy\\Downloads\\HocusFocusSeg\\HocusFocusSeg\\'

    import os

    DownImages = []
    for f in os.listdir(Folder + 'down'):
        DownImages.append(Folder + 'down\\' + str(f))

    UpImages = []
    for f in os.listdir(Folder + 'up'):
        UpImages.append(Folder + 'up\\' + str(f))

    for u, d in zip(UpImages, DownImages):
        print(u, d)
        im1 = cv2.imread(u, cv2.IMREAD_GRAYSCALE)
        im2 = cv2.imread(d, cv2.IMREAD_GRAYSCALE)

        # dilated1 = cv2.dilate(im1, kernel=np.zeros(shape=(3, 3)), iterations=1)
        # dilated2 = cv2.dilate(im2, kernel=np.zeros(shape=(3, 3)), iterations=1)

        # imDiff(dilated1, dilated2)
        imOut = CropImage.cropImage(im1, im2)
        imDiff(im1, imOut)