from drafter import *
from dataclasses import dataclass
from bakery import assert_equal
from PIL import Image as PIL_Image
import random

#At least 5 routes, including your index route
#At least 3 field in your state, including one of type list
#Suitable unit tests for all the routes so far. Instructions for unit test will be forthcoming!
#Website is actually usable without issues

BINGO_PAGE_CSS = """
<style>

body {
    background-color: lightblue;
    font-size: 20px;
}

.btlw-debug {
    display: none;
}

footer {
    display: none;
}
    
.btlw-header {
    text-indent: 10px;
}
    
.btlw-container {
    text-align: center;
}

.bingo-row {
    justify-content: center;
    display: grid;
    grid: 80px / 80px 80px 80px 80px 80px;
}

.bingo-box-dark {
    background-color: #a0a0df;
}

.bingo-box-light {
    background-color: #ffffff;
}
    
</style>
"""

row = 0
num_pools = 0

def generate_number_pools():
     number_pools = {
        0: random.sample(range(1, 16), 5),
        1: random.sample(range(16, 31), 5),
        2: random.sample(range(31, 46), 5),
        3: random.sample(range(46, 61), 5),
        4: random.sample(range(61, 76), 5),
    }
     return number_pools

def get_num(col: int, row: int) -> str:
    global num_pools
    return str(num_pools[col][row])

def create_bingo_board():
    global row
    global num_pools
    num_pools = generate_number_pools()
    rows = []
    row = 0
    for i in range(5):
        rows.append(create_row())
    return Div(
        *rows
        )

def create_row():
    global row
    boxes = []
        
    for col in range(5):
        boxes.append(box(row, col))
        
    row += 1
    return Span(
                *boxes,
                classes="bingo-row"
            )

def box(row: int, col: int):
    num = get_num(col,row)
    name = "board" + str(col) + str(row)
    
    if row == 2 and col == 2:
        num = "★"
        box = True
    else:
        box = False
        
    if row % 2 == 0 and col % 2 == 0:
        bingo_box_type = "bingo-box-dark"
    elif row % 2 != 0 and col % 2 != 0:
        bingo_box_type = "bingo-box-dark"
    else:
        bingo_box_type = "bingo-box-light"
        
    return Div(
                num,
                Div(CheckBox(name, box)),
                classes = bingo_box_type
            )

@dataclass
class State:
    name: str
    highscore: int
    
@route
def index(state: State) -> Page:
    return Page(state, [
        BINGO_PAGE_CSS,
        "What is your name?",
        TextBox("name", state.name),
        " ",
        Button("Play Bingo?", bingo)
        
        
    ])

@route
def bingo(state: State, name = str) -> Page:
    
    state.name = name
    
    return Page(state, [
        BINGO_PAGE_CSS,
        state.name,
        "Highscore: " + str(state.highscore),
        
        create_bingo_board(),
        " ",
        Button("New Board", bingo)
        
        
        
    ])

start_server(State("", 0))
