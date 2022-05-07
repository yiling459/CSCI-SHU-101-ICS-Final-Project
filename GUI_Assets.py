import tkinter
import customtkinter

def slim_button(master, button_color, text, text_color):
    button = customtkinter.CTkButton(
        master = master,
        bg_color="#000000",
        fg_color=button_color,
        border_width=0,
        corner_radius=28,
        text=text,
        text_font= ("Futura Medium", 20 * -1),
        text_color=text_color,
        width=336,
        height=56
        )
    button.pack(padx=10,pady=10)
    return button

def bold_button(master, button_color, text, text_color):
    button = customtkinter.CTkButton(
        master = master,
        bg_color="#000000",
        fg_color=button_color,
        border_width=0,
        corner_radius=28,
        text=text,
        text_font= ("Futura Medium", 36 * -1),
        text_color=text_color,
        width=336,
        height=110
        )
    button.pack(padx=10,pady=10)
    return button

def back_button(master,bg_color):
    button = customtkinter.CTkButton(
        master=master,
        bg_color=bg_color,
        fg_color="#000000",
        border_width=0,
        corner_radius=28,
        text="back"

    )

def labeled_entry(master, label_text, entry_color, entry_text_color):
    entry_frame = customtkinter.CTkFrame(
            master = master,
            bg_color="#000000",
            fg_color="#000000",
            corner_radius=0
            )
    entry_label = customtkinter.CTkLabel(
            master=entry_frame,
            fg_color="#000000",
            corner_radius=0,
            text=label_text,
            justify=tkinter.LEFT,
            text_font=("Futura Medium", 12 * -1),
            text_color="#A9CEF0"
            )
    entry_label.pack(side=tkinter.TOP)
    entry = customtkinter.CTkEntry(
            master=entry_frame,
            bg_color="#000000",
            fg_color=entry_color,
            justify=tkinter.CENTER,
            text_font=("Futura Medium", 16 * -1),
            text_color=entry_text_color,
            border_width=0,
            corner_radius=28,
            width=336,
            height=56
            )
    entry.pack()
    entry_frame.pack(padx=10,pady=10)
    return entry

    


