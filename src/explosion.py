#coding: utf-8

import pygame
from pygame import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load(u'.\\res\\Explosion.png')
        self.image = self.raw_image.subsurface(0, 0, 96, 96)
        self.player_expo_sound = pygame.mixer.Sound('.\\res\\explosion3.wav')
        self.player_expo_sound.play()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = 0 #帧数计数器
    
    def update(self):
        self.frame = 12 #动画帧数
        self.frame_last = 96 #动画持续帧数
        if self.last_update % int(self.frame_last / self.frame) == 0:
            self.image = self.raw_image.subsurface(self.last_update / int(self.frame_last / self.frame) * 96, 0, 96, 96)
        self.last_update += 1 
        if self.last_update == self.frame_last:
            self.kill()
