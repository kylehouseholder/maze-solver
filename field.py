from graphics import Window, Point, Line
from time import sleep
import random


class Maze:
    def __init__(self, x1, y1,
                 numberOfRows, numberOfColumns,
                 cellWidth, cellHeight, time=0.005,
                 window=None, seed=None):
        if seed is not None:
            random.seed(seed)
        self.__x1, self.__y1 = x1, y1
        self.__nRows = numberOfRows
        self.__nCols = numberOfColumns
        self.__cellH = cellHeight
        self.__cellW = cellWidth
        self.__win = window
        self.__sec = time
        self.__cells = []
        self.__buildMaze()
        self.__breakEnds()
        self.__breakWalls(0, 0)
        self.__resetCells()
        
        # Create player and set up keyboard callback
        self.__player = Player(self.__win, 0, 0)
        if self.__win:
            self.__win.setKeyCallback(self.playerMove)
        
        # Create player and set up keyboard callback
        self.__player = Player(self.__win, 0, 0)
        if self.__win:
            self.__win.setKeyCallback(self.playerMove)

    def __animate(self):
        if self.__win:
            self.__win.redraw()
        sleep(self.__sec)

    def __buildMaze(self):
        for row in range(self.__nRows):
            rowCells = []
            for col in range(self.__nCols):
                rowCells.append(Cell(self.__win, row, col))
            self.__cells.append(rowCells)
        for row in range(self.__nRows):
            for col in range(self.__nCols):
                self.__drawCell(row, col)

    def __drawCell(self, row, col):
        cx1 = col * self.__cellW + self.__x1
        cx2 = cx1 + self.__cellW
        cy1 = row * self.__cellH + self.__y1
        cy2 = cy1 + self.__cellH
        self.__cells[row][col].draw(cx1, cy1, cx2, cy2)
        self.__animate()

    def __breakEnds(self):
        self.__cells[0][0].hasTopWall = False
        self.__drawCell(0, 0)
        exitCell = self.__cells[self.__nRows - 1][self.__nCols - 1]
        exitCell.hasBottomWall = False
        self.__drawCell(self.__nRows - 1, self.__nCols - 1)

    def __breakWalls(self, row, col):
        currentCell = self.__cells[row][col]
        currentCell.visited = True

        while True:
            neighbors = []

            if row > 0 and not self.__cells[row - 1][col].visited:
                neighbors.append(("up", row - 1, col))
            if col > 0 and not self.__cells[row][col - 1].visited:
                neighbors.append(("left", row, col - 1))
            if row < (self.__nRows - 1) and not self.__cells[row + 1][col].visited:
                neighbors.append(("down", row + 1, col))
            if col < (self.__nCols - 1) and not self.__cells[row][col + 1].visited:
                neighbors.append(("right", row, col + 1))

            if not neighbors:
                self.__drawCell(row, col)
                return

            direction, nextRow, nextCol = random.choice(neighbors)
            nextCell = self.__cells[nextRow][nextCol]

            if direction == "left":
                currentCell.hasLeftWall, nextCell.hasRightWall = False, False
            elif direction == "right":
                currentCell.hasRightWall, nextCell.hasLeftWall = False, False
            elif direction == "up":
                currentCell.hasTopWall, nextCell.hasBottomWall = False, False
            elif direction == "down":
                currentCell.hasBottomWall, nextCell.hasTopWall = False, False

            self.__drawCell(row, col)
            self.__drawCell(nextRow, nextCol)
            self.__breakWalls(nextRow, nextCol)

    def __resetCells(self):
        for row in self.__cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        return self.__solver(0, 0)

    def __solver(self, row, col):
        self.__animate()
        moves = ["right", "left", "up", "down"]
        currentCell = self.__cells[row][col]
        currentCell.visited = True
        exitCell = self.__cells[self.__nRows - 1][self.__nCols - 1]

        if currentCell == exitCell:
            return True

        sleep(self.__sec * 35)
        for move in moves:
            if move == "right" and col < (self.__nCols - 1):
                nextRow, nextCol = row, col + 1
                nextCell = self.__cells[nextRow][nextCol]
                if (
                    currentCell.hasRightWall == False and 
                    nextCell.hasLeftWall == False and 
                    nextCell.visited == False
                ):
                    currentCell.path(nextCell)
                    if self.__solver(nextRow, nextCol):
                        return True
                    else:
                        currentCell.path(nextCell, undo = True)
            if move == "left" and col > 0:
                nextRow, nextCol = row, col - 1
                nextCell = self.__cells[nextRow][nextCol]
                if (
                    currentCell.hasLeftWall == False and 
                    nextCell.hasRightWall == False and 
                    nextCell.visited == False
                ):
                    currentCell.path(nextCell)
                    if self.__solver(nextRow, nextCol):
                        return True
                    else:
                        currentCell.path(nextCell, undo = True)
            if move == "up" and row > 0:
                nextRow, nextCol = row - 1, col
                nextCell = self.__cells[nextRow][nextCol]
                if (
                    currentCell.hasTopWall == False and 
                    nextCell.hasBottomWall == False and 
                    nextCell.visited == False
                ):
                    currentCell.path(nextCell)
                    if self.__solver(nextRow, nextCol):
                        return True
                    else:
                        currentCell.path(nextCell, undo = True)
            if move == "down" and row < (self.__nRows - 1):
                nextRow, nextCol = row + 1, col
                nextCell = self.__cells[nextRow][nextCol]
                if (
                    currentCell.hasBottomWall == False and 
                    nextCell.hasTopWall == False and 
                    nextCell.visited == False
                ):
                    currentCell.path(nextCell)
                    if self.__solver(nextRow, nextCol):
                        return True
                    else:
                        currentCell.path(nextCell, undo = True)
        return False

    def getPlayer(self):
        return self.__player
    
    def playerMove(self, direction):
        print(f"Player moving {direction}")
        # TODO: Add movement validation here
        self.__player.move(direction)

