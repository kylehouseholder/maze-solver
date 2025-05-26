from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(
            self.__root, bg="black", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        
        # Add keyboard handling
        self.__root.focus_set()
        self.__root.bind("<Key>", self.keyHandler)
        self.__keyCallback = None

    def setKeyCallback(self, callbackFunction):
        """Allow someone else to register for key events"""
        self.__keyCallback = callbackFunction

    def keyHandler(self, event):
        if (
            event.keysym == "Up" or
            event.keysym == "Down" or
            event.keysym == "Left" or
            event.keysym == "Right"
        ):
            if self.__keyCallback:
                self.__keyCallback(event.keysym)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def awaitClose(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed...")

    def close(self):
        self.__running = False

    def drawLine(self, line, fill_color="white"):
        line.draw(self.__canvas, fill_color)

    def drawPlayer(self, x, y, width, color):
        self.__canvas.create_oval(x, y, x + width, y + width, fill=color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2

    def draw(self, canvas, fill_color="white"):
        canvas.create_line(
            self.pt1.x, self.pt1.y,
            self.pt2.x, self.pt2.y,
            fill=fill_color,
            width=2)
