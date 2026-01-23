import customtkinter
from CTkToolTip import *
from CTkMessagebox import CTkMessagebox
from solver import WordleSolver, SolverError
from analyzer import ImageAnalyzer, AnalyzerError, DarkImageAnalyzer, LightImageAnalyzer
from screenSelector import ScreenSelector, SelectorError
import cv2
import numpy as np
from PIL import Image
import os


class SolverGui:

    # Initializes gui, sets default settings
    def __init__(self):
        self.solver = WordleSolver()
        self.mode = "dark"
        """ self.darkAnalyzer = DarkImageAnalyzer()
        self.lightAnalyzer = LightImageAnalyzer() """
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
        self.logoLabel.grid(row=0, column=0, pady=30, columnspan=3)

        # Define start new game button
        self.startButton = customtkinter.CTkButton(
            self.app,
            text="New Game",
            font=("Helvetica", 24, "bold"),
            width=180,
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

        # Load icon for screenshot button
        img = Image.open(
            "C:/Users/amera/OneDrive/Desktop/Skafiskafnjak/Amer/wordle-solver/assets/icons/screenshot.png"
        )
        icon = customtkinter.CTkImage(
            light_image=img,
            size=(50, 50),
        )

        # Define screenshot button
        self.screenshotButton = customtkinter.CTkButton(
            self.app,
            text="",
            image=icon,
            width=60,
            height=60,
            fg_color="#74a67a",
            hover_color="#213020",
            command=self.takeScreenshot,
        )
        self.screenshotButton.grid(
            row=1,
            column=1,
            columnspan=1,
            padx=10,
            pady=10,
        )

        # Define tooltip for screenshot button using CTkToolTip library
        CTkToolTip(
            self.screenshotButton,
            delay=0.2,
            message="Take a screenshot",
            x_offset=15,
            y_offset=-25,
        )

        # Define upload button
        self.uploadButton = customtkinter.CTkButton(
            self.app,
            text="Upload",
            font=("Helvetica", 24, "bold"),
            width=180,
            height=60,
            fg_color="#74a67a",
            hover_color="#5f8c5c",
            text_color="#ffffff",
            command=self.uploadImage,
        )
        self.uploadButton.grid(
            row=1,
            column=2,
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

        # Define switch for changing themes
        self.switchTheme = customtkinter.CTkSwitch(
            self.app, text="Dark", command=self.toggleMode
        )
        self.switchTheme.place(relx=0.98, rely=0.98, anchor="se")
        self.switchTheme.deselect()
        self.applyTheme()

    # Display starting words in the empty label
    def startGame(self):
        try:
            startingWords = self.solver.fetchStartingWords()
        except SolverError as e:
            self.showError(str(e))
            return

        self.displayWords(startingWords)

    # Press method when screenshot button is pressed
    def takeScreenshot(self):
        try:
            ScreenSelector(self.app, self.processImage)
        except SelectorError as e:
            self.showError(str(e))
            return

    # Based on passed image or screenshot displays next best 3 words
    def processImage(self, _image):
        # If screenshot
        if isinstance(_image, np.ndarray):
            img = _image
        # If uploaded image
        else:
            if not os.path.exists(_image):
                raise AnalyzerError("File not found.")

            img = cv2.imread(_image)

        try:
            letters = self.analyzer.analyzeImage(img, self.mode)
            """ if self.mode == "dark":
                letters = self.darkAnalyzer.analyzeImage(img)
            elif self.mode == "light":
                letters = self.lightAnalyzer.analyzeImage(img) """
        except AnalyzerError as e:
            self.showError(str(e))
            return

        try:
            suggestedWords = self.solver.suggestWords(letters)
        except SolverError as e:
            self.showError(str(e))
            return

        self.displayWords(suggestedWords)

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

        self.processImage(filepath)

    # Display suggested words in the labels
    def displayWords(self, words):
        for i, frame in enumerate(self.wordFrames):
            label = self.wordLabels[i]
            if i < len(words):
                label.configure(text=words[i].upper())
                frame.grid(
                    row=3 + i, column=0, pady=(30 if i == 0 else 10, 0), columnspan=3
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

    # Change to appropriate colors based on the mode
    # Completely written by Al because I was lazy to make designs at 2am
    def applyTheme(self):
        if self.mode == "dark":
            customtkinter.set_appearance_mode("dark")
            self.app.configure(fg_color="#121213")

            logo_color = "#538d4e"
            frame_color = "#242526"
            btn_color = "#74a67a"
            btn_hover = "#5f8c5c"
            btn_text = "#ffffff"

        else:
            customtkinter.set_appearance_mode("light")

            self.app.configure(fg_color="#FAFAFA")

            logo_color = "#538d4e"

            frame_color = "#ffffff"
            frame_border_color = "#D3D6DA"

            btn_color = "#538d4e"
            btn_hover = "#467a42"
            btn_text = "#ffffff"

        if hasattr(self, "logoLabel"):
            self.logoLabel.configure(text_color=logo_color)

        for name in ("startButton", "screenshotButton", "uploadButton"):
            if hasattr(self, name):
                btn = getattr(self, name)
                btn.configure(
                    fg_color=btn_color,
                    hover_color=btn_hover,
                    text_color=btn_text,
                )

        if hasattr(self, "wordFrames"):
            for fr in self.wordFrames:
                fr.configure(fg_color=frame_color)

                if self.mode == "light":
                    fr.configure(border_color=frame_border_color, border_width=1)
                else:
                    fr.configure(border_width=0)

            # buttons
            for name in ("startButton", "screenshotButton", "uploadButton"):
                if hasattr(self, name):
                    btn = getattr(self, name)
                    btn.configure(
                        fg_color=btn_color,
                        hover_color=btn_hover,
                        text_color=btn_text,
                    )

                    if self.mode == "light":
                        btn.configure(border_color=frame_border_color, border_width=1)

            if hasattr(self, "wordFrames"):
                for fr in self.wordFrames:
                    fr.configure(fg_color=frame_color)

                    if self.mode == "light":
                        fr.configure(border_color=frame_border_color, border_width=1)

    def toggleMode(self):
        if self.mode == "dark":
            self.mode = "light"
        else:
            self.mode = "dark"

        self.switchTheme.configure(text="Dark" if self.mode == "dark" else "Light")
        self.applyTheme()

        messageText = "Switching mode will influence how image is processes. Make sure you're using same mode as the game is in screenshots. "
        CTkMessagebox(title="Note", message=messageText, icon="info")
