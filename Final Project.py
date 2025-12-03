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

.goaway {
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

.ball {
    display: flex;
    background-color: white;
    margin-left: 20px;
    border-radius: 100px;
    justify-content: center;
    align-items: center;
    height: 75px;
    width: 75px;
    border-width: 5px;
    border-color: #eeeeee;
}

.board-and-balls {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 40px; /* space between board and balls */
}

.ball-column {
    display: flex;
    flex-direction: column;
    gap: 15px;
}
    
</style>
"""

@dataclass
class State:
    name: str
    highscore: int
    board: list
    
@dataclass
class Box:
    num: int
    col: int
    row: int
    called: bool = False

board = Div()
board_list = []
row = 0
num_pools = 0

def check_if_bingo() -> bool:
    pass
    return False

def check_if_called(box: Box):
    pass
    return False

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
    global board_list
    global row
    global num_pools
    
    board_list = []
    row = 0
    num_pools = generate_number_pools()
    
    rows = []
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
    global board_list
    
    board_list.append(Box(get_num(col,row), col, row))
    
    num = get_num(col,row)
    name = "board" + str(col) + str(row) #not relevant but needed for compile
    
    
    
    if row == 2 and col == 2:
        num = "★"
        box = False
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

def render_saved_board(board_data):
    rows = []
    for row in range(5):
        row_boxes = []
        for col in range(5):
            box = board_data[row * 5 + col]
            
            if row == 2 and col == 2:
                display_num = "★"
            else:
                display_num = box.num
                
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                bingo_box_type = "bingo-box-dark"
            else:
                bingo_box_type = "bingo-box-light"
            
            row_boxes.append(
                Div(
                    display_num,
                    Div(CheckBox("fillername", box.called)),
                    classes = bingo_box_type
                )
            )
        rows.append(Span(*row_boxes, classes="bingo-row"))
    return Div(*rows)

    
@route
def index(state: State) -> Page:
    return Page(state, [
        BINGO_PAGE_CSS,
        "What is your name?",
        TextBox("name", state.name),
        " ",
        Button("Play Bingo?", select_board_page)
    ])

@route
def select_board_page(state: State, name: str) -> Page:
    global board
    
    state.name = name
    board = create_bingo_board()
    state.board = board_list
    
    return Page(state, [
        BINGO_PAGE_CSS,
        state.name,
        TextBox("name", state.name, classes="goaway"),
        "Choose your Board",
        
        board,
        " ",
        Button("Confirm", bingo_page),
        Button("New Board", select_board_page)
    ])

@route
def bingo_page(state: State, name: str) -> Page:
    
    state.name = name
    
    return Page(state, [
        BINGO_PAGE_CSS,
        state.name,
        TextBox("name", state.name, classes="goaway"),
        "Highscore: " + str(state.highscore),
        
        Div(
            render_saved_board(state.board),

            Div(
                Div("18", classes="ball"),
                Div("42", classes="ball"),
                Div("7", classes="ball"),
                Div("63", classes="ball"),
                Div("67", classes="ball"),
                classes="ball-column"
            ),

            classes="board-and-balls"
        ),
        
        " ",
        Button("BINGO!!!!", check_page),
        Button("Next Ball", bingo_page)
    ])

@route
def check_page(state: State, name: str) -> Page:
    
    state.name = name
    
    return Page(state, [
        BINGO_PAGE_CSS,
        state.name,
        TextBox("name", state.name, classes="goaway"),
        "Highscore: " + str(state.highscore),
        "You Win!!!"
        " ",
        Button("BINGO!!!!", check_page)
    ])

start_server(State("", 0, []))
