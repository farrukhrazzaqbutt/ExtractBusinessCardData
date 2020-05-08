# import all the necessary packages
# from fpt import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils

from PIL import Image
import PIL.Image

from pytesseract import image_to_string
import pytesseract

import re

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # return the warped image
    return warped

def extractInfo(imageUrl):
    print(imageUrl)
    Url = "media/"+str(imageUrl)
    im = cv2.imread(Url)
    row, col = im.shape[:2]
    bottom = im[row - 2:row, 0:col]
    mean = cv2.mean(bottom)[0]
    color=[0,0,0]
    if(mean>0 and mean<100):
        color = [255, 255, 255]
    bordersize = 10
    image = cv2.copyMakeBorder(
        im,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=color
    )
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    # show the original image and the edge detected image
    print("STEP 1: Edge Detection")

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]


    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # our approximated contour should have four points
        if len(approx) == 4:
            screenCnt = approx
            break

    # show the contour
    print("STEP 2: Find contours of paper")
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)

    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset=10, method="gaussian")
    warped = (warped > T).astype("uint8") * 255

    # show the scanned image and save one copy in out folder
    print("STEP 3: Apply perspective transform")

    imS = cv2.resize(warped, (650, 650))
    # cv2.imshow("output", imS)
    cv2.imwrite('media/' + 'Output Image.PNG', imS)
    # cv2.waitKey(0)

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    TESSDATA_PREFIX = 'C:/Program Files /Tesseract-OCR'
    output = pytesseract.image_to_string(PIL.Image.open('media/'+ 'Output Image.PNG').convert("RGB"), lang='eng')
    print(output)

    f = open('../../output.json', 'w')
    f.write(output)
    f.close()

    #regular expression to find emails
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", output)
    #regular expression to find phone numbers
    numbers = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', output)

    print(numbers)
    print(emails)
    listEmail = []
    listNumber = []
    for email in emails:
        print('EMAIL :-> ' + email)
        listEmail.append(str(email))
        F = open('../../emails.json', 'a+')
        F.write('EMAIL :-> ' + email)

    for number in numbers:
        print('Phone No. :-> ' + number)
        listNumber.append(str(number))
        F = open('../../numbers.json', 'a+')
        F.write('\n Phone No. :-> ' + number)

    return ({"output":output,"email":(','.join(listEmail)),"mobile":(','.join(listNumber))})