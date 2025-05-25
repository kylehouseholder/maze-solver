from graphics import Window, Point, Line
from field import Cell, Maze

def main():
    win = Window(920, 920)

    maze = Maze(10, 10, 15, 15, 60, 60, win, 2517, 0.0025)
    # maze = Maze(10, 10, 30, 30, 30, 30, win, 377)

    
    win.awaitClose()

main()
