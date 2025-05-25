import unittest
from field import Maze


class Tests(unittest.TestCase):
    def testMaze10x12(self):
        rows = 7
        cols = 9
        maze = Maze(0, 0, rows, cols, 10, 10)
        self.assertEqual(
            len(maze._Maze__cells),
            rows,
        )
        self.assertEqual(
            len(maze._Maze__cells[0]),
            cols,
        )

    def testMaze15x20(self):
        rows = 10
        cols = 12
        maze = Maze(0, 0, rows, cols, 10, 10)

        self.assertEqual(
            len(maze._Maze__cells),
            rows,
        )
        self.assertEqual(
            len(maze._Maze__cells[0]),
            cols,
        )

    def testMaze20x30(self):
        rows = 15
        cols = 20
        maze = Maze(0, 0, rows, cols, 10, 10)
        self.assertEqual(
            len(maze._Maze__cells),
            rows,
        )
        self.assertEqual(
            len(maze._Maze__cells[0]),
            cols,
        )

    def testMazeBreakEnds(self):
        rows = 8
        cols = 8
        maze = Maze(0, 0, rows, cols, 10, 10)
        self.assertEqual(
            maze._Maze__cells[0][0].hasTopWall,
            False,
        )
        self.assertEqual(
            maze._Maze__cells[rows - 1][cols - 1].hasBottomWall,
            False,
        )

    def testResetCells(self):
        rows = 6
        cols = 6
        maze = Maze(10, 10, rows, cols, 10, 10, seed=150)
        self.assertEqual(
            maze._Maze__cells[2][2].visited,
            False,
        )

if __name__ == "__main__":
    unittest.main()
