from gui import SolverGui
from solver import WordleSolver

words = [("P", "C"), ("E", "M"), ("T", "I"), ("A", "C"), ("L", "M")]

solver = WordleSolver()
suggestedWords = solver.suggestWords(words)
print(suggestedWords)

# gui = SolverGui()
