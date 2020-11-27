#!/usr/bin/env python3

"""
File Name:      my_agent.py
Authors:        Jeremy Webb
Date:           11/6/20

Description:    Python file for my agent.
Source:         Adapted from recon-chess (https://pypi.org/project/reconchess/)
"""



import random
from player import Player
from mcts import MCTS


# TODO: Rename this class to what you would like your bot to be named during the game.
class MyAgent(Player):

    def __init__(self):
        self.color = None
        self.current_board = None
        
    def handle_game_start(self, color, board):
        """
        This function is called at the start of the game.

        :param color: chess.BLACK or chess.WHITE -- your color assignment for the game
        :param board: chess.Board -- initial board state
        :return:
        """

        self.color = color
        self.current_board = board
        pass
        
    def handle_opponent_move_result(self, captured_piece, captured_square):
        """
        This function is called at the start of your turn and gives you the chance to update your board.

        :param captured_piece: bool - true if your opponents captured your piece with their last move
        :param captured_square: chess.Square - position where your piece was captured
        """
        #TODO: Assume our opponents policy is random and update our board
        #TODO: If we have a piece captured, update the board with known piece position
        print('\--------------Opponent Move--------------/')
        print(captured_piece)
        print(captured_square)
        moves = list(self.current_board.legal_moves)
        self.current_board.push(random.choice(moves))
        pass

    def choose_sense(self, possible_sense, possible_moves, seconds_left):
        """
        This function is called to choose a square to perform a sense on.

        :param possible_sense: List(chess.SQUARES) -- list of squares to sense around
        :param possible_moves: List(chess.Moves) -- list of acceptable moves based on current board
        :param seconds_left: float -- seconds left in the game

        :return: chess.SQUARE -- the center of 3x3 section of the board you want to sense
        :example: choice = chess.A1
        """

        #TODO: Honestly not sure we might need some sort of policy to decide where to sense, or we can go random

        print('\--------------Choose Sense--------------/')
        print(possible_sense)
        print(possible_moves)
        print(seconds_left)
        return random.choice(possible_sense)
        
    def handle_sense_result(self, sense_result):
        """
        This is a function called after your picked your 3x3 square to sense and gives you the chance to update your
        board.

        :param sense_result: A list of tuples, where each tuple contains a :class:`Square` in the sense, and if there
                             was a piece on the square, then the corresponding :class:`chess.Piece`, otherwise `None`.
        :example:
        [
            (A8, Piece(ROOK, BLACK)), (B8, Piece(KNIGHT, BLACK)), (C8, Piece(BISHOP, BLACK)),
            (A7, Piece(PAWN, BLACK)), (B7, Piece(PAWN, BLACK)), (C7, Piece(PAWN, BLACK)),
            (A6, None), (B6, None), (C8, None)
        ]
        """
        print('\--------------Handle Sense--------------/')
        print(sense_result)
        # TODO: Sense the board, update our current board with this sense
        # TODO: Fill in the rest of the board with guesses as to where the remaining unsensed enemy pieces are
        # Hint: until this method is implemented, any senses you make will be lost.
        pass

    def choose_move(self, possible_moves, seconds_left):
        """
        Choose a move to enact from a list of possible moves.

        :param possible_moves: List(chess.Moves) -- list of acceptable moves based only on pieces
        :param seconds_left: float -- seconds left to make a move
        
        :return: chess.Move -- object that includes the square you're moving from to the square you're moving to
        :example: choice = chess.Move(chess.F2, chess.F4)
        
        :condition: If you intend to move a pawn for promotion other than Queen, please specify the promotion parameter
        :example: choice = chess.Move(chess.G7, chess.G8, promotion=chess.KNIGHT) *default is Queen
        """
        # TODO: update this method
        print('\--------------Choose Move--------------/')
        print(possible_moves)
        print(list(self.current_board.legal_moves))
        search_tree = MCTS(5, self.color, self.current_board)
        search_tree.search()
        move = search_tree.pick_move()['move']
        self.current_board.push(move)

        return move
        
    def handle_move_result(self, requested_move, taken_move, reason, captured_piece, captured_square):
        """
        This is a function called at the end of your turn/after your move was made and gives you the chance to update
        your board.

        :param requested_move: chess.Move -- the move you intended to make
        :param taken_move: chess.Move -- the move that was actually made
        :param reason: String -- description of the result from trying to make requested_move
        :param captured_piece: bool - true if you captured your opponents piece
        :param captured_square: chess.Square - position where you captured the piece
        """
        print('\--------------Handle Move--------------/')
        print(requested_move, taken_move, reason, captured_piece, captured_square)
        # TODO: implement this method
        pass
        
    def handle_game_end(self, winner_color, win_reason):  # possible GameHistory object...
        """
        This function is called at the end of the game to declare a winner.

        :param winner_color: Chess.BLACK/chess.WHITE -- the winning color
        :param win_reason: String -- the reason for the game ending
        """
        # TODO: implement this method
        print('\--------------Game End--------------/')
        print(winner_color)
        print(win_reason)
        pass
