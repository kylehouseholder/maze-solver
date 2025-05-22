from graphics import Window, Point, Line

def main():
    win = Window(800,600)

    l0 = Line(Point(120,120), Point(440,440))
    win.draw_line(l0, "white")

    l1 = Line(Point(125, 125), Point(170, 450))
    win.draw_line(l1, "green")

    l2 = Line(Point(777, 222), Point(172, 454))
    win.draw_line(l2, "blue")




    win.wait_for_close()

main()
