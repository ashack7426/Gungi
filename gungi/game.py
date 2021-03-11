import pygame
from gungi.constants import *
from gungi.board import *
from gungi.computer import *

font = pygame.font.SysFont('Arial', 23)

class Game:
    def __init__(self):
        self._init()

    def update(self, win):
        self.board.draw(win, self)

        if self.turn == 53:
            self.both_pass = 2

        if self.end:
            self._disp_end_screen(self.end, win)
            self.mode = 2

        if self.selected and self.selected.color == self.turn and (self.selected.pile or self.both_pass == 2):
            if self.mode == 0:
                self.draw_valid_moves(self.valid_moves, LIGHT_BLUE, win)
            else:
                self.draw_valid_moves(self.valid_attacks, RED, win)

        if self.turn == WHITE:
            pygame.draw.circle(win, GREEN, (SQUARE_SIZE//2 + 220, -10 + SQUARE_SIZE//2), 15)
        else:
            pygame.draw.circle(win, GREEN, (SQUARE_SIZE//2 + 915, -10 +  SQUARE_SIZE//2), 15)

        if self.selected:
            if self.selected.pile:
                self.selected.draw_pile_pick(win)

        if self.both_pass == 3:
            del self.board.white_pieces[(7,1)]
            del self.board.white_pieces[(7,2)]
            del self.board.black_pieces[(7,14)]
            del self.board.black_pieces[(7,15)]
            
        #Should be 17 and 26
        if (self.turn_num > 36 and self.turn_num < 53) and self.both_pass < 2:
            if self.turn == WHITE:
                pygame.draw.rect(win, RED, pygame.Rect(2 * SQUARE_SIZE - 20, 9 * SQUARE_SIZE - 30, 60, 25))
                win.blit(font.render('PASS', True, (0,0,0)), (2 * SQUARE_SIZE - 20, 9 * SQUARE_SIZE - 30))
            else:
                pygame.draw.rect(win, RED, pygame.Rect(15 * SQUARE_SIZE - 30, 9 * SQUARE_SIZE - 30, 60, 25))
                win.blit(font.render('PASS', True, (0,0,0)), (15 * SQUARE_SIZE - 30, 9 * SQUARE_SIZE - 30))


        #Display the stack when piece is clicked
        if self.selected and not self.selected.pile:
            row = SQUARE_SIZE * 2
            col = SQUARE_SIZE * 1.5

            (r,c) = (self.selected.row, self.selected.col)
            pieces = self.board.board[r][c]

            for p in reversed(pieces):
                if p.color == WHITE:
                    name = str(p) + 'W'
                else:
                    name = str(p) + 'B'

                logo = logos[name]

                if self.turn == WHITE:
                    win.blit(logo, (col,row))
                else:
                    win.blit(logo, (col + (SQUARE_SIZE * (COLS + 4)),row))

                row += 50

        pygame.display.flip()

    def _init(self):
        self.both_pass = 0
        self.end = None
        self.selected = None
        self.pawn_move_or_capture = 0

        self.turn_num = 1
        self.board = Board()
        self.turn = BLACK
        self.mode = 0
        self.valid_moves = {}
        self.valid_attacks = {}

        self.boards = {}
        self.boards[self.board.dis_board()] = 1

    def winner(self):
        if self.turn == WHITE:
            if self.both_pass == 3 and self.board.is_checked(BLACK,0)[0]:
                return 'White Wins!'
            
            #Any move you do will force the player into check
            if self.board.is_checkmated(BLACK):
                return 'White Wins!'

            self.both_pass = min(2,self.both_pass)

        else:
            #Any move you do will force the player into check
            if self.board.is_checkmated(WHITE):
                return 'Black Wins!'

        #Impossibility of checkmate
        if self.both_pass == 2 and self.board.black_on_board <= 3 and self.board.black_on_board <= 3:
            return "Draw! Impossibility of checkmate"
        
        #50 move rule
        if self.pawn_move_or_capture == 100:
            return "Draw! 50 moves on both sides without moving pawns or captures"
        
        #threefold repetition
        try:
            if self.boards[self.board.dis_board()] == 3:
                return "Draw! Threefold reptition"
        except:
            pass

        return 0

    def reset(self, win):
        self._init()
        self.update(win)

    #Return False when there is a loser
    def select(self, row, col, on_board):
        piece = self.board.get_piece(row, col, on_board, self.turn)

        if self.selected:
            #Did you click the same piece twice or failed to move piece
            if piece and self.selected.row == piece.row and self.selected.col == piece.col and not self.selected.pile:
                if not self.mode and self.valid_attacks:
                    self.mode = 1
                #Deselected piece
                else:
                    self.valid_moves = {}
                    self.valid_attacks = {}
                    self.selected = None
                    self.mode = 0
                    return True

            (game_over, moved) = self._move(row, col, on_board)

            if game_over:
                return False

            self.valid_moves = {}
            self.valid_attacks = {}
            self.selected = None

            if not moved:
                self.select(row,col,on_board)
            
        else:
            if type(piece) == Pass and self.turn_num > 36 and self.turn_num < 53 and self.both_pass < 2:
                if piece.color == BLACK:
                    self.both_pass += 1
                else:
                    if self.both_pass == 1:
                        self.both_pass += 1
                        self.change_turn()
                    else:
                        self.both_pass = 0

                self.change_turn()
                self.turn_num += 1
                return True

            if self.both_pass < 2:
                self.both_pass = 0

            if piece:
                valid = piece.get_valid(self.board, self.turn_num, self.both_pass, 1)
            else:
                return True

            self.selected = piece 

            if valid:
                self.valid_moves = valid[0]
                self.valid_attacks = valid[1]

        return True
    
    def _move(self, row, col, on_board):
        #is block on board
        # is row, col in valid moves
        if on_board and self.turn == self.selected.color and ((not self.mode and (row, col) in self.valid_moves) or (self.mode and (row, col) in self.valid_attacks)):
            #Capture a piece
            if self.mode:
                self.board.capture(self.selected, row, col)
                self.mode = 0
                self.pawn_move_or_capture = 0

            #Move a piece
            else:
                self.board.move(self.selected, row, col)

                if type(self.selected) == Pawn:
                    self.pawn_move_or_capture = 0
                else:
                    self.pawn_move_or_capture += 1

            if self.both_pass == 2:
                try:
                    self.boards[self.board.dis_board()] += 1
                except:
                    self.boards[self.board.dis_board()] = 1

            self.turn_num += 1
            self.end = self.winner()

            if self.end:
                return (1, True)
            else:
                self.change_turn()
                return (0, True)

        return (0,False)


    #Display message and 
    def _disp_end_screen(self, winner, win):
        # draw text
        txt = winner
        text = font.render(txt, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        win.blit(text, text_rect)

    def draw_valid_moves(self, moves, color, win):
        for move in moves:
            row, col = move
            pygame.draw.circle(win, color, (col * SQUARE_SIZE + SQUARE_SIZE//2 + 285, row * SQUARE_SIZE + SQUARE_SIZE//2), 10)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK