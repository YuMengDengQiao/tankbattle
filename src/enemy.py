#coding: utf-8
import pygame
from pygame.locals import *
import time, sys, random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, center, img, face_to = {'UP': False,'DOWN': False,'LEFT': True,'RIGHT': False}):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = img
        self.image = self.raw_image.subsurface(0, 0 , 32, 32)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.size = [128, 128]
        self.pos = [self.rect.x, self.rect.y]
        self.temp_pos = [self.rect.x, self.rect.y]
        self.speed = 2 
        self.face_to = face_to
        self.move_to = {'UP': False,'DOWN': False,'LEFT': False,'RIGHT': False}
        self.is_move = False
        self.MOVEFREQ = 0
        self.action = 0
        self.action_wait = 4
        self.last_move_time = time.time()
        self.last_show_time = time.time()
        self.reload_time = 1 
        self.last_shooting_time = 0
        self.moving_sound = pygame.mixer.Sound('.\\res\\move.wav')

        self.is_collide = False

    def Move_foreward(self):
        if self.face_to == {'UP': True,'DOWN': False,'LEFT': False,'RIGHT': False}:
            self.rect.y -= self.speed
        if self.face_to == {'UP': False,'DOWN': True,'LEFT': False,'RIGHT': False}:
            self.rect.y += self.speed
        if self.face_to == {'UP': False,'DOWN': False,'LEFT': True,'RIGHT': False}:
            self.rect.x -= self.speed
        if self.face_to == {'UP': False,'DOWN': False,'LEFT': False,'RIGHT': True}:
            self.rect.x += self.speed

    def Turn_UP(self):
        self.face_to = {'UP': True,'DOWN': False,'LEFT': False,'RIGHT': False}

    def Turn_DOWN(self):
        self.face_to = {'UP': False,'DOWN': True,'LEFT': False,'RIGHT': False}

    def Turn_LEFT(self):
        self.face_to = {'UP': False,'DOWN': False,'LEFT': True,'RIGHT': False}

    def Turn_RIGHT(self):
        self.face_to = {'UP': False,'DOWN': False,'LEFT': False,'RIGHT': True}


    def AI(self):
        if self.is_collide == True and self.face_to['UP'] == True:
            self.rect.y += self.speed * 2
            self.Turn_DOWN()
            self.Move_foreward()
            self.is_collide = False
        if self.is_collide == True and self.face_to['DOWN'] == True:
            self.rect.y -= self.speed * 2
            self.Turn_UP()
            self.Move_foreward()
            self.is_collide = False
        if self.is_collide == True and self.face_to['LEFT'] == True:
            self.rect.x += self.speed * 2
            self.Turn_RIGHT()
            self.Move_foreward()
            self.is_collide = False
        if self.is_collide == True and self.face_to['RIGHT'] == True:
            self.rect.x -= self.speed * 2
            self.Turn_LEFT()
            self.Move_foreward()
            self.is_collide = False

        rnd = random.randint(0, 99)
        if rnd > 1:
            self.Move_foreward()
            if self.rect.y < 0:
                self.Turn_DOWN()
                self.Move_foreward()
            if self.rect.y > 448:
                self.Turn_UP()
                self.Move_foreward()
            if self.rect.x < 0:
                self.Turn_RIGHT()
                self.Move_foreward()
            if self.rect.x > 608:
                self.Turn_LEFT()
                self.Move_foreward()
        else:
            rnd = random.randint(1, 4)
            if rnd == 1:
                self.Turn_UP()
            if rnd == 2:
                self.Turn_DOWN()
            if rnd == 3:
                self.Turn_LEFT()
            if rnd == 4:
                self.Turn_RIGHT()



        #self.rect = Rect((self.pos[0],self.pos[1]), (32, 32))

    def Draw_Hero(self):
        if self.face_to['UP'] == True:
            SCREEN.blit(self.image, (self.pos[0], self.pos[1]), \
                             (self.size[0] / 4 * (self.action / self.action_wait) , \
                             self.size[1] / 4 * 3,self.size[0] / 4,self.size[1] / 4))
        elif self.face_to['DOWN'] == True:
            SCREEN.blit(self.image, (self.pos[0], self.pos[1]), \
                             (self.size[0] / 4 * (self.action / self.action_wait) , \
                             self.size[1] / 4 * 0,self.size[0] / 4,self.size[1] / 4))
        elif self.face_to['LEFT'] == True:
            SCREEN.blit(self.image, (self.pos[0], self.pos[1]), \
                             (self.size[0] / 4 * (self.action / self.action_wait) , \
                             self.size[1] / 4 * 1,self.size[0] / 4,self.size[1] / 4))
        elif self.face_to['RIGHT'] == True:
            SCREEN.blit(self.image, (self.pos[0], self.pos[1]), \
                             (self.size[0] / 4 * (self.action / self.action_wait) , \
                             self.size[1] / 4 * 2,self.size[0] / 4,self.size[1] / 4))

    def update(self, player_group):
        self.player_group = player_group
        self.AI()

        if self.face_to['UP'] == True:
            self.image = self.raw_image.subsurface( \
                             self.size[0] / 4 * (self.action / self.action_wait) , \
                             self.size[1] / 4 * 3,self.size[0] / 4,self.size[1] / 4)
        elif self.face_to['DOWN'] == True:
            self.image = self.raw_image.subsurface( \
                             self.size[0] / 4 * (self.action / self.action_wait) , \
                             self.size[1] / 4 * 0,self.size[0] / 4,self.size[1] / 4)
        elif self.face_to['LEFT'] == True:
            self.image = self.raw_image.subsurface( \
                             self.size[0] / 4 * (self.action / self.action_wait) , \
                             self.size[1] / 4 * 1,self.size[0] / 4,self.size[1] / 4)
        elif self.face_to['RIGHT'] == True:
            self.image = self.raw_image.subsurface( \
                             self.size[0] / 4 * (self.action / self.action_wait) , \
                             self.size[1] / 4 * 2,self.size[0] / 4,self.size[1] / 4)

    def shooting(self):
        self.shell = Shell(self.rect.center, self.face_to)
        self.player_group.add(self.shell)

            
    def check_for_collision(self,is_collision):
        self.is_collision = is_collision
        if self.is_collision == True:
            self.is_move = False
            self.pos[0] = self.temp_pos[0]
            self.pos[1] = self.temp_pos[1]


