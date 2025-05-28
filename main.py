from graphics import Window, Point, Line
from field import Cell, Maze

def main():
    # MTEST- 200 moves
    numRows = 8
    numCols = 8
    grid = 48
    win = Window(numCols * grid + 20, numRows * grid + 20, grid)
    maze = Maze(10, 10,         # x1, y1 starting offset
                numRows,        # numberOfRows
                numCols,        # numberOfColumns
                grid,           # cellSize
                0.0000001,       # sleep seconds
                win,
                2477)           # seed

    # EASY - 100 moves
    # numRows = 12
    # numCols = 12
    # grid = 75
    # win = Window(numCols * grid + 20, numRows * grid + 20, grid)
    # maze = Maze(10, 10,       # starting offset
    #             numRows,      # numberOfRows
    #             numCols,      # numberOfColumns
    #             grid,         # cellSize
    #             0.000001,     # delay between steps
    #             win,
    #             14594)        # seed

    # MEDIUM - 200 moves
    # numRows = 20
    # numCols = 20
    # grid = 45
    # win = Window(numCols * grid + 20, numRows * grid + 20, grid)
    # maze = Maze(10, 10,         # x1, y1 starting offset
    #             numRows,        # numberOfRows
    #             numCols,        # numberOfColumns
    #             grid,           # cellSize
    #             0.0000001,       # sleep seconds
    #             win,
    #             2477)           # seed


    # DIFFICULT - 750 moves
    # numRows = 40
    # numCols = 40
    # grid = 30
    # win = Window(numCols * grid + 20, numRows * grid + 20, grid)
    # maze = Maze(10, 10,         # x1, y1 starting offset
    #             numRows,        # numberOfRows
    #             numCols,        # numberOfColumns
    #             grid,           # cellSize
    #             0.000001,       # sleep seconds
    #             win,            # window
    #             2186)           # seed


    maze.solve()

    win.awaitClose()

main()
