import sys
import socket
import re
import time
import traceback

from calc import card_probability#, card_strength
from model.card import Card
from model.player import Player
# from decision import cards2_judge

# 0,1-hands 2,3,4-flop 5-turn 6-river
hand_card = [None]*2
board_card = []
probability = [None]*10

# state
board_state = ''
round_state = 0

# key is player's PID
num_player = 0
opponent_dic = {}

# my PID
client_pid = ''

# game over flag
is_game_over = False

# parse socket command_block
def init_player_seat(lines):
    global opponent_dic
    global is_game_over
    global num_player
    opponent_dic = {}
    num_player = 0

    for line in lines:
        parameter = line.split(' ')
        try:
            pid = parameter[-4]
            if pid != client_pid:
                num_player += 1
                opponent_dic[pid] = Player()
        except:
            is_game_over = True
            print 'seat parse error'

def card_parse(lines):
    cards = []

    for line in lines:
        parameter = line.split(' ')
        try:
            card_str = str(Card(parameter[0], parameter[1]))
            cards.append(card_str)
        except:
            global is_game_over
            is_game_over = True
            print 'card parse error'

    if len(cards) == 1:
        return card_str
    return cards

def oppo_parse(lines):
    global opponent_dic
    global is_game_over

    for line in lines[:-1]:
        parameter = line.split(' ')
        pid = parameter[0]
        try:
            if pid != client_pid:
                opponent_dic[pid].update_bet_from_inquire(line)
        except:
            is_game_over = True
            print 'oppo parse error'

def creat_oppo_array():
    oppobehave = []
    opponum = []
    for key in opponent_dic:
        oppo = opponent_dic[key]
        if oppo.state != []:
            oppobehave.append(oppo.state)
            opponum.append(oppo.bet)

    return oppobehave, opponum

def parse_with_recv(recv):
    command_block = re.finditer(r"(\w+)/ \n([\s\S]*?)/(\1) \n", recv)

    for block in command_block:
        command = block.group(1)
        body = block.group(2).splitlines()

        if command == 'inquire':
            # oppo_parse(body)
            # (oppobehave, opponum) = creat_oppo_array()
            return make_decision()
        # elif command == 'showdown':
        #     return 
        elif command == 'seat':
            init_player_seat(body)
        elif command in ['hold','flop','turn','river']:
            card_update(command, body)

    return None

def card_update(command, body):
    global board_state
    board_state = command

    global round_state
    round_state = 0

    global board_card
    global probability
    if command == 'hold':
        global hand_card
        hand_card = card_parse(body)
    elif command == 'flop':
        board_card = card_parse(body)
        probability = card_probability.calc(hand_card, board_card)
    elif command == 'turn':
        board_card.append(card_parse(body))
        probability = card_probability.calc(hand_card, board_card)
    elif command == 'river':
        board_card.append(card_parse(body))

def make_decision():
    global round_state
    round_state += 1

    action = 'check'
    print 'send message to server: %s\n' % action
    return action

def run(argv):

    global client_pid

    # parameter init
    server_ip = argv[0]
    server_port = int(argv[1])
    client_ip = argv[2]
    client_port = int(argv[3])
    client_pid = argv[4]

    # register to gameserver
    while True:
        try:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
            clientsocket.bind((client_ip, client_port))
            clientsocket.connect((server_ip, server_port))
            print 'connect to server success'
            reg_message = 'reg: ' + client_pid + ' ' + 'yutian' + ' \n'
            print 'send register message: ' + reg_message
            clientsocket.send(reg_message)
            break
        except socket.error, (value, message):
            print 'connect error: ' + message
            print 'try to reconnect in 1 seconds'
            time.sleep(1.0)
            continue

    while not is_game_over :
        try:
            recv = clientsocket.recv(1024)
            if len(recv) > 0:
                print 'recv is:\n---------------\n' + recv
                if recv == 'game-over \n':
                    break
                else:
                    result = parse_with_recv(recv)
                    if result is not None:
                        clientsocket.send(result)
            else:
                break

        except socket.error, (value, message):
            print "rec err: " + message
            break

    clientsocket.close()
    print '\n------------\nconnection closed and GAME OVER\n------------'

if __name__ == '__main__':
    run(sys.argv[1:])
