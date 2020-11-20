from mcts import MCTS
import chess

search_tree = MCTS(15, 1, chess.Board())
search_tree.search()
print(search_tree.pick_move()['move'])


def print_tree(root, i=0):
    print('layer: ' + str(i))
    print(root['state'].fen())
    print(root['num_wins'], root['num_sims'])
    j = i + 1
    for child in root['children']:
        print_tree(child, j)