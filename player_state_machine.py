from game_utils import *
import json

class PlayerSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.room = ''
        self.me = ''
        #my reactions
        self.out_msg = ''
        #s means socket
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    # join_room replaces connect_to here
    def join_room(self, room):
        msg = json.dumps({"action":"join","target": room})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            # replace peer in chat system with room here
            self.room = room
            # not sure what to reply to the player yet
            self.out_msg += 'You are in the room ' + self.room
            return(True)
        # maybe some other situatons, add more later
        else:
            self.out_msg += 'No such room.'
            return(False)
    
    def create_room(self, room_name):
        msg = json.dumps({"action":"create","name": room_name})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.room = room_name
            self.out_msg += 'You have created the room' + self.room
            return(True)
        elif response["status"] == "duplicate":
            self.out_msg += 'Room name has already been taken'
        else:
            self.out_msg += 'Something goes wrong. Fail to create the room.'
            return(False)

    def proc(self, my_action, room_reply):
        # my_action here replaces my_msg
        self.out_msg = ''
#==============================================================================
# After logged in, player need to: join a room, create a room
# Handling state "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            if len(my_action) > 0:
                # my_action is a dictionary
                if my_action['action'] == 'join':
                    # 'join' means join room
                    room = my_action['room']
                    if self.join_room(room) == True:
                        self.state = S_PAIRING
                        # self.out_msg += 
                    else:
                        self.out_msg += 'Fail to join the room\n'
                
                elif my_action['action'] == 'create':
                    # 'c' means create room
                    room_name = my_action['room_name']
                    if self.create_room(room_name) == True:
                        self.state = S_PAIRING

#==============================================================================
# Start pairing
#==============================================================================
        elif self.state == S_PAIRING:
            if len(my_action) > 0:
                mysend(self.s, json.dumps({'action':'start the game', 'from': self.me}))
            if len(room_reply) > 0:
                room_reply = json.loads(room_reply)
                if room_reply['action'] == 'denied':
                    self.out_msg += 'You can only start the game if there are more than two people'
                elif room_reply['action'] == 'set the game':
                    self.state = S_SETTING
                elif room_reply['action'] ==  'all set':
                    self.state = S_PLAYING

#==============================================================================
# Choose to create question. Handle the stage S_SETTING
#==============================================================================
        elif self.state == S_SETTING:
            if len(my_action) > 0:
                if my_action['action'] == 'set questions':
                    # questions and answers
                    #change mysend later
                    mysend(self.s, json.dumps({'action':'set questions', 'from': self.me}))
                elif my_action['action'] == 'answer_question':
                    mysend(self.s, json.dumps({'action':'answer questions', 'from': self.me}))

            elif len(room_reply) > 0:
                if room_reply['action'] == 'all set':
                    self.state = S_PLAYING










