import time
import math
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height, size):
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
        self.cellSize = size
        self.playerSize = self.cellSize // 3

        self.isAnimating = False
        self.startPos = None
        self.endPos = None
        self.animationProgress = 0.0
        self.animationStartTime = None
        self.animationDuration = 0.222

        self.isBouncing = False
        self.bounceStartTime = None
        self.bounceDuration = 0.25
        self.bounceRestDuration = 0.075
        self.bounceColorDuration = 1.0
        self.bounceDirection = None
        self.bounceStartPos = None
        self.bounceImpactPos = None

        self.wallThickness = 2

    def setKeyCallback(self, callbackFunction):
        self.__keyCallback = callbackFunction

    def keyHandler(self, event):
        key = event.keysym.lower()
        direction = None
        
        if key == "up":
            direction = "up"
        elif key == "down":
            direction = "down"
        elif key == "left":
            direction = "left"
        elif key == "right":
            direction = "right"
        elif key == "w":
            direction = "up"
        elif key == "s":
            direction = "down"
        elif key == "a":
            direction = "left"
        elif key == "d":
            direction = "right"
        elif key == "k":
            direction = "up"
        elif key == "j":
            direction = "down"
        elif key == "h":
            direction = "left"
        elif key == "l":
            direction = "right"
        
        if direction and self.__keyCallback:
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

    def animateBounce(self, playerPos, direction, cellSize):
        self.bounceStartPos = playerPos
        self.bounceDirection = direction
        self.bounceStartTime = time.time()
        self.isBouncing = True

        distanceToWallInnerEdge = (cellSize // 2)
        playerRadius = self.cellSize // 3
        overlapAmount = 2
        bounceDistance = distanceToWallInnerEdge - playerRadius + overlapAmount
        
        if direction == "up":
            self.bounceImpactPos = Point(playerPos.x, playerPos.y - bounceDistance)
        elif direction == "down":
            self.bounceImpactPos = Point(playerPos.x, playerPos.y + bounceDistance)
        elif direction == "left":
            self.bounceImpactPos = Point(playerPos.x - bounceDistance, playerPos.y)
        elif direction == "right":
            self.bounceImpactPos = Point(playerPos.x + bounceDistance, playerPos.y)
        
        self.redraw()

    def updateAnimation(self):
        if self.isAnimating:
            elapsed = time.time() - self.animationStartTime
            if elapsed >= self.animationDuration:
                self.isAnimating = False
                self.drawPlayer(self.endPos.x - self.playerSize//2,
                                self.endPos.y - self.playerSize//2, self.playerSize, "yellow")
                return

            self.animationProgress = elapsed / self.animationDuration

            x = self.startPos.x + (self.endPos.x - self.startPos.x) * self.calcEasing(self.animationProgress)
            y = self.startPos.y + (self.endPos.y - self.startPos.y) * self.calcEasing(self.animationProgress)

            self.drawPlayer(x - self.playerSize//2, y - self.playerSize//2, self.playerSize, "yellow")
        
        elif self.isBouncing:
            elapsed = time.time() - self.bounceStartTime
            totalDuration = self.bounceDuration + self.bounceRestDuration
            
            if elapsed >= totalDuration:
                self.isBouncing = False
                self.drawPlayer(self.bounceStartPos.x - self.playerSize//2,
                                self.bounceStartPos.y - self.playerSize//2, self.playerSize, "yellow")
                return
            
            if elapsed <= self.bounceDuration:
                progress = elapsed / self.bounceDuration
                self._updateBounceMovement(progress)
            else:
                restProgress = (elapsed - self.bounceDuration) / self.bounceRestDuration
                color = self._calculateBounceColor(elapsed)
                self.drawPlayer(self.bounceStartPos.x - self.playerSize//2,
                                self.bounceStartPos.y - self.playerSize//2, self.playerSize, color)

    def calcEasing(self, progress):
        return 0.5 - math.cos(progress * math.pi) / 2

    def _updateBounceMovement(self, progress):
        if progress <= 0.4:
            phase_progress = progress / 0.4
            x = self.bounceStartPos.x + (self.bounceImpactPos.x - self.bounceStartPos.x) * phase_progress
            y = self.bounceStartPos.y + (self.bounceImpactPos.y - self.bounceStartPos.y) * phase_progress
            self.drawPlayer(x - self.playerSize//3, y - self.playerSize//3, self.playerSize, "yellow")
        
        elif progress <= 0.6:
            width, height = self._calculateDistortion()
            offset_x, offset_y = self._calculateDistortionOffset(width, height)
            self.drawPlayer(self.bounceImpactPos.x + offset_x,
                            self.bounceImpactPos.y + offset_y, width, "red", height)
        
        else:
            phase_progress = (progress - 0.6) / 0.4
            x = self.bounceImpactPos.x + (self.bounceStartPos.x - self.bounceImpactPos.x) * phase_progress
            y = self.bounceImpactPos.y + (self.bounceStartPos.y - self.bounceImpactPos.y) * phase_progress
            color = self._calculateBounceColor(progress * self.bounceDuration)
            self.drawPlayer(x - self.playerSize//3, y - self.playerSize//3, self.playerSize, color)

    def _calculateDistortion(self):
        if self.bounceDirection in ["up", "down"]:
            return self.playerSize, self.playerSize//3
        else:
            return self.playerSize//3, self.playerSize

    def _calculateDistortionOffset(self, width, height):
        return -width // 2, -height // 2

    def _calculateBounceColor(self, elapsed):
        if elapsed >= self.bounceColorDuration:
            return "blue"
        
        progress = elapsed / self.bounceColorDuration
        if progress < 0.5:
            return "red"
        else:
            return "blue"

    def drawLine(self, line, fill_color="white"):
        line.draw(self.__canvas, fill_color)

    def drawPlayer(self, x, y, width, color, height=None):
        if height is None:
            height = width
        
        if self.playerID is None:
            self.playerID = self.__canvas.create_oval(x, y, x + width, y + height, fill=color)
        else:
            self.__canvas.coords(self.playerID, x, y, x + width, y + height)
            self.__canvas.itemconfig(self.playerID, fill=color)

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
