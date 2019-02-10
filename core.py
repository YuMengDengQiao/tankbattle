#coding: utf-8
import pygame
from pygame.locals import *

from src import desert 
from src import garage

import sys

def check_for_quit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def terminate():
    pygame.quit()
    sys.exit()

pygame.init()
SCREEN = pygame.display.set_mode((640, 480))
FPSCLOCK = pygame.time.Clock()
FPS = 30
WIDTH = 640
HEIGHT = 480


class CORE():
    def __init__(self, STAGE_KEY):
        self.current_stage = STAGE_KEY

        self.stage_dic = {u'GARAGE' : garage.STAGE(), \
                          u'DESERT' : desert.STAGE()}
        
        self.stage = self.stage_dic[self.current_stage]

        self.stage.setup_background()
        self.stage.setup_sprite()

    def main(self):
        while True:
            pygame.event.pump()
            check_for_quit()

            if self.stage.check_stage():
                self.current_stage = self.stage.change_stage()
                print self.current_stage
                self.stage = None
                self.stage = self.stage_dic[self.current_stage]
                self.stage.setup_background()
                self.stage.setup_sprite()
         
            self.stage.update_all()
            self.stage.draw_all()

            pygame.display.update()
            FPSCLOCK.tick(FPS)

