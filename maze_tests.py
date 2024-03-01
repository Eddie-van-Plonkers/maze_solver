import unittest
from mazeresolver import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_entrance(self):
        num_cols = 6
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False,
        )

    def test_exit(self):
        num_cols = 6
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[5][4].has_bottom_wall,
            False,
        )

    def test_reset_visited(self):
        num_cols = 6
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[1][1].visited,
            False,
        )
        self.assertEqual(
            m1._cells[4][3].visited,
            False,
        )

if __name__ == "__main__":
    unittest.main()
