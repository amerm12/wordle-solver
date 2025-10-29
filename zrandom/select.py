import tkinter as tk

class ScreenSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)        # Fullscreen overlay
        self.root.attributes("-alpha", 0.3)              # Make it semi-transparent
        self.root.configure(bg="black")
        self.root.bind("<Escape>", lambda e: self.root.destroy())  # Exit on Esc

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.root.mainloop()

    def on_click(self, event):
        # Save starting point
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # Create rectangle
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=3)

    def on_drag(self, event):
        # Update rectangle while dragging
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        # Final rectangle coordinates
        end_x, end_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
        w, h = x2 - x1, y2 - y1

        print(f"Selected region: x={x1}, y={y1}, width={w}, height={h}")
        self.root.destroy()   # Close overlay

# Run it
ScreenSelector()