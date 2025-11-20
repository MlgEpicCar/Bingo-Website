from drafter import *

def home_page():
    return Column(
        Text("Hello World!"),
        Text("Welcome to Drafter")
    )

start_server(home_page)