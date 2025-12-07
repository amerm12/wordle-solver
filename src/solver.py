import re
import random


class SolverError(Exception):
    pass


class WordleSolver:

    def __init__(self):
        """self.wrongLetters = []
        self.correctLetters = [(), (), (), (), ()]  # () is tuple. Can only be changed.
        self.misplacedLetters = [[], [], [], [], []]  # [] is list. Can be modified."""

    def suggestWords(self, _words):
        self.wrongLetters = []
        self.correctLetters = [(), (), (), (), ()]
        self.misplacedLetters = [[], [], [], [], []]

        if 0 <= len(_words) > 24:
            raise SolverError("Error suggesting words.")

        words = _words
        for index, (letter, key) in enumerate(words):
            index = index % 5  # Keep index from 0 to 4
            match key:
                case "I":  # I - Incorrect
                    # ToDo: If written word has 2 same letters, and correct has only one of those
                    # one will appear yellow, and the other one will appear gray. But both are
                    # misplaced, and should be treaded as such. I assume wordle will handle this
                    # case giving yellow color to first letter that appears, and the next ones will
                    # be grayed out. Check if this is the case.
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
            "C:/Users/amera/OneDrive/Desktop/Skafiskafnjak/Amer/wordle-solver/solutions.txt"
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

        return filteredWords

    def constructRegex(self):

        # Remove all correct letters from misplaced letters group
        wrongLettersString = "".join(self.wrongLetters)
        """ for correctLetter in self.correctLetters:
            for misplacedPosition in self.misplacedLetters:
                if correctLetter in misplacedPosition:
                    misplacedPosition.remove(correctLetter) """

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
