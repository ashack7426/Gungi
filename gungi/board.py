import pygame
from gungi.constants import *
from gungi.piece import *
import copy

myfont = pygame.font.SysFont("comicsansms", 30)

class Board:
    def __init__(self):
        self.board =  [] 
        self.black_pile_pieces = {} #key = (row,col) of pile piece, val = (black pile piece, number left) 
        self.white_pile_pieces = {} #key = (row,col) of pile piece, val = (white pile piece, number_left)
        self.create_board() #initalize the board, black_pile_pieces, and white_pile_pieces

        self.black_board_pieces = [] #(row,col) of black board pieces
        self.white_board_pieces = [] #(row,col) of white board pieces
        self.black_on_board = self.white_on_board = 0 #number of pieces on the board of each side

        self.black_king_pos = None #pos of black king
        self.white_king_pos = None #pos of white king

    #initalize the board, black_pile_pieces, and white_pile_pieces
    def create_board(self):
        for row in range(ROWS):
            lst = []
            for col in range(COLS):
                lst.append([])
            self.board.append(lst)

        #Pass 
        self.white_pile_pieces[(7,1)] = (Pass(7,1,WHITE,False), 8)
        self.white_pile_pieces[(7,2)] = (Pass(7,2,WHITE,False), 8)
        self.black_pile_pieces[(7,14)] = (Pass(7,14,BLACK,False), 8)
        self.black_pile_pieces[(7,15)] = (Pass(7,15,BLACK,False), 8)

        #Marshall
        self.white_pile_pieces[(0,0)] = (Marshall(0,0, WHITE, True), 1)
        self.black_pile_pieces[(0,16)] = (Marshall(0,16, BLACK, True), 1)

        #General
        self.white_pile_pieces[(0,3)] = (General(0,3, WHITE, True), 6)
        self.black_pile_pieces[(0,13)] = (General(0,13, BLACK, True), 6)

        #Pawn
        self.white_pile_pieces[(1,0)] = (Pawn(1, 0, WHITE, True), 9)
        self.black_pile_pieces[(1, 16)] = (Pawn(1, 16, BLACK, True), 9)

        #Knight
        self.white_pile_pieces[(1,3)] = (Knight(1, 3, WHITE, True), 2)
        self.black_pile_pieces[(1, 13)] = (Knight(1, 13, BLACK, True), 2)

        #Samourai
        self.white_pile_pieces[(2,0)] = (Samourai(2, 0, WHITE, True), 2)
        self.black_pile_pieces[(2, 16)] = (Samourai(2, 16, BLACK, True), 2)

        #Cannon
        self.white_pile_pieces[(2,3)] = (Cannon(2, 3, WHITE, True), 2)
        self.black_pile_pieces[(2, 13)] = (Cannon(2, 13, BLACK, True), 2)

        #Spy
        self.white_pile_pieces[(3,0)] = (Spy(3, 0, WHITE, True), 2)
        self.black_pile_pieces[(3, 16)] = (Spy(3, 16, BLACK, True), 2)

        #Fortress
        self.white_pile_pieces[(3,3)] = (Fortress(3, 3, WHITE, True), 2)
        self.black_pile_pieces[(3, 13)] = (Fortress(3, 13, BLACK, True), 2)

        #LGeneral
        self.white_pile_pieces[(4,0)] = (LGeneral(4, 0, WHITE, True), 2)
        self.black_pile_pieces[(4, 16)] = (LGeneral(4, 16, BLACK, True), 2)

        #Archer
        self.white_pile_pieces[(4,3)] = (Archer(4, 3, WHITE, True), 2)
        self.black_pile_pieces[(4, 13)] = (Archer(4, 13, BLACK, True), 2)

        #MGeneral
        self.white_pile_pieces[(5,0)] = (MGeneral(5, 0, WHITE, True), 4)
        self.black_pile_pieces[(5, 16)] = (MGeneral(5, 16, BLACK, True), 4)

        #Captain
        self.white_pile_pieces[(5,3)] = (Captain(5, 3, WHITE, True), 2)
        self.black_pile_pieces[(5, 13)] = (Captain(5, 13, BLACK, True), 2)

        #Musketeer
        self.white_pile_pieces[(6,0)] = (Musketeer(6, 0, WHITE, True), 2)
        self.black_pile_pieces[(6, 16)] = (Musketeer(6, 16, BLACK, True), 2)


    #Get the piece at the (row,col)
    def get_piece(self, row, col, on_board, turn):
        if on_board:
                try:
                    p = self.board[row][col]
                except IndexError:
                    return Marshall(row, col, turn, False)

                if len(p) > 0:
                    return p[-1]
        else:
            try:
                pile_piece = []
                if turn == WHITE:
                    pile_piece = self.white_pile_pieces[(row,col)]
                else:
                    pile_piece = self.black_pile_pieces[(row,col)]
            
                if pile_piece[1]:
                    return copy.deepcopy(pile_piece[0])
            except:
                return None

        return None



    #Moving piece to row and col
    def move(self, piece, row, col):
        #Drop a piece
        if piece.pile:
            piece.pile = False
            piece.tier = len(self.board[row][col]) + 1
    
            if piece.color == WHITE:
                p = self.white_pile_pieces[(piece.row,piece.col)] 

                if p[1]:
                    self.white_pile_pieces[(piece.row,piece.col)] = (p[0], p[1] - 1)

                self.white_on_board += 1

            else:
                p = self.black_pile_pieces[(piece.row,piece.col)] 

                if p[1]:
                    self.black_pile_pieces[(piece.row,piece.col)] = (p[0], p[1] - 1)

                self.black_on_board += 1

        #Move a piece on the board
        else:
            self.board[piece.row][piece.col].pop()
            new_cell = self.board[row][col]
            piece.tier = len(new_cell) + 1
            old_cell = self.board[piece.row][piece.col]

            #No more pieces at old cell or old cell is now controlled by opponent after move
            if piece.color == WHITE:
                if not old_cell:
                    self.white_board_pieces.remove((piece.row,piece.col))
                elif old_cell[-1].color != piece.color:
                    self.white_board_pieces.remove((piece.row,piece.col))
                    self.black_board_pieces.append((piece.row,piece.col))
            else:
                if not old_cell:
                    self.black_board_pieces.remove((piece.row,piece.col))
                elif old_cell[-1].color != piece.color:
                    self.black_board_pieces.remove((piece.row,piece.col))
                    self.white_board_pieces.append((piece.row,piece.col))

        #store piece location
        if piece.color == WHITE:
            if piece.king:
                self.white_king_pos = (row,col)
            if (row,col) in self.black_board_pieces:
                self.black_board_pieces.remove((row,col))
            if (row,col) not in self.white_board_pieces:
                self.white_board_pieces.append((row,col))
        else:
            if piece.king:
                self.black_king_pos = (row,col)
            if (row,col) in self.white_board_pieces:
                self.white_board_pieces.remove((row,col))
            if (row,col) not in self.black_board_pieces:
                self.black_board_pieces.append((row,col))
            
        piece.move(row, col)
        self.board[row][col].append(piece)

    #Capture a piece
    def capture(self, piece, row, col):
        p = self.board[row][col].pop()

        if p.color == WHITE:
            self.white_on_board -= 1
        else:
            self.black_on_board -= 1

        self.move(piece, row, col)

    #Is color currently in check
    def is_checked(self, color, checkmate_check):
        checks = []
        count = 0
        move_to_these_cells = []
        stay_in_these_cells = []

        if color == WHITE:
            king_pos = self.white_king_pos
            board_pieces = self.black_board_pieces
        else:
            king_pos = self.black_king_pos
            board_pieces = self.white_board_pieces

        stay_in_these_cells = [king_pos]
        for (row,col) in board_pieces:
            p = self.board[row][col][-1]
            can_attack, path = p.can_attack(king_pos,self, 0)

            if can_attack:
                if not checkmate_check:
                    return (True, checks, move_to_these_cells, stay_in_these_cells)
                
                checks.append(p)

                if len(move_to_these_cells) == 0:
                    move_to_these_cells = path
                else:
                    move_to_these_cells = list(set(move_to_these_cells) & set(path)) #intersect
            else:
                if (path and path not in stay_in_these_cells):
                    stay_in_these_cells.append(path)

        if len(checks) > 0:
            return (True, checks, move_to_these_cells, stay_in_these_cells)
        return (False, checks, move_to_these_cells, stay_in_these_cells)


    def is_checkmated(self, color):
        checked, attackers, move_to, stay_in = self.is_checked(color, 1)

        if checked:
            if color == WHITE:
                (row,col) = self.white_king_pos
                board_pieces = self.white_board_pieces
                pile_pieces = self.white_pile_pieces
                board_piece_cnt = self.white_on_board
            else:
                (row,col) = self.black_king_pos
                board_pieces = self.black_board_pieces
                pile_pieces = self.black_pile_pieces
                board_piece_cnt = self.black_on_board

            #can move out of check with king 
            king = self.board[row][col][-1]
            moves = king.get_valid(self, 53, 2, 1) #criteria for valid move is that wont be put in checked
            if moves:
                return False

            #can capture the sole attacker (only 1 and can attack)
            if len(attackers) == 1:
                for (row,col) in board_pieces:
                    p = self.board[row][col][-1]
                    if p.can_attack((attackers[0].row, attackers[0].col),self, 0)[0] and (row,col) not in stay_in:
                        return False
            
            # can block the attackers
             # need to path to the king (not including king_pos) for reach attacker
                # get the intersection between all of them if any of them are 0 (knight archer etc) return true
                # if the intersection has len 0 return true
                # otherwise check if any of my pieces can move to that spot (not including king)
            if len(move_to) == 0:
                return True
            else:
                #Drop a piece on the spot?
                if board_piece_cnt < 26:
                    for m in move_to:
                        for (row,col) in pile_pieces.keys():
                            p = pile_pieces[(row,col)][0]
                            moves = p.get_valid(self, 53, 2, 1)
                            if moves and m in moves[0]:
                                return False

                #Move board piece to the spot?
                for m in move_to:
                    for (row,col) in board_pieces:
                        p = self.board[row][col][-1]
                        moves = p.get_valid(self, 53, 2, 1)
                        if (row,col) not in stay_in and moves and m in moves[0]:
                            return False
            return True
        return False


    #Draw the piles
    def _draw_piles(self,win):
        #Drawing the piece_nums for both piles
        ArcherW_num = myfont.render(str(self.white_pile_pieces[(4,3)][1]), 1, (0,0,0))
        ArcherB_num = myfont.render(str(self.black_pile_pieces[(4,13)][1]), 1, (0,0,0))
        CannonW_num = myfont.render(str(self.white_pile_pieces[(2,3)][1]), 1, (0,0,0))
        CannonB_num = myfont.render(str(self.black_pile_pieces[(2,13)][1]), 1, (0,0,0))
        CaptainW_num = myfont.render(str(self.white_pile_pieces[(5,3)][1]), 1, (0,0,0))
        CaptainB_num = myfont.render(str(self.black_pile_pieces[(5,13)][1]), 1, (0,0,0))
        FortressW_num = myfont.render(str(self.white_pile_pieces[(3,3)][1]), 1, (0,0,0))
        FortressB_num = myfont.render(str(self.black_pile_pieces[(3,13)][1]), 1, (0,0,0))
        GeneralW_num = myfont.render(str(self.white_pile_pieces[(0,3)][1]), 1, (0,0,0))
        GeneralB_num = myfont.render(str(self.black_pile_pieces[(0,13)][1]), 1, (0,0,0))
        KnightW_num = myfont.render(str(self.white_pile_pieces[(1,3)][1]), 1, (0,0,0))
        KnightB_num = myfont.render(str(self.black_pile_pieces[(1,13)][1]), 1, (0,0,0))
        LGeneralW_num = myfont.render(str(self.white_pile_pieces[(4,0)][1]), 1, (0,0,0))
        LGeneralB_num = myfont.render(str(self.black_pile_pieces[(4,16)][1]), 1, (0,0,0))
        MarshallW_num = myfont.render(str(self.white_pile_pieces[(0,0)][1]), 1, (0,0,0))
        MarshallB_num = myfont.render(str(self.black_pile_pieces[(0,16)][1]), 1, (0,0,0))
        MGeneralW_num = myfont.render(str(self.white_pile_pieces[(5,0)][1]), 1, (0,0,0))
        MGeneralB_num = myfont.render(str(self.black_pile_pieces[(5,16)][1]), 1, (0,0,0))
        MusketW_num = myfont.render(str(self.white_pile_pieces[(6,0)][1]), 1, (0,0,0))
        MusketB_num = myfont.render(str(self.black_pile_pieces[(6,16)][1]), 1, (0,0,0))
        PawnW_num = myfont.render(str(self.white_pile_pieces[(1,0)][1]), 1, (0,0,0))
        PawnB_num = myfont.render(str(self.black_pile_pieces[(1,16)][1]), 1, (0,0,0))
        SamouraiW_num = myfont.render(str(self.white_pile_pieces[(2,0)][1]), 1, (0,0,0))
        SamouraiB_num = myfont.render(str(self.black_pile_pieces[(2,16)][1]), 1, (0,0,0))
        SpyW_num = myfont.render(str(self.white_pile_pieces[(3,0)][1]), 1, (0,0,0))
        SpyB_num = myfont.render(str(self.black_pile_pieces[(3,16)][1]), 1, (0,0,0))
        piece_num_off = 12 #offset for piece_num

        #Marshall
        win.blit(Marshall_W, (0,piece_num_off - 12)) #White logo
        win.blit(Marshall_B, ((COLS + 7) * SQUARE_SIZE,piece_num_off - 12)) #Black logo
        win.blit(MarshallW_num, (SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(MarshallB_num, (SQUARE_SIZE * (COLS + 7), piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #General
        win.blit(General_W, (3 * SQUARE_SIZE + 10, piece_num_off - 12)) #White logo
        win.blit(General_B, ((COLS + 4) * SQUARE_SIZE + 10,piece_num_off - 12)) #Black logo
        win.blit(GeneralW_num, (3 * SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(GeneralB_num, ((COLS + 5) * SQUARE_SIZE, piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #Pawn
        win.blit(Pawn_W, (0,piece_num_off - 12)) #White logo
        win.blit(Pawn_B, ((COLS + 7) * SQUARE_SIZE + 10,piece_num_off - 12)) #Black logo
        win.blit(PawnW_num, (SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(PawnB_num, (SQUARE_SIZE * (COLS + 7), piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #Knight
        win.blit(Knight_W, (3 * SQUARE_SIZE + 10,piece_num_off - 12)) #White logo
        win.blit(Knight_B, ((COLS + 4) * SQUARE_SIZE + 10,piece_num_off - 12)) #Black logo
        win.blit(KnightW_num, (3 * SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(KnightB_num, ((COLS + 5) * SQUARE_SIZE, piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #Samourai
        win.blit(Samourai_W, (0,piece_num_off - 12)) #White logo
        win.blit(Samourai_B, ((COLS + 7) * SQUARE_SIZE + 10,piece_num_off - 12)) #Black logo
        win.blit(SamouraiW_num, (SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(SamouraiB_num, (SQUARE_SIZE * (COLS + 7), piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #Cannon
        win.blit(Cannon_W, (3 * SQUARE_SIZE + 10,piece_num_off - 12)) #White logo
        win.blit(Cannon_B, ((COLS + 4) * SQUARE_SIZE + 10,piece_num_off - 12)) #Black logo
        win.blit(CannonW_num, (3 * SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(CannonB_num, ((COLS + 5) * SQUARE_SIZE, piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #Spy
        win.blit(Spy_W, (0,piece_num_off - 12)) #White logo
        win.blit(Spy_B, ((COLS + 7) * SQUARE_SIZE + 10,piece_num_off - 12)) #Black logo
        win.blit(SpyW_num, (SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(SpyB_num, (SQUARE_SIZE * (COLS + 7), piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #Fortress
        win.blit(Fortress_W, (3 * SQUARE_SIZE + 10,piece_num_off - 12)) #White logo
        win.blit(Fortress_B, ((COLS + 4) * SQUARE_SIZE + 10,piece_num_off - 12)) #Black logo
        win.blit(FortressW_num, (3 * SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(FortressB_num, ((COLS + 5) * SQUARE_SIZE, piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #LGeneral
        win.blit(LGeneral_W, (0, piece_num_off - 12)) #White logo
        win.blit(LGeneral_B, ((COLS + 7) * SQUARE_SIZE + 10,piece_num_off - 12)) #Black logo
        win.blit(LGeneralW_num, (SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(LGeneralB_num, (SQUARE_SIZE * (COLS + 7), piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #Archer
        win.blit(Archer_W, (3 * SQUARE_SIZE + 10, piece_num_off - 12)) #White logo
        win.blit(Archer_B, ((COLS + 4) * SQUARE_SIZE + 10,piece_num_off - 12)) #Black logo
        win.blit(ArcherW_num, (3 * SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(ArcherB_num, ((COLS + 5) * SQUARE_SIZE, piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #MGeneral
        win.blit(MGeneral_W, (0, piece_num_off - 12)) #White logo
        win.blit(MGeneral_B, ((COLS + 7) * SQUARE_SIZE + 10, piece_num_off - 12)) #Black logo
        win.blit(MGeneralW_num, (SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(MGeneralB_num, (SQUARE_SIZE * (COLS + 7), piece_num_off)) #Black piece_num
        piece_num_off += split
        
        #Captain
        win.blit(Captain_W, (3 * SQUARE_SIZE + 10, piece_num_off - 12)) #White logo
        win.blit(Captain_B, ((COLS + 4) * SQUARE_SIZE + 10, piece_num_off - 12)) #Black logo
        win.blit(CaptainW_num, (3 * SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(CaptainB_num, ((COLS + 5) * SQUARE_SIZE, piece_num_off)) #Black piece_num
        piece_num_off += split

        #Musketeer
        win.blit(Musket_W, (0, piece_num_off - 12)) #White logo
        win.blit(Musket_B, ((COLS + 7) * SQUARE_SIZE + 10, piece_num_off - 12)) #Black logo
        win.blit(MusketW_num, (SQUARE_SIZE, piece_num_off)) #White piece_num
        win.blit(MusketB_num, (SQUARE_SIZE * (COLS + 7), piece_num_off)) #Black piece_num
       
    #Draw the board
    def _draw_board(self,win, game):
        #Draw Backgrounds
        win.fill(BLACK)

        for column in range(4 * SQUARE_SIZE + MARGIN, (COLS + 4) * SQUARE_SIZE + COLS * MARGIN, SQUARE_SIZE+MARGIN):
            for row in range(MARGIN - 1, SQUARE_SIZE * ROWS, SQUARE_SIZE+MARGIN):
                rect = pygame.Rect(column, row, SQUARE_SIZE,SQUARE_SIZE)
                pygame.draw.rect(win, TAN, rect)

        
        if game.selected and not game.selected.pile:
            row = MARGIN - 1 + game.selected.row * (SQUARE_SIZE+MARGIN)
            col = 4 * SQUARE_SIZE + MARGIN +  game.selected.col * (SQUARE_SIZE+MARGIN)

            if game.mode:
                color = RED
            else:
                color = LIGHT_BLUE
            
            rect = pygame.Rect(col, row, SQUARE_SIZE,SQUARE_SIZE)
            pygame.draw.rect(win, color, rect)


        pygame.draw.rect(win, GREY, [0,0,4 * SQUARE_SIZE + MARGIN,SQUARE_SIZE * ROWS])
        pygame.draw.rect(win, GREY, [13 * SQUARE_SIZE + 9 * MARGIN,0,4 * SQUARE_SIZE + MARGIN,SQUARE_SIZE * ROWS])

        #Draw number of pieces on the board of each side
        black_on = myfont.render(str(self.black_on_board), 1, (0,0,0))
        white_on = myfont.render(str(self.white_on_board), 1, (0,0,0))

        win.blit(black_on, ((COLS + 4) * SQUARE_SIZE + 20, ROWS * SQUARE_SIZE - 50))

        if self.white_on_board < 10:
            win.blit(white_on, (3 * SQUARE_SIZE + 40, ROWS * SQUARE_SIZE - 50))
        else:
            win.blit(white_on, (3 * SQUARE_SIZE + 30, ROWS * SQUARE_SIZE - 50))

    #Draw the game
    def draw(self, win, game):
        self._draw_board(win, game)
        self._draw_piles(win)

        for (row,col) in self.black_board_pieces:
            p = self.board[row][col][-1]
            p.draw(win)

        for (row,col) in self.white_board_pieces:
            p = self.board[row][col][-1]
            p.draw(win)

    def _disp_cell(self, row, col):
        board_str = ''

        if self.board[row][col]:
            for p in self.board[row][col]:
                board_str += str(p)
                if p.color == WHITE:
                    board_str += 'W'
                else:
                    board_str += 'B'    
        else:
            board_str += '0'

        board_str += str(row)
        board_str += str(col)
        return board_str

    def dis_board(self):
        board_str = ''
        for row in range(ROWS):
            for col in range(COLS):
                board_str += self._disp_cell(row,col)

        return board_str

    def dis_full_board(self):
        board_str = self.dis_board()

        for (row,col) in self.black_pile_pieces.keys():
            piece = self.black_pile_pieces[(row,col)]
            board_str += (str(piece[0]) + 'B' + piece[1])

        for (row,col) in self.white_pile_pieces.keys():
            piece = self.black_pile_pieces[(row,col)]
            board_str += (str(piece[0]) + 'W' + piece[1])

        board_str += 'B' + str(self.black_on_board)
        board_str += 'W' + str(self.white_on_board)

        return board_str

            

    
        

               
