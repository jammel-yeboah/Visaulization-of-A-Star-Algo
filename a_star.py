import pygame
import math
from queue import PriorityQueue

WIDTH = 720
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Jammel's Path Finding Algo with A*")

CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
TAN = (255, 204, 102)
BROWN = (153, 102, 51)
RED = (255, 0, 0)
TEAL = (0, 128, 128)
OLIVE = (128, 128, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)


class Node:
    def __init__(self, row, column, width, total_rows):
        """[tracks each node of the grid]

        Args:
            row ([integer]): [row of node]
            column ([integer]): [column of node]
            width ([integer]): [how wide node is]
            total_rows ([integer]): [track record of total rows counted]
        """
        self.row = row
        self.column = column
        self.xcoordinate = row * width
        self.ycoordinate = column * width
        self.color = BLACK
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.column

    def is_closed(self):
        return self.color == ORANGE

    def is_open(self):
        return self.color == PURPLE

    def is_barrier(self):
        return self.color == WHITE

    def is_start(self):
        return self.color == CYAN

    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = BLACK

    def make_start(self):
        """first node user clicks on, or starting node

        Returns:
            bool: if True, node is colored cyan
        """
        self.color = CYAN

    def make_closed(self):
        """Determines if node has been considered or not

        Returns:
            [bool]: if True, node is colored orange
        """
        self.color = ORANGE

    def make_open(self):
        """Determines if node is open, or has't been considered

        Returns:
            bool: if False, node is colored purple
        """
        self.color = PURPLE

    def make_barrier(self):
        """if user input converts node into a barrier for  pathfinindg algorithm

        Returns:
            [bool]: if True, node is colored white
        """
        self.color = WHITE

    def make_end(self):
        """Destination node as determined by user input

        Returns:
            bool: if True, node is colored red
        """
        self.color = RED

    def make_path(self):

        self.color = GREEN

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.xcoordinate, self.ycoordinate, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.column])

        if self.row > 0 and not grid[self.row - 1][self.column].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.column])

        if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.column + 1])

        if self.column > 0 and not grid[self.row][self.column - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.column - 1])

    def _It_(self, other):
        return False


def h(p1, p2):
    """[Calculates distance between point 1 and point 2 and returns it]

    Args:
        p1 ([integer]): [initial point]
        p2 ([integer]): [second point]

    Returns:
        [integer]: [heuristic distance]
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(origin, current, draw):
    while current in origin:
        current = origin[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    origin = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    """F Score = G Score + H Score, where G Score is the cost of the current 
    path from start to the current node. H score is the cost from the current node
    to the end node"""

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(origin, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                origin[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    """Data structure to hold all nodes in the list that will be manipulated

    Args:
        rows ([integer]): [number of rows]
        width ([integer]): [the width of grid (Since window is square, width == height)]

    Returns:
        [integer]: [the width of each node]
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, BROWN, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BROWN, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(BLACK)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """Uses mouse position to determine row/column and return the exact node clicked on

    Args:
        pos ([float]): [mouse position]
        rows ([integer]): [# of row in grid]
        width ([integer]): [width of grid]

    Returns:
        [integer]: [x and y coordinate of grid or exact row and column clicked on]
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    column = x // gap
    return row, column


##Main##
def main(win, width):
    """The following is responsible for collision checks and the correct output of various user inputs"""
    ROWS = 35
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT Mouse Click
                pos = pygame.mouse.get_pos()
                row, column = get_clicked_pos(pos, ROWS, width)
                node = grid[row][column]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT Mouse Click
                pos = pygame.mouse.get_pos()
                row, column = get_clicked_pos(pos, ROWS, width)
                node = grid[row][column]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
