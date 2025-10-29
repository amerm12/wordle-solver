import tkinter as tk
from tkinter import filedialog

class SolverGui:

    # Initializes gui and frames, sets default settings
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("wordle-solver")

        self.uploadButton = tk.Button(self.root, text="Upload", command=self.uploadScreenshot)

        self.uploadButton.pack()

        self.root.mainloop()

    def uploadScreenshot(self):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        return filename