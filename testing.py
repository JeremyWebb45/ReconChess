import random
from copy import deepcopy

import chess
import time
import chess.engine
from copy import deepcopy, copy


class BoardState:

    def __init__(self, possible_moves=[], board=chess.Board(), player=1):
        self.team = player
        self.board_state = board
        self.moves = possible_moves


    def getPossibleActions(self):
        return list(self.board_state.legal_moves)

    def takeAction(self, a):
        board_copy = copy(self.board_state)
        board_copy.push(a)
        self.board_state = board_copy
        self.team = self.team * -1

    def isTerminal(self):
        return self.board_state.is_checkmate()

    def getReward(self):
        return 5 * self.team


def mcts(board=chess.Board(), time_limit=10, player=1):
    start_time = time.time()
    root = {'state': board, 'turn': player, 'num_wins': 0, 'num_sims': 0, 'children': []}
    select()
    print(sim(board, player))


def sim(board, team):
    curr_state = board
    random.seed(9)
    while 1:
        board_copy = copy(curr_state)
        if board_copy.is_game_over(claim_draw=True):
            if board_copy.is_checkmate():
                turn = board_copy.fen().split()[1]
                return 1 if turn == team else -1
            return .5
        else:
            possible_moves = list(board_copy.legal_moves)
            next_move = random.choice(possible_moves)
            board_copy.push(next_move)
            curr_state = board_copy


# state = BoardState(list(chess.Board().legal_moves), chess.Board(), 1)
# print(state.board_state)
# print(list(state.board_state.legal_moves))
# print(state.board_state.fen())
# state.takeAction(list(chess.Board().legal_moves)[1])
# print(state.board_state)
# print(list(state.board_state.legal_moves))
# print(state.board_state.fen())
mcts()


