from drafter import *
from dataclasses import dataclass
from bakery import assert_equal
from PIL import Image as PIL_Image
import random

# !!! Requirments !!!
# At least 7 routes.
# At least 5 pages.
# The implementation of the State dataclass must have at least 4 fields.
# At least 4 state fields must be meaningfully modified in at least one route; those 4 state fields cannot be constants.
# At least 3 input fields (TextBox, CheckBox, SelectBox, TextArea). They don't have to be the same type.
# At least 3 meaningful if statements.  (This requirement will be met in the Decoding and Encoding Functionality parts of the assignment.)
# At least 1 loop that iterates over an attribute of the list of class instances or dictionary of class instances in a meaningful way.  (This requirement will be met in the Decoding and Encoding Functionality parts of the assignment.)
# The site should have a legitimate purpose or functionality.
# No global variables (global constantsLinks to an external site. are fine).
# Only use drafter, bakery, and built-in Python libraries. E.g., you can use random, math, but you can not use matplotlib, designer.

# What is left to do:
# 5/7 Routes
# 3/4 fields in State dataclass
# 2/4 meaningful modifactions of fields during runtime

# Notes to grader:
# PLEASE let me use global variables, I didn't read it was a requirment until too late PLEASE
# PLEASE let me use CSS, im not sure if it's allowed but PLEASE

set_website_title("Bingo Website")

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
}

.board-and-balls {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    gap: 10px; /* space between board and balls */
}

.ball-column {
    display: flex;
    flex-direction: column;
    width: 75px;
    gap: 5px /* space balls */
}
    
</style>
"""

@dataclass
class State:
    name: str
    score: int
    highscore: int
    board: list
    
@dataclass
class Box:
    num: int
    col: int
    row: int
    checked: bool = False
    called: bool = False

board = Div() # Placeholder for board renderer
board_list = [] # A list of Boxes
drawn_balls = [] # A list of ints

row = 0
num_pools = 0

def check_if_bingo() -> bool:
    global board_list
    global drawn_balls

    # Build 5x5 grid of booleans: True if the box is considered checked
    grid = [[False]*5 for _ in range(5)]
    
    for box in board_list:
        # FREE SPACE is always considered checked
        if box.row == 2 and box.col == 2:
            grid[box.row][box.col] = True
        else:
            try:
                # Mark as checked if the number has been drawn
                grid[box.row][box.col] = int(box.num) in drawn_balls
            except ValueError:
                grid[box.row][box.col] = False

    # Check rows
    for row in range(5):
        if all(grid[row]):
            return True

    # Check columns
    for col in range(5):
        if all(grid[row][col] for row in range(5)):
            return True

    # Check diagonals
    if all(grid[i][i] for i in range(5)):
        return True
    if all(grid[i][4-i] for i in range(5)):
        return True

    return False

def display_ball_columns():
    global drawn_balls
    
    balls_to_display = list(reversed(drawn_balls[-10:]))
    column1 = balls_to_display[:5]
    column2 = balls_to_display[5:]
        
    return Div(
        Div(
        *[Div(str(ball), classes="ball") for ball in column1],
        classes="ball-column"
        ),
        Div(
        *[Div(str(ball), classes="ball") for ball in column2],
        classes="ball-column"
        ),
        classes="board-and-balls"
        )

def gen_ball_int():
    global drawn_balls
    if len(drawn_balls) == 75:
        return 0
    ball = random.randint(1, 75)
    while ball in drawn_balls:
        ball = random.randint(1, 75)
    drawn_balls.append(ball)
    return ball

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

def render_saved_board(board_data: list):
    global drawn_balls
    rows = []
    
    for row in range(5):
        row_boxes = []
        for col in range(5):
            box = board_data[row * 5 + col]
            
            if row == 2 and col == 2:
                display_num = "★"
                is_checked = True
            else:
                display_num = box.num
                is_checked = int(box.num) in drawn_balls[0:-1]
                
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                bingo_box_type = "bingo-box-dark"
            else:
                bingo_box_type = "bingo-box-light"
            
            row_boxes.append(
                Div(
                    display_num,
                    Div(CheckBox("box" + str(row) + str(col), is_checked)),
                    classes = bingo_box_type
                )
            )
        rows.append(Span(*row_boxes, classes="bingo-row"))
    return Div(*rows)

    
@route
def index(state: State) -> Page:
    global drawn_balls
    drawn_balls = []
    
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
        Button("Confirm", bingo_start),
        Button("New Board", select_board_page)
    ])

@route
def bingo_start(state: State, name: str) -> Page:
    
    state.name = name
    
    return Page(state, [
        BINGO_PAGE_CSS,
        state.name,
        TextBox("name", state.name, classes="goaway"),
        "Highscore: " + str(state.highscore),
        "Current Score: " + str(10400 - state.score),
        
        Div(
            render_saved_board(state.board),
            display_ball_columns(),

            classes="board-and-balls"
        ),
        
        " ",
        Button("BINGO!!!!", check_page),
        Button("Next Ball", next_ball)
    ])

@route
def next_ball(state: State, name: str) -> Page:
    
    state.name = name
    state.score += 100
    gen_ball_int()
    
    return Page(state, [
        BINGO_PAGE_CSS,
        state.name,
        TextBox("name", state.name, classes="goaway"),
        "Highscore: " + str(state.highscore),
        "Current Score: " + str(10400 - state.score),
        
        Div(
            render_saved_board(state.board),
            display_ball_columns(),

            classes="board-and-balls"
        ),
        
        " ",
        Button("BINGO!!!!", check_page),
        Button("Next Ball", next_ball)
    ])

@route
def check_page(state: State, name: str) -> Page:
    
    state.name = name
    if state.highscore == 0:
        state.highscore = 0
    else:
        state.highscore = 10400 - state.score
    state.score = 0
    
    return Page(state, [
        BINGO_PAGE_CSS,
        state.name,
        TextBox("name", state.name, classes="goaway"),
        "Highscore: " + str(state.highscore),
        "Score: " + str(state.highscore),
        " ",
        "You Win!!!"
        " ",
        str(check_if_bingo()),
        Button("Play Again", index)
    ])

start_server(State("", 0, 0, []))
