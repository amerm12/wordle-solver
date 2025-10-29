import pyautogui

pyautogui.displayMousePosition()

""" -------------------------------- """
from PIL import Image
import pytesseract

img = Image.open('C:/Users/amera/OneDrive/Desktop/wordle-solver/src/test.png')

text = pytesseract.image_to_string(img)

print(text) 

""" -------------------------------- """

import numpy as nm
import pytesseract
import cv2
from PIL import ImageGrab
import time

while(True):

    pytesseract.pytesseract.tesseract_cmd ='C:/Program Files/Tesseract-OCR/tesseract.exe'

    cap = ImageGrab.grab(bbox =(700, 300, 1400, 900))

    tesstr = pytesseract.image_to_string(
            cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY), 
            lang ='eng')
    print(tesstr)

    time.sleep(5)