class Cell:
    def __init__(self, window, row, col):
        self.__win = window
        self.hasLeftWall, self.hasRightWall = True, True
        self.hasTopWall, self.hasBottomWall = True, True
        self.row = row
        self.col = col
        self.__x1, self.__y1 = -1, -1
        self.__x2, self.__y2 = -1, -1
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1, self.__y1 = x1, y1
        self.__x2, self.__y2 = x2, y2
        self.__width = self.__x2 - self.__x1
        self.__height = self.__y2 - self.__y1
        self.ctr = Point(
            self.__x1 + (self.__width / 2),
            self.__y1 + (self.__height / 2)
        )

        def wallToggle(point1, point2, wallExists):
            if self.__win:
                if wallExists:
                    self.__win.drawLine(Line(point1, point2))
                else:
                    self.__win.drawLine(Line(point1, point2), "black")

        wallToggle(Point(x1, y1), Point(x1, y2), self.hasLeftWall)
        wallToggle(Point(x2, y1), Point(x2, y2), self.hasRightWall)
        wallToggle(Point(x1, y2), Point(x2, y2), self.hasBottomWall)
        wallToggle(Point(x1, y1), Point(x2, y1), self.hasTopWall)

    def path(self, to_cell, undo=False):
        color = "green"
        if undo:
            color = "red"
        if self.__win:
            self.__win.drawLine(Line(self.ctr, to_cell.ctr), color)

class Player:
    def __init__(self, window, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.row = 0
        self.col = 0
        self.color = "green"
        self.width = 20
        self.height = 20
    
    def draw(self):
        self.window.drawPlayer(self.x, self.y, self.width, self.color)
    
    def move(self, direction):
        if direction == "Up":
            self.row -= 1
        elif direction == "Down":
            self.row += 1
        elif direction == "Left":
            self.col -= 1
        elif direction == "Right":
            self.col += 1
        self.x = self.col * self.width
        self.y = self.row * self.height
        self.draw()
