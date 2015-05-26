import sys
import socket
import re
import time
import traceback

import cards2
import holdem_calc

# 0,1-hands 2,3,4-flop 5-turn 6-river
cards = [None]*7
card_index = 0
hand_probability = [None]*10

# key is player's PID
num_player = 0
opponent_dic = {}

# my PID
my_pid = ''

# game over flag
is_game_over = False

# state
round_state = 0

# Basic class for card and opponent
class Card:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def __str__(self):
        if self.number == '10':
            return 'T' + self.color[0].lower()
        return self.number + self.color[0].lower()

class Player:
    def __init__(self):
        self.bet = []
        self.state = []

    def update_bet_from_inquire(self, line_string):
        parameter = line_string.split(' ')
        self.bet.append(int(parameter[3]))
        self.state.append(parameter[4])

# parse socket command_block
def seat_parse(lines):
    #reset card_index when new hand begin
    global opponent_dic
    global is_game_over
    global num_player
    global card_index
    global cards
    card_index = 0
    cards = [None]*7
    opponent_dic = {}
    num_player = 0

    for line in lines:
        parameter = line.split(' ')
        try:
            pid = parameter[-4]
            if pid != my_pid:
                num_player += 1
                opponent_dic[pid] = Player()
        except:
            is_game_over = True
            print 'seat parse error'

def card_parse(lines):
    global cards
    global card_index
    global is_game_over

    for line in lines:
        parameter = line.split(' ')
        try:
            cards[card_index] = str(Card(parameter[0], parameter[1]))
            card_index += 1
        except:
            is_game_over = True
            print 'card parse error'

    if cards[6] is None and cards[2] is not None:
        global hand_probability
        hand_probability = holdem_calc.calc(cards)

def oppo_parse(lines):
    global opponent_dic
    global is_game_over

    for line in lines[:-1]:
        parameter = line.split(' ')
        pid = parameter[0]
        try:
            if pid != my_pid:
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
    global round_state

    command_block = re.finditer(r"(\w+)/ \n([\s\S]*?)/(\1) \n", recv)

    for block in command_block:
        command = block.group(1)
        body = block.group(2)

        if command == 'inquire':
            round_state += 1
            oppo_parse(body.splitlines())
            (oppobehave, opponum) = creat_oppo_array()
            print ' oppobehave is '
            print oppobehave
            print opponum
            action = ''
            if cards[6]:
                print 'river round , count is: %s', round_state
                action = cards2.makeDecisionRiver(cards, round_state, oppobehave, opponum, num_player)
            elif cards[5]:
                print 'turn round , count is: %s', round_state
                action = cards2.makeDecisionTurn(cards, round_state, hand_probability, oppobehave, opponum, num_player)
            elif cards[2]:
                print 'flop round , count is: %s', round_state
                action = cards2.makeDecisionFlop(cards, round_state, hand_probability, oppobehave, opponum, num_player)
            elif cards[0]:
                print 'blind round , count is: %s', round_state
                action = cards2.makeDecisionBlind(cards, round_state, oppobehave, opponum, num_player)

            print 'send message to server: %s\n' % action
            return action

        round_state = 0

        if command == 'seat':
            seat_parse(body.splitlines())
        elif command in ['hold', 'flop', 'turn', 'river']:
            card_parse(body.splitlines())

    return None

def run(argv):

    # parameter init
    server_ip = argv[0]
    server_port = int(argv[1])
    client_ip = argv[2]
    client_port = int(argv[3])
    client_name = argv[4]

    global my_pid
    my_pid = client_name

    # register to gameserver
    while True:
        try:
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientsocket.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
            clientsocket.bind((client_ip, client_port))
            clientsocket.connect((server_ip, server_port))
            print 'connect to server success'
            reg_message = 'reg: ' + client_name + ' ' + 'yutian' + ' \n'
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
