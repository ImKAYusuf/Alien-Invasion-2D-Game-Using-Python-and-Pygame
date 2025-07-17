import pygame as py
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settengs=ai_game.settings
        self.original_image = py.image.load("images/shipp.png").convert_alpha()
        self.image = py.transform.scale(self.original_image, (60, 90))
        self.rect=self.image.get_rect()
        self.rect.midbottom=self.screen_rect.midbottom
        self.moving_right=False
        self.moving_left=False
        self.moving_top=False
        self.moving_bottom=False
        self.x=float(self.rect.x)
        self.y=float(self.rect.y)
    def blitme(self):
        self.screen.blit(self.image,self.rect)
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x +=self.settengs.ship_speed
        if self.moving_left and self.rect.left >0:
            self.x -=self.settengs.ship_speed
        self.rect.x=self.x
        if self.moving_top and self.rect.top >0:
            self.y -=self.settengs.ship_speed
        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.y +=self.settengs.ship_speed
        self.rect.y=self.y
    
    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)