import customtkinter
from solver import WordleSolver


class SolverGui:

    # Initializes gui, sets default settings
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title("wordle-solver")
        self.app.geometry("400x400")
        self.app.resizable(False, False)
        self.app.grid_columnconfigure(0, weight=1)

        self.button = customtkinter.CTkButton(
            self.app, text="Upload", command=self.uploadImage
        )
        self.button.grid(row=0, column=0, padx=20, pady=20)

        self.label = customtkinter.CTkLabel(self.app, text="")
        self.label.grid(row=1, column=0, padx=20, pady=20)

        self.app.mainloop()

    def uploadImage(self):
        filepath = customtkinter.filedialog.askopenfilename(
            title="Select Image",
            filetypes=(
                ("png images", "*.png"),
                ("jpg images", "*.jpg"),
                ("jpeg images", "*.jpeg"),
            ),
        )

        suggestedWords = WordleSolver.analyzeImage(filepath)
        self.displayWords(suggestedWords)

    def displayWords(self, words):
        self.button.configure(text="Upload New")

        self.label.configure(text=words)
