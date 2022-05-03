S_ALONE = 0
S_PAIRING = 1

class Room:

    def __init__(self):
        self.members = {}
        self.game_rooms = {}

    # substitute function join(self, me)
    def enter_game(self,name):
        self.members[name] = S_ALONE
    
    # def is_member(self,name):
    #     return name in self.members.keys()
    
    def leave(self, name):
        self.disconnect(name)
        del self.members[name]
        return

    def find_room(self, room):
        found = False
        if room in self.game_rooms.keys():
            found = True
        return found


    def join_room(self, me, room):
        room_exist = self.find_room(room)
        if room_exist == True:
            print("You are in the room" + room)
            self.game_rooms[room].append(me)
            self.members[me] = S_PAIRING
        else:
            print("No such room named " + room + ". Please try again.")

    def create_room(self, me, room):
        room_exist = self.find_room(room)
        if room_exist == False:
            print("You have successfully created the room " + room)
            self.game_rooms[room] = [me]
            self.members[me] = S_PAIRING

    # def quit_room(self, me):
    
    def room_members(self, room):
        return self.game_rooms[room]

    
