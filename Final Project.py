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
    """
    Represents the state of the website.

    Attributes:
        name (str): The player's name.
        score (int): The current score penalty (lower is better).
        highscore (int): The best score the player has achieved.
        board (list): A saved list of Box objects representing the board layout.
    """
    name: str
    score: int
    highscore: int
    board: list
    
@dataclass
class Box:
    """
    Represents a single space on the Bingo board.

    Attributes:
        num (int): The number displayed in the box.
        col (int): The column index of the box (0–4).
        row (int): The row index of the box (0–4).
        checked (bool): Whether the box is marked as selected.
    """
    num: int
    col: int
    row: int
    checked: bool = False
    
@dataclass
class Score:
    """
    Represents an entry on the leaderboard.

    Attributes:
        name (str): Player name.
        score (int): Player score (higher is better).
    """
    name: str
    score: int

board = Div() # Placeholder for board renderer
board_list = [] # A list of Boxes
drawn_balls = [] # A list of ints
leaderboard = [Score("Hatrickexe", 4500), Score("Tacoman", 3700), Score("Emu", -3036),
               Score("Gestalten", 5000), Score("Colusius", 6700), Score("Razikof", 1400),
               Score("Debuggyo", 3100), Score("Theeno", 7500), Score("Besser", 6000),
               Score("CinnaminiMax", 1400)
               ] # Default Leaderboard

row = 0
num_pools = 0

# --------------------
# FUNCTIONS
# --------------------

def check_if_bingo() -> bool:
    """
    Check whether the current board state forms a valid Bingo.

    Returns:
        bool: True if any row, column, or diagonal is fully filled
              based on the balls drawn so far (with the free space always counted).
    """
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
    """
    Render the last 10 drawn balls in two vertical columns.

    Returns:
        Div: A layout component containing two Div columns of ball numbers.
    """
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
    """
    Generate a new Bingo ball (1–75) that has not been drawn yet.

    Returns:
        int: The unique ball number added to drawn_balls,
             or 0 if all 75 have been drawn.
    """
    global drawn_balls
    if len(drawn_balls) == 75:
        return 0
    ball = random.randint(1, 75)
    while ball in drawn_balls:
        ball = random.randint(1, 75)
    drawn_balls.append(ball)
    return ball

def generate_number_pools():
    """
    Create the number distribution for a Bingo board:
    each column is assigned numbers from its appropriate range.

    Returns:
        A list of 5 random numbers with no duplicates.
    """
    number_pools = {
        0: random.sample(range(1, 16), 5),
        1: random.sample(range(16, 31), 5),
        2: random.sample(range(31, 46), 5),
        3: random.sample(range(46, 61), 5),
        4: random.sample(range(61, 76), 5),
    }
    return number_pools

def get_num(col: int, row: int) -> str:
    """
    Get the number assigned to a specific board cell.

    Args:
        col (int): Column index.
        row (int): Row index.

    Returns:
        str: The number at that location (as a string).
    """
    global num_pools
    return str(num_pools[col][row])

def create_bingo_board():
    """
    Generate a full Bingo board and update board_list.

    Returns:
        Div: A full 5-row 5-column Div structure representing the board layout.
    """
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
    """
    Create a single row of the Bingo board UI.

    Returns:
        Span: A row containing 5 rendered box components.
    """
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
    """
    Render one Bingo board cell, create its Box dataclass entry,
    and return a styled Div containing the number and checkbox.

    Args:
        row (int): Row index.
        col (int): Column index.

    Returns:
        Div: UI representation of the box.
    """
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
    """
    Re-render a previously saved board layout, showing checkboxes as checked
    if the number has already been drawn.

    Args:
        board_data (list): List of Box objects representing the saved board.

    Returns:
        Div: A visual representation of the restored board.
    """
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

# --------------------
# ROUTES
# --------------------
    
@route
def index(state: State) -> Page:
    """
    Landing page: asks for user name and resets drawn balls.

    Args:
        state (State): Website state.

    Returns:
        Page: The rendered index page.
    """
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
    """
    Page where user selects a Bingo board.

    Args:
        state (State): Website state.
        name (str): Player name.

    Returns:
        Page: Board selection UI.
    """
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
    """
    Launch Bingo gameplay page.

    Args:
        state (State): Website state.
        name (str): Player's name.

    Returns:
        Page: Bingo board, score, and buttons.
    """
    
    state.name = name
    
    return Page(state, [
        BINGO_PAGE_CSS,
        TextBox("name", state.name, classes="goaway"),
        "Current Score: " + str(10400 - state.score),
        Button("BINGO!!!!", check),
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
    """
    Draws the next ball, increases the score penalty,
    and refreshes the Bingo game page.

    Args:
        state (State): Website state.
        name (str): Player name.

    Returns:
        Page: Updated Bingo page after drawing a ball.
    """
    
    state.name = name
    state.score += 100
    gen_ball_int()
    
    return Page(state, [
        BINGO_PAGE_CSS,
        TextBox("name", state.name, classes="goaway"),
        "Current Score: " + str(10400 - state.score),
        Button("BINGO!!!!", check),
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
def check(state: State, name: str) -> Page:
    """
    Handle BINGO check request.

    If winning:
        - update highscore
        - reset score
        - move to win page

    Else:
        - move to lose page
    """
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
    """
    Page shown when the user wins Bingo.

    Args:
        state (State): Website state.

    Returns:
        Page: Win page.
    """
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
    """
    Page shown when the user incorrectly claims Bingo.

    Args:
        state (State): Website state.

    Returns:
        Page: Lose page encouraging user to continue.
    """
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
    """
    Display the top 10 scores from the leaderboard.

    Args:
        state (State): Website state.

    Returns:
        Page: Leaderboard UI showing rank, name, and score.
    """
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
