import pygame
from gungi.constants import *

font = pygame.font.SysFont("comicsansms", 16)
piece_num = 53
import copy


class Piece:
    def __init__(self, row, col, color, pile):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.tier = 1
        self.selected = False
        self.move_list = []
        self.pile = pile

    def _moves_and_attacks(self, moves, attacks, p, board, row, col, check_for_check):
        if row < 0 or row > 8 or col < 0 or col > 8 or (self.row == row and self.col == col):
            return

        if not p or (type(p) != Marshall and p.tier < 3):
            if check_for_check:
                new_board = copy.deepcopy(board)
                piece = copy.deepcopy(self)
                new_board.move(piece,row,col)

                if not new_board.is_checked(self.color, 0)[0]:
                    moves.append((row,col))
            else:
                moves.append((row,col))

        if p and p.color != self.color:
            if check_for_check:
                new_board = copy.deepcopy(board)
                piece = copy.deepcopy(self)
                new_board.move(piece,row,col)

                if not new_board.is_checked(self.color, 0)[0]:
                    attacks.append((row,col))
            else:
                attacks.append((row,col))

    def move(self, row, col):
        self.row = row
        self.col = col

    def _drop(self,both_pass, board, check_for_check):
        moves = []

        if both_pass == 2:
            num = 3
        else:
            num = 0

        if self.color == WHITE:
            for row in range(0, 3 + num):
                for col in range(COLS):
                    p = board.get_piece(row,col,1,WHITE)
                    if not p or (type(p) != Marshall and p.tier < 3):
                        if check_for_check:
                            new_board = copy.deepcopy(board)
                            piece = copy.deepcopy(self)
                            new_board.move(piece,row,col)

                            if not new_board.is_checked(self.color, 0)[0]:
                                moves.append((row,col))
                        else:
                            moves.append((row,col))
        else:
            for row in range(6 - num, 9):
                for col in range(COLS):
                     p = board.get_piece(row,col,1,BLACK)
                     if not p or (type(p) != Marshall and p.tier < 3):
                        if check_for_check:
                            new_board = copy.deepcopy(board)
                            piece = copy.deepcopy(self)
                            new_board.move(piece,row,col)

                            if not new_board.is_checked(self.color, 0)[0]:
                                moves.append((row,col))
                        else:
                            moves.append((row,col))
        return moves

    #Return number of fortresses nearby of same color
    def _near_fortress(self, board):
        cnt = 0
        for col in [1, 0, -1]:
                for row in [1, 0, -1]:
                    if row != 0 or col != 0:
                        p = board.get_piece(self.row + row, self.col + col, 1, self.color)
                        if type(p) == Fortress and p.color == self.color:
                            cnt += 1
                            if cnt + self.tier == 3:
                                return cnt
        return cnt

    def draw(self, win):
        if self.tier > 1:
            tier = font.render(str(self.tier), 1, (0,0,0))
            win.blit(tier, (284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)))

class Pass(Piece):
    def valid_moves(self, board, turn, attack, both_pass, check_for_check):
        return []

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        return None
    
    def __str__(self):
        return 'Pass'

#Pawn cannot drop for checkmate
#p.get_valid(board, self.turn_num, b_pass) => None or ([move pos], [attack pos])
#can_attack, path = p.can_attack(king_pos,self)

