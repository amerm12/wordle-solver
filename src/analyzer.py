import cv2
import numpy as np
from templateMap import TEMPLATES
from PIL import Image


class AnalyzerError(Exception):
    pass


# Parent Image Analyzer Class
class ImageAnalyzer:

    def analyzeImage(self, img, mode):
        self.lightAnalyzer = LightImageAnalyzer()
        self.darkAnalyzer = DarkImageAnalyzer()

        if mode == "light":
            squares = self.lightAnalyzer.findSquares(img)
        elif mode == "dark":
            squares = self.darkAnalyzer.findSquares(img)

        if not squares:
            raise AnalyzerError("Error analying image. Try uploading different image.")

        letters = []

        for square in squares:
            if mode == "light":
                letter = self.lightAnalyzer.extractLetter(square, img)
            elif mode == "dark":
                letter = self.darkAnalyzer.extractLetter(square, img)

            if letter == None:
                break

            correctness = self.getColor(square, img)
            if letter and correctness:
                letters.append((letter, correctness))

        if letters == []:
            raise AnalyzerError(
                "Error reading the letters from the images. Try uploading different image."
            )

        return letters

    # Detects color in the square
    def getColor(self, _square, _img):
        (x, y, w, h) = _square

        croppedImage = _img[y : y + h, x : x + w]

        corners = [
            croppedImage[0:5, 0:5],
            croppedImage[0:5, -5:],
            croppedImage[-5:, 0:5],
            croppedImage[-5:, -5:],
        ]

        background_samples = np.vstack([corner.reshape(-1, 3) for corner in corners])
        avg_background_color = np.mean(background_samples, axis=0)

        b, g, r = avg_background_color

        if 48 < r < 68 and 48 < b < 68 and 50 < g < 70:
            return "I"
        elif 171 < r < 191 and 149 < g < 169 and 49 < b < 69:
            return "M"
        elif 73 < r < 93 and 131 < g < 151 and 68 < b < 88:
            return "C"
        else:
            pass


# Inherized Image Analyzer class for Dark mode
class DarkImageAnalyzer(ImageAnalyzer):

    # Find all squares in the image
    def findSquares(self, _img):
        grayImage = cv2.cvtColor(_img, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(grayImage, 25, 255, cv2.THRESH_BINARY)[1]

        contours, h = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 2)

        squares = []
        for cnt in contours:

            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(cnt)
                aspectRatio = w / h

                if 0.7 <= aspectRatio <= 1.3 and cv2.contourArea(cnt) > 100:
                    squares.append((x, y, w, h))

        squares.sort(key=lambda rect: (rect[1], rect[0]))

        return squares

    # Detects letter in the square
    def extractLetter(self, _square, _img):
        (x, y, w, h) = _square

        croppedImg = _img[y : y + h, x : x + w]
        grayImg = cv2.cvtColor(croppedImg, cv2.COLOR_BGR2GRAY)

        bestValue = None
        bestLetter = None

        for letter, tmplPath in TEMPLATES.items():

            grayTmpl = cv2.imread(tmplPath, cv2.IMREAD_GRAYSCALE)

            result = cv2.matchTemplate(grayImg, grayTmpl, cv2.TM_CCOEFF_NORMED)
            maxVal = cv2.minMaxLoc(result)[1]

            if bestValue == None or maxVal > bestValue:
                bestValue = maxVal
                bestLetter = letter

        if bestValue >= 0.7:
            return bestLetter
        else:
            return None


# Inherized Image Analyzer class for Light mode
class LightImageAnalyzer(ImageAnalyzer):

    # Find all squares in the image
    def findSquares(self, _img):
        grayImage = cv2.cvtColor(_img, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(grayImage, 250, 255, cv2.THRESH_BINARY_INV)[1]

        """ cv2.imshow("img", thresh)
        cv2.waitKey(0)
        exit() """

        contours, h = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 2)

        squares = []
        for cnt in contours:

            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(cnt)
                aspectRatio = w / h

                if 0.7 <= aspectRatio <= 1.3 and cv2.contourArea(cnt) > 100:
                    squares.append((x, y, w, h))

        squares.sort(key=lambda rect: (rect[1], rect[0]))

        return squares

    # ToDo: Add letter screenshots on light mode
    # Detects letter in the square
    def extractLetter(self, _square, _img):
        (x, y, w, h) = _square

        croppedImg = _img[y : y + h, x : x + w]
        grayImg = cv2.cvtColor(croppedImg, cv2.COLOR_BGR2GRAY)

        bestValue = None
        bestLetter = None

        for letter, tmplPath in TEMPLATES.items():

            grayTmpl = cv2.imread(tmplPath, cv2.IMREAD_GRAYSCALE)

            result = cv2.matchTemplate(grayImg, grayTmpl, cv2.TM_CCOEFF_NORMED)
            maxVal = cv2.minMaxLoc(result)[1]

            if bestValue == None or maxVal > bestValue:
                bestValue = maxVal
                bestLetter = letter

        if bestValue >= 0.7:
            return bestLetter
        else:
            return None