class Shell(pygame.sprite.Sprite):
    def __init__(self, center, face_to):
        pygame.sprite.Sprite.__init__(self)
        self.face_to = face_to
        self.shell = pygame.image.load(u'.\\res\\shell.png') 
        self.up_shell = self.shell.subsurface(13, 4, 6, 19)
        self.down_shell = self.shell.subsurface(45, 9, 6, 19)
        self.left_shell = self.shell.subsurface(4, 44, 19, 6)
        self.right_shell = self.shell.subsurface(41, 45, 19, 6)
        self.speed_y = 0
        self.speed_x = 0
        self.SHELL_SPEED = 5

        if self.face_to == {'UP': True,'DOWN': False,'LEFT': False,'RIGHT': False}:
            self.image = self.up_shell
            self.speed_y = self.SHELL_SPEED * (-1)
        if self.face_to == {'UP': False,'DOWN': True,'LEFT': False,'RIGHT': False}:
            self.image = self.down_shell
            self.speed_y = self.SHELL_SPEED
        if self.face_to == {'UP': False,'DOWN': False,'LEFT': True,'RIGHT': False}:
            self.image = self.left_shell
            self.speed_x = self.SHELL_SPEED * (-1)
        if self.face_to == {'UP': False,'DOWN': False,'LEFT': False,'RIGHT': True}:
            self.image = self.right_shell
            self.speed_x = self.SHELL_SPEED
                
        self.rect = self.image.get_rect()
        self.rect.center = center 
    
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.bottom < 0 or self.rect.top > 480 or self.rect.left > 640 or self.rect.right < 0:
            self.kill()

    def is_hit(self):
        pass