class Marshall(Piece):
    def __init__(self, row, col, color, pile):
        super().__init__(row, col, color, pile)
        self.king = True

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        moves = []
        attacks = []

        if turn_num < 3 and self.pile:
            moves = self._drop(both_pass, board, 0)
        

        if both_pass == 2 and not self.pile:
            for col in [1, 0, -1]:
                for row in [1, 0, -1]:
                    if row != 0 or col != 0:
                        p = board.get_piece(self.row + row,self.col + col,1,self.color)
                        self._moves_and_attacks(moves,attacks,p, board, self.row + row,self.col + col, check_for_check)
     
        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            return (True, [(self.row,self.col)])
        return (False, [])
    
    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(Marshall_W, (110,500))
        else:
            win.blit(Marshall_B, (1025,500))
            
    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(MarshallW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(MarshallB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def __str__(self):
        return 'Marshall'

class Pawn(Piece):
    #Cannot drop for checkmate
    def _pawn_drop(self,both_pass, board, check_for_check):
        moves = []
        attacks = []

        if both_pass == 2:
            num = 3
        else:
            num = 0

        if self.color == WHITE:
            pawn_cols = []
            for (r, c) in board.white_board_pieces:
                p = board.get_piece(r,c,1,WHITE)
                if p and type(p) == Pawn and p.color == WHITE:
                    pawn_cols.append(c)

            for col in range(COLS):
                if col not in pawn_cols:
                    for row in range(0, 3 + num):
                        p = board.get_piece(row,col,1,WHITE)
                        if not p or (type(p) != Marshall and p.tier < 3):
                            if check_for_check:
                                new_board = copy.deepcopy(board)
                                piece = copy.deepcopy(self)
                                new_board.move(piece,row,col)

                                if not new_board.is_checked(self.color, 0)[0]:
                                    moves.append((row,col))
                            else:
                                moves.append((row,col))
        else:
            pawn_cols = []
            for (r, c) in board.black_board_pieces:
                p = board.get_piece(r,c,1,BLACK)
                if p and type(p) == Pawn and p.color == BLACK:
                    pawn_cols.append(c)

            for col in range(COLS):
                if col not in pawn_cols:
                    for row in range(6 - num, 9):
                        p = board.get_piece(row,col,1,BLACK)
                        if not p or (type(p) != Marshall and p.tier < 3):
                            if check_for_check:
                                new_board = copy.deepcopy(board)
                                piece = copy.deepcopy(self)
                                new_board.move(piece,row,col)

                                if not new_board.is_checked(self.color, 0)[0]:
                                    moves.append((row,col))
                            else:
                                moves.append((row,col))
        return moves

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        moves = []
        attacks = []
        tier = self.tier + self._near_fortress(board)

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._pawn_drop(both_pass, board, 0)
            else:
                moves = self._pawn_drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            if self.color == WHITE:
                row = 1
            else:
                row = -1

            p = board.get_piece(self.row + row, self.col, 1, self.color)
            self._moves_and_attacks(moves,attacks,p, board, self.row + row, self.col, check_for_check)

            if (self.row == 2 and self.color == WHITE) or (self.row == 7 and self.color == BLACK):
                p = board.get_piece(self.row + 2 * row, self.col, 1, self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + 2 * row, self.col, check_for_check)

            if tier > 1:
                for col in [-1, 1]:
                    p = board.get_piece(self.row + row, self.col + col, 1, self.color)
                    self._moves_and_attacks(moves,attacks,p, board,self.row + row, self.col + col, check_for_check)

        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            return (True, [(self.row,self.col)])
        return (False, [])

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(Pawn_W, (110,500))
        else:
            win.blit(Pawn_B, (1025,500))

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(PawnW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(PawnB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def __str__(self):
        return 'Pawn'


class Spy(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(Spy_W, (110,500))
        else:
            win.blit(Spy_B, (1025,500))

    def __str__(self):
        return 'Spy'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(SpyW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(SpyB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        tier = self.tier + self._near_fortress(board)
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._drop(both_pass, board, 0)
            else:
                moves = self._drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            if tier < 3:
                num = tier
            else:
                num = 8

            #UP
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row + cnt,self.col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + cnt,self.col, check_for_check)
                if p and p.color != self.color:
                    break
            
            #Down
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row - cnt,self.col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row - cnt,self.col, check_for_check)
                if p and p.color != self.color:
                    break

            #Left
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row,self.col - cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row,self.col - cnt, check_for_check)
                if p and p.color != self.color:
                    break

            #Right
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row,self.col + cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row,self.col + cnt, check_for_check)
                if p and p.color != self.color:
                    break

            #UpLeft
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row + cnt,self.col - cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + cnt,self.col - cnt, check_for_check)
                if p and p.color != self.color:
                    break
            
            #UpRight
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row + cnt,self.col + cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + cnt,self.col + cnt, check_for_check)
                if p and p.color != self.color:
                    break

            #DownLeft
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row - cnt,self.col - cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row - cnt,self.col - cnt, check_for_check)
                if p and p.color != self.color:
                    break

            #DownRight
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row - cnt,self.col + cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row - cnt,self.col + cnt, check_for_check)
                if p and p.color != self.color:
                    break

        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            (r,c) = pos
            lst = [(self.row,self.col)]

            if r == self.row:
                if c < self.col:
                    while(c != self.col):
                        lst.append((r,c))
                        c += 1
                else:
                    while(c != self.col):
                        lst.append((r,c))
                        c -= 1

            elif r < self.row:
                if c == self.col:
                    while(r != self.row):
                        lst.append((r,c))
                        r += 1

                elif c < self.col:
                    while (r != self.row):
                        lst.append((r,c))
                        r += 1
                        c += 1
                else:
                    while (r != self.row):
                        lst.append((r,c))
                        r += 1
                        c -= 1
            else:
                if c == self.col:
                    while(r != self.row):
                        lst.append((r,c))
                        r -= 1

                elif c < self.col:
                    while(r != self.row):
                        lst.append((r,c))
                        r -= 1
                        c += 1
                else:
                    while(r != self.row):
                        lst.append((r,c))
                        r -= 1
                        c -= 1

            lst.remove(pos)
            return (True, lst)
        return (False, [])

