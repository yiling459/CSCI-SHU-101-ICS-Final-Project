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
        # self.room = 
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




