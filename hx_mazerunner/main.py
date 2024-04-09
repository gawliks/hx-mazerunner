from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pyhiccup.core import convert

import components
from maze import generate_maze, maze_to_hiccup, calc_next_position, Symbol

app = FastAPI(default_response_class=HTMLResponse)  # type: ignore
app.mount("/static", StaticFiles(directory="static"), name="static")

SIZE = 5
MAZE = generate_maze(SIZE, SIZE)
CURR_POS = (1, 1)
EXIT_POS = (1, 0)


@app.get("/")
async def index():
    return components.layout(maze_to_hiccup(MAZE))


@app.get("/move")
async def move(direction: str, row: int, col: int, response: Response):
    global CURR_POS, MAZE
    path = components.maze_path(row, col)
    next_row, next_col = calc_next_position(direction, row, col)
    if MAZE[next_row][next_col] == Symbol.WALL:
        character = components.maze_character(row, col)
        return convert(character)

    success_dialog = ['']
    exit_cell = ['']
    if MAZE[next_row][next_col] == Symbol.TREASURE:
        success_dialog = components.success_dialog(components.treasure_found_msg())
        exit_row, exit_col = EXIT_POS
        MAZE[exit_row][exit_col] = Symbol.EXIT
        exit_cell = components.maze_exit(exit_row, exit_col)

    if MAZE[next_row][next_col] == Symbol.EXIT:
        success_dialog = components.success_dialog(components.got_out_msg())

    MAZE[row][col] = Symbol.PATH
    MAZE[next_row][next_col] = Symbol.CHARACTER
    CURR_POS = (next_row, next_col)
    character = components.maze_character(next_row, next_col, swap=True)
    return convert([path, character, success_dialog, exit_cell])


@app.get("/reset")
async def reset():
    global MAZE, CURR_POS
    MAZE = generate_maze(SIZE, SIZE)
    CURR_POS = (1, 1)
    return convert(components.body(maze_to_hiccup(MAZE)))


@app.get("/countdown")
async def countdown(current: int = 10, swap: bool = False):
    if EXIT_POS == CURR_POS:
        return convert(['div', {'id': 'countdown'}, ''])

    if current == 0:
        return convert([components.coffin(CURR_POS), components.failure_dialog()])

    return convert(components.countdown(current, swap))
