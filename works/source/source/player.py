from card import Card
import cards2_normal
getRank = cards2_normal.getRank4

action_dic = {'fold':0,
              'check':1,
              'call':2,
              'raise':3,
              'all_in':4}

class Player:
    def __init__(self):
        self.bet = []
        self.state = []
        self.card_history = []
        self.card_strength_history = []
        self.action_count_history = [0]*5

    def reset_bet_and_action(self):
        self.bet = []
        self.action = []

    def update_from_inquire(self, line_string):
        parameter = line_string.split(' ')
        if parameter[4] == 'blind':
            return
        bet = int(parameter[3])
        state = parameter[4]

        self.bet.append(bet)
        self.state.append(state)
        self.action_count_history[action_dic[state]] += 1

    def update_from_showdown(self, line_string, board_cards):
        parameter = line_string.split(' ')
        card1_str = str(Card(parameter[2], parameter[3]))
        card2_str = str(Card(parameter[4], parameter[5]))
        cards = [card1_str, card2_str] + board_cards
        self.card_history.append([card1_str, card2_str])
        self.card_strength_history.append(getRank(cards))
