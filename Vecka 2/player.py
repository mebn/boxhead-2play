import pygame
from BFS import *
import random
import dimensions


class Player():
    def __init__(self, pos, hp, width, height, color):
        self.image = pygame.image.load('./Images/LEFT.png')
        self.x = pos[0]
        self.y = pos[1]
        self.hp = hp
        self.width = width
        self.height = height
        self.color = color

        self.vel = 5
        self.arrow_keys = [False, False, False, False]
        self.direction = 0

    # Draws on canvas.
    def draw(self, win):
        win.blit(self.image, (self.x,self.y))

        if self.direction == 3:
            self.image = pygame.image.load('./Images/LEFT.png')
        
        if self.direction == 2:
            self.image = pygame.image.load('./Images/FacingLeft.png')
        
        if self.direction == 0:
            self.image = pygame.image.load('./Images/FacingUp.png')
        
        if self.direction == 1:
            self.image = pygame.image.load('./Images/FacingDown.png')


    # Sends keystrokes to server as a bool list.
    def move(self):
        keys = pygame.key.get_pressed()
        self.arrow_keys = [False, False, False, False]

        # 0=up 1=down 2=left 3=right
        if keys[pygame.K_UP]:
            self.arrow_keys[0] = True
            self.direction = 0

        if keys[pygame.K_DOWN]:
            self.arrow_keys[1] = True
            self.direction = 1

        if keys[pygame.K_LEFT]:
            self.arrow_keys[2] = True
            self.direction = 2

        if keys[pygame.K_RIGHT]:
            self.arrow_keys[3] = True
            self.direction = 3

        return bytes(self.arrow_keys)


    # Updates position of player after getting new coords from server.
    def update_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def position(self):
        return [self.x, self.y]