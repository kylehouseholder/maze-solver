from graphics import Window, Point, Line
from field import Cell, Maze

def main():
    win = Window(920, 920)

    maze = Maze(10, 10, 30, 30, 30, 30, win, 777)

    
    win.awaitClose()

main()
