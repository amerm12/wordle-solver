from PIL import ImageGrab, Image
import pyautogui
import time
import cv2
import numpy

#ss = ImageGrab.grab(all_screens=True)

while(True):
    #location = pyautogui.locateCenterOnScreen('C:/Users/amera/OneDrive/Desktop/wordle-solver/src/WordleOriginalDarks.png', confidence=0.9)
    try: 
        location = pyautogui.locateOnScreen('src/WordleOriginalDark.png', grayscale=True, confidence=0.6)
        print('Grid visible', location)
        time.sleep(3)
    except pyautogui.ImageNotFoundException:
        print('Grid not visible')
        time.sleep(3)  