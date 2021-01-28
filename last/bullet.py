import pygame
import player
import dimensions

WIDTH = dimensions.WIDTH
HEIGHT = dimensions.HEIGHT
pullet = pygame.image.load('Images/Bullet.png')

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_arrowkeys):
        pygame.sprite.Sprite.__init__(self)
        width = 25
        height = 25
        self.image = pullet
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.speedx = 0
        self.speedy = 0

        if player_arrowkeys == 3:
            self.image = pullet
            self.speedy = 0
            self.speedx = 12

        if player_arrowkeys == 2:
            self.image = pygame.transform.rotate(pullet, 180)
            self.speedy = 0
            self.speedx = -12

        if player_arrowkeys == 0:
            self.image = pygame.transform.rotate(pullet, 90)
            self.speedy = -12
            self.speedx = 0

        if player_arrowkeys == 1:
            self.image = pygame.transform.rotate(pullet, 270)
            self.speedy = 12
            self.speedx = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.kill()

        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.kill()