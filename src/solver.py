import re
import random
from pathlib import Path


class SolverError(Exception):
    pass


class WordleSolver:

    def suggestWords(self, _words):
        self.wrongLetters = []
        self.correctLetters = [(), (), (), (), ()]  # () is tuple. Can only be changed.
        self.misplacedLetters = [[], [], [], [], []]  # [] is list. Can be modified.

        if 0 <= len(_words) > 25:
            raise SolverError("Error suggesting words.")

        words = _words
        for index, (letter, key) in enumerate(words):
            index = index % 5  # Keep index from 0 to 4
            match key:
                case "I":  # I - Incorrect
                    # If the guess has duplicate letters but the correct word has only one,
                    # the first occurrence is marked yellow, the rest gray (Wordle behavior).
                    if any(
                        letter.lower() in subMisplaced
                        for subMisplaced in self.misplacedLetters
                    ):
                        self.misplacedLetters[index].append(letter.lower())
                    else:
                        self.wrongLetters.append(letter.lower())

                case "C":  # C - Correct
                    self.correctLetters[index] = letter.lower()

                case "M":  # M - Misplaced, wrong spot
                    if letter.lower() not in self.misplacedLetters[index]:
                        self.misplacedLetters[index].append(letter.lower())

        with open(
            Path(__file__).resolve().parent.parent / "solutions.txt"
        ) as f:
            fileWords = f.read().splitlines()

        regex = self.constructRegex()

        pattern = re.compile(regex)

        matches = list(filter(pattern.findall, fileWords))

        misplacedLettersString = ""

        for letters in self.misplacedLetters:
            if letters != []:
                for letter in letters:
                    misplacedLettersString = misplacedLettersString + letter

        filteredWords = [
            w for w in matches if all(c in w for c in misplacedLettersString)
        ]

        # bestWords = self.getBestWords(filteredWords)

        return filteredWords

    def constructRegex(self):

        wrongLettersString = "".join(self.wrongLetters)

        # Remove misplaced letters if they became correct during the game
        for i, misplacedPosition in enumerate(self.misplacedLetters):
            for misplacedLetter in misplacedPosition:
                if misplacedLetter in self.correctLetters:
                    self.misplacedLetters[i].remove(misplacedLetter)

        # Construct regex dynamically
        regex = ""
        for x in range(5):
            # Letter on x position is correct, just set it
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
                            # and character not in wrongLettersString
                            and character not in onPositionWrongString
                        ):
                            onPositionWrongString = onPositionWrongString + character

                regex = (
                    regex
                    + f"([^{re.escape(wrongLettersString + onPositionWrongString)}])"
                )

        return regex

    # From all possible words gets best words
    def getBestWords(self, filteredWords):
        # Put all known letters (correct and misplaced) into one list
        knownLetters = []
        for correctLetter in self.correctLetters:
            if correctLetter != ():
                knownLetters.append(correctLetter)

        for misplacedPosition in self.misplacedLetters:
            if misplacedPosition != []:
                for misplacedLetter in misplacedPosition:
                    knownLetters.append(misplacedLetter)

        for i, word in enumerate(filteredWords):
            # Remove all known letters from filtered word
            for knownLetter in knownLetters:
                if knownLetter in word:
                    word = word.replace(knownLetter, "")

            # Check if word contains most common letters and add points
            if "s" in word:
                filteredWords[i].append(+1)
            if "e" in word:
                filteredWords[i].append(+1)
            if "a" in word:
                filteredWords[i].append(+1)
            if "o" in word:
                filteredWords[i].append(+1)
            if "r" in word:
                filteredWords[i].append(+1)
            if "i" in word:
                filteredWords[i].append(+1)
            if "l" in word:
                filteredWords[i].append(+1)
            if "t" in word:
                filteredWords[i].append(+1)
            if "n" in word:
                filteredWords[i].append(+1)
            if "u" in word:
                filteredWords[i].append(+1)
            if "d" in word:
                filteredWords[i].append(+1)
            if "y" in word:
                filteredWords[i].append(+1)
            if "c" in word:
                filteredWords[i].append(+1)
            if "p" in word:
                filteredWords[i].append(+1)
            if "m" in word:
                filteredWords[i].append(+1)
            if "h" in word:
                filteredWords[i].append(1)
            if "g" in word:
                filteredWords[i].append(+1)

        print(filteredWords)

    # Fetches 3 random words
    def fetchStartingWords(self):
        bestStartingWords = (
            "about",
            "crane",
            "adieu",
            "trace",
            "arose",
            "audio",
            "media",
            "roast",
            "slate",
            "stare",
            "least",
            "roate",
            "salet",
            "sauce",
            "aisle",
            "alone",
            "canoe",
            "cream",
            "react",
            "slant",
            "tales",
            "cones",
            "later",
            "ouija",
        )

        # Randomly select 3 words from the list of best starting words
        threeStaringWords = random.sample(bestStartingWords, 3)

        if not threeStaringWords or len(threeStaringWords) != 3:
            raise SolverError("Error suggesting starting words.")

        return threeStaringWords
