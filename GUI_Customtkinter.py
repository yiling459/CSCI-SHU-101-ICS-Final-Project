from pathlib import Path
import re
from turtle import bgcolor, right
from xml.etree.ElementTree import TreeBuilder

from click import command
from game_utils import *
from GUI_Assets import *
import tkinter
import json
import threading
import select
import sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./ASSETS")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

import customtkinter
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

class GUI:
    def __init__(self, send, recv, state, s):
        self.window = customtkinter.CTk()
        self.window.geometry("1200x800")
        self.window.configure(bg = "#5294D0")
        self.canvas_width = 1200.0
        self.canvas_height = 800.0
        # init color palettes
        self.color_primary = "#57A2E8"
        self.color_secondary = "#96C3ED"
        self.color_tertiary = "#D5E9F9"
        self.color_on_primary = "#FFFFFF"
        self.color_on_secondary = "#FFFFFF"
        self.color_on_tertiary = "#000000"
        self.color_background = "#5293CF"
        # init socket
        self.send = send
        self.recv = recv
        self.state = state
        self.socket = s
        # init the member_lst of the room
        self.members_lst = []
        self.round_num = 1

    def start_page(self,notification="Enter Your Name"):
        # create the CTKcanvas
        canvas = customtkinter.CTkCanvas(self.window,
                                        bg = "#FFFFFF",
                                        height = self.canvas_height,
                                        width = self.canvas_width,
                                        bd = 0,
                                        highlightthickness = 0,
                                        relief = "ridge")
        canvas.place(x=0,y=0)
        # create the background image
        background_image = tkinter.PhotoImage(file = relative_to_assets("start_page_background.png"))
        canvas.create_image(0,
                            0,
                            anchor = 'nw',
                            image = background_image)
        
        # make the frame for contents
        frame = customtkinter.CTkFrame(
            master = self.window,
            width=417,
            height=282,
            bg_color="#000000",
            fg_color="#000000",
            )
        frame.place(relx=0.5,y=454,anchor="n")

        # create entry
        name_entry = labeled_entry(frame,notification,self.color_tertiary,self.color_on_tertiary)
        
        # create new room button
        new_room_button = slim_button(frame, self.color_secondary, "New Room", self.color_on_secondary)
        new_room_button.config(command = lambda: self.register_name(name_entry.get(),"create"))
        
        # create join room button
        join_room_button = slim_button(frame, self.color_primary,"Join Room", self.color_on_primary)
        join_room_button.config(command = lambda: self.register_name(name_entry.get(),"join"))
          
        self.window.mainloop()

    def register_name(self, player_name, action):
        if len(player_name) > 0:
            msg = json.dumps({"action": "login", "name": player_name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == "ok":
                self.state.set_state(S_LOGGEDIN)
                self.state.set_myname(player_name)
                if action == "create":
                    self.create_page(player_name)
                elif action == "join":
                    self.join_page(player_name)
            elif response["status"] == "duplicate":
                self.start_page(notification="This name has been registered. Please enter another")

    def create_page(self, player_name="empty", notification="Enter Room Name:"):
        # create the CTKcanvas
        canvas = customtkinter.CTkCanvas(self.window,
                                        bg = "#FFFFFF",
                                        height = self.canvas_height,
                                        width = self.canvas_width,
                                        bd = 0,
                                        highlightthickness = 0,
                                        relief = "ridge")
        canvas.place(x=0,y=0)


        # create the background image
        background_image = tkinter.PhotoImage(file = relative_to_assets("create_page_background.png"))
        canvas.create_image(0,
                            0,
                            anchor = 'nw',
                            image = background_image)

        # make the frame for contents
        frame = customtkinter.CTkFrame(
            master = self.window,
            width=417,
            height=431,
            bg_color="#000000",
            fg_color="#000000",
            )
        frame.place(x=932.5,y=280,anchor="n")

        # create entry
        room_name_entry = labeled_entry(frame,notification,self.color_tertiary,self.color_on_tertiary)
        
        # create continue button
        new_room_button = slim_button(frame, self.color_secondary, "CONTINUE", self.color_on_secondary)
        new_room_button.config(command = lambda: self.register_room(player_name,room_name_entry.get(),"create"))
        
        # create back button
        back= slim_button(frame,self.color_primary,"BACK",self.color_on_primary)
        back.config(command = lambda: self.start_page())

        self.window.mainloop()


    def join_page(self, player_name="empty", notification="Enter room name:"):
        # create the CTKcanvas
        canvas = customtkinter.CTkCanvas(self.window,
                                        bg = "#FFFFFF",
                                        height = self.canvas_height,
                                        width = self.canvas_width,
                                        bd = 0,
                                        highlightthickness = 0,
                                        relief = "ridge")
        canvas.place(x=0,y=0)


        # create the background image
        background_image = tkinter.PhotoImage(file = relative_to_assets("join_page_background.png"))
        canvas.create_image(0,
                            0,
                            anchor = 'nw',
                            image = background_image)


        # make the frame for contents
        frame = customtkinter.CTkFrame(
            master = self.window,
            width=417,
            height=431,
            bg_color="#000000",
            fg_color="#000000",
            )
        frame.place(x=932.5,y=280,anchor="n")

        # create entry
        room_name_entry = labeled_entry(frame,notification,self.color_tertiary,self.color_on_tertiary)
        

        # create continue button
        continue_button = slim_button(frame, self.color_secondary, "CONTINUE", self.color_on_secondary)
        continue_button.config(command = lambda: self.register_room(player_name,room_name_entry.get(),"join"))
        
        # create back button
        back= slim_button(frame,self.color_primary,"BACK",self.color_on_primary)
        back.config(command = lambda: self.start_page())

        self.window.mainloop()

    def register_room(self, player_name, room_name, action):
        if len(room_name) > 0:
            if action == "create":
                msg = json.dumps({"action": action, "name": room_name})
            elif action == "join":
                msg = json.dumps({"action": action, "name": room_name})
            self.send(msg)
            response = json.loads(self.recv())
            # create&join share the same
            if response["status"] == "success":
                self.members_lst = response["members"]
                self.state.set_state(S_PAIRING)
                self.pairing_page(room_name)

            # create only
            elif response["status"] == "duplicate":
                self.create_page(player_name, notification="This room has been registered. Please enter another:")
            # join only
            elif response["status"] == "no such room":
                self.join_page(player_name, notification="No such room. Please enter another:")
            elif response["status"] == "waiting":
                self.members_lst.append(response["from"])




    def pairing_page(self,room_name="init"):
        self.room_name = room_name


        background_left = customtkinter.CTkFrame(
            master = self.window,
            width=425,
            height=800,
            fg_color=self.color_primary,
            corner_radius=0
            )
        background_left.place(x=0,y=0)
        self.window.config(bg="#FFFFFF")
        room = customtkinter.CTkLabel(
            master = background_left,
            text_color = self.color_on_primary,
            text = "Room:\n" + room_name,
            text_font= ("Montserrat Alternates SemiBold", 40 * -1),
            justify = tkinter.LEFT
            )
        room.place(relx=0.1,rely=0.2)

        divider = customtkinter.CTkFrame(
            master = background_left,
            width = 220,
            height = 10,
            fg_color = self.color_on_primary,
            )
        divider.place(relx=0.12, y =279)

        guide = customtkinter.CTkLabel(
            master = background_left,
            text_color = self.color_on_primary,
            text = "Use your knowledge\nto compete with\nyour friends.\nLearn for fun!",
            text_font= ("Geo", 28 * -1),
            justify = tkinter.LEFT
            )
        guide.place(relx=0.1, rely=0.4)

        background_right = customtkinter.CTkFrame(
            master = self.window,
            width=775,
            height=800,
            fg_color="#FFFFFF",
            corner_radius=0
            )
        background_right.place(x=425,y=0)
        

        title = customtkinter.CTkLabel(
            master = background_right,
            text_color = self.color_on_tertiary,
            text = "Waiting For Players...",
            text_font= ("Montserrat Alternates SemiBold", 60 * -1),
            justify = tkinter.LEFT
            )
        title.place(relx=0.5,y=157,anchor="center")

        self.member_frame = customtkinter.CTkFrame(
            master = background_right,
            bg_color="#FFFFFF",
            fg_color="#FFFFFF"
            )
        self.member_frame.place(relx=0.1,y=220)


        # show who are in the room
        for player in self.members_lst:
            customtkinter.CTkLabel(
                master = self.member_frame,
                text = player,
                text_color = self.color_on_secondary,
                text_font = ("Montserrat Alternates SemiBold", 24 * -1),
                corner_radius=5,
                bg_color=self.color_on_primary,
                fg_color=self.color_secondary
                ).pack(side=tkinter.LEFT,padx=10)

        join_button = bold_button(
            master=background_right,
            button_color=self.color_primary,
            text="Start Game",
            text_color=self.color_on_primary
            )
        join_button.config(bg_color = "#FFFFFF")
        join_button.place(relx=0.1,rely=0.75)
        join_button.config(command = lambda:self.send_game_start_msg())


        self.update = True
        self.response = {}

        self.response_threading = threading.Thread(target=self.get_response)
        self.response_threading.daemon = True
        self.response_threading.start()

        self.member_frame.after(10,lambda:self.update_member())

        self.window.mainloop()
    
    def send_game_start_msg(self):
        msg = json.dumps({"action":"game start", "from room":self.room_name})
        self.send(msg)

    def get_response(self):
        while True:
            self.response = json.loads(self.recv())

    def update_member(self):
        if self.update == True:
            if len(self.response) > 0:
                if self.response["action"] == "pairing":
                    player = self.response["from"]
                    if player not in self.members_lst:
                        self.members_lst.append(player)
                        customtkinter.CTkLabel(
                            master = self.member_frame,
                            text = player,
                            text_color = self.color_on_secondary,
                            text_font = ("Montserrat Alternates SemiBold", 24 * -1),
                            corner_radius=5,
                            bg_color=self.color_on_primary,
                            fg_color=self.color_secondary
                            ).pack(side=tkinter.LEFT,padx=10)
                elif self.response["action"] == "game start":
                    if self.response["status"] == "success":
                        self.update = False
                        self.game_rule_page()
                        
                    elif self.response["status"] == "denied":
                        caution = customtkinter.CTkLabel(
                            master=self.window,
                            bg_color="#FFFFFF",
                            fg_color="#FFFFFF",
                            text="*Caution: There should be at least two people in a room to start a game",
                            text_color="red",
                            text_font = ("Montserrat Alternates SemiBold", 12 * -1)
                            )
                        caution.place(x=495,y=720)

            self.member_frame.after(10,lambda:self.update_member())                   

    def game_rule_page(self):
        # make the frame for contents
        frame = customtkinter.CTkFrame(
            master = self.window,
            width=1200,
            height=800,
            bg_color="#000000",
            fg_color="#000000",
            )
        frame.place(x=0,y=0)


        # create "GAME RULES"
        reminder = customtkinter.CTkLabel(
            master = frame,
            text_color = self.color_primary,
            text = "GAME RULES",
            text_font= ("Montserrat Alternates SemiBold", 80 * -1),
            )
        reminder.place(relx=0.5,rely=0.25,anchor="n")

        #create reminder
        reminder = customtkinter.CTkLabel(
            master = frame,
            text_color = self.color_primary,
            text = "Choose the word\nthat matchesthe question.\nDo not be confused by the button color.\n\nFive rounds in total\nThe quickest wins",
            text_font= ("Geo", 38 * -1),
            )
        reminder.place(relx=0.5,rely=0.4,anchor="n")

        # init the count down timer here
        count_down = 5

        reminder = customtkinter.CTkLabel(
            master = frame,
            text_color = self.color_primary,
            text_font= ("Montserrat Alternates SemiBold", 25),
            text = "Game will start in "+str(count_down),
            justify = "right"
            )
        reminder.place(x=900,y=60,anchor="nw")

        frame.after(1000,lambda: self.count_down_game_rule(frame,reminder,count_down-1))

        self.window.mainloop()
    
    def count_down_game_rule(self,frame,reminder,count_down):
        if count_down == 0:
            question =self.response["question"]
            answers_name=self.response["answers_name"]
            answers_hex=self.response["answers_hex"]
            color_name_lst=[question]
            color_hex_lst=answers_hex
            for idx in range(len(answers_name)):
                color_name_lst.append(answers_name[idx][0])
                if answers_name[idx][1] == True:
                    right_idx = idx
                
            self.play_game_page(color_name_lst,self.round_num,color_hex_lst,right_idx)
        else:
            reminder.config(text = "Game will start in "+str(count_down))
            reminder.place(x=860,y=60,anchor="nw")

            frame.after(1000,lambda: self.count_down_game_rule(frame,reminder,count_down-1))
            
    def play_game_page(self, color_name=["question","color1","color2","color3","color4"],question_num=0,button_color=["#000000","#000000","#000000","#000000"],right_idx=1):
        question_num = self.round_num
        # make the frame for contents
        frame = customtkinter.CTkFrame(
            master = self.window,
            width=1200,
            height=800,
            bg_color = "#FFFFFF",
            fg_color = "#FFFFFF",
            )
        frame.place(x=0,y=0,anchor="nw")

        # create title
        title = customtkinter.CTkLabel(
            master = frame,
            text_color = "#5293CF",
            text = "Question("+str(question_num)+"/5)",
            text_font= ("Montserrat Alternates SemiBold", 40 * -1)
            )
        title.place(relx=0.05,rely=0.05)

        # create frame for questions & answers
        frame_question = customtkinter.CTkFrame(
            master = self.window,
            width=1200,
            height=800,
            bg_color = self.color_background,
            fg_color = self.color_background,
            )
        frame_question.place(relx=0.5,rely=0.5,anchor='n')

        # set the question
        question = question_label(
            master = frame_question, 
            text = color_name[0].upper()
            )
        frame_question.place(relx=0.5,rely=0.185)
        
        frame_answers = customtkinter.CTkFrame(
            master = self.window,
            width=1200,
            height=800,
            bg_color = "#FFFFFF",
            fg_color = "#FFFFFF",
            )
        frame_answers.place(relx=0.5,rely=0.4,anchor='n')
        
        # create "options" label
        options = customtkinter.CTkLabel(
            master = frame,
            text_color = "#FFFFFF",
            text = "Options",
            text_font= ("Geo", 40 * -1),
            )
        options.place(relx=0.08,rely=0.333)

        answer1 = thick_button(
            master = frame_answers,
            button_color = button_color[0],
            text = color_name[1],
            text_color = "#FFFFFF"
            )
        answer1.config(command = lambda: self.change_button_color(answer1,False))
    
        answer2 = thick_button(
            master = frame_answers,
            button_color = button_color[1],
            text = color_name[2],
            text_color = "#FFFFFF",
            )
        answer2.config(command = lambda: self.change_button_color(answer2,False))

        answer3 = thick_button(
            master = frame_answers,
            button_color = button_color[2],
            text =color_name[3],
            text_color = "#FFFFFF",
            )
        answer3.config(command = lambda: self.change_button_color(answer3,False))

        answer4 = thick_button(
            master = frame_answers,
            button_color = button_color[3],
            text = color_name[4],
            text_color = "#FFFFFF",
            )
        answer4.config(command = lambda: self.change_button_color(answer4,False))

        # a very brutal way
        if right_idx == 0:
            answer1.config(command = lambda: self.change_button_color(answer1,True))
        elif right_idx == 1:
            answer2.config(command = lambda: self.change_button_color(answer2,True))
        elif right_idx == 2:
            answer3.config(command = lambda: self.change_button_color(answer3,True))
        elif right_idx == 3:
            answer4.config(command = lambda: self.change_button_color(answer4,True))
        

        self.window.mainloop()

    def change_button_color(self,answer_button,label):
        if label == "get response":
            if self.response["action"] == "round end":
                top_player = " & ".join(self.response["top players"])
                top_score = self.response["top score"]
                player_score = self.response["player score"]
   
                if self.round_num == 5:
                    top_three_lst = self.response["top three"]
                    self.player_ranking_page(top_three_lst)
                else:
                    self.new_round_starter(top_player,top_score,player_score)

            elif self.response["action"] == "able to start next round":
    
                top_player = " & ".join(self.response["top players"])
                top_score = self.response["top score"]
                player_score = self.response["player score"]
                if self.round_num < 5:
                    self.send_game_start_msg()
                    self.new_round_starter(top_player,top_score,player_score)

                elif self.round_num == 5:
                    top_three_lst = self.response["top three"]
                    self.player_ranking_page(top_three_lst)

            else:
                answer_button.after(10,lambda: self.change_button_color(answer_button,label))

        else:
            if label == True:
                answer_button.config(border_color="green")
                msg = json.dumps({"action":"choice made","status":"right","from room":self.room_name})
                self.send(msg)
                label = "get response"
            elif label == False:
                answer_button.config(border_color="red")
                msg = json.dumps({"action":"choice made","status":"wrong","from room":self.room_name})
                self.send(msg)
                label = "get response"

            answer_button.after(10,lambda: self.change_button_color(answer_button,label))

    def new_round_starter(self,top_player,top_score,your_current_score):
        self.update = True
        while self.update:
            if self.response["action"] == "game start":
                if self.response["status"] == "success":
                        self.update = False
                        self.billboard_page(top_player,top_score,your_current_score)

    def billboard_page(self,top_player="empty",top_score=0,your_current_score=0,round_num=0):
        # create the CTKcanvas
        round_num = self.round_num

        # make the frame for contents
        frame = customtkinter.CTkFrame(
            master = self.window,
            width=1200,
            height=800,
            bg_color="#000000",
            fg_color="#000000",
            )
        frame.place(x=0,y=0)

        # create "Billboard"
        billboard_title = customtkinter.CTkLabel(
            master = frame,
            text_color = self.color_primary,
            text = "Billboard",
            text_font= ("Montserrat Alternates SemiBold", 80 * -1),
            )
        billboard_title.place(relx=0.5,rely=0.25,anchor="n")

        #create details
        details = customtkinter.CTkLabel(
            master = frame,
            text_color = self.color_primary,
            text = "current TOP1: "+top_player+"\nSCORE: "+str(top_score)+"\nYour current score: "+str(your_current_score),
            text_font= ("Geo", 38 * -1),
            justify = "center"
            )
        details.place(relx=0.5,rely=0.4,anchor="n")

        #create "round number"
        round_number = customtkinter.CTkLabel(
            master = frame,
            text_color = "#FFFFFF",
            text = "Round "+str(round_num),
            text_font= ("Montserrat Alternates SemiBold", 25),
            )
        round_number.place(x=1000,y=60,anchor="nw")

        #create the countdown timer
        count_down = 5
        timer = customtkinter.CTkLabel(
            master = frame,
            text_color = self.color_primary,
            text = "next round will start in "+str(count_down),
            text_font= ("Montserrat Alternates SemiBold", 25),
            justify = "right"
            )
        timer.place(relx=0.5,rely=0.8,anchor="n")
        frame.after(1000,lambda: self.count_down_billboard(frame,timer,count_down))
        
        self.window.mainloop()

    def count_down_billboard(self,frame,timer,count_down):
        if count_down == 0:
            self.round_num += 1
            question =self.response["question"]
            answers_name=self.response["answers_name"]
            answers_hex=self.response["answers_hex"]
            color_name_lst=[question]
            color_hex_lst=answers_hex

            for idx in range(len(answers_name)):
                color_name_lst.append(answers_name[idx][0])
                if answers_name[idx][1] == True:
                    right_idx = idx

            self.play_game_page(color_name_lst,self.round_num,color_hex_lst,right_idx)

        else:
            timer.config(text = "next round will start in "+str(count_down))
            frame.after(1000,lambda: self.count_down_billboard(frame,timer,count_down-1))
            
    def player_ranking_page(self,top_three_lst=["First","Second","Third"]):
        # create the CTKcanvas
        canvas = customtkinter.CTkCanvas(self.window,
                                        bg = "#FFFFFF",
                                        height = self.canvas_height,
                                        width = self.canvas_width,
                                        bd = 0,
                                        highlightthickness = 0,
                                        relief = "ridge")
        canvas.place(x=0,y=0)
        # create the background image
        background_image = tkinter.PhotoImage(file = relative_to_assets("player_ranking_page_background.png"))
        canvas.create_image(0,
                            0,
                            anchor = 'nw',
                            image = background_image)
        
        ranking_first_image = tkinter.PhotoImage(file = relative_to_assets("ranking_first.png"))
        ranking_second_image = tkinter.PhotoImage(file = relative_to_assets("ranking_second.png"))
        ranking_third_image = tkinter.PhotoImage(file = relative_to_assets("ranking_third.png"))
        first_x = 1200
        first_stop_place = 220
        first_step = -10

        second_x = -290
        second_stop_place = 10
        second_step = 10

        third_x = -290
        third_stop_place = 10
        third_step = 10

        stop_place_lst = [first_stop_place,second_stop_place,third_stop_place]
        x_lst = [first_x,second_x,third_x]
        y_lst = [165,484,633]
        step_lst = [first_step,second_step,third_step]
        interval_time = 10
        
        ranking_first = customtkinter.CTkButton(
            master=self.window,
            image=ranking_first_image,
            corner_radius=0,
            border_width=0,
            hover=False,
            text=""
            )
        ranking_first.place(x=first_x,y=165,anchor="nw")
        

        ranking_second = customtkinter.CTkButton(
            master=self.window,
            image=ranking_second_image,
            corner_radius=0,
            border_width=0,
            hover=False,
            text=""
            )
        ranking_second.place(x=second_x,y=484,anchor="nw")

        ranking_third = customtkinter.CTkButton(
            master=self.window,
            image=ranking_third_image,
            corner_radius=0,
            border_width=0,
            hover=False,
            text=""
            )
        ranking_third.place(x=third_x,y=633,anchor="nw")
        
        ranking_first.after(interval_time,lambda: self.first_ranking_animation(stop_place_lst,x_lst,y_lst,step_lst,[ranking_first,ranking_second,ranking_third],interval_time,top_three_lst))

        self.window.mainloop()   
    
    def first_ranking_animation(self,stop_place:list,x:list,y:list,step:list,ranking:list,interval_time,top_three_lst):
        if x[0] == stop_place[0]:
            # create 1st player label
            customtkinter.CTkLabel(
                master = self.window,
                text_color = "#000000",
                text = top_three_lst[0],
                text_font= ("Montserrat Alternates SemiBold", 120),
                bg_color="#FFFFFF"
                ).place(x=530,y=190,anchor="nw") 

            self.others_ranking_animation(stop_place[1],x[1],y[1],y[2],step[1],ranking[1],ranking[2],interval_time,top_three_lst)

        else:
            x[0] += step[0]
            ranking[0].place(x=x[0],y=y[0],anchor="nw")
            ranking[0].after(interval_time,lambda: self.first_ranking_animation(stop_place,x,y,step,ranking,interval_time,top_three_lst))
    
    def others_ranking_animation(self,stop_place,x,second_y,third_y,step,ranking_second,ranking_third,interval_time,top_three_lst):
        if x == stop_place:
            # create 2nd player label
            customtkinter.CTkLabel(
                master = self.window,
                text_color = "#FFFFFF",
                text = top_three_lst[1],
                text_font= ("Montserrat Alternates SemiBold", 96),
                bg_color=self.color_background
                ).place(x=530,y=460,anchor="nw") 
            
            # create 3rd player label
            customtkinter.CTkLabel(
                master = self.window,
                text_color = "#FFFFFF",
                text = top_three_lst[2],
                text_font= ("Montserrat Alternates SemiBold", 96),
                bg_color=self.color_background
                ).place(x=530,y=620,anchor="nw") 
        else:
            ranking_second.place(x=x,y=second_y,anchor="nw")
            ranking_third.place(x=x,y=third_y,anchor="nw")
            ranking_second.after(interval_time,lambda: self.others_ranking_animation(stop_place,x+step,second_y,third_y,step,ranking_second,ranking_third,interval_time,top_three_lst))

    def run(self):
        self.start_page()

if __name__ == "__main__":
    g = GUI('','','','')
    # g.start_page()
    # g.create_page()
    # g.join_page()
    # g.pairing_page()
    # g.choose_identity_page()
    # g.game_rule_page()
    # g.play_game_page()
    # g.billboard_page()
    # g.play()
    g.player_ranking_page()