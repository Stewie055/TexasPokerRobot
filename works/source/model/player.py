from card import Card

class Player:
    def __init__(self):
        self.bet = []
        self.state = []
        self.rank = []
        self.cards = [None]*2
        self.action_count = [0]*5

    def update_bet_state_from_inquire(self, line_string):
        parameter = line_string.split(' ')
        self.bet.append(int(parameter[3]))
        self.state.append(parameter[4])

    def update_rank_from_showdown(self, line_string):
        parameter = line_string.split(' ')
