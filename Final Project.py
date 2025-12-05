from drafter import *
from dataclasses import dataclass
from bakery import assert_equal
from PIL import Image as PIL_Image
import random

set_website_title("Bingo Website")
hide_debug_information()


BINGO_PAGE_CSS = """
<style>

body {
    background-color: lightblue;
    font-size: 20px;
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

.leaderboard {
    justify-content: center;
    display: flex;
    gap: 100px;
}

.left {
    justify-content: left;
    padding-left: 50px;
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
    
@dataclass
class Score:
    name: str
    score: int

board = Div() # Placeholder for board renderer
board_list = [] # A list of Boxes
drawn_balls = [] # A list of ints
leaderboard = [Score("Hatrickexe", 4500), Score("Tacoman", 3700), Score("Emu", -3036), Score("Gestalten", 5000), Score("Colusius", 6700), Score("Razikof", 1400), Score("Debuggyo", 3100), Score("Theeno", 7500), Score("Besser", 6000), Score("CinnaminiMax", 1400)]

row = 0
num_pools = 0

def check_if_bingo() -> bool:
    global board_list
    global drawn_balls

    grid = [[False]*5 for _ in range(5)]
    
    for box in board_list:
        if box.row == 2 and box.col == 2:
            grid[box.row][box.col] = True
        else:
            try:
                grid[box.row][box.col] = int(box.num) in drawn_balls
            except ValueError:
                grid[box.row][box.col] = False
    for row in range(5):
        if all(grid[row]):
            return True
    for col in range(5):
        if all(grid[row][col] for row in range(5)):
            return True
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
    state.score = 0
    
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
        TextBox("name", state.name, classes="goaway"),
        state.name + ", Choose your Board",
        
        Button("Confirm", bingo_start),
        Button("New Board", select_board_page),
        
        board,
        " "
    ])

@route
def bingo_start(state: State, name: str) -> Page:
    
    state.name = name
    
    return Page(state, [
        BINGO_PAGE_CSS,
        TextBox("name", state.name, classes="goaway"),
        "Current Score: " + str(10400 - state.score),
        Button("BINGO!!!!", check_page),
        Button("Next Ball", next_ball),
        
        Div(
            render_saved_board(state.board),
            display_ball_columns(),

            classes="board-and-balls"
        ),
        " ",
        "Highscore: " + str(state.highscore),
        
        " "
    ])

@route
def next_ball(state: State, name: str) -> Page:
    
    state.name = name
    state.score += 100
    gen_ball_int()
    
    return Page(state, [
        BINGO_PAGE_CSS,
        TextBox("name", state.name, classes="goaway"),
        "Current Score: " + str(10400 - state.score),
        Button("BINGO!!!!", check_page),
        Button("Next Ball", next_ball),
        
        Div(
            render_saved_board(state.board),
            display_ball_columns(),

            classes="board-and-balls"
        ),
        " ",
        "Highscore: " + str(state.highscore),
        " "
    ])

@route
def check_page(state: State, name: str) -> Page:
    global leaderboard
    state.name = name
    
    if check_if_bingo():
        state.highscore = 10400 - state.score
        leaderboard.append(Score(state.name,state.highscore))
        state.score = 0
        return win_page(state)
    else:
        return lose_page(state)
    

@route
def win_page(state: State) -> Page:
    return Page(state, [
        BINGO_PAGE_CSS,
        TextBox("name", state.name, classes="goaway"),
        Image("https://media.istockphoto.com/id/1252787937/vector/impression.jpg?s=612x612&w=0&k=20&c=fnHTVScp1F_29KIjVF1BX5X3v5YGanAAV6xI5mWykrg="),
        "You Win!!!",
        " ",
        Button("Play Again", index),
        Button("Leaderboard", leaderboard_page)
    ])


@route
def lose_page(state: State) -> Page:
    return Page(state, [
        BINGO_PAGE_CSS,
        TextBox("name", state.name, classes="goaway"),
        Image("https://content.presentermedia.com/content/clipart/00028000/28699/sad_worry_emoji_face_800_clr.png"),
        "Sorry, no bingo yet, keep going",
        "I believe in you, twin",
        " ",
        Button("Try Again", bingo_start),
        Button("Leaderboard", leaderboard_page)
    ])

@route
def leaderboard_page(state: State) -> Page:
    global leaderboard

    sorted_board = sorted(leaderboard, key=lambda score: score.score, reverse=True)
    top_ten = sorted_board[:10]

    entries = []
    names = []
    scores = []
    for i, entry in enumerate(top_ten, start=1):
        entries.append(Div(str(i) + "."))
        names.append(Div(str(entry.name)))
        scores.append(Div(str(entry.score)))

    return Page(state, [
        BINGO_PAGE_CSS,
        Div("Leaderboard - Top Scores", classes="btlw-header"),
        Div(
            Div(*entries),
            Div(*names),
            Div(*scores),
            classes="leaderboard",
        ),
        TextBox("name", state.name, classes="goaway"),
        " ",
        Button("Back to Bingo", bingo_start),
        Button("Home", index)
    ])

start_server(State("", 0, 0, []))
