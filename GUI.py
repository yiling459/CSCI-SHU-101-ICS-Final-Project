from pathlib import Path
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./ASSETS")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class GUI:
    def __init__(self, send, recv, state, s):
        self.window = Tk()
        self.window.geometry("1200x800")
        self.window.configure(bg = "#FFFFFF")
        # self.Window.withdraw()
        self.canvas_width = 1200.0
        self.canvas_height = 800.0
        self.send = send
        self.recv = recv
        self.state = state
        self.socket = s
        self.my_msg = ''
        self.system_msg = ''


    def start_page(self):
        # create the canvas
        canvas = Canvas(
            self.window,
            bg = "#FFFFFF",
            height = self.canvas_height,
            width = self.canvas_width,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        # create the background image
        background_image = PhotoImage(file = relative_to_assets("start_page_background.png"))
        canvas.create_image(0,
                            0,
                            anchor = 'nw',
                            image = background_image)

        # create the entry for name
        canvas.create_text(444.0,
                            462.0,
                            anchor="nw",
                            text="ENTER YOUR NAME",
                            fill="#A9CEF0",
                            font=("Futura Medium", 12 * -1))
        name_entry_image = PhotoImage(file=relative_to_assets("TextBox.png"))
        canvas.create_image(435,
                            484,
                            anchor = 'nw',
                            image=name_entry_image)
        name_entry = Entry(bd=0,
                            bg="#D5E8F8",
                            font=("Futura Medium", 15 * -1),
                            highlightthickness=0)
        name_entry.place(x=462.5,
                            y=484.0,
                            width=281.0,
                            height=53.0)

        # create the button for creating a new room
        create_room_button_image = PhotoImage(file=relative_to_assets("Light_Button_Slim.png"))
        create_room_button = Button(image=create_room_button_image,
                            borderwidth=0,
                            highlightthickness=0,
                            command=lambda: print("button_1 clicked"),
                            relief="flat")
        create_room_button.place(x=435,
                                y=556,
                                width = 336,
                                height = 55)
        

        

        self.window.mainloop()
    
    def run(self):
        self.start_page()    

if __name__ == "__main__":
    g = GUI('','','','')
    g.start_page()


