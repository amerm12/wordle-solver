import customtkinter
from PIL import ImageGrab


class SelectorError(Exception):
    pass


class ScreenSelector(customtkinter.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)

        self.callback = callback

        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.3)
        self.configure(bg="black")
        self.bind("<Escape>", lambda e: self.destroy())

        self.canvas = customtkinter.CTkCanvas(self, cursor="cross", bg="black")
        self.canvas.pack(fill=customtkinter.BOTH, expand=True)

        self.startX = None
        self.startY = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.onClick)
        self.canvas.bind("<B1-Motion>", self.onDrag)
        self.canvas.bind("<ButtonRelease-1>", self.onRelease)

    def onClick(self, event):
        self.startX = self.canvas.canvasx(event.x)
        self.startY = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(
            self.startX,
            self.startY,
            self.startX,
            self.startY,
            outline="#538d4e",
            width=3,
        )

    def onDrag(self, event):
        curX, curY = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.startX, self.startY, curX, curY)

    def onRelease(self, event):
        endX = self.canvas.canvasx(event.x)
        endY = self.canvas.canvasy(event.y)

        x1 = int(min(self.startX, endX))
        y1 = int(min(self.startY, endY))
        x2 = int(max(self.startX, endX))
        y2 = int(max(self.startY, endY))

        self.destroy()

        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        if not screenshot:
            raise SelectorError("Could not take a screenshot. Try again.")

        self.callback(screenshot)
