import re
from PIL import Image
import pytesseract
import cv2
import numpy as np


class WordleSolver:

    def __init__(self):
        self.wrongLetters = []
        self.correctLetters = [(), (), (), (), ()]
        self.misplacedLetters = [[], [], [], [], []]

    def analyzeImage(imagePath):
        if imagePath:
            return "WORLD"

    # C - Correct
    # I - Incorrect
    # M - Misplaced, wrong spot
    def suggestWords(self, _words):
        if len(_words) <= 0:
            print("There are no words")
            return

        words = _words
        for index, (letter, key) in enumerate(words):
            # Keep index from 0 to 4
            index = index % 5
            match key:
                case "I":
                    self.wrongLetters.append(letter.lower())
                case "C":
                    self.correctLetters[index] = letter.lower()
                case "M":
                    if letter.lower() not in self.misplacedLetters[index]:
                        self.misplacedLetters[index].append(letter.lower())

        with open(
            "C:/Users/amera/OneDrive/Desktop/Skafiskafnjak/Amer/wordle-solver/solutions.txt"
        ) as f:
            fileWords = f.read().splitlines()

        # Remove all correct letters from misplaced letters group
        wrongLettersString = "".join(self.wrongLetters)
        """ for correctLetter in self.correctLetters:
            for misplacedPosition in self.misplacedLetters:
                if correctLetter in misplacedPosition:
                    misplacedPosition.remove(correctLetter) """

        # Construct regex dynamically
        # ToDo: Make a new function and move the code
        regex = ""
        for x in range(5):
            # Letter in a position is correct, just set it
            if self.correctLetters[x] != ():
                regex = regex + self.correctLetters[x]
            # There is no correct letter in a position, create regex
            elif self.correctLetters[x] == ():

                misplacedLettersString = ""
                onPositionWrongString = ""
                for position in self.misplacedLetters:
                    for character in position:
                        if (
                            character not in misplacedLettersString
                            and character not in self.misplacedLetters[x]
                        ):
                            misplacedLettersString = misplacedLettersString + character
                        elif (
                            character in self.misplacedLetters[x]
                            and character not in wrongLettersString
                        ):
                            # onPositionWrongString = onPositionWrongString + character
                            onPositionWrongString = onPositionWrongString + character

                regex = (
                    regex
                    + f"([{re.escape(misplacedLettersString)}]|[^{re.escape(wrongLettersString + onPositionWrongString)}])"
                )

        # print(regex)

        pattern = re.compile(regex)

        matches = list(filter(pattern.findall, fileWords))

        print(matches)


## If if there is no correct letter for that position, rules:
# - On that position it should be a letter from misplaced letter, from which are selected
#   all except ones on that position.
# - On that position there shouldn't be any letters from wrong letters.
# - On that position there shouldn't be any letters that are misplaced on that position.


""" def analyzeImage(self):
    imagePath = "C:/Users/amera/OneDrive/Desktop/Skafiskafnjak/Amer/wordle-solver/assets/wordleScreenshot.png"
    readConfig = r"--psm 6 --oem 3"

    image = cv2.imread(imagePath)

    height, width, _ = image.shape

    boxes = pytesseract.image_to_boxes(image, config=readConfig)

    for box in boxes.splitlines():
        box = box.split(" ")
        image = cv2.rectangle(
            image,
            (int(box[1]), height - int(box[2])),
            (int(box[3]), height - int(box[4])),
            (0, 255, 0),
            2,
        )

    cv2.imshow("image", image)
    cv2.waitKey(0)


    pass """