class Cannon(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(Cannon_W, (110,500))
        else:
            win.blit(Cannon_B, (1025,500))

    def __str__(self):
        return 'Cannon'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(CannonW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(CannonB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        tier = self.tier + self._near_fortress(board)
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._drop(both_pass, board, 0)
            else:
                moves = self._drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            if tier < 3:
                num = tier
            else:
                num = 8


            #UP
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row + cnt,self.col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + cnt,self.col, check_for_check)
                if p and p.color != self.color:
                    break
            
            #Down
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row - cnt,self.col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row - cnt,self.col, check_for_check)
                if p and p.color != self.color:
                    break


            #Left
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row,self.col - cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row,self.col - cnt, check_for_check)
                if p and p.color != self.color:
                    break

            #Right
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row,self.col + cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row,self.col + cnt, check_for_check)
                if p and p.color != self.color:
                    break

        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            (r,c) = pos
            lst = [(self.row,self.col)]

            if r == self.row:
                if c < self.col:
                    while (c != self.col):
                        lst.append((self.row,c))
                        c += 1
                else:
                    while (c != self.col):
                        lst.append((self.row,c))
                        c -= 1
            else:
                if r < self.row:
                    while (r != self.row):
                        lst.append((r, self.col))
                        r += 1
                else:
                    while (r != self.row):
                        lst.append((r, self.col))
                        r -= 1

            lst.remove(pos)
            return (True, lst)
        return (False, [])

