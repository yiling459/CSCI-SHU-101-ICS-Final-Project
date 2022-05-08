import socket
import time
import random

# use local loop back address by default
#CHAT_IP = '127.0.0.1'
# CHAT_IP = socket.gethostbyname(socket.gethostname())
CHAT_IP = ''  # socket.gethostbyname(socket.gethostname())

CHAT_PORT = 1112
SERVER = (CHAT_IP, CHAT_PORT)

#maybe we can add something like menu here

S_OFFLINE = 0
S_LOGGEDIN = 1
S_PAIRING = 2
S_SETTING = 3
S_PLAYING = 4

SIZE_SPEC = 5

# CHAT_WAIT = 0.2

def print_state(state):
    print('**** State *****::::: ')
    if state == S_OFFLINE:
        print('Offline')
    elif state == S_LOGGEDIN:
        print('Logged in')
    elif state == S_PAIRING:
        print('Paring other players')
    elif state == S_SETTING:
        print('Setting the game')
    elif state == S_PLAYING:
        print('Gaming')
    else:
        print('Error: wrong state')

def mysend(s, msg):
    # append size to message and send it
    msg = ('0' * SIZE_SPEC + str(len(msg)))[-SIZE_SPEC:] + str(msg)
    msg = msg.encode()
    total_sent = 0
    while total_sent < len(msg):
        sent = s.send(msg[total_sent:])
        if sent == 0:
            print('server disconnected')
            break
        total_sent += sent

def myrecv(s):
    # receive size first
    size = ''
    while len(size) < SIZE_SPEC:
        text = s.recv(SIZE_SPEC - len(size)).decode()
        if not text:
            print('disconnected')
            return('')
        size += text
    size = int(size)
    # now receive message
    msg = ''
    while len(msg) < size:
        text = s.recv(size-len(msg)).decode()
        if text == b'':
            print('disconnected')
            break
        msg += text
    return (msg)

def label_time(msg, label):
    current_time = time.strftime('%d.%m.%y,%H:%M:%S', time.localtime())
    msg[label] = current_time

def generate_question_and_answers(color_dict:dict):
    choices = [random.choice(list(color_dict)) for i in range(4)]
    # question is also the right color
    question = choices[0]
    answers_name = [[question,True]]
    answers_hex = [color_dict[question]]
    for wrong_color in choices[1:]:
        answers_name.append([wrong_color,False])
        answers_hex.append(color_dict[wrong_color])
    random.shuffle(answers_name)
    random.shuffle(answers_hex)
    return question, answers_name, answers_hex

        





#def text_proc(text, user):
    # ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
    # # message goes directly to screen
    # return('(' + ctime + ') ' + user + ' : ' + text)
