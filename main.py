from graphics import Window

def main():
    win = Window(800,600)

    l = Line(Point(120,120), Point(440,440))
    win.draw_line(l, "white")





    win.wait_for_close()

main()
