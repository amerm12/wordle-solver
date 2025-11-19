from solver import WordleSolver

solver = WordleSolver()

# word = [("P", "I"), ("L", "M"), ("A", "C"), ("N", "I"), ("T", "I")]

imagePath = "C:/Users/amera/OneDrive/Desktop/Skafiskafnjak/Amer/wordle-solver/assets/wordleScreenshot.png"

word = solver.analyzeImage(imagePath)

print(word)
