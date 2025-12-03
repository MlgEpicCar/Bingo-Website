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
    
.btlw-header {
    text-indent: 10px;
}
    
.btlw-container {
    text-align: center;
}

.bingo-row {
    justify-content: center;
    display: grid;
    grid: 80px / 40px 40px 40px 40px 40px;
}
    
</style>
"""

row = 0
column = 0

def column_rand(cord: int) -> str:
    if cord == 0:
        return str(random.randint(1,15))
    elif cord == 1:
        return str(random.randint(16,30))
    elif cord == 2:
        return str(random.randint(31,45))
    elif cord == 3:
        return str(random.randint(46,60))
    elif cord == 4:
        return str(random.randint(61,75))

def create_bingo_board():
    rows = []
    for i in range(5):
        rows.append(create_row())
    return Div(rows)

def create_row():
    global row
    boxes = []
    for i in range(5):
        boxes.append(box())
    row += 1
    return Span(
                boxes,
                classes="bingo-row"
            )

def box():
    global column
    num = column_rand(column)
    name = "board" + str(column) + str(row)
    if row == 2 and column == 2:
        num = "★"
        box = True
    else:
        box = False
    column += 1
    return Div(
                num,
                Div(CheckBox(name, box))
            )

@dataclass
class State:
    image: PIL_Image
    input_message: str
    encoded_data: str
    decoded_message: str
    
@route
def index(state: State) -> Page:
    return Page(state, [
        "Bingo", #first number is row, second number is column
        BINGO_PAGE_CSS,
        
        create_bingo_board(),
        
        Span(
            Div(
                str(random.randint(1,15)),
                Div(CheckBox("board00")),
            ),
            
            Div(
                "★",
                Div(CheckBox("board00")),
            ),
            
            Div(
                str(random.randint(1,15)),
                Div(CheckBox("board00")),
            ),
            
            Div(
                str(random.randint(1,15)),
                Div(CheckBox("board00")),
            ),
            
            Div(
                str(random.randint(1,15)),
                Div(CheckBox("board00")),
            ),
            classes="bingo-row"
        ),
        
        LineBreak(),
        CheckBox("board00"),
        CheckBox("board01"),
        CheckBox("board02"),
        CheckBox("board03"),
        CheckBox("board04"),
        
        LineBreak(),
        Span(
        str(random.randint(16,30)),
        " ",
        str(random.randint(16,30)),
        " ",
        str(random.randint(16,30)),
        " ",
        str(random.randint(16,30)),
        " ",
        str(random.randint(16,30))
        ),
        LineBreak(),
        CheckBox("board10"),
        CheckBox("board11"),
        CheckBox("board12"),
        CheckBox("board13"),
        CheckBox("board14"),
        
        LineBreak(),
        Span(
        str(random.randint(31,45)),
        " ",
        str(random.randint(31,45)),
        " ",
        "Free",
        " ",
        str(random.randint(31,45)),
        " ",
        str(random.randint(31,45))
        ),
        LineBreak(),
        CheckBox("board20"),
        CheckBox("board21"),
        CheckBox("board22", True),
        CheckBox("board23"),
        CheckBox("board24"),
        
        LineBreak(),
        Span(
        str(random.randint(46,60)),
        " ",
        str(random.randint(46,60)),
        " ",
        str(random.randint(46,60)),
        " ",
        str(random.randint(46,60)),
        " ",
        str(random.randint(46,60))
        ),
        LineBreak(),
        CheckBox("board30"),
        CheckBox("board31"),
        CheckBox("board32"),
        CheckBox("board33"),
        CheckBox("board34"),
        
        LineBreak(),
        Span(
        str(random.randint(61,75)),
        " ",
        str(random.randint(61,75)),
        " ",
        str(random.randint(61,75)),
        " ",
        str(random.randint(61,75)),
        " ",
        str(random.randint(61,75))
        ),
        LineBreak(),
        CheckBox("board40"),
        CheckBox("board41"),
        CheckBox("board42"),
        CheckBox("board43"),
        CheckBox("board44"),
    ])

@route
def display_message_page(state: State, encode_image: bytes) -> Page:
    state.image = PIL_Image.open(io.BytesIO(encode_image)).convert('RGB')

    return Page(state, [
        "Image Loaded! Now enter your message:",
        Text(state.input_message),
        Button("Back", index)
    ])

@route
def display_message(state: State) -> Page:
    return Page(state, [
        f"Your message: {state.input_message}",
        Button("Back", index)
    ])

@route
def decode_page(state: State, decode_image: bytes) -> Page:
    state.image = PIL_Image.open(io.BytesIO(decode_image)).convert("RGB")

    # placeholder – your decoding goes later
    state.decoded_message = "(decoded message will go here)"

    return Page(state, [
        "Decoded Message:",
        Text(state.decoded_message),
        Button("Back", index)
    ])

start_server(State(None, "", "", ""))
