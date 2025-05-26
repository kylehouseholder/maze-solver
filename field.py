import random
from enum import Enum
from time import sleep
from graphics import Window, Point, Line


class Move(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Tried(Enum):
    NO = 0
    YES = 1
    RETRY = 2


class Maze:
    def __init__(self, x1, y1,
                 numberOfRows, numberOfColumns,
                 cellWidth, cellHeight, time=0.005,
                 window=None, seed=None):
        if seed is not None:
            random.seed(seed)
        self.__x1, self.__y1 = x1, y1
        self.nRows = numberOfRows
        self.nCols = numberOfColumns
        self.__cellH = cellHeight
        self.__cellW = cellWidth
        self.__win = window
        self.__sec = time
        self.cells = []
        self.__buildMaze()
        self.__breakEnds()
        self.__breakWalls(0, 0)
        self.__resetCells()
        
        self.__player = Player(self.__win, 0, 0, self)
        if self.__win:
            self.__win.setKeyCallback(self.playerMove)

    def __animate(self):
        if self.__win:
            self.__win.redraw()
        sleep(self.__sec)

    def __buildMaze(self):
        for row in range(self.nRows):
            rowCells = []
            for col in range(self.nCols):
                rowCells.append(Cell(self.__win, row, col))
            self.cells.append(rowCells)
        for row in range(self.nRows):
            for col in range(self.nCols):
                self.__drawCell(row, col)

    def __drawCell(self, row, col):
        cx1 = col * self.__cellW + self.__x1
        cx2 = cx1 + self.__cellW
        cy1 = row * self.__cellH + self.__y1
        cy2 = cy1 + self.__cellH
        self.cells[row][col].draw(cx1, cy1, cx2, cy2)
        self.__animate()

    def __breakEnds(self):
        self.cells[0][0].hasTopWall = False
        self.__drawCell(0, 0)
        exitCell = self.cells[self.nRows - 1][self.nCols - 1]
        exitCell.hasBottomWall = False
        self.__drawCell(self.nRows - 1, self.nCols - 1)

    def __breakWalls(self, row, col):
        currentCell = self.cells[row][col]
        currentCell.visited = True

        while True:
            neighbors = []

            if row > 0 and not self.cells[row - 1][col].visited:
                neighbors.append((Move.UP, row - 1, col))
            if col > 0 and not self.cells[row][col - 1].visited:
                neighbors.append((Move.LEFT, row, col - 1))
            if row < (self.nRows - 1) and not self.cells[row + 1][col].visited:
                neighbors.append((Move.DOWN, row + 1, col))
            if col < (self.nCols - 1) and not self.cells[row][col + 1].visited:
                neighbors.append((Move.RIGHT, row, col + 1))

            if not neighbors:
                self.__drawCell(row, col)
                return

            direction, nextRow, nextCol = random.choice(neighbors)
            nextCell = self.cells[nextRow][nextCol]

            if direction == Move.LEFT:
                currentCell.hasLeftWall, nextCell.hasRightWall = False, False
            elif direction == Move.RIGHT:
                currentCell.hasRightWall, nextCell.hasLeftWall = False, False
            elif direction == Move.UP:
                currentCell.hasTopWall, nextCell.hasBottomWall = False, False
            elif direction == Move.DOWN:
                currentCell.hasBottomWall, nextCell.hasTopWall = False, False

            self.__drawCell(row, col)
            self.__drawCell(nextRow, nextCol)
            self.__breakWalls(nextRow, nextCol)

    def __resetCells(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        return self.__solver(0, 0)

    def __solver(self, row, col):
        self.__animate()
        moves = [Move.RIGHT, Move.LEFT, Move.UP, Move.DOWN]
        currentCell = self.cells[row][col]
        currentCell.visited = True
        exitCell = self.cells[self.nRows - 1][self.nCols - 1]

        if currentCell == exitCell:
            return True

        sleep(self.__sec * 35)
        for move in moves:
            if move == Move.RIGHT and col < (self.nCols - 1):
                nextRow, nextCol = row, col + 1
                nextCell = self.cells[nextRow][nextCol]
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
            if move == Move.LEFT and col > 0:
                nextRow, nextCol = row, col - 1
                nextCell = self.cells[nextRow][nextCol]
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
            if move == Move.UP and row > 0:
                nextRow, nextCol = row - 1, col
                nextCell = self.cells[nextRow][nextCol]
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
            if move == Move.DOWN and row < (self.nRows - 1):
                nextRow, nextCol = row + 1, col
                nextCell = self.cells[nextRow][nextCol]
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
        print(f"Moving {direction}...")
        if self.__player.isMoveValid(direction):
            self.__player.move(direction)
        self.__animate()
        self.__win.redraw()
    
    def __drawCellWalls(self, row, col):
        x1 = col * self.__cellW + self.__x1
        x2 = x1 + self.__cellW
        y1 = row * self.__cellH + self.__y1
        y2 = y1 + self.__cellH
        self.cells[row][col].draw(x1, y1, x2, y2, animate=False)

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
        self.tried = Tried.NO

    def draw(self, x1, y1, x2, y2, animate=True):
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
    def __init__(self, window, x, y, maze):
        self.window = window
        self.row = 0
        self.col = 0
        self.color = "blue"
        self.size = 24
        self.maze = maze
        self.currentCell = self.maze.cells[self.row][self.col]
        self.draw()

    def getPosition(self):
        return self.currentCell.ctr
    
    def draw(self):
        center = self.getPosition()
        self.window.drawPlayer(
            center.x - self.size//2,
            center.y - self.size//2, 
            self.size, 
            self.color
        )
    
    def move(self, direction):
        if self.isMoveValid(direction):
            oldPosition = self.getPosition()
            
            if direction == "up":
                self.row -= 1
            elif direction == "down":
                self.row += 1
            elif direction == "left":
                self.col -= 1
            elif direction == "right":
                self.col += 1
            
            self.currentCell = self.maze.cells[self.row][self.col]
            self.currentCell.tried = Tried.YES
            
            newPosition = self.getPosition()
            self.window.animatePlayer(oldPosition, newPosition)
            
            print(f"Move: ({self.row}, {self.col})")
            print(f"Cell walls - Top: {self.currentCell.hasTopWall}")
            print(f"Bottom: {self.currentCell.hasBottomWall}")
            print(f"Left: {self.currentCell.hasLeftWall}")  
            print(f"Right: {self.currentCell.hasRightWall}")
        else:
            print(f"Invalid move {direction}")
            print(f"Current cell: ({self.row}, {self.col})")

    def isMoveValid(self, direction):
        if direction == "up":
            if self.row <= 0:
                print(f"Invalid move {direction}, already at top edge of maze.")
                return False
            elif self.currentCell.hasTopWall:
                print(f"Invalid move {direction}, blocked by top wall.")
                return False
            else:
                return True
        elif direction == "down":
            if self.row >= self.maze.nRows - 1:
                print(f"Invalid move {direction}, already at bottom edge of maze.")
                return False
            elif self.currentCell.hasBottomWall:
                print(f"Invalid move {direction}, blocked by bottom wall.")
                return False
            else:
                return True
        elif direction == "left":
            if self.col <= 0:
                print(f"Invalid move {direction}, already at left edge of maze.")
                return False
            elif self.currentCell.hasLeftWall:
                print(f"Invalid move {direction}, blocked by left wall.")
                return False
            else:
                return True
        elif direction == "right":
            if self.col >= self.maze.nCols - 1:
                print(f"Invalid move {direction}, already at right edge of maze.")
                return False
            elif self.currentCell.hasRightWall:
                print(f"Invalid move {direction}, blocked by right wall.")
                return False
            else:
                return True
        return False