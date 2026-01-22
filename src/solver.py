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

        with open(Path(__file__).resolve().parent.parent / "solutions.txt") as f:
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

        bestWords = self.getBestWords(filteredWords)

        return bestWords

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

    # ToDo: Recheck
    def getBestWords(self, filteredWords):
        # Loop through all words
        for i, word in enumerate(filteredWords):
            filteredWords[i] = {"word": word, "points": 0}
            # Check if word contains most common letters and add points
            if "s" in word:
                filteredWords[i]["points"] += 45
            if "e" in word:
                filteredWords[i]["points"] += 44
            if "a" in word:
                filteredWords[i]["points"] += 41
            if "o" in word:
                filteredWords[i]["points"] += 30
            if "r" in word:
                filteredWords[i]["points"] += 30
            if "i" in word:
                filteredWords[i]["points"] += 27
            if "l" in word:
                filteredWords[i]["points"] += 24
            if "t" in word:
                filteredWords[i]["points"] += 23
            if "n" in word:
                filteredWords[i]["points"] += 21
            if "u" in word:
                filteredWords[i]["points"] += 18
            if "d" in word:
                filteredWords[i]["points"] += 17
            if "y" in word:
                filteredWords[i]["points"] += 15
            if "c" in word:
                filteredWords[i]["points"] += 14
            if "p" in word:
                filteredWords[i]["points"] += 14
            if "m" in word:
                filteredWords[i]["points"] += 13
            if "h" in word:
                filteredWords[i]["points"] += 11
            if "g" in word:
                filteredWords[i]["points"] += 11
            if "b" in word:
                filteredWords[i]["points"] += 11
            if "k" in word:
                filteredWords[i]["points"] += 11
            if "w" in word:
                filteredWords[i]["points"] += 8
            if "f" in word:
                filteredWords[i]["points"] += 7

        filteredWords.sort(reverse=True, key=self.wordsSorter)

        rankedWords = []

        for word in filteredWords:
            rankedWords.append(word["word"])

        return rankedWords

    def wordsSorter(self, e):
        return e["points"]

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
