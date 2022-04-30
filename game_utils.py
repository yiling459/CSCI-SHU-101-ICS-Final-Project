import socket
import time

# use local loop back address by default
#CHAT_IP = '127.0.0.1'
# CHAT_IP = socket.gethostbyname(socket.gethostname())
CHAT_IP = ''  # socket.gethostbyname(socket.gethostname())

CHAT_PORT = 1112
SERVER = (CHAT_IP, CHAT_PORT)

#maybe we can add something like menu here

S_OFFLINE = 0
S_CONNECTED = 1
S_PAIRING = 2
S_PLAYING = 3

#SIZE_SPEC = 5

# CHAT_WAIT = 0.2

def print_state(state):
    print('**** State *****::::: ')
    if state == S_OFFLINE:
        print('Offline')
    elif state == S_CONNECTED:
        print('Connected')
    elif state == S_PAIRING:
        print('Paring other players')
    elif state == S_PLAYING:
        print('Gaming')
    else:
        print('Error: wrong state')

#def mysend(s,msg)

#def myrecv(s)

#def text_proc(text, user):
    # ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
    # # message goes directly to screen
    # return('(' + ctime + ') ' + user + ' : ' + text)
