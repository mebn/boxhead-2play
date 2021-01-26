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
        
        self.rect = self.image.get_rect()
        self.rect.center = (dimensions.WIDTH / 2, dimensions.HEIGHT / 2)
        self.rect.centerx = random.randint(1, dimensions.HEIGHT)
        self.rect.bottom = random.randint(1, dimensions.HEIGHT)

    # Draws on canvas.
    def draw(self, win):
        win.blit(self.image,(self.x,self.y))

        if self.direction == 3:
            self.image = pygame.image.load('./Images/LEFT.png')
        
        if self.direction == 2:
            self.image = pygame.image.load('./Images/FacingLeft.png')
        
        if self.direction == 0:
            self.image = pygame.image.load('./Images/FacingUp.png')
        
        if self.direction == 1:
            self.image = pygame.image.load('./Images/FacingDown.png')
        
        # if self.direction == "UR":
        #     self.image = pygame.image.load('Images/NE.png')
        # if self.direction == "UL":
        #     self.image = pygame.image.load('Images/NW.png')
        # if self.direction == "DR":
        #     self.image = pygame.image.load('Images/SE.png')
        # if self.direction == "DL":
        #     self.image = pygame.image.load('Images/SW.png')


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

#
# # Define colors
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# FPS = 144
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         width = 108.75
#         height = 150
#
#         self.image = pygame.image.load('Images/FacingUp.png')
#         self.image.set_colorkey(WHITE)
#         self.rect = self.image.get_rect()
#         self.rect.center = (WIDTH / 2, HEIGHT / 2)
#         self.rect.centerx = random.randint(1, WIDTH)
#         self.rect.bottom = random.randint(1, HEIGHT)
#         self.life = 4
#         self.direction = 'R'
#         self.p = (self.rect.x, self.rect.y)
#
#     # def shoot(self):
#     #     bullet = Bullet(self.rect.x, self.rect.centery)
#     #     all_sprites.add(bullet)
#     #     bullets.add(bullet)
#     #     pygame.mixer.Sound.play(bullet_sound)
#
#
#     def position(self):
#         return [self.rect.x, self.rect.y]
#
#     def update(self):
#
#         # update the image depending on the direction
#         if self.direction == "R":
#             self.image = pygame.image.load('Images/LEFT.png')
#         if self.direction == "L":
#             self.image = pygame.image.load('Images/FacingLeft.png')
#         if self.direction == "U":
#             self.image = pygame.image.load('Images/FacingUp.png')
#         if self.direction == "D":
#             self.image = pygame.image.load('Images/FacingDown.png')
#         if self.direction == "UR":
#             self.image = pygame.image.load('Images/NE.png')
#         if self.direction == "UL":
#             self.image = pygame.image.load('Images/NW.png')
#         if self.direction == "DR":
#             self.image = pygame.image.load('Images/SE.png')
#         if self.direction == "DL":
#             self.image = pygame.image.load('Images/SW.png')
#
#         self.speedx = 0
#         self.speedy = 0
#
#         #Movement
#         keystate = pygame.key.get_pressed()
#         if keystate[pygame.K_a]:
#             self.speedx = -3
#             self.direction = 'L'
#         if keystate[pygame.K_d]:
#             self.speedx = 3
#             self.direction = 'R'
#         if keystate[pygame.K_w]:
#             self.speedy = -3
#             self.direction = 'U'
#         if keystate[pygame.K_s]:
#             self.speedy = 3
#             self.direction = 'D'
#
#         if keystate[pygame.K_a] and keystate[pygame.K_w]:
#             self.speedx = -3
#             self.speedy = -3
#             self.direction = 'UL'
#         if keystate[pygame.K_d] and keystate[pygame.K_w]:
#             self.speedx = 3
#             self.speedy = -3
#             self.direction = 'UR'
#         if keystate[pygame.K_s] and keystate[pygame.K_a]:
#             self.speedy = 3
#             self.speedx = -3
#             self.direction = 'DL'
#         if keystate[pygame.K_s] and keystate[pygame.K_d]:
#             self.speedy = 3
#             self.speedx = 3
#             self.direction = 'DR'
#
#         self.rect.x += self.speedx
#         self.rect.y += self.speedy
#
#         # Off Screen Protection
#         if self.rect.right > WIDTH:
#             self.rect.right = WIDTH
#         if self.rect.left < 0:
#             self.rect.left = 0
#         if self.rect.top < 0:
#             self.rect.top = 0
#         if self.rect.bottom > HEIGHT - 5:
#             self.rect.bottom = HEIGHT - 5
#
