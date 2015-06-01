import sys
sys.path.insert(0, "../libs/holdem_calc/")

import holdem_argparser
import holdem_functions

def calc(hold_card, board_card=None):

    # generate parameter
    hole_cards = holdem_argparser.parse_hole_cards(hold_card)
    given_board = holdem_argparser.parse_cards(board_card)

    if given_board:
        all_cards = list(hole_cards)
        all_cards.append(given_board)
        deck = holdem_functions.generate_deck(all_cards)
    else:
        deck = holdem_functions.generate_deck(hole_cards)

    num_iterations = 10000
    exact = False

    # copy from holem_calc.py main fuction
    num_players = 1
    # Create results data structures which tracks results of comparisons
    # 1) result_histograms: a list for each player that shows the number of
    #    times each type of poker hand (e.g. flush, straight) was gotten
    # 2) winner_list: number of times each player wins the given round
    # 3) result_list: list of the best possible poker hand for each pair of
    #    hole cards for a given board
    result_list, winner_list = [None] * num_players, [0] * (num_players + 1)
    result_histograms = []
    for player in xrange(num_players):
        result_histograms.append([0] * 10)
    # Choose whether we're running a Monte Carlo or exhaustive simulation
    board_length = 0 if given_board == None else len(given_board)
    # When a board is given, exact calculation is much faster than Monte Carlo
    # simulation, so default to exact if a board is given
    if exact or given_board is not None:
        generate_boards = holdem_functions.generate_exhaustive_boards
    else:
        generate_boards = holdem_functions.generate_random_boards
    # Run simulations
    for remaining_board in generate_boards(deck, num_iterations, board_length):
        # Generate a new board
        if given_board:
            board = given_board[:]
            board.extend(remaining_board)
        else:
            board = remaining_board
        # Find the best possible poker hand given the created board and the
        # hole cards and save them in the results data structures
        (suit_histogram,
                histogram, max_suit) = holdem_functions.preprocess_board(board)
        for index, hole_card in enumerate(hole_cards):
            result_list[index] = holdem_functions.detect_hand(hole_card, board,
                                         suit_histogram, histogram, max_suit)
        # Find the winner of the hand and tabulate results
        winner_index = holdem_functions.compare_hands(result_list)
        winner_list[winner_index] += 1
        # Increment what hand each player made
        for index, result in enumerate(result_list):
            result_histograms[index][result[0]] += 1

    float_iterations = float(sum(winner_list))
    pro_result = [None]*10
    for index, elem in enumerate(result_histograms[0]):
        pro_result[index] = float(elem) / float_iterations

    return pro_result