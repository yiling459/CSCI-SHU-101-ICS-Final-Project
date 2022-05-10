from cProfile import label
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
        text="Back",
        text_font= ("Futura Medium", 36 * -1),
        text_color="#FFFFFF",
        width=200,
        height=56
        )
    # button.pack(padx=10,pady=10)
    return button

def next_button(master,bg_color):
    button = customtkinter.CTkButton(
        master=master,
        bg_color=bg_color,
        fg_color="#000000",
        border_width=0,
        corner_radius=28,
        text="Next",
        text_font= ("Futura Medium", 36 * -1),
        text_color="#FFFFFF",
        width=200,
        height=100
        )
    button.pack(padx=10,pady=10)

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

# def long_entry(master, bg_color, entry_color, entry_text_color):
#     entry = customtkinter.CTkEntry(
#         master=master,
#         bg_color=bg_color,
#         fg_color=entry_color,
#         justify=tkinter.CENTER,
#         text_font=("Futura Medium", 16 * -1),
#         text_color=entry_text_color,
#         border_width=0,
#         corner_radius=28,
#         width=1020,
#         height=56
#         )
#     entry.pack()
#     return entry
def thick_button(master, button_color, text, text_color):
    button = customtkinter.CTkButton(
        master = master,
        bg_color="#FFFFFF",
        fg_color=button_color,
        border_width=5,
        border_color="red",
        corner_radius=28,
        text=text,
        text_font= ("Futura Medium", 20 * -1),
        text_color=text_color,
        width=213,
        height=360
        )
    button.pack(padx=10,pady=10,side = tkinter.LEFT)
    return button


# def question_entry(master,frame_background_color,label_color,entry_color,entry_text_color):
#     question_frame =  customtkinter.CTkFrame(
#             master = master,
#             bg_color=frame_background_color,
#             fg_color=frame_background_color,
#             corner_radius=0
#             )
#     entry_label = customtkinter.CTkLabel(
#             master=question_frame,
#             fg_color=frame_background_color,
#             corner_radius=0,
#             text="Type the question in the box",
#             justify=tkinter.LEFT,
#             text_font=("Futura Medium", 12 * -1),
#             text_color=label_color
#             )
#     entry_label.pack(side=tkinter.TOP)
#     entry=long_entry(question_frame,frame_background_color,entry_color,entry_text_color)
#     entry.pack()
#     # change the padding later
#     question_frame.pack(padx=10,pady=10)
#     return entry


def question_label(master, text="question yeahyeahyeahyeahyeahyeah"):
    question = customtkinter.CTkLabel(
        master=master,
        fg_color="#FFFFFF",
        corner_radius=0,
        text=text,     
        justify=tkinter.CENTER,
        text_font=("Futura Medium", 64 * -1),
        text_color="#000000"
        )
    question.pack()


# a brutal way to write entries for answers
# return a list
# def answers_entry(master,frame_background_color,label_color,entry_colors:list,entry_text_colors:list):
#     answers_frame = customtkinter.CTkFrame(
#             master = master,
#             bg_color=frame_background_color,
#             fg_color=frame_background_color,
#             corner_radius=0
#             )
#     entry_label = customtkinter.CTkLabel(
#             master=answers_frame,
#             fg_color=frame_background_color,
#             corner_radius=0,
#             text="Options",
#             justify=tkinter.LEFT,
#             text_font=("Futura Medium", 12 * -1),
#             text_color=label_color
#             )
#     entry_label.pack(side=tkinter.TOP)
#     entry_1 = long_entry(answers_frame,frame_background_color,entry_colors[0],entry_text_colors[0])
#     entry_1.pack(padx=0,pady=10)
#     entry_2 = long_entry(answers_frame,frame_background_color,entry_colors[1],entry_text_colors[1])
#     entry_2.pack(padx=0,pady=10)
#     entry_3 = long_entry(answers_frame,frame_background_color,entry_colors[2],entry_text_colors[2])
#     entry_3.pack(padx=0,pady=10)
#     entry_4 = long_entry(answers_frame,frame_background_color,entry_colors[3],entry_text_colors[3])
#     entry_4.pack(padx=0,pady=10)

#     return [entry_1, entry_2, entry_3, entry_4]

#use loop to write entries for answers
def answers_entry(master,frame_background_color,label_color,entry_colors:list,entry_text_colors:list):
    entry_1,entry_2,entry_3,entry_4=None,None,None,None
    entry_lst=[entry_1,entry_2,entry_3,entry_4]
    answers_frame = customtkinter.CTkFrame(
            master = master,
            bg_color=frame_background_color,
            fg_color=frame_background_color,
            corner_radius=0
            )
    entry_label = customtkinter.CTkLabel(
            master=answers_frame,
            fg_color=frame_background_color,
            corner_radius=0,
            text="Options",
            justify=tkinter.LEFT,
            text_font=("Futura Medium", 12 * -1),
            text_color=label_color
            )
    entry_label.pack(side=tkinter.TOP)
    for entry in entry_lst:
        idx=0
        entry = long_entry(answers_frame,frame_background_color,entry_colors[idx],entry_text_colors[idx])
        entry.pack(padx=0,pady=10)
        idx+=1
    
    return entry_lst


    




    


