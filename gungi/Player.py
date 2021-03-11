import pygame

class Player:
   def __init__(self, color, game):
      self.color = color
      self.game = game
   
   def move(self, row, col, on_board):
      ret = True
      if self.game.turn == self.color:
         ret = self.game.select(row, col, on_board)
      return ret

   def draw(self,win):
      self.game.update(win)
      pygame.display.update()


  



 
   