class Fortress(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(Fortress_W, (110,500))
        else:
            win.blit(Fortress_B, (1025,500))

    def __str__(self):
        return 'Fortress'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(FortressW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(FortressB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])


    def _fortress_drop(self, both_pass, board, check_for_check):
        moves = []

        if both_pass == 2:
            num = 3
        else:
            num = 0

        if self.color == WHITE:
            for row in range(0, 3 + num):
                for col in range(COLS):
                    if not board.board[row][col]:
                        if check_for_check:
                            new_board = copy.deepcopy(board)
                            piece = copy.deepcopy(self)
                            new_board.move(piece,row,col)

                            if not new_board.is_checked(self.color, 0)[0]:
                                moves.append((row,col))
                        else:
                            moves.append((row,col))
        else:
            for row in range(6 - num, 9):
                for col in range(COLS):
                     if not board.board[row][col]:
                        if check_for_check:
                            new_board = copy.deepcopy(board)
                            piece = copy.deepcopy(self)
                            new_board.move(piece,row,col)

                            if not new_board.is_checked(self.color, 0)[0]:
                                moves.append((row,col))
                        else:
                            moves.append((row,col))
        return moves

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._fortress_drop(both_pass, board, 0)
            else:
                moves = self._fortress_drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            for col in [1, 0, -1]:
                for row in [1, 0, -1]:
                    if row != 0 or col != 0:
                        p = board.get_piece(self.row + row,self.col + col,1,self.color)
                        self._moves_and_attacks(moves,attacks,p, board, self.row + row,self.col + col, check_for_check)
     
        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            return (True, [(self.row,self.col)])
        return (False, [])

            
class Samourai(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(Samourai_W, (110,500))
        else:
            win.blit(Samourai_B, (1025,500))
    
    def __str__(self):
        return 'Samourai'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(SamouraiW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(SamouraiB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        tier = self.tier + self._near_fortress(board)
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._drop(both_pass, board, 0)
            else:
                moves = self._drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            if tier < 3:
                num = tier
            else:
                num = 8

            #UpLeft
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row + cnt,self.col - cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + cnt,self.col - cnt, check_for_check)
                if p and p.color != self.color:
                    break
            
            #UpRight
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row + cnt,self.col + cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + cnt,self.col + cnt, check_for_check)
                if p and p.color != self.color:
                    break

            #DownLeft
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row - cnt,self.col - cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row - cnt,self.col - cnt, check_for_check)
                if p and p.color != self.color:
                    break

            #DownRight
            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row - cnt,self.col + cnt,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row - cnt,self.col + cnt, check_for_check)
                if p and p.color != self.color:
                    break
            
        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        if self.color == WHITE:
            row = 1
        else:
            row = -1

        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            (r,c) = pos
            lst = [(self.row,self.col)]

            if r < self.row:
                if c < self.col:
                    while (r != self.row):
                        lst.append((r,c))
                        r += 1
                        c += 1
                else:
                    while (r != self.row):
                        lst.append((r,c))
                        r += 1
                        c -= 1
            else:
                if c < self.col:
                    while (r != self.row):
                        lst.append((r,c))
                        r -= 1
                        c += 1
                else:
                    while (r != self.row):
                        lst.append((r,c))
                        r -= 1
                        c -= 1

            lst.remove(pos)
            return (True, lst)
        return (False, [])

