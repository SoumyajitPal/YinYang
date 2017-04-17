import numpy as np
import cv2
# from matplotlib import pyplot as plt
import ImDiffMod
import math


def cropImage(img1, img2):

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # print(matches)

    good = []
    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]

    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1, 0]
            good.append(m)

    sourcePoints = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    desPoints = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # print(sourcePoints)
    # print(desPoints)

    M, mask = cv2.findHomography(sourcePoints, desPoints, cv2.RANSAC, 10.0)
    ss = M[0, 1]
    sc = M[0, 0]
    scaleRecovered = math.sqrt(ss * ss + sc * sc)
    thetaRecovered = math.atan2(ss, sc) * 180 / math.pi
    print("Calculated scale difference: %.2f\nCalculated rotation difference: %.2f" % (scaleRecovered, thetaRecovered))

    im_out = cv2.warpPerspective(img2, np.linalg.inv(M), (img1.shape[1], img1.shape[0]))
    # im_in = cv2.warpPerspective(img1, np.linalg.inv(M), (img1.shape[1], img1.shape[0]))
    # plt.imshow(im_out, 'gray')
    # plt.show()

    # draw_params = dict(matchColor=(0, 255, 0),
    #                    singlePointColor=(255, 0, 0),
    #                    matchesMask=matchesMask,
    #                    flags=0)
    # img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
    # cv2.imwrite('MatchedImage.png', img3)
    # cv2.imshow('sift', img3)
    # cv2.waitKey()
    return im_out


# if __name__ == '__main__':
#     # img1 = cv2.imread('box.png', 0)  # queryImage
#     # img2 = cv2.imread('box_in_scene.png', 0)  # trainImage

#     im = 'D:\\Hocus-Focus\\p2.png '
#     im1, im2 = ImDiffMod.cropPhoto(im)

#     # im1 = cv2.imread('D:\\HocusFocusCropped\\1\\p1.jpg', cv2.IMREAD_GRAYSCALE)
#     # im2 = cv2.imread('D:\\HocusFocusCropped\\1\\p2.jpg', cv2.IMREAD_GRAYSCALE)

#     cropImage(im1, im2)
