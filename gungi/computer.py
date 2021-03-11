import pygame
from gungi.constants import *
from gungi.board import *
import random


class Computer:
    #Player_num should just be 1 for start
    def __init__(self, color):
        self.values = self.create_vals()
        self.color = color
    
    def create_vals(self):
        lst = {}
        lst['Marshall1'] = 0
        lst['Marshall2'] = 0
        lst['Marshall3'] = 0

        lst['Pawn1'] = 1
        lst['Pawn2'] = 1.25
        lst['Pawn3'] = 1.25

        lst['General1'] = 1.8
        lst['General2'] = 2
        lst['General3'] = 2.5
       
        lst['Knight1'] = 1.5
        lst['Knight2'] = 2
        lst['Knight3'] = 3

        lst['Samourai1'] = 1.5
        lst['Samourai2'] = 2.5
        lst['Samourai3'] = 3

        lst['Cannon1'] = 2.5
        lst['Cannon2'] = 3.5
        lst['Cannon3'] = 5

        lst['Spy1'] = 1
        lst['Spy2'] = 1.5
        lst['Spy3'] = 9

        lst['Fortress1'] = 3
        lst['Fortress2'] = 3
        lst['Fortress3'] = 3

        lst['Archer1'] = 2
        lst['Archer2'] = 3
        lst['Archer3'] = 4

        lst['LGeneral1'] = 1.5
        lst['LGeneral2'] = 1.65
        lst['LGeneral3'] = 2

        lst['MGeneral1'] = 1.15
        lst['MGeneral2'] = 1.5
        lst['MGeneral3'] = 1.8

        lst['Captain1'] = 2
        lst['Captain2'] = 2
        lst['Captain3'] = 2
       
        lst['Musketeer1'] = 1
        lst['Musketeer2'] = 1.2
        lst['Musketeer3'] = 2.75

        return lst


    def get_board_score(self, game):
        score = game.winner()

        if score == 'Black Wins!':
            if self.color == BLACK:
                return maxsize
            else:
                return -maxsize

        elif score == 'White Wins!':
            if self.color == BLACK:
                return -maxsize
            else:
                return maxsize
        
        elif score == "Draw!":
            return 0

        else:
            black_score = 0
            white_score = 0

            for (row,col) in game.board.black_board_pieces:
                p = game.board.board[row][col]

                if type(p[-1]) == Captain and p.tier > 1:
                    p = p[-2]
                else:
                    p = p[-1]

                name = str(p) + str(p.tier)
                black_score += self.values[name]

            for (row,col) in game.board.black_pile_pieces.keys():
                p = game.board.black_pile_pieces[(row,col)]
                if type(p[0]) != Pass:
                    name = str(p[0]) + '3'
                    val = self.values[name] * p[1]
                    black_score += val
                
            for (row,col) in game.board.white_board_pieces:
                p = game.board.board[row][col]

                if type(p[-1]) == Captain and p.tier > 1:
                    p = p[-2]
                else:
                    p = p[-1]

                name = str(p) + str(p.tier)
                white_score += self.values[name]

            for (row,col) in game.board.white_pile_pieces.keys():
                p = game.board.white_pile_pieces[(row,col)]
                if type(p[0]) != Pass:
                    name = str(p[0]) + '3'
                    val = self.values[name] * p[1]
                    white_score += val

        if self.color == WHITE:
            return white_score - black_score
        return black_score - white_score

    
    def get_all_actions(self, game):
        piles = {}
        boards = {}

        if self.color == WHITE:
            board_pieces = game.board.white_board_pieces
            pile_pieces = game.board.white_pile_pieces
        else:
            board_pieces = game.board.black_board_pieces
            pile_pieces = game.board.black_pile_pieces


        for (row,col) in board_pieces:
            p = game.board.board[row][col][-1]
            valid = p.get_valid(game.board, game.turn_num, game.both_pass, 1)

            if valid:
                boards[(row,col)] = valid

        for (row,col) in pile_pieces:
            p = pile_pieces[(row,col)][0]

            valid = p.get_valid(game.board, game.turn_num, game.both_pass, 1)

            if valid:
                piles[(row,col)] = valid

        
        return (piles, boards)


    def minmaxRoot(self,depth, game,isMaximizing):
        possibleMoves = self.get_all_actions(game)
        bestMove = -9999
        bestMoveFinal = None
        piece = None
        mode = -1

        for (row,col) in possibleMoves[0].keys():
            p = game.board.get_piece(row, col, 0, self.color)

            for (r,c) in possibleMoves[0][(row,col)][0]:
                new_board = copy.deepcopy(game.board)
                piece = copy.deepcopy(p)
                new_board.move(piece,r,c)
                value = max(bestMove, self.minimax(depth - 1, game,-10000,10000, not isMaximizing))

                if value > bestMove:
                    print("Best score: " ,str(bestMove))
                    print("Best move: ",str(bestMoveFinal))
                    bestMove = value
                    bestMoveFinal = (r,c)
                    mode = 0
                    piece = p

        for (row,col) in possibleMoves[1].keys():
            p = game.board.get_piece(row, col, 1, self.color)

            for (r,c) in possibleMoves[1][(row,col)][0]:
                new_board = copy.deepcopy(game.board)
                piece = copy.deepcopy(p)
                new_board.move(piece,r,c)
                value = max(bestMove, self.minimax(depth - 1, game.board,-10000,10000, not isMaximizing))

                if value > bestMove:
                    print("Best score: " ,str(bestMove))
                    print("Best move: ",str(bestMoveFinal))
                    bestMove = value
                    bestMoveFinal = (r,c)
                    mode = 0
                    piece = p

            for (r,c) in possibleMoves[1][(row,col)][1]:
                new_board = copy.deepcopy(game.board)
                piece = copy.deepcopy(p)
                new_board.capture(piece,r,c)
                value = max(bestMove, self.minimax(depth - 1, game,-10000,10000, not isMaximizing))

                if value > bestMove:
                    print("Best score: " ,str(bestMove))
                    print("Best move: ",str(bestMoveFinal))
                    bestMove = value
                    bestMoveFinal = (r,c)
                    mode = 1
                    piece = p

        return (bestMoveFinal, piece, mode)

    def minimax(self,depth, game, alpha, beta, is_maximizing):
        if(depth == 0):
            return -self.get_board_score(game)
        possibleMoves = self.get_all_actions(game)
        if(is_maximizing):
            bestMove = -9999

            for (row,col) in possibleMoves[0].keys():
                p = game.board.get_piece(row, col, 0, self.color)

                for (r,c) in possibleMoves[0][(row,col)][0]:
                    new_board = copy.deepcopy(game.board)
                    piece = copy.deepcopy(p)
                    new_board.move(piece,r,c)
                    bestMove = max(bestMove, self.minimax(depth - 1, game,-10000,10000, not is_maximizing))

                    alpha = max(alpha,bestMove)
                    if beta <= alpha:
                        return bestMove

            for (row,col) in possibleMoves[1].keys():
                p = game.board.get_piece(row, col, 1, self.color)

                for (r,c) in possibleMoves[1][(row,col)][0]:
                    new_board = copy.deepcopy(game.board)
                    piece = copy.deepcopy(p)
                    new_board.move(piece,r,c)
                    bestMove = max(bestMove, self.minimax(depth - 1, game,-10000,10000, not is_maximizing))

                    alpha = max(alpha,bestMove)
                    if beta <= alpha:
                        return bestMove

                for (r,c) in possibleMoves[1][(row,col)][1]:
                    new_board = copy.deepcopy(game.board)
                    piece = copy.deepcopy(p)
                    new_board.capture(piece,r,c)
                    bestMove = max(bestMove, self.minimax(depth - 1, game,-10000,10000, not is_maximizing))

                    alpha = max(alpha,bestMove)
                    if beta <= alpha:
                        return bestMove
            return bestMove

        else:
            bestMove = 9999
            for (row,col) in possibleMoves[0].keys():
                p = game.board.get_piece(row, col, 0, self.color)

                for (r,c) in possibleMoves[0][(row,col)][0]:
                    new_board = copy.deepcopy(game.board)
                    piece = copy.deepcopy(p)
                    new_board.move(piece,r,c)
                    bestMove = min(bestMove, self.minimax(depth - 1, game,-10000,10000, not is_maximizing))

                    beta = min(beta,bestMove)
                    if beta <= alpha:
                        return bestMove

            for (row,col) in possibleMoves[1].keys():
                p = game.board.get_piece(row, col, 1, self.color)

                for (r,c) in possibleMoves[1][(row,col)][0]:
                    new_board = copy.deepcopy(game.board)
                    piece = copy.deepcopy(p)
                    new_board.move(piece,r,c)
                    bestMove = min(bestMove, self.minimax(depth - 1, game,-10000,10000, not is_maximizing))

                    beta = min(beta,bestMove)
                    if beta <= alpha:
                        return bestMove

                for (r,c) in possibleMoves[1][(row,col)][1]:
                    new_board = copy.deepcopy(game.board)
                    piece = copy.deepcopy(p)
                    new_board.capture(piece,r,c)
                    bestMove = min(bestMove, self.minimax(depth - 1, game,-10000,10000, not is_maximizing))

                    beta = min(beta,bestMove)
                    if beta <= alpha:
                        return bestMove
            return bestMove

    
    def get_best_move(self, depth, game):
        return self.minmaxRoot(depth, game, True)







 

        