
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1200x800")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 800,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    600.0,
    400.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    603.0,
    511,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D5E8F8",
    highlightthickness=0
)
entry_1.place(
    x=462.5,
    y=484.0,
    width=281.0,
    height=53.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=435.0,
    y=556.0,
    width=336.0,
    height=55.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=435.0,
    y=628.0,
    width=336.0,
    height=55.0
)

canvas.create_text(
    444.0,
    462.0,
    anchor="nw",
    text="ENTER YOUR NAME",
    fill="#A9CEF0",
    font=("Futura Medium", 12 * -1)
)

canvas.create_text(
    395.0,
    339.0,
    anchor="nw",
    text="Use your knowledge and talents to compete with your friends!",
    fill="#000000",
    font=("Geo Regular", 25 * -1)
)
window.resizable(False, False)
window.mainloop()