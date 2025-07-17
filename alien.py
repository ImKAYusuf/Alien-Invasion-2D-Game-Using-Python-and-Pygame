from pygame.sprite import Sprite
import pygame as py

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        
        self.original_image=py.image.load("images\ALIEN.png").convert_alpha()
        self.image=py.transform.scale(self.original_image,(50,50))
        self.rect=self.image.get_rect()
        
        self.rect.x=self.image.get_width()
        self.rect.y=self.image.get_height()
        
        self.x=float(self.rect.x)
        
    def update(self):
        self.x+=(self.settings.alien_speed*self.settings.fleet_direction)
        self.rect.x=self.x
        
    def check_edges(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right>screen_rect.right or self.rect.left<screen_rect.left:
            return True 