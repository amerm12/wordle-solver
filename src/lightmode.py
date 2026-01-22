import cv2
from PIL import Image

def getMainColor(file):
    img = Image.open(file)
    colors = img.getcolors(maxcolors=1024)
    maxOccurence, mostPresent = 0, 0
    try:
        for c in colors:
            if c[0] > maxOccurence:
                (maxOccurence, mostPresent) = c
        return mostPresent
    except TypeError:
        raise Exception("Too many colors in the image")
    



imagePath = "C:/Users/amera/OneDrive/Desktop/Skafiskafnjak/Amer/wordle-solver/src/lightmode.png"
#imagePath = "C:/Users/amera/OneDrive/Desktop/Skafiskafnjak/Amer/wordle-solver assets/Test Data/wordleScreenshot.png"

lightImage = cv2.imread(imagePath)

getMainColor(imagePath)

""" grayImage = cv2.cvtColor(lightImage, cv2.COLOR_BGR2GRAY)

thresh = cv2.threshold(grayImage, 230, 255, cv2.THRESH_BINARY)[1]

cv2.imshow("img", thresh)
cv2.waitKey(0) """

