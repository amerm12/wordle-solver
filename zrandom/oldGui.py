import tkinter as tk
import tkinter.font as tkFont

class SolverGui:

    # Initializes gui and frames, sets default settings
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("wordle-solver")

        # Initial Screen - Game not visible on the screen
        self.frameInitial = tk.Frame(self.root, bg="black") 
        self.labelGameNotVisible = tk.Label(self.frameInitial, text="Wordle game not visible on the screen!", font=tkFont.Font(size=20))
        self.labelGameNotVisible.pack(pady=20)

        # Main Screen
        self.frameMain = tk.Frame(self.root, bg="red")
        self.labelMain = tk.Label(self.frameMain, text="test")
        self.labelMain.pack(pady=20)

        #End Screen
        self.frameEnd = tk.Frame(self.root, bg="blue")
        self.labelEnd = tk.Label(self.frameEnd, text="test")
        self.labelEnd.pack(pady=20)

        for frame in (self.frameInitial, self.frameMain, self.frameEnd):
            frame.place(relwidth=1, relheight=1)
        self.showFrame(self.frameInitial)

    # Opens gui 
    def start(self):
        self.root.mainloop()

    # Loads Inital screen
    def loadInitialScreen(self):
        self.showFrame(self.frameInitial)

    # Load Main screen
    def loadMainScreen(self):
        self.showFrame(self.frameMain)

    # Load End screen
    def loadEndScreen(self):
        self.showFrame(self.frameEnd)

    # Show given frame, used to load specific screen
    def showFrame(self, frame):
        frame.tkraise()