class Captain(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(Captain_W, (110,500))
        else:
            win.blit(Captain_B, (1025,500))

    def __str__(self):
        return 'Captain'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(CaptainW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(CaptainB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = []
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._drop(both_pass, board, 0)
            else:
                moves = self._drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            for col in [1, 0, -1]:
                for row in [1, 0, -1]:
                    if row != 0 or col != 0:
                        p = board.get_piece(self.row + row,self.col + col,1,self.color)
                        self._moves_and_attacks(moves,attacks,p, board, self.row + row,self.col + col, check_for_check)
     
        if moves or attacks:
            valid = (moves, attacks)
        return valid

    def can_attack(self,pos, board, check_for_check):
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            return (True, [(self.row,self.col)])
        return (False, [])

class General(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(General_W, (110,500))
        else:
            win.blit(General_B, (1025,500))

    def __str__(self):
        return 'General'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(GeneralW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(GeneralB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        tier = self.tier + self._near_fortress(board)
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._drop(both_pass, board, 0)
            else:
                moves = self._drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            if self.color == WHITE:
                row = 1
            else:
                row = -1

            #Tier 1
            for col in [-1, 0, 1]:
                for r in [row, 0]:
                    p = board.get_piece(self.row + r,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row + r,self.col + col, check_for_check)

            p = board.get_piece(self.row - row,self.col,1,self.color)
            self._moves_and_attacks(moves,attacks,p, board, self.row - row,self.col, check_for_check)

            #Tier 2
            if tier == 2:
                for col in [-1, 1]:
                    p = board.get_piece(self.row - row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row - row,self.col + col, check_for_check)

            #Tier 3:
            if tier == 3:
                for col in [-1, 0, 1]:
                    p = board.get_piece(self.row + 2 * row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row + 2 * row,self.col + col, check_for_check)

            #top left
            p = board.get_piece(self.row + row,self.col - 1,1,self.color)
            p2 = board.get_piece(self.row + row,self.col,1,self.color)

            if p and p.color != self.color and p2 and p2.color != self.color:
               moves.remove((self.row + 2 * row,self.col - 1))
               attacks.remove((self.row + 2 * row,self.col - 1))

            #Top middle
            p = board.get_piece(self.row + row,self.col,1,self.color)
            p2 = board.get_piece(self.row + row,self.col - 1,1,self.color)
            p3 = board.get_piece(self.row + row,self.col + 1,1,self.color)

            if p and p.color != self.color and p2 and p2.color != self.color and p3 and p3.color != self.color:
               moves.remove((self.row + 2 * row,self.col))
               attacks.remove((self.row + 2 * row,self.col))

            #Top right
            p = board.get_piece(self.row + row,self.col + 1,1,self.color)
            p2 = board.get_piece(self.row + row,self.col,1,self.color)

            if p and p.color != self.color and p2 and p2.color != self.color:
               moves.remove((self.row + 2 * row,self.col + 1))
               attacks.remove((self.row + 2 * row,self.col + 1))
          
        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        if self.color == WHITE:
            r = 1
        else:
            r = -1

        (row,col) = pos
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            lst = [(self.row,self.col)]
            if abs(row - self.row) == 2:
                if col != self.col:
                    lst.append((self.row + r, col))
                else:
                    for c in [-1,0,1]:
                        p = board.get_piece(self.row + r,self.col + c,1,self.color)
                        if not p or p.color == self.color:
                            lst.append((self.row + r,self.col + c))
                            break

            if pos in lst:
                lst.remove(pos)
            return (True, lst)
        return (False, [])

class Archer(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(Archer_W, (110,500))
        else:
            win.blit(Archer_B, (1025,500))

    def __str__(self):
        return 'Archer'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(ArcherW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(ArcherB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        tier = self.tier + self._near_fortress(board)
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._drop(both_pass, board, 0)
            else:
                moves = self._drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            for row in range(-tier, tier):
                #left col
                p = board.get_piece(self.row + row,self.col - tier,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + row,self.col - tier, check_for_check)

                #Right col
                p = board.get_piece(self.row + row,self.col + tier,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + row,self.col + tier, check_for_check)

            for col in range(-tier, tier):
                #Up row
                p = board.get_piece(self.row + tier,self.col + col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + tier,self.col + col, check_for_check)
            
                #Top row
                p = board.get_piece(self.row - tier,self.col + col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row - tier,self.col + col, check_for_check)
            
        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            return (True, [(self.row,self.col)])
        return (False, [])
    
    
class Knight(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(Knight_W, (110,500))
        else:
            win.blit(Knight_B, (1025,500))

    def __str__(self):
        return 'Knight'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(KnightW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(KnightB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        tier = self.tier + self._near_fortress(board)
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._drop(both_pass, board, 0)
            else:
                moves = self._drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            if self.color == WHITE:
                row = 1
            else:
                row = -1

            if tier == 1:
                for col in [-1,1]:
                    p = board.get_piece(self.row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row,self.col + col, check_for_check)

                    p = board.get_piece(self.row + 2 * row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row + 2*  row,self.col + col, check_for_check)
            else:
                for col in [-2,2]:
                    p = board.get_piece(self.row + row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row + row,self.col + col, check_for_check)

                for col in [-1,1]:
                    p = board.get_piece(self.row + 2 * row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row + 2 * row,self.col + col, check_for_check)

            if tier == 3:
                for col in [-2,2]:
                    p = board.get_piece(self.row - row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row - row,self.col + col, check_for_check)

                for col in [-1,1]:
                    p = board.get_piece(self.row - 2 * row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row - 2 * row,self.col + col, check_for_check)

        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            return (True, [(self.row,self.col)])
        return (False, [])

class Musketeer(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(Musket_W, (110,500))
        else:
            win.blit(Musket_B, (1025,500))

    def __str__(self):
        return 'Musketeer'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(MusketW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(MusketB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        tier = self.tier + self._near_fortress(board)
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._drop(both_pass, board, 0)
            else:
                moves = self._drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            if self.color == WHITE:
                row = 1
            else:
                row = -1

            if tier < 3:
                num = tier
            else:
                num = 8

            cnt = 0
            while(cnt < num):
                cnt += 1
                p = board.get_piece(self.row + cnt * row,self.col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + cnt * row,self.col, check_for_check)
                if p and p.color != self.color:
                    break
            
        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        if self.color == WHITE:
            row = 1
        else:
            row = -1

        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            (r,c) = pos
            lst = [(self.row,self.col)]

            while (r != self.row):
                r -= row
                lst.append[(r, self.col)]

            lst.remove(pos)
            return (True, lst)
        return (False, [])
    

class LGeneral(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(LGeneral_W, (110,500))
        else:
            win.blit(LGeneral_B, (1025,500))

    def __str__(self):
        return 'LGeneral'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(LGeneralW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
            win.blit(LGeneralB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
    
    
    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        tier = self.tier + self._near_fortress(board)
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._drop(both_pass, board, 0)
            else:
                moves = self._drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            if self.color == WHITE:
                row = 1
            else:
                row = -1

            #Tier 1
            for col in [-1, 0, 1]:
                for r in [row, -row]:
                    if r != -row and col != 0:
                        p = board.get_piece(self.row + r,self.col + col,1,self.color)
                        self._moves_and_attacks(moves,attacks,p, board, self.row + r,self.col + col, check_for_check)

            #Tier 2:
            if tier > 1:
                p = board.get_piece(self.row + -row,self.col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + -row,self.col, check_for_check)

            #Tier 3:
            if tier > 2:
                for col in[-1,1]:
                    p = board.get_piece(self.row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row,self.col + col, check_for_check)

        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            return (True, [(self.row,self.col)])
        return (False, [])


class MGeneral(Piece):

    def draw_pile_pick(self, win):
        if self.color == WHITE:
            win.blit(MGeneral_W, (110,500))
        else:
            win.blit(MGeneral_B, (1025,500))
    
    def __str__(self):
        return 'MGeneral'

    def draw(self, win):
        super().draw(win)

        if self.color == WHITE:
            win.blit(MGeneralW, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])
        else:
             win.blit(MGeneralB, [284+MARGIN + self.col * (SQUARE_SIZE+MARGIN), MARGIN - 1 + self.row * (SQUARE_SIZE+MARGIN)])

    def get_valid(self, board, turn_num, both_pass, check_for_check):
        valid = None
        tier = self.tier + self._near_fortress(board)
        moves = []
        attacks = []

        if turn_num >= 3 and self.pile:
            if both_pass != 2:
                moves = self._drop(both_pass, board, 0)
            else:
                moves = self._drop(both_pass, board, check_for_check)

        if both_pass == 2 and not self.pile:
            if self.color == WHITE:
                row = 1
            else:
                row = -1

            for col in [1,-1]:
                p = board.get_piece(self.row + row,self.col + col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + row,self.col + col, check_for_check)

            if tier > 1:
                p = board.get_piece(self.row + row,self.col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row + row,self.col, check_for_check)

            if tier == 2:
                for col in [1,-1]:
                    p = board.get_piece(self.row - row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row - row,self.col + col, check_for_check)

            if tier == 3:
                p = board.get_piece(self.row - row,self.col,1,self.color)
                self._moves_and_attacks(moves,attacks,p, board, self.row - row,self.col, check_for_check)

                for col in [1,-1]:
                    p = board.get_piece(self.row,self.col + col,1,self.color)
                    self._moves_and_attacks(moves,attacks,p, board, self.row,self.col + col, check_for_check)
               
        if moves or attacks:
            valid = (moves, attacks)
        return valid
        
    def can_attack(self, pos, board, check_for_check):
        valid = self.get_valid(board, 53, 2, check_for_check)
        if valid and pos in valid[1]:
            return (True, [(self.row,self.col)])
        return (False, [])
