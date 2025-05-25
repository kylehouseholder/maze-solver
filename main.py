from graphics import Window, Point, Line
from field import Cell, Maze

def main():
    # test
    win = Window(1220, 1220)
    maze = Maze(10, 10,       # starting offset
                40, 40,       # rows, columns
                30, 30,       # cell dimensions
                0.000001,     # delay between steps
                win, 216)   # seed
    # DIFFICULT
    # win = Window(1220, 1220)
    # maze = Maze(10, 10,       # starting offset
    #             40, 40,       # rows, columns
    #             30, 30,       # cell dimensions
    #             0.000001,     # delay between steps
    #             win, 2186)   # seed
    # maze = Maze(10, 10,     # starting offset
    #             12, 12,     # rows, columns
    #             75, 75,     # cell dimensions
    #             0.0035,   # delay between steps
    #             win, 14594) # seed

    maze.solve()

    win.awaitClose()

main()
