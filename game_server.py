import time
import socket
import select
import sys
import string
# import indexer
import json
import pickle as pkl
from game_utils import *
import game_room as room

class Server:
    def __init__(self):
        self.new_players = []  # list of new sockets of which the user id is not known
        self.logged_name2sock = {}  # dictionary mapping username to socket
        self.logged_sock2name = {}  # dict mapping socket to user name
        self.all_sockets = []
        self.room = room.Room()
        # start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        # # initialize past chat indices
        # self.indices = {}
        # # sonnet
        # self.sonnet_f = open('AllSonnets.txt.idx', 'rb')
        # self.sonnet = pkl.load(self.sonnet_f)
        # self.sonnet_f.close()

    def new_player(self, sock):
        # add to all sockets and to new players
        print('new player...')
        sock.setblocking(0)
        self.new_players.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        try:
            msg = json.loads(myrecv(sock))
            print("login:", msg)
            if len(msg) > 0:

                if msg["action"] == "login":
                    name = msg["name"]

                    if self.room.is_member(name) != True:
                        # move socket from new clients list to logged clients
                        self.new_players.remove(sock)
                        # add into the name to sock mapping
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        # load chat history? Write that later
                        print(name + ' logged in')
                        self.room.enter_game(name)
                        # maybe change the send later
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "ok"}))

                    else: # a player under this name has already logged in
                        # duplicate? I may change it to "retry" later
                        mysend(sock, json.dumps(
                            {"action": "login", "status": "duplicate"}))
                        print(name + ' duplicate login attempt')
                else:
                    print('wrong code received')
            else:  # client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        # remove sock from all lists
        name = self.logged_sock2name[sock]
        # pkl.dump(self.indices[name], open(name + '.idx', 'wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.room.leave(name)
        sock.close()

# ==============================================================================
# main command switchboard
# ==============================================================================
    def handle_msg(self, from_sock):
        # read msg code
        msg = myrecv(from_sock)
        if len(msg) > 0:
# ==============================================================================
# handle create/join room request
# ==============================================================================
            msg = json.loads(msg)
            if msg["action"] == "create":
                room_name = msg["name"]
                from_name = self.logged_sock2name[from_sock]
                print(room_name, from_name)
                # check whether the room has already existed
                if self.room.find_room(room_name) == False:
                    print("start creating the room")
                    # create the room
                    self.room.create_room(from_name, room_name)
                    msg = json.dumps(
                        {"action": "create", "status": "success","members":[from_name]})
                elif self.room.find_room(room_name) == True:
                    print("room has been created")
                    # "duplicate" means the room name has already been taken by others
                    msg = json.dumps(
                        {"action": "create", "status": "duplicate"})
                else:
                    print("something goes wrong with create function")
                mysend(from_sock, msg)
            elif msg["action"] == "join":
                room_name = msg["name"]
                from_name = self.logged_sock2name[from_sock]
                # check whether the room exists
                if self.room.find_room(room_name) == True:
                    # join the room
                    self.room.join_room(from_name, room_name)
                    other_players = self.room.room_others(from_name, room_name)
                    all_players = self.room.room_members(room_name)
                    msg = json.dumps(
                        {"action": "join", "status": "success","members":all_players})
                    for player in other_players:
                        to_sock = self.logged_name2sock[player]
                        # status here means waiting for the game to start, may change later
                        # action here may also be changed later
                        print(player)
                        mysend(to_sock, json.dumps(
                            {"action": "pairing", "status": "waiting", "from": from_name}))
                elif self.room.find_room(room_name) == False:
                    msg = json.dumps(
                        {"action": "join", "status": "no such room"})

                else:
                    print("something goes wrong with join function")
                mysend(from_sock, msg)
# ==============================================================================
# decide whether to set the game base on the number of players
# ==============================================================================
            elif msg["action"] == "start the game":
                player_num = len(self.room.room_members)
                if player_num < 2:
                    msg = json.dumps(
                        {"action": "denied", "reason": "there must be over two players"})
                elif player_num == 2:
                    msg = json.dumps(
                        {"action": "all set"})
                elif player_num > 2:
                    msg = json.dumps(
                        {"action": "set the game"})

# ==============================================================================
# set the game
# ==============================================================================
            elif msg["action"] == "set questions":
                pass
        
        else:
            # client died unexpectedly
            self.logout(from_sock)




    def run(self):
        print('starting game server...')
        while(1):
            read, write, error = select.select(self.all_sockets, [], [])
            print('checking logged players..')
            for logc in list(self.logged_name2sock.values()):
                if logc in read:
                    self.handle_msg(logc)
            print('checking new players..')
            for newc in self.new_players[:]:
                if newc in read:
                    self.login(newc)
            print('checking for new connections..')
            if self.server in read:
                # new player request
                sock, address = self.server.accept()
                self.new_player(sock)


def main():
    server = Server()
    server.run()

if __name__ == "__main__":
    main()



                        
                        






