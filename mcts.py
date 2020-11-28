import random
import chess
import numpy as np
import time
from copy import copy


class MCTS:

    def __init__(self, time_limit, player, board=chess.Board()):
        self.board_state = board
        self.limit = time_limit
        self.team = player
        self.tree = None
        self.moves = list(board.legal_moves)

    def search(self):
        start_time = time.time()
        root = {'state': self.board_state, 'actions': self.moves, 'turn': self.team, 'num_wins': 0, 'num_sims': 0, 'children': []}
        while time.time() - start_time < self.limit:
            selected = self.sel(root)
            new_node = self.expand(selected)
            selected['children'].append(new_node)
            result = self.sim(new_node['state'].copy(), self.team)
            self.backprop(new_node, result)
        self.tree = root

    def pick_move(self):
        evaluation = [c['num_wins'] / c['num_sims'] for c in self.tree['children']]
        return self.tree['children'][evaluation.index(min(evaluation))]

    def backprop(self, node, result):
        curr_node = node
        team = node['turn']
        while 1:
            curr_node['num_sims'] = curr_node['num_sims'] + 1
            if team == curr_node['turn']:
                if result == 1:
                    curr_node['num_wins'] = curr_node['num_wins'] + 1
                elif result == .5:
                    curr_node['num_wins'] = curr_node['num_wins'] + .5
            else:
                if result == 0:
                    curr_node['num_wins'] = curr_node['num_wins'] + 1
                elif result == .5:
                    curr_node['num_wins'] = curr_node['num_wins'] + .5
            if 'parent' not in curr_node.keys():
                break
            else:
                curr_node = curr_node['parent']

    def expand(self, node):
        board_copy = copy(node['state'])
        moves = node['actions'].copy()
        if len(moves) == 0:
            moves.append(chess.Move.null())
        move = random.choice(moves)
        moves.remove(move)
        node['actions'] = moves
        board_copy.push(move)
        return {'parent': node, 'actions': list(board_copy.pseudo_legal_moves), 'move': move, 'state': board_copy, 'turn': node['turn'] * -1, 'num_wins': 0, 'num_sims': 0, 'children': []}

    def sel(self, root):
        if len(root['children']) == 0:
            return root
        stack = [root]
        sel_node = root
        curr_max = 0
        while len(stack) != 0:
            curr_node = stack.pop()
            uct = self.UCT(curr_node)
            if uct > curr_max:
                curr_max = uct
                sel_node = curr_node
            for c in curr_node['children']:
                stack.append(c)
        return sel_node

    def UCT(self, node):
        if 'parent' not in node.keys():
            return node['num_wins'] / node['num_sims'] + np.sqrt(2) * np.sqrt(np.log(node['num_sims']) / node['num_sims'])
        else:
            return node['num_wins'] / node['num_sims'] + np.sqrt(2) * np.sqrt(np.log(node['parent']['num_sims']) / node['num_sims'])

    def sim(self, board, team, n=150):
        curr_state = board
        i = 0
        while i < n:
            board_copy = copy(curr_state)
            if board_copy.fen().split()[0].lower().count('k') < 2:
                winner = chess.WHITE if board.copy().fen().split()[0].count('k') == 0 else chess.BLACK
                if winner == team:
                    return 1
                else:
                    return 0
            else:
                possible_moves = list(board_copy.pseudo_legal_moves)
                possible_moves.append(chess.Move.null())
                next_move = random.choice(possible_moves)
                board_copy.push(next_move)
                curr_state = board_copy
            i = i + 1
        return .5

    def build_example_tree(self, board, player):
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
        return root

