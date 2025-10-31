import pyautogui
import time
import re


class WordleSolver:

    def __init__(self):
        self.wrongLetters = []
        self.correctLetters = [(), (), (), (), ()]
        self.misplacedLetters = []

    def analyzeImage(self):
        pass

    # C - Correct
    # I - Incorrect
    # M - Misplaced, wrong spot
    def suggestWords(self, _words):
        # ToDo: Handle logic where words have double letters
        if len(_words) <= 0:
            print("There are no words")
            return

        words = _words
        for index, (letter, key) in enumerate(words):
            if index >= 5:
                index = index - 5

            match key:
                case "I":
                    self.wrongLetters.append(letter.lower())
                case "C":
                    self.correctLetters[index] = letter.lower()
                case "M":
                    if self.misplacedLetters == []:
                        self.misplacedLetters.append((letter.lower(), [index]))
                    else:
                        i = 0
                        while i < len(self.misplacedLetters):
                            if (
                                self.misplacedLetters[i][0] == letter.lower()
                                and index not in self.misplacedLetters[i][1]
                            ):
                                self.misplacedLetters[i][1].append(index)

                            i += 1

        with open(
            "C:/Users/amera/OneDrive/Desktop/Skafiskafnjak/Amer/wordle-solver/solutions.txt"
        ) as f:
            words = f.read().splitlines()

        # First check if there are some letters in both groups. If there are new letter to
        # correct letters group, remove them from misplaced letters group.
        wrongLettersString = "".join(self.wrongLetters)

        regex = ""
        for x in range(5):
            if self.correctLetters[x] == ():
                regex = regex + f"[^{re.escape(wrongLettersString)}]"
            else:
                regex = regex + self.correctLetters[x]

        pattern = re.compile(regex)

        matches = list(filter(pattern.findall, words))

        print(matches)
