import pygame
from gungi.constants import *
from gungi.game import Game
from Network import Network
from gungi.Player import Player

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


def get_row_col_from_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE

    if col >= 4 and col <= 12:
        col -= 4
        row = y // SQUARE_SIZE
        on_board = 1
    else:
        row = y // (split * 2)
        on_board = 0

    return row, col, on_board


def main():
    run = True
    ret = True
    n = Network()
    p = n.getP()
    p2 = n.send(p)
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        p2 = n.send(p)

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            row, col, on_board = get_row_col_from_mouse(pos)
            print((row,col, on_board))
        
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Display blank wins and play again button
                if ret:
                    ret = p.move(row,col,on_board)
                else:
                    run = False

        if p and p2:
            if p.game.turn_num < p2.game.turn_num:
                p.game = p2.game
            else:
                p2.game = p.game
            
            p.game.update(WIN)

    pygame.quit()
main()