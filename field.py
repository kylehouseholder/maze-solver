from graphics import Window, Point, Line
from time import sleep
import random


class Maze:
    def __init__(self, x1, y1, numberOfRows, numberOfColumns,
                 cellWidth, cellHeight, window=None, seed=None):
        self.__x1, self.__y1 = x1, y1
        self.__nRows = numberOfRows
        self.__nCols = numberOfColumns
        self.__cellH = cellHeight
        self.__cellW = cellWidth
        self.__win = window
        self.__cells = []
        self.__buildMaze()
        self.__breakEnds()
        if seed:
            random.seed(a=seed)

    def __buildMaze(self):
        for row in range(self.__nRows):
            rowCells = []
            for col in range(self.__nCols):
                rowCells.append(Cell(self.__win))
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
        self.__drawCell(row=0, col=0)
        exitCell = self.__cells[self.__nRows - 1][self.__nCols - 1]
        exitCell.hasBottomWall = False
        self.__drawCell(row=self.__nRows - 1, col=self.__nCols - 1)

    def __animate(self):
        if self.__win:
            self.__win.redraw()
        sleep(0.0025)


class Cell:
    def __init__(self, window):
        self.__win = window
        self.hasLeftWall, self.hasRightWall = True, True
        self.hasTopWall, self.hasBottomWall = True, True
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
