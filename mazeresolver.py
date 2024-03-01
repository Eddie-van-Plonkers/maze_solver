import random
from tkinter import Tk, BOTH, Canvas
import time


class Window:
    def __init__(self, width, height) -> None:
        self.__root = Tk()
        self.__root.title("Maze resolver")
        self.__canvas = Canvas(self.__root, background='white', width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        # self.__root.geometry(f'{width}x{height}+300+300') 
        self.__root.resizable(False, False)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
           self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color) -> None:
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, topLeft, bottomRight, win = None) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = topLeft.x
        self._y1 = topLeft.y
        self._x2 = bottomRight.x
        self._y2 = bottomRight.y
        self.__win = win
        self.visited = False

    def draw(self):
        if self.__win is None:
            return
        if self.has_left_wall:
            self.__draw_left_wall()
        if self.has_right_wall:
            self.__draw_right_wall()
        if self.has_top_wall:
            self.__draw_top_wall()
        if self.has_bottom_wall:
            self.__draw_bottom_wall()

    def draw_move(self, to_cell, undo=False):
        if self.__win is None:
            return
        p1 = Point((self._x1+self._x2)/2, (self._y1+self._y2)/2)
        p2 = Point((to_cell._x1+to_cell._x2)/2, (to_cell._y1+to_cell._y2)/2)
        if undo:
            self.__win.draw_line(Line(p1, p2), 'gray')
        else:
            self.__win.draw_line(Line(p1, p2), 'red')

    def __draw_left_wall(self):
        p1 = Point(self._x1, self._y1)
        p2 = Point(self._x1, self._y2)
        self.__win.draw_line(Line(p1, p2), 'green')

    def __draw_right_wall(self):
        p1 = Point(self._x2, self._y1)
        p2 = Point(self._x2, self._y2)
        self.__win.draw_line(Line(p1, p2), 'green')

    def __draw_top_wall(self):
        p1 = Point(self._x1, self._y1)
        p2 = Point(self._x2, self._y1)
        self.__win.draw_line(Line(p1, p2), 'green')

    def __draw_bottom_wall(self):
        p1 = Point(self._x1, self._y2)
        p2 = Point(self._x2, self._y2)
        self.__win.draw_line(Line(p1, p2), 'green')

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self._create_cells()
        if seed:
            random.seed(seed)

    def _create_cells(self):
        for i in range(self.num_cols):
            x1 = self.x1 + (self.cell_size_x*i)
            x2 = self.x1 + (self.cell_size_x*(i+1))
            col = []
            for j in range(self.num_rows):
                y1 = self.y1 + (self.cell_size_y*j)
                y2 = self.y1 + (self.cell_size_y*(j+1))
                cell = Cell(Point(x1, y1), Point(x2, y2), self.win)
                col.append(cell)
            self._cells.append(col)

        self._break_entrance_and_exit()
        self._break_walls_r(0, 0) 
        self._reset_cells_visited()   

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
        
    def _draw_cell(self, i, j):
        self._cells[i][j].draw()

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        if len(self._cells)==0:
            return
        self._cells[0][0].has_top_wall = False 
        self._cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])        

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        
        if i == self.num_cols-1 and j==self.num_rows-1:
            return True    
        
        # left
        if i > 0 and not self._cells[i - 1][j].visited and not self._cells[i][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i-1, j):
                return True
            else:
               self._cells[i][j].draw_move(self._cells[i - 1][j], True) 
        # right
        if i < self.num_cols - 1 and not self._cells[i + 1][j].visited and not self._cells[i][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i+1, j):
                return True
            else:
               self._cells[i][j].draw_move(self._cells[i + 1][j], True) 
        # up
        if j > 0 and not self._cells[i][j - 1].visited and not self._cells[i][j].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j-1):
                return True
            else:
               self._cells[i][j].draw_move(self._cells[i][j - 1], True) 
        # down
        if j < self.num_rows - 1 and not self._cells[i][j + 1].visited and not self._cells[i][j].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j+1):
                return True
            else:
               self._cells[i][j].draw_move(self._cells[i][j + 1], True)
        
        return False 


def main():
    win = Window(800, 600)
    maze = Maze(100, 50, 10, 10, 50, 50, win);
    maze.solve()
    win.wait_for_close() 

if __name__ == "__main__":
    main()