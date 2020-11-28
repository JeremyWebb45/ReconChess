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
import chess


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

        # if a piece was captured, check to see if we can figure out what move was made to capture it
        if captured_piece:
            self.current_board.turn = not self.color
            moves = list(self.current_board.pseudo_legal_moves)
            for move in moves.copy(): # iterate through moves looking for one that captures our piece
                if move.to_square != captured_square:
                    moves.remove(move)
            if len(moves) == 1: # if there was exactly one capture move, then obviously that was taken
                self.current_board.push(moves[0])
            else: # otherwise (if either there were multiple or no options found), just sense that square
                self.current_board.remove_piece_at(captured_square)



    def choose_sense(self, possible_sense, possible_moves, seconds_left):
        """
        This function is called to choose a square to perform a sense on.

        :param possible_sense: List(chess.SQUARES) -- list of squares to sense around
        :param possible_moves: List(chess.Moves) -- list of acceptable moves based on current board
        :param seconds_left: float -- seconds left in the game

        :return: chess.SQUARE -- the center of 3x3 section of the board you want to sense
        :example: choice = chess.A1
        """

        #need to remove edges of board for sense
        smart_sense = possible_sense[8:-8]
        sides = []
        for sense in smart_sense:
            if sense % 8 == 0:
                sides.append(sense)
            if sense % 8 == 7:
                sides.append(sense)

        smart_sense = [i for i in smart_sense if i not in sides]

        our_pieces = []
        for square in possible_sense:
            if self.current_board.color_at(square) == self.color:
                our_pieces.append(square)

        sense = random.choice(smart_sense)

        # a 3x3 square around sence
        sense_area = [sense-9, sense-8, sense-7, sense-1, sense, sense+1, sense+7, sense+8, sense+9]

        num_pieces = 0
        for square in sense_area:
            if self.current_board.color_at(square) == self.color:
                num_pieces += 1

        while num_pieces >= 5:
            sense = random.choice(smart_sense)

            # a 3x3 square around sence
            sense_area = [sense-9, sense-8, sense-7, sense-1, sense, sense+1, sense+7, sense+8, sense+9]

            num_pieces = 0
            for square in sense_area:
                if self.current_board.color_at(square) == self.color:
                    num_pieces += 1

        return sense


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
        sense_squares = [sense_result[i][0] for i in
                         range(len(sense_result))]  # list of specifically the squares that were sensed
        for square, piece in sense_result:  # iterate through the sense result
            # if the current board has a piece here, but it's the wrong piece
            if self.current_board.piece_at(square) == None or self.current_board.piece_at(square) == piece:
                continue
            # check if there's another sensed square that wants the piece that's at this one
            self.current_board.turn = not self.color
            moves = list(self.current_board.pseudo_legal_moves)
            for square_to, piece_to in sense_result:  # iterate through the sense results
                # if the piece at this sensed square is also wrong but the earlier piece was right and we're not just looking at the same square
                if self.current_board.piece_at(square_to) != piece_to and self.current_board.piece_at(
                        square) == piece_to and square != square_to:
                    move = chess.Move(square, square_to)
                    # if it's a valid move and nothing is being captured, make it
                    if move in moves and self.current_board.is_capture(move) != True:
                        self.current_board.push(move)
                        break
            # check again if the current board still has a piece at this square
            if self.current_board.piece_at(square) == None or self.current_board.piece_at(square) == piece:
                continue
            # if there's still a piece and it's the wrong piece, literally just look for any move that'll move it out of the sensed squares
            self.current_board.turn = not self.color
            moves = list(self.current_board.pseudo_legal_moves)
            for move in moves:
                if move.from_square == square and move.to_square not in sense_squares and self.current_board.is_capture(
                        move) != True:
                    self.current_board.push(move)
                    break
            # check once again if the current board STILL has a piece here
            if self.current_board.piece_at(square) == None or self.current_board.piece_at(square) == piece:
                continue
            # alright I give up; just move this piece to any empty square on the board
            rand_square = random.choice(chess.SQUARES)
            while rand_square in sense_squares or self.current_board.color_at(rand_square) != None:
                rand_square = random.choice(chess.SQUARES)
            self.current_board.set_piece_at(rand_square, self.current_board.remove_piece_at(square))

        # now that we've guaranteed every square in the sense results either has the right piece or no piece, iterate through the results again
        for square, piece in sense_result:
            # if there's a piece here, it's most likely the right one
            if self.current_board.piece_at(square) != None:
                continue
            # look for any valid move that will place the right piece in this spot
            self.current_board.turn = not self.color
            moves = list(self.current_board.pseudo_legal_moves)
            random.shuffle(moves)
            for move in moves:
                if move.to_square == square and self.current_board.piece_at(
                        move.from_square) == piece and move.from_square not in sense_squares:
                    self.current_board.push(move)
                    break
                if move.to_square == square and move.promotion != None and move.promotion == piece.piece_type and move.from_square not in sense_squares:
                    self.current_board.push(move)
                    break
            # if the right piece is now here, great
            if self.current_board.piece_at(square) == piece:
                continue
            # if there was no valid move to move the right piece here, well... uh... just randomly pick a piece of the right type and move it here
            random_squares = list(chess.SQUARES)
            random.shuffle(random_squares)
            for from_square in random_squares:
                if from_square in sense_squares:
                    continue
                if self.current_board.color_at(from_square) != (not self.color):
                    continue
                if piece.piece_type == self.current_board.piece_at(from_square).piece_type:
                    if piece.piece_type == chess.BISHOP:
                        from_type = (chess.square_rank(from_square) + chess.square_file(from_square)) % 2
                        to_type = (chess.square_rank(square) + chess.square_file(square)) % 2
                        if from_type != to_type:
                            continue
                    self.current_board.set_piece_at(square, self.current_board.remove_piece_at(from_square))

        # set the current board turn back to our turn (otherwise the MCTS will get upset)
        self.current_board.turn = self.color

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
        if taken_move is not None: # if a move was actually taken
            # if it was a valid move in our board model, do it
            self.current_board.turn = self.color
            moves = list(self.current_board.pseudo_legal_moves)
            if taken_move in moves and self.current_board.is_capture(taken_move) == captured_piece:
                self.current_board.push(taken_move)
            # if it was a valid move but whether or not a capture happens is what's wrong
            elif taken_move in moves and self.current_board.is_capture(taken_move) != captured_piece:
                if captured_piece is True: # if a piece was captured but the current board has no clue, then make the move anyway. Too many pieces is better than too few
                    self.current_board.push(taken_move)
                else: # if a piece wasn't captured but current board says there will be one captured, oof
                    # see if there is a valid move that'll just move the captured piece out of the way
                    self.current_board.turn = not self.color
                    moves_opp = list(self.current_board.pseudo_legal_moves)
                    for move in moves_opp:
                        if move.from_square == taken_move.to_square and self.current_board.is_capture(move) is False:
                            board_temp = self.current_board.copy()
                            board_temp.push(move)
                            board_temp.turn = self.color
                            if taken_move in list(board_temp.pseudo_legal_moves) and board_temp.is_capture(taken_move) is False:
                                self.current_board = board_temp
                                break
                    # if there is no valid move to move the captured piece out of the way, put it on a random empty spot
                    self.current_board.turn = self.color
                    if self.current_board.is_capture(taken_move) != captured_piece:
                        rand_square = random.choice(chess.SQUARES)
                        while self.current_board.color_at(rand_square) is not None:
                            rand_square = random.choice(chess.SQUARES)
                        self.current_board.set_piece_at(rand_square, self.current_board.remove_piece_at(taken_move.to_square))
                        self.current_board.push(taken_move)
            # if the taken move wasn't a valid move to begin with
            else:
                # if there is currently a piece that is occupying the square that was moved to, and it's not supposed to be captured, move it to a random empty square
                if self.current_board.color_at(taken_move.to_square) is not None and (captured_piece is not True or self.current_board.color_at(taken_move.to_square) == self.color):
                    rand_square = random.choice(chess.SQUARES)
                    while self.current_board.color_at(rand_square) is not None:
                        rand_square = random.choice(chess.SQUARES)
                    self.current_board.set_piece_at(rand_square, self.current_board.remove_piece_at(taken_move.to_square))
                # now that there is no piece at the destination square, force the taken move to occur
                self.current_board.set_piece_at(taken_move.to_square, self.current_board.remove_piece_at(taken_move.from_square))
        print(self.current_board)

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
