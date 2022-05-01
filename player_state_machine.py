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
        else:
            self.out_msg += 'Something goes wrong. Fail to create the room.'
            return(False)

    # def disconnect(self):

    def proc(self, my_action, peer_action):
        # my_action here replaces my_msg
        self.out_msg = ''
#==============================================================================
# After logged in, player need to: join a room, create a room
# Handling state "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            if len(my_action) > 0:
                # my_action is a string
                if my_action[0] == 'j':
                    # 'j' means join room
                    room = my_action[1:]
                    if self.join_room(room) == True:
                        self.state = S_PAIRING
                        # self.out_msg += 
                    else:
                        self.out_msg += 'Fail to join the room\n'
                
                elif my_action[0] == 'c':
                    # 'c' means create room
                    room_name = my_action[1:]
                    if self.create_room(room_name) == True:
                        self.state = S_PAIRING






