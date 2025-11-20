from drafter import *
from dataclasses import dataclass
from bakery import assert_equal
from PIL import Image as PIL_Image

@dataclass
class State:
    image: PIL_Image
    input_message: str
    encoded_data: str
    decoded_message: str
    alist: list
    
@route
def index(state: State) -> Page:
    return Page(state, [
        "Steganographic Encoder",

        "--- Encode Section ---",
        FileUpload("encode_image", accept="image/png"),
        TextBox("input_message", placeholder="Enter your message here"),
        Button("Next Step", display_message_page),

        "--- Decode Section ---",
        FileUpload("decode_image", accept="image/png"),
        Button("Decode Message", decode_page)
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

start_server(State(None, "", "", "", []))