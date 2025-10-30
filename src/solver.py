import pyautogui
import time
import re


class WordleSolver:

    def __init__(self):
        self.wrongLetters = []
        # self.correctLetters = [None, None, None, None, None]
        self.correctLetters = ["None", "None", "None", "None", "None"]
        self.misplacedLetters = []

    def analyzeImage(self):
        pass

    # C - Correct
    # I - Incorrect
    # M - Misplaced, wrong spot
    def suggestWords(self, currentWord):
        # DoTo: Handle logic where words have double letters
        currentWord = currentWord
        for letter, key in currentWord:
            if key == "I":
                self.wrongLetters.append(letter.lower())
            elif key == "C":
                # ToDo: Check if there is any better solution than manually removing and inserting
                self.correctLetters.pop(currentWord.index((letter, key)))
                self.correctLetters.insert(
                    currentWord.index((letter, key)), letter.lower()
                )
            elif key == "M":
                # self.misplacedLetters.append(letter.lower())
                self.misplacedLetters.insert(
                    currentWord.index((letter, key)), letter.lower()
                )

        with open(
            "C:/Users/amera/OneDrive/Desktop/Skafiskafnjak/Amer/wordle-solver/solutions.txt"
        ) as f:
            words = f.read().splitlines()

        wrongLetters = "".join(self.wrongLetters)

        regex = ""
        for x in range(5):
            if self.correctLetters[x] == "None":
                # regex = regex + r'\dw'
                # regex = regex + r"[^wrongLetters]"
                regex = regex + r"[^+re.escape(wrongLetters)+]"
            else:
                regex = regex + self.correctLetters[x]
                pass

        pattern = re.compile(regex)

        matches = list(filter(pattern.findall, words))

        print(matches)
