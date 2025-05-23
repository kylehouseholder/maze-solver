from graphics import Window, Point, Line
from field import Cell, Maze

def main():
    win = Window(920, 630)

    maze = Maze(10, 15, 20, 30, 30, 30, win)

    win.wait_for_close()

main()
