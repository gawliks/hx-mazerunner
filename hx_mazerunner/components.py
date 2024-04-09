from typing import Union
from pyhiccup.core import html


def layout(content: Union[str, list] = 'No Content'):
    elements = [
        ['head',
            ['title', 'Maze Runner'],
            ['script', {'src': '/static/js/htmx.min.js',
                        'defer': ''}, '()'],
            ['script', {'src': '/static/js/app.js', 'defer': ''}, '()'],
            ['meta', {'charset': 'utf-6'}],
            ['meta', {'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1'}],
            ['script', {'src': 'https://cdn.tailwindcss.com'}, '()']],
        body(content),
    ]
    return html(elements)


def body(content: Union[str, list] = 'No Content'):
    return ['body',
            ['div',
             {'class': 'min-h-screen bg-gray-200'
              ' flex flex-col justify-center items-center'},
             container(content),
             ['div',
              {'class': 'flex justify-center items-center gap-x-4 pt-4'},
              reset_button(),
              ['div', {'id': 'countdown'}, ' '],
              ['div', {'id': 'dialog'}, ' ']]]]


def container(content: Union[str, list] = 'No Content'):
    return ['div',
            {'id': 'container',
             'class': 'center p-4'},
            content]


def reset_button():
    return [
        ['button',
            {'hx-get': '/reset',
             'hx-swap': 'outerHTML',
             'hx-target': 'body',
             'class': 'bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'},
            'Play Again']]


def maze_path(row: int, col: int, size: int = 6):
    return ['div',
            {'id': f'cell-{row}-{col}',
             'class': f'text-white bg-white w-{size} h-{size}'},
            ' ']


def maze_wall(row: int, col: int, size: int = 6):
    return ['div',
            {'id': f'cell-{row}-{col}',
             'class': f'text-black bg-black w-{size} h-{size}'},
            '&#9606;']


def maze_character(row: int, col: int, swap: bool = False, size: int = 6):
    attrs = {
        'id': f'cell-{row}-{col}',
        'class': f'bg-white flex justify-center items-center w-{size} h-{size}',
        'hx-get': '/move',
        'hx-swap': 'outerHTML',
        'hx-trigger': "keyup[key=='ArrowUp'||key=='ArrowDown'||key=='ArrowLeft'||key=='ArrowRight'] from:body",
    }
    if swap:
        attrs['hx-swap-oob'] = 'true'
    return ['div', attrs, ['img', {'src': '/static/svg/character.svg'}]]


def maze_treasure(row: int, col: int, size: int = 6):
    return ['div',
            {'id': f'cell-{row}-{col}',
             'class': f'bg-white flex justify-center items-center w-{size} h-{size}'},
            ['img', {'src': '/static/svg/treasure.svg'}]]


def maze_exit(row: int, col: int, size: int = 6):
    return ['div',
            {'id': f'cell-{row}-{col}',
             'hx-swap-oob': 'true',
             'class': f'bg-white flex justify-center items-center w-{size} h-{size}'},
            ['img', {'src': '/static/svg/exit.svg'}]]


def treasure_found_msg():
    return [
        ['h2', 'You found the treasure!'],
        ['h3', 'Run for your life now!'],
    ]


def got_out_msg():
    return [
        ['h2', 'Congratulations! You got out!'],
    ]


def success_dialog(content):
    return ['div',
            {'id': 'dialog',
             'class': 'fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full'},
            ['div',
             {'class': 'flex items-center justify-center min-h-screen'},
             ['div',
              {'class': 'bg-white rounded-lg shadow-lg p-5 md:p-20 mx-2 text-center'},
              *[msg for msg in content],
              ['form',
               {
                   'hx-get': '/countdown',
                   'hx-swap': 'delete',
                   'hx-target': '#dialog'
               },
               ['input', {'type': 'hidden', 'name': 'swap', 'value': 'true'}],
               ['hr class="my-4 border-none"'],
               ['button',
                {'type': 'submit',
                 'name': 'current',
                 'value': 10,
                 'class': 'bg-blue-500 text-white rounded hover:bg-blue-700 focus:outline-none w-full py-2 px-4'},
                'GO!']]]]]


def failure_dialog():
    return ['div',
            {'id': 'dialog',
             'class': 'fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full',
             'hx-swap-oob': 'true'},
            ['div',
             {'class': 'flex items-center justify-center min-h-screen'},
             ['div',
              {'class': 'bg-white rounded-lg shadow-lg p-5 md:p-20 mx-2 text-center flex flex-col items-center'},
              ['img', {'src': '/static/svg/coffin.svg', 'width': '64', 'height': '80'}],
              'You died.',
              reset_button()]]]


def countdown(current: int = 10, swap: bool = False):
    text_cls = 'text-2xl text-black' if current > 3 else 'text-3xl text-red-500'
    attrs = {
        'id': 'countdown',
        'class': f'font-bold {text_cls} transition-all 200ms ease-in',
        'hx-get': '/countdown',
        'hx-swap': 'outerHTML',
        'hx-trigger': 'load delay:1s',
    }
    if swap:
        attrs['hx-swap-oob'] = 'true'

    return ['form',
            attrs,
            ['input', {'type': 'hidden', 'name': 'current', 'value': current - 1}],
            ['p',
             str(current)]]


def coffin(curr_pos: tuple[int, int], size: int = 6):
    return ['div',
            ['div',
             {
                 'id': f'cell-{curr_pos[0]}-{curr_pos[1]}',
                 'class': f'flex justify-center items-center transition-all 1s ease-in w-{size} h-{size} bg-white',
                 'hx-swap-oob': 'true'},
             ['img', {'src': '/static/svg/coffin.svg', 'width': '16', 'height': '20'}]],
            ['div', '']]
