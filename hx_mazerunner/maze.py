import random
import components

from enum import Enum


class Symbol(Enum):
    WALL = 'W'
    PATH = 'P'
    CHARACTER = 'C'
    TREASURE = 'T'
    EXIT = 'E'


def generate_maze(width, height):
    # Directions: north, south, east, west
    dx = {'E': 1, 'W': -1, 'N': 0, 'S': 0}
    dy = {'E': 0, 'W': 0, 'N': -1, 'S': 1}
    # opposite = {'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'}

    # Initialize maze (walls everywhere)
    maze = [[Symbol.WALL for _ in range(2 * width + 1)] for _ in range(2 * height + 1)]

    # Function to carve the maze from a cell
    def carve(x, y):
        directions = ['N', 'S', 'E', 'W']
        random.shuffle(directions)

        for direction in directions:
            nx, ny = x + dx[direction], y + dy[direction]

            if (0 <= ny < height) \
                    and (0 <= nx < width) \
                    and (maze[2 * ny + 1][2 * nx + 1] == Symbol.WALL):
                maze[2 * y + 1 + dy[direction]][2 *
                                                x + 1 + dx[direction]] = Symbol.PATH
                # Path
                maze[2 * ny + 1][2 * nx + 1] = Symbol.PATH
                carve(nx, ny)

    # Start carving from point (0, 0)
    maze[1][1] = Symbol.PATH  # Starting point

    carve(0, 0)
    maze[1][1] = Symbol.CHARACTER  # Place Maze runner in
    maze[-2][-2] = Symbol.TREASURE

    return maze


def maze_to_hiccup(maze):
    grid = []
    for i, row in enumerate(maze):
        grid_items = []
        grid_row = ['div', {'class': 'flex'}, grid_items]
        for j, cell in enumerate(row):
            if cell == Symbol.CHARACTER:
                grid_items.append(components.maze_character(i, j))
            elif cell == Symbol.TREASURE:
                grid_items.append(components.maze_treasure(i, j))
            elif cell == Symbol.WALL:
                grid_items.append(components.maze_wall(i, j))
            else:
                grid_items.append(components.maze_path(i, j))
        grid.append(grid_row)

    return ['div', {'class': 'text-sm'}, grid]


def calc_next_position(direction, row, col):
    if direction == 'N':
        return row - 1, col
    elif direction == 'S':
        return row + 1, col
    elif direction == 'E':
        return row, col + 1
    elif direction == 'W':
        return row, col - 1
    return row, col


def add_exit(maze):
    maze[1][0] = Symbol.EXIT
