import customtkinter
from analyzer import ImageAnalyzer
from solver import WordleSolver
from PIL import Image, ImageTk


class SolverGui:

    # Initializes gui, sets default settings
    def __init__(self):
        self.app = customtkinter.CTk(fg_color="#121213")
        self.app.title("wordle-solver")
        self.app.geometry("500x600")
        self.app.resizable(False, False)
        self.app.grid_columnconfigure(0, weight=1)

        # Define label for logo
        self.logoLabel = customtkinter.CTkLabel(
            self.app,
            font=("Helvetica Neue", 40, "bold"),
            text="wordle-solver",
            text_color="#538d4e",
        )
        self.logoLabel.grid(row=0, column=0, pady=30)

        # Define upload button
        self.button = customtkinter.CTkButton(
            self.app,
            text="Upload",
            font=("Helvetica", 24, "bold"),
            width=200,
            height=60,
            fg_color="#74a67a",
            hover_color="#5f8c5c",
            text_color="#ffffff",
            command=self.uploadImage,
        )
        self.button.grid(row=1, column=0, pady=10)

        # Define empty label for recommended words
        self.label = customtkinter.CTkLabel(
            self.app,
            font=("Helvetica", 24),
            text="",
            text_color="#ffffff",
        )
        self.label.grid(row=2, column=0, padx=20, pady=20)

        self.app.mainloop()

    # Press method when upload button is pressed
    def uploadImage(self):
        filepath = customtkinter.filedialog.askopenfilename(
            title="Select Image",
            filetypes=(
                ("png images", "*.png"),
                ("jpg images", "*.jpg"),
                ("jpeg images", "*.jpeg"),
            ),
        )

        # If user closes file dialog
        if not filepath:
            return

        # Do analyzing and solving logic
        analyzer = ImageAnalyzer()
        solver = WordleSolver()
        letters = analyzer.analyzeImage(filepath)

        suggestedWords = solver.suggestWords(letters)

        self.displayWords(suggestedWords)

    # Display suggested words in the empty label and update button text
    def displayWords(self, words):
        words = "\n".join(words)
        self.button.configure(text="Upload New")

        self.label.configure(text=words)
