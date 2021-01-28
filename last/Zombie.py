import pygame
import random
from BFS import *

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width = 108.75
        height = 150

        self.image = pygame.image.load('Images/ZombieS.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(400, 600)
        self.rect.y = random.choice([10, 990])
        self.direction = 3
        self.health = 100
        self.speedx = 1
        self.speedy = 1
        self.positions = [self.rect.x, self.rect.y]
       # self.pathfinder = SEARCH()
       # self.path = [(0, 0)]

    def draw(self, win, player_pos):
        win.blit(self.image, (self.rect.x, self.rect.y))
        self.update(player_pos)


    def update_img(self): # private
        if self.direction == 3: # R
            self.image = pygame.image.load('Images/ZombieE.png')
        
        if self.direction == 2: # L
            self.image = pygame.image.load('Images/ZombieW.png')
        
        if self.direction == 0: # U
            self.image = pygame.image.load('Images/ZombieN.png')
        
        if self.direction == 1: # D
            self.image = pygame.image.load('Images/ZombieW.png')

    def update(self, player_pos):
        self.update_img()

        if len(self.path) <= 1:
            self.zombie_position = [self.rect.x, self.rect.y]
            self.path = self.pathfinder.update_bfs(player_pos, self.zombie_position)

        else:
            prevgridcord_x, prevgridcord_y = self.path[0][0], self.path[0][1]

            self.path.remove(self.path[0])
            nextgridcord_x, nextgridcord_y = self.path[0][0], self.path[0][1]  # first zombie point

            # 0=up 1=down 2=left 3=right
            if prevgridcord_x == nextgridcord_x and prevgridcord_y == nextgridcord_x:
                self.speedx = 0
                self.speedy = 0
                self.path.remove((nextgridcord_x, nextgridcord_y))

            elif nextgridcord_x == prevgridcord_x and nextgridcord_y > prevgridcord_y:
                self.speedy = 1
                self.direction = 1 # D
                self.speedx = 0

            elif nextgridcord_x == prevgridcord_x and nextgridcord_y < prevgridcord_y:
                self.speedy = -1
                self.speedx = -0
                self.direction = 0 # U

            elif nextgridcord_y == prevgridcord_y and nextgridcord_x > prevgridcord_x:
                self.speedx = 1
                self.direction = 3 # R
                self.speedy = 0

            elif nextgridcord_y == prevgridcord_y and nextgridcord_x < prevgridcord_x:
                self.speedx = -1
                self.speedy = 0
                self.direction = 2 # L

            self.rect.x += self.speedx
            self.rect.y += self.speedy


        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.top < 0:
            self.rect.top = 0
        
        if self.rect.bottom > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5



    def pos(self):
        return self.rect.x, self.rect.y
