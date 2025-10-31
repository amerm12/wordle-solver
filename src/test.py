from solver import WordleSolver

solver = WordleSolver()

# word = [("P", "I"), ("L", "M"), ("A", "C"), ("N", "I"), ("T", "I")]

words = [
    ("R", "M"),  # RAVES ABORT
    ("A", "M"),
    ("V", "I"),
    ("E", "I"),
    ("S", "I"),
    ("A", "C"),
    ("B", "C"),
    ("O", "M"),
    ("R", "M"),
    ("T", "I"),
]

solver.suggestWords(words)
