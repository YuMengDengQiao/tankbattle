#coding: utf-8
import pygame
from pygame.locals import *
import time, sys

class Hero(pygame.sprite.Sprite):
    def __init__(self, center, img, face_to = {'UP': False,'DOWN': False,'LEFT': False,'RIGHT': True}):
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
        self.shooting_sound = pygame.mixer.Sound('.\\res\\fire2.wav')

    def Get_Order(self):
        self.is_collision = False
        for event in pygame.event.get():
            if event.type == KEYUP:
                #self.moving_sound.stop()
                if event.key == K_UP or event.key == K_w:
                    self.move_to['UP'] = False
                    self.action = 0
                elif event.key == K_DOWN or event.key == K_s:
                    self.move_to['DOWN'] = False
                    self.action = 0
                elif event.key == K_LEFT or event.key == K_a:
                    self.move_to['LEFT'] = False
                    self.action = 0
                elif event.key == K_RIGHT or event.key == K_d:
                    self.move_to['RIGHT'] = False
                    self.action = 0
                elif event.key == K_SPACE:
                    pass
            elif event.type == KEYDOWN:
               #self.moving_sound.play(loops=-1)
                if event.key == K_UP or event.key == K_w:
                    self.move_to['UP'] = True
                    self.move_to['DOWN'] = False
                    self.move_to['LEFT'] = False
                    self.move_to['RIGHT'] = False
                    self.last_move_time = time.time()
                    self.is_move = True
                    self.face_to['UP'] =True
                    self.face_to['DOWN'] = False
                    self.face_to['LEFT'] =False
                    self.face_to['RIGHT'] =False
                elif event.key == K_DOWN or event.key == K_s:
                    self.move_to['UP'] = False
                    self.move_to['DOWN'] = True
                    self.move_to['LEFT'] = False
                    self.move_to['RIGHT'] = False
                    self.last_move_time = time.time()
                    self.is_move = True
                    self.face_to['UP'] = False
                    self.face_to['DOWN'] = True
                    self.face_to['LEFT'] = False
                    self.face_to['RIGHT'] = False
                elif event.key == K_LEFT or event.key == K_a:
                    self.move_to['UP'] = False
                    self.move_to['DOWN'] = False
                    self.move_to['LEFT'] = True
                    self.move_to['RIGHT'] = False
                    self.last_move_time = time.time()
                    self.is_move = True
                    self.face_to['UP'] = False
                    self.face_to['DOWN'] = False
                    self.face_to['LEFT'] = True
                    self.face_to['RIGHT'] = False
                elif event.key == K_RIGHT or event.key == K_d:
                    self.move_to['UP'] = False
                    self.move_to['DOWN'] = False
                    self.move_to['LEFT'] = False
                    self.move_to['RIGHT'] = True
                    self.last_move_time = time.time()
                    self.is_move = True
                    self.face_to['UP'] = False
                    self.face_to['DOWN'] = False
                    self.face_to['LEFT'] = False
                    self.face_to['RIGHT'] = True
                elif event.key == K_SPACE:
                    self.current_shooting_time = time.time()
                    if self.current_shooting_time - self.last_shooting_time > self.reload_time:
                        self.shooting() 
                        self.last_shooting_time = time.time()

    def Calcu_Pos(self):
        self.temp_pos[0] = self.pos[0]
        self.temp_pos[1] = self.pos[1]
        if (self.move_to['UP'] or self.move_to['DOWN'] or self.move_to['LEFT'] or self.move_to['RIGHT']) \
           and time.time() - self.last_move_time + 1 > self.MOVEFREQ and self.is_move == True:
            self.action = (self.action + 1) % (self.action_wait * 4)
            if self.move_to['UP']:
                if self.pos[1] < 0:
                    self.pos[1] = 0
                else:self.pos[1] -= self.speed
            elif self.move_to['DOWN']:
                if self.pos[1] > 448:
                    self.pos[1] = 448
                else:self.pos[1] += self.speed
            elif self.move_to['LEFT']:
                if self.pos[0] < 0:
                    self.pos[0] = 0
                else:self.pos[0] -= self.speed
            elif self.move_to['RIGHT']:
                if self.pos[0] > 608:
                    self.pos[0] = 608
                else:self.pos[0] += self.speed
        elif (self.move_to['UP'] == False and self.move_to['DOWN'] == False and \
              self.move_to['LEFT'] == False and self.move_to['RIGHT'] == False):
            if self.pos[1] % 1 != 0 and self.face_to['UP']:
                self.pos[1] -= 1
            elif self.pos[1] % 1 != 0 and self.face_to['DOWN']:
                self.pos[1] += 1
            elif self.pos[0] % 1 != 0 and self.face_to['LEFT']:
                self.pos[0] -= 1
            elif self.pos[0] % 1 != 0 and self.face_to['RIGHT']:
                self.pos[0] += 1
        self.rect = Rect((self.pos[0],self.pos[1]), (32, 32))

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
        self.Get_Order()
        self.Calcu_Pos()
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
        self.shooting_sound.play()
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
