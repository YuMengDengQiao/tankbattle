#coding: utf-8

import pygame
from pygame.locals import *

import tank
import collider


BLACK = [0, 0, 0]
class STAGE:
    def __init__(self):
        WIDTH = 640
        HEIGHT = 480
        #pygame.mixer.music.load(u'.\\res\\The Good Fight (w intro).ogg')
        #pygame.mixer.music.play(-1)

    def setup_background(self):
        self.background_image = pygame.image.load(u'.\\res\\garage.png')
        self.screen = pygame.display.get_surface()
        self.screen.fill(BLACK)
        self.screen.blit(self.background_image, (116, 108))

        self.wall_sprites = pygame.sprite.Group()
        self.wall = collider.Collider(0, 0, 640, 150)
        self.wall_sprites.add(self.wall)
        self.wall = collider.Collider(0, 0, 140, 480)
        self.wall_sprites.add(self.wall)
        self.wall = collider.Collider(500, 0, 140, 480)
        self.wall_sprites.add(self.wall)
        self.wall = collider.Collider(0, 370, 640, 150)
        self.wall_sprites.add(self.wall)

    def setup_sprite(self):
        self.weapon_sprites = pygame.sprite.Group() #保存武器精灵
        self.hero_and_enemy = pygame.sprite.Group()
        HEROIMAGE = pygame.image.load(u'.\\res\\red_wolf.png')
        self.tank = tank.Hero((320, 340), HEROIMAGE, face_to = {'UP': True,'DOWN': False,'LEFT': False,'RIGHT': False})
        self.hero_and_enemy.add(self.tank)

    def update_all(self):
        self.hero_and_enemy.update(self.weapon_sprites)
        self.weapon_sprites.update()
        if pygame.sprite.spritecollideany(self.tank, self.wall_sprites):
            self.tank.check_for_collision(True)

    def draw_all(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background_image, (116, 108))
        self.hero_and_enemy.draw(self.screen)
        self.weapon_sprites.draw(self.screen)

    def check_stage(self):
        if self.tank.rect.y > 330:
            return True
        else:
            return False

    def change_stage(self):
        return u'DESERT'

def check_wall(x, y):
    is_collide = pygame.sprite.collideany(x, y)
    return is_collide


