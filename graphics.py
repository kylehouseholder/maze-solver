import time
import math
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
        
        self.__root.focus_set()
        self.__root.bind("<Key>", self.keyHandler)
        self.__keyCallback = None

        self.playerID = None

        self.startPos = None
        self.endPos = None
        self.animationProgress = 0.0
        self.animationStartTime = None
        self.animationDuration = 0.222  # seconds
        self.isAnimating = False

    def setKeyCallback(self, callbackFunction):
        self.__keyCallback = callbackFunction

    def keyHandler(self, event):
        if (
            event.keysym == "Up" or
            event.keysym == "Down" or
            event.keysym == "Left" or
            event.keysym == "Right"
        ):
            if self.__keyCallback:
                direction = event.keysym.lower()
                self.__keyCallback(direction)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def animatePlayer(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos
        self.animationProgress = 0.0
        self.animationStartTime = time.time()
        self.isAnimating = True

        self.redraw()

    def updateAnimation(self):
        if not self.isAnimating:
            return

        elapsed = time.time() - self.animationStartTime
        if elapsed >= self.animationDuration:
            self.isAnimating = False
            # Draw player at final position
            self.drawPlayer(self.endPos.x - 12, self.endPos.y - 12, 24, "blue")
            return

        self.animationProgress = elapsed / self.animationDuration

        x = self.startPos.x + (self.endPos.x - self.startPos.x) * self.calcEasing(self.animationProgress)
        y = self.startPos.y + (self.endPos.y - self.startPos.y) * self.calcEasing(self.animationProgress)

        # Draw player at interpolated position (offset by half size to center)
        self.drawPlayer(x - 12, y - 12, 24, "blue")
    
    def calcEasing(self, progress):
        return 0.5 - math.cos(progress * math.pi) / 2

    def drawLine(self, line, fill_color="white"):
        line.draw(self.__canvas, fill_color)

    def drawPlayer(self, x, y, width, color):
        if self.playerID is None:
            self.playerID = self.__canvas.create_oval(x, y, x + width, y + width, fill=color)
        else:
            self.__canvas.coords(self.playerID, x, y, x + width, y + width)

    def awaitClose(self):
        self.__running = True
        while self.__running:
            self.updateAnimation()
            self.redraw()
        print("Window closed...")

    def close(self):
        self.__running = False


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
