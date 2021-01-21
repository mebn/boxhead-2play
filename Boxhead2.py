import math
import pygame
import random
import sys
from threading import Timer

from BFS import *


# Button Class
class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Arial', 40)
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


# Buttons
SinglePlayer = button((0, 0, 0), 310, 200, 400, 100, 'Single Player')
MultiPlayer = button((0, 0, 0), 310, 400, 400, 100, 'Multiplayer')
HighScore = button((0, 0, 0), 310, 600, 400, 100, 'Hall of Fame')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WIDTH = 1000
HEIGHT = 1000
FPS = 144


pygame.init()

# Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Box Head")

# Sounds
bullet_sound = pygame.mixer.Sound('gun.wav')
zombie_sound = pygame.mixer.Sound('zombie.wav')
grunt_sound = pygame.mixer.Sound('gruntsound.wav')
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

# Font
font_name = pygame.font.match_font('arial')

clock = pygame.time.Clock()
zombies_last_tick = pygame.time.get_ticks()

# Zombie Spawn Timer
spawn_interval = 5000


# Drawing hearts
heartimage = pygame.image.load('Heart.png')

def hearts(x, y, health):
    heart = pygame.transform.scale(heartimage, (50,50))

    if health == 4:
        screen.blit(heart, (x, y))
        screen.blit(heart, (x+50, y))
        screen.blit(heart, (x+100, y))
        screen.blit(heart, (x+150, y))
    elif health == 3:
        screen.blit(heart, (x, y))
        screen.blit(heart, (x+50, y))
        screen.blit(heart, (x+100, y))
    elif health == 2:
        screen.blit(heart, (x, y))
        screen.blit(heart, (x+50, y))
    else:
        screen.blit(heart, (x, y))


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        heartimage = pygame.image.load('Heart.png')
        self.image = pygame.transform.scale(heartimage, (50, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

BackGround = Background('background.png', [0, 0])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width = 108.75  # height and width of the sprite player
        height = 150

        self.image = pygame.image.load('FacingUp.png')
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.centerx = random.randint(1, WIDTH)
        self.rect.bottom = random.randint(1, HEIGHT)
        self.life = 4
        self.direction = 'R'
        self.p = (self.rect.x, self.rect.y)

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)
        pygame.mixer.Sound.play(bullet_sound)


    def position(self):
        return [self.rect.x, self.rect.y]

    def update(self):

        # update the image depending on the direction
        if self.direction == "R":
            self.image = pygame.image.load('LEFT.png')
        if self.direction == "L":
            self.image = pygame.image.load('FacingLeft.png')
        if self.direction == "U":
            self.image = pygame.image.load('FacingUp.png')
        if self.direction == "D":
            self.image = pygame.image.load('FacingDown.png')
        if self.direction == "UR":
            self.image = pygame.image.load('NE.png')
        if self.direction == "UL":
            self.image = pygame.image.load('NW.png')
        if self.direction == "DR":
            self.image = pygame.image.load('SE.png')
        if self.direction == "DL":
            self.image = pygame.image.load('SW.png')

        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -3
            self.direction = 'L'
        if keystate[pygame.K_d]:
            self.speedx = 3
            self.direction = 'R'
        if keystate[pygame.K_w]:
            self.speedy = -3
            self.direction = 'U'
        if keystate[pygame.K_s]:
            self.speedy = 3
            self.direction = 'D'

        if keystate[pygame.K_a] and keystate[pygame.K_w]:
            self.speedx = -3
            self.speedy = -3
            self.direction = 'UL'
        if keystate[pygame.K_d] and keystate[pygame.K_w]:
            self.speedx = 3
            self.speedy = -3
            self.direction = 'UR'
        if keystate[pygame.K_s] and keystate[pygame.K_a]:
            self.speedy = 3
            self.speedx = -3
            self.direction = 'DL'
        if keystate[pygame.K_s] and keystate[pygame.K_d]:
            self.speedy = 3
            self.speedx = 3
            self.direction = 'DR'

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # cases for when player hits the edge of the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width = 108.75  # height and width of the sprite player
        height = 150
        self.image = pygame.image.load('ZombieS.png')
        self.rect = self.image.get_rect()
        ry = [10,990]
        self.rect.x = random.randrange(400, 600)
        self.rect.y = random.choice(ry)
        self.direction = 'R'
        self.health = 100
        self.speedx = 1
        self.speedy = 1
        self.positions = [self.rect.x, self.rect.y]
        self.pathfinder = SEARCH()
        self.path = [(0, 0)]

    def get_position(self):
        return self.positions[0]

    def update(self):
        if self.direction == "R":
            self.image = pygame.image.load('ZombieE.png')
        if self.direction == "L":
            self.image = pygame.image.load('ZombieW.png')
        if self.direction == "U":
            self.image = pygame.image.load('ZombieN.png')
        if self.direction == "D":
            self.image = pygame.image.load('ZombieW.png')
        if self.direction == "UR":
            self.image = pygame.image.load('ZombieNE.png')
        if self.direction == "UL":
            self.image = pygame.image.load('ZombieNW.png')
        if self.direction == "DR":
            self.image = pygame.image.load('ZombieSE.png')
        if self.direction == "DL":
            self.image = pygame.image.load('ZombieSW.png')

        if len(self.path) <= 1:

            player_position = player.position()
            self.zombie_position = [self.rect.x, self.rect.y]
            self.path = self.pathfinder.update_bfs(player_position, self.zombie_position)

        elif len(self.path) > 1:

            prevgridcord_x, prevgridcord_y = self.path[0][0], self.path[0][1]

            self.path.remove(self.path[0])
            nextgridcord_x, nextgridcord_y = self.path[0][0], self.path[0][1]  # first zombie point

            if prevgridcord_x == nextgridcord_x and prevgridcord_y == nextgridcord_x:
                self.speedx = 0
                self.speedy = 0
                self.path.remove((nextgridcord_x, nextgridcord_y))

            elif nextgridcord_x == prevgridcord_x and nextgridcord_y > prevgridcord_y:
                self.speedy = 1
                self.direction = 'D'
                self.speedx = 0

            elif nextgridcord_x == prevgridcord_x and nextgridcord_y < prevgridcord_y:
                self.speedy = -1
                self.speedx = -0
                self.direction = 'U'

            elif nextgridcord_y == prevgridcord_y and nextgridcord_x > prevgridcord_x:
                self.speedx = 1
                self.direction = 'R'
                self.speedy = 0

            elif nextgridcord_y == prevgridcord_y and nextgridcord_x < prevgridcord_x:
                self.speedx = -1
                self.speedy = 0
                self.direction = 'L'

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

    def drop(self):
        heart = Heart(self.rect.x, self.rect.centery)
        all_sprites.add(heart)
        heartsprite.add(heart)

    def posx(self):
        return self.rect.x

    def posy(self):
        return self.rect.y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        pullet = pygame.image.load('Bullet.png')
        self.image = pullet
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x


        if player.direction == "R":
            self.image = pullet
            self.speedy = 0
            self.speedx = 25
        if player.direction == "L":
            self.image = pygame.transform.rotate(pullet, 180)
            self.speedy = 0
            self.speedx = -25
        if player.direction == "U":
            self.image = pygame.transform.rotate(pullet, 90)
            self.speedy = -25
            self.speedx = 0
        if player.direction == "D":
            self.image = pygame.transform.rotate(pullet, 270)
            self.speedy = 25
            self.speedx = 0
        if player.direction == "UR":
            self.image = pygame.transform.rotate(pullet, 45)
            self.speedy = -25
            self.speedx = 25
        if player.direction == "UL":
            self.image = pygame.transform.rotate(pullet, 135)
            self.speedy = -25
            self.speedx = -25
        if player.direction == "DR":
            self.image = pygame.transform.rotate(pullet, 315)
            self.speedy = 25
            self.speedx = 25
        if player.direction == "DL":
            self.image = pygame.transform.rotate(pullet, 225)
            self.speedy = 25
            self.speedx = -25

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.kill()

        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.kill()


test = 0
game_over = True
running = True
Menu_Loop = True
while running:
    while Menu_Loop:
        screen.fill((60, 25, 100))
        SinglePlayer.draw(screen, (0, 100, 0))
        MultiPlayer.draw(screen, (0, 100, 0))
        HighScore.draw(screen, (0, 100, 0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # SinglePlayer Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SinglePlayer.isOver(pos):
                    Menu_Loop = False

            # SinglePlayer Button Hover color
            if event.type == pygame.MOUSEMOTION:
                if SinglePlayer.isOver(pos):
                    SinglePlayer.color = (0, 255, 0)
                else:
                    SinglePlayer.color = (100, 40, 0)

            # MultiPlayer Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MultiPlayer.isOver(pos):
                    Menu_Loop = False

            # MultiPlayer Button Hover color
            if event.type == pygame.MOUSEMOTION:
                if MultiPlayer.isOver(pos):
                    MultiPlayer.color = (0, 255, 0)
                else:
                    MultiPlayer.color = (100, 40, 0)

            # HighScore Button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HighScore.isOver(pos):
                    Menu_Loop = False

            # HighScore Button Hover color
            if event.type == pygame.MOUSEMOTION:
                if HighScore.isOver(pos):
                    HighScore.color = (0, 255, 0)
                else:
                    HighScore.color = (100, 40, 0)
        pygame.display.update()
        clock.tick(144)

    if game_over:
        score = 0
        game_over = False

        all_sprites = pygame.sprite.Group()
        player = Player()
        heartsprite = pygame.sprite.Group()
        all_sprites.add(player)
        zombies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()


    # creating 4 zombies every 7 seconds

    zombies_current_tick = pygame.time.get_ticks()  # getting the current time ticks
    if zombies_current_tick - zombies_last_tick >= spawn_interval:
        zombies_last_tick = zombies_current_tick

        for i in range(4):
            z = Zombie()
            all_sprites.add(z)
            zombies.add(z)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    screen.fill(WHITE)
    screen.blit(BackGround.image, BackGround.rect)
    hearts(5, 5, player.life)


    hits = pygame.sprite.groupcollide(zombies, bullets, False, True)

    for hit in hits:
        score += 10
        pygame.mixer.Sound.play(zombie_sound)
        zombies.update()
        hit.kill()
        a = random.randrange(0, 100)
        if a < 10:
            hit.drop()
            test = hit.get_position()

    if player.p == test:
        player.life += 1

    all_sprites.update()

    attacks = pygame.sprite.spritecollide(player, zombies, True)

    for attack in attacks:
        pygame.mixer.Sound.play(grunt_sound)

        if player.direction == 'U':
            player.speedy = 12
            player.speedx = 0

        if player.direction == 'D':
            player.speedy = -12
            player.speedx = 0

        if player.direction == 'R':
            player.speedx = -12
            player.speedy = 0

        if player.direction == 'L':
            player.speedx = 12
            player.speedy = 0

        player.rect.x += player.speedx
        player.rect.y += player.speedy

        player.life -= 1
        if player.life > 4:
            player.life = 4

        if player.life == 0:
            game_over = True

    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
