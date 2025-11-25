import numpy as np
import cv2
import pytesseract
import warnings
from PIL import Image

""" try:
    import easyocr
except ImportError:
    print("EasyOCR not installed - run: pip install easyocr")
    exit() """

warnings.filterwarnings("ignore")
image = cv2.imread(
    "C:/Users/amera/OneDrive/Desktop/Skafiskafnjak/Amer/wordle-solver/assets/wordleScreenshot.png"
)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

contours, h = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 2)

squares = []
for i, cnt in enumerate(contours):

    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(cnt)
        color = (0, 0, 255)
        aspectRatio = w / h

        if 0.7 <= aspectRatio <= 1.3 and cv2.contourArea(cnt) > 100:
            squares.append((x, y, w, h))

        # cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        # cv2.putText(image, str(i), (x, y + h), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

squares.sort(key=lambda rect: (rect[1], rect[0]))

# ----------------------------------------------------------------------------------

for i, square in enumerate(squares):
    # (x, y, w, h) = squares[3]
    (x, y, w, h) = square

    croppedImage = image[y : y + h, x : x + w]

    grayImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)

    resizedImage = cv2.resize(grayImage, (200, 200), cv2.INTER_CUBIC)

    thresholdImage = cv2.threshold(resizedImage, 230, 255, cv2.THRESH_BINARY_INV)[1]

    letter = pytesseract.image_to_string(
        thresholdImage,
        lang="eng",
        config="--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    )
    if letter:
        print(letter)
    else:
        thresholdImage = cv2.threshold(croppedImage, 230, 255, cv2.THRESH_BINARY_INV)[1]
        letter = pytesseract.image_to_string(
            thresholdImage,
            lang="eng",
            config="--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        )
        if letter:
            print(letter)
        else:
            print("?")

""" cv2.imshow("img", thresholdImage)
cv2.waitKey(0) """

""" corners = [
    crop[0:5, 0:5],
    crop[0:5, -5:],
    crop[-5:, 0:5],
    crop[-5:, -5:],
]

background_samples = np.vstack([corner.reshape(-1, 3) for corner in corners])
avg_background_color = np.mean(background_samples, axis=0)

b, g, r = avg_background_color

print("-----", i, "------")
if 48 < r < 68 and 48 < b < 68 and 50 < g < 70:
    print("Gray")
    _, thresh = cv2.threshold(grayCrop, 60, 255, cv2.THRESH_BINARY_INV)
elif 171 < r < 191 and 149 < g < 169 and 49 < b < 69:
    print("Yellow")
    _, thresh = cv2.threshold(grayCrop, 180, 255, cv2.THRESH_BINARY)
elif 73 < r < 93 and 131 < g < 151 and 68 < b < 88:
    print("Green")
    _, thresh = cv2.threshold(grayCrop, 180, 255, cv2.THRESH_BINARY)
else:
    print("Empty") """
