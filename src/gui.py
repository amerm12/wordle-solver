import customtkinter
from analyzer import ImageAnalyzer
from solver import WordleSolver
from CTkToolTip import *
from CTkMessagebox import CTkMessagebox
from analyzer import AnalyzerError
from solver import SolverError


class SolverGui:

    # Initializes gui, sets default settings
    def __init__(self):
        self.solver = WordleSolver()
        self.analyzer = ImageAnalyzer()
        self.createApp()
        self.createWidgets()
        self.app.mainloop()

    # Creates app and defines base properties
    def createApp(self):
        self.app = customtkinter.CTk(fg_color="#121213")
        self.app.title("wordle-solver")
        self.app.geometry(self.centerWindow(500, 600, self.app._get_window_scaling()))
        self.app.resizable(False, False)
        self.app.grid_columnconfigure(0, weight=1)

    # Creates all widgets inside of the main window, and places them using grid placement
    def createWidgets(self):
        # Define label for logo
        self.logoLabel = customtkinter.CTkLabel(
            self.app,
            font=("Helvetica Neue", 50, "bold"),
            text="wordle-solver",
            text_color="#538d4e",
        )
        self.logoLabel.grid(row=0, column=0, pady=30, columnspan=2)

        # Define start new game button
        self.startButton = customtkinter.CTkButton(
            self.app,
            text="New Game",
            font=("Helvetica", 24, "bold"),
            width=200,
            height=60,
            fg_color="#74a67a",
            hover_color="#5f8c5c",
            text_color="#ffffff",
            command=self.startGame,
        )
        self.startButton.grid(
            row=1,
            column=0,
            padx=(30, 0),
            pady=10,
            columnspan=1,
            sticky="w",
        )

        # Define tooltip for start new game button using CTkToolTip library
        CTkToolTip(
            self.startButton,
            delay=0.2,
            message="Get 3 best words to start with",
            x_offset=15,
            y_offset=-25,
        )

        # Define upload button
        self.uploadButton = customtkinter.CTkButton(
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
        self.uploadButton.grid(
            row=1,
            column=1,
            padx=(0, 30),
            pady=10,
            columnspan=1,
            sticky="w",
        )

        # Define tooltip for upload button using CTkToolTip library
        CTkToolTip(
            self.uploadButton,
            delay=0.2,
            message="Get best words for uploaded image",
            x_offset=15,
            y_offset=-25,
        )

        # Crates 3 same frames and labels for displaying recommended words
        self.wordFrames = []
        self.wordLabels = []
        for i in range(3):
            wordFrame = customtkinter.CTkFrame(self.app, height=60, fg_color="#242526")
            wordFrame.grid_columnconfigure(0, weight=1)
            wordFrame.grid_propagate(False)

            wordLabel = customtkinter.CTkLabel(
                wordFrame,
                font=("Helvetica Neue", 24, "bold"),
            )
            wordLabel.place(relx=0.5, rely=0.5, anchor="center")

            self.wordFrames.append(wordFrame)
            self.wordLabels.append(wordLabel)

    # Display starting words in the empty label
    def startGame(self):
        try:
            startingWords = self.solver.fetchStartingWords()
        except SolverError as e:
            self.showError(str(e))
            return

        self.displayWords(startingWords)

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

        try:
            letters = self.analyzer.analyzeImage(filepath)
        except AnalyzerError as e:
            self.showError(str(e))
            return

        try:
            suggestedWords = self.solver.suggestWords(letters)
        except SolverError as e:
            self.showError(str(e))
            return

        self.displayWords(suggestedWords)

    # Display suggested words in the labels
    def displayWords(self, words):
        for i, frame in enumerate(self.wordFrames):
            label = self.wordLabels[i]
            if i < len(words):
                label.configure(text=words[i].upper())
                frame.grid(
                    row=3 + i, column=0, pady=(30 if i == 0 else 10, 0), columnspan=2
                )
            else:
                frame.grid_forget()

    # Show error box with passed message using CTkMessagebox library
    def showError(self, message):
        CTkMessagebox(title="Error", message=message, icon="cancel")

    # Centers root window to the center of the user's screen
    def centerWindow(
        self,
        width: int,
        height: int,
        scale_factor: float = 1.0,
    ):
        screenWidth = self.app.winfo_screenwidth()
        screenHeight = self.app.winfo_screenheight()
        x = int(((screenWidth / 2) - (width / 2)) * scale_factor)
        y = int(((screenHeight / 2) - (height / 1.5)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"
