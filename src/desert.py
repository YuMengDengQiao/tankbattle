#coding: utf-8

import pygame
from pygame.locals import *

import tank
import collider
import wall
import explosion
import enemy

import random


BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
class STAGE:
    def __init__(self):
        WIDTH = 640
        HEIGHT = 480
        #pygame.mixer.music.load(u'.\\res\\The Good Fight (w intro).ogg')
        #pygame.mixer.music.play(-1)

    def setup_background(self):
        self.background_image = pygame.image.load(u'.\\res\\desert_background.png')
        self.screen = pygame.display.get_surface()
        self.wall_img = pygame.image.load(u'.\\res\\brick_collection.png')
        self.broken_wall_img = pygame.image.load(u'.\\res\\brick_broken1.png')
        self.wall_sprites = pygame.sprite.Group()

        self.garage_map = pygame.image.load(u'.\\res\\garage_map.png')
        
        self.wall = wall.WALL((160, 144), self.wall_img.subsurface(243, 224, 13, 10))
        self.wall_sprites.add(self.wall)
        self.wall = wall.WALL((150, 160), self.wall_img.subsurface(224, 234, 32, 22))
        self.wall_sprites.add(self.wall)

        self.wall = wall.WALL((160, 128), self.wall_img.subsurface(243, 32, 13, 32))
        self.wall_sprites.add(self.wall)
        self.wall = wall.WALL((160, 96), self.wall_img.subsurface(243, 64, 13, 32))
        self.wall_sprites.add(self.wall)
        self.wall = wall.WALL((160, 64), self.wall_img.subsurface(243, 96, 13, 32))
        self.wall_sprites.add(self.wall)
        self.wall = wall.WALL((160, 32), self.wall_img.subsurface(243, 128, 13, 32))
        self.wall_sprites.add(self.wall)
        self.wall = wall.WALL((160, 0), self.wall_img.subsurface(243, 160, 13, 32))
        self.wall_sprites.add(self.wall)

        for i in range(30):
            self.wall = wall.WALL((random.randint(12, 40) * 16 + 16, random.randint(4, 30) * 16 + 16), \
                    self.broken_wall_img)
            self.wall_sprites.add(self.wall) 


    def setup_sprite(self):
        self.weapon_sprites = pygame.sprite.Group() #保存武器精灵
        self.enemy_weapon_sprites = pygame.sprite.Group() #保存武器精灵
        self.hero_and_enemy = pygame.sprite.Group()
        HEROIMAGE = pygame.image.load(u'.\\res\\red_wolf.png')
        self.tank = tank.Hero((64, 64), HEROIMAGE, face_to = {'UP': False,'DOWN': True,'LEFT': False,'RIGHT': False})
        self.hero_and_enemy.add(self.tank)

        self.explo_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        ENEMYIMAGE = pygame.image.load(u'.\\res\\enemy.png')
        for i in range(1):
            self.enemy = enemy.Enemy((608, 64 + i * 32), ENEMYIMAGE, face_to = {'UP': False,'DOWN': False,'LEFT': True,'RIGHT': False})
            self.enemy_sprites.add(self.enemy)

    def update_all(self):
        self.hero_and_enemy.update(self.weapon_sprites)
        self.weapon_sprites.update()
        self.wall_sprites.update()
        self.enemy_sprites.update(self.enemy_weapon_sprites)

        if pygame.sprite.spritecollide(self.tank, self.wall_sprites, dokill=False):
            self.tank.check_for_collision(True)

        is_explo = pygame.sprite.groupcollide(self.weapon_sprites, self.wall_sprites, True, True)
        #返回以self.weapon_sprites为key的字典，
        #每个key的值为self.wall_sprites中与self.weapon_sprites碰撞的元素
        for key in is_explo:
            if is_explo[key]:
                self.explo = explosion.Explosion(is_explo[key][0].rect.center)
                self.explo_sprites.add(self.explo)
        self.explo_sprites.update()

        hero_wall_collide = pygame.sprite.groupcollide(self.hero_and_enemy, self.wall_sprites, False, False)
        for key in hero_wall_collide:
            key.is_collide = True

        enemy_wall_collide = pygame.sprite.groupcollide(self.enemy_sprites, self.wall_sprites, False, False)
        for key in enemy_wall_collide:
            key.is_collide = True
        
        hit_collide = pygame.sprite.groupcollide(self.weapon_sprites, self.enemy_sprites, True, True)
        for key in hit_collide:
            if hit_collide[key]:
                self.enemy_explo = explosion.Explosion(hit_collide[key][0].rect.center)
                self.explo_sprites.add(self.enemy_explo)
        self.explo_sprites.update()
        

    def draw_all(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.garage_map, (0,0))        
        self.wall_sprites.draw(self.screen)
        self.hero_and_enemy.draw(self.screen)
        self.weapon_sprites.draw(self.screen)
        self.explo_sprites.draw(self.screen)
        self.enemy_sprites.draw(self.screen)


    def check_stage(self):
        if self.tank.rect.x < 96 and self.tank.rect.y < 32:
            return True
        else:
            return False

    def change_stage(self):
        return u'GARAGE'

def check_wall(x, y):
    is_collide = pygame.sprite.collideany(x, y)
    return is_collide


