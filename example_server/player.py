import pygame

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 5

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        arrow_keys = [False, False, False, False] # up down left right

        if keys[pygame.K_LEFT]:
            arrow_keys[2] = True
        
        if keys[pygame.K_RIGHT]:
            arrow_keys[3] = True

        if keys[pygame.K_UP]:
            arrow_keys[0] = True

        if keys[pygame.K_DOWN]:
            arrow_keys[1] = True

        return bytearray(arrow_keys)

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)