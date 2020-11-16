import random
from copy import deepcopy

import chess
import time
import chess.engine
from copy import deepcopy, copy


def mcts(board=chess.Board(), time_limit=10, player=1):
    start_time = time.time()
    root = {'state': board, 'turn': player, 'num_wins': 11, 'num_sims': 21, 'children': []}
    node1 = {'parent': root, 'state': board, 'turn': player * -1, 'num_wins': 7, 'num_sims': 10, 'children': []}
    node2 = {'parent': root, 'state': board, 'turn': player * -1, 'num_wins': 0, 'num_sims': 3, 'children': []}
    node3 = {'parent': root, 'state': board, 'turn': player * -1, 'num_wins': 3, 'num_sims': 8, 'children': []}
    root['children'].append(node1)
    root['children'].append(node2)
    root['children'].append(node3)
    node4 = {'parent': node1, 'state': board, 'turn': player, 'num_wins': 2, 'num_sims': 4, 'children': []}
    node5 = {'parent': node1, 'state': board, 'turn': player, 'num_wins': 1, 'num_sims': 6, 'children': []}
    node1['children'].append(node4)
    node1['children'].append(node5)
    node6 = {'parent': node3, 'state': board, 'turn': player, 'num_wins': 1, 'num_sims': 2, 'children': []}
    node7 = {'parent': node3, 'state': board, 'turn': player, 'num_wins': 2, 'num_sims': 3, 'children': []}
    node8 = {'parent': node3, 'state': board, 'turn': player, 'num_wins': 2, 'num_sims': 3, 'children': []}
    node3['children'].append(node6)
    node3['children'].append(node7)
    node3['children'].append(node8)
    node9 = {'parent': node5, 'state': board, 'turn': player * -1, 'num_wins': 2, 'num_sims': 3, 'children': []}
    node0 = {'parent': node5, 'state': board, 'turn': player * -1, 'num_wins': 3, 'num_sims': 3, 'children': []}
    node5['children'].append(node9)
    node5['children'].append(node0)
    selected = sel(root, player)
    print(selected)
    new_node = expand(selected)
    print(new_node['parent']['num_wins'])
    print(new_node['parent']['num_sims'])
    result = sim(new_node['state'], player)
    print(result)
    backprop(new_node, result)
    print(root)


def backprop(node, result):
    curr_node = node
    team = node['turn'] * -1
    while 1:
        curr_node['num_sims'] = curr_node['num_sims'] + 1
        if team == curr_node['turn']:
            if result:
                curr_node['num_wins'] = curr_node['num_wins'] + 1
            elif result == .5:
                curr_node['num_wins'] = curr_node['num_wins'] + .5
        else:
            if not result:
                curr_node['num_wins'] = curr_node['num_wins'] + 1
            elif result == .5:
                curr_node['num_wins'] = curr_node['num_wins'] + .5
        if 'parent' not in curr_node.keys():
            break
        else:
            curr_node = curr_node['parent']


def expand(node):
    board_copy = copy(node['state'])
    move = random.choice(list(board_copy.legal_moves))
    board_copy.push(move)
    return {'parent': node, 'state': board_copy, 'turn': node['turn'] * -1, 'num_wins': 0, 'num_sims': 0, 'children': []}


def sel(tree, team):
    curr_node = tree
    turn = curr_node['turn'] * -1
    while len(curr_node['children']) != 0:
        eval = [c['num_wins'] / c['num_sims'] for c in curr_node['children']]
        curr_node = curr_node['children'][eval.index(max(eval))] if team == turn else curr_node['children'][eval.index(min(eval))]
        turn = turn * -1
    return curr_node


def sim(board, team):
    curr_state = board
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


