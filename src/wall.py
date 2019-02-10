#coding: utf-8
import pygame
from pygame.locals import *
import time, sys

class WALL(pygame.sprite.Sprite):
    def __init__(self, center, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = center


    
