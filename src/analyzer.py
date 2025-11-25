import cv2
import pytesseract
import numpy as np


class ImageAnalyzer:

    def analyzeImage(self, imagePath):
        img = cv2.imread(imagePath)
        squares = self.findSquares(img)

        letters = []

        for square in squares:
            letter = self.extractLetter(square, img)
            correctness = self.getColor(square, img)
            if letter and correctness:
                letters.append((letter, correctness))

        return letters

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

    def extractLetter(self, _square, _img):
        (x, y, w, h) = _square

        croppedImage = _img[y : y + h, x : x + w]

        grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)

        resizedImage = cv2.resize(grayImage, (200, 200), cv2.INTER_CUBIC)

        thresholdImage = cv2.threshold(resizedImage, 230, 255, cv2.THRESH_BINARY_INV)[1]

        letter = pytesseract.image_to_string(
            thresholdImage,
            lang="eng",
            config="--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        ).strip()
        if letter:
            return letter
        else:
            thresholdImage = cv2.threshold(
                croppedImage, 230, 255, cv2.THRESH_BINARY_INV
            )[1]
            letter = pytesseract.image_to_string(
                thresholdImage,
                lang="eng",
                config="--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            ).strip()
            if letter:
                return letter
            else:
                pass
                # ToDo: Implement error message that says program could not read text from image

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
            # ToDo: Implement error message that says program could not read text from image
