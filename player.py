import pygame

class Player():
    def __init__(self, pos, width, height, color):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.color = color
        self.vel = 5

        self.rect = (self.x, self.y, self.width, self.height)

    # Draws on canvas.
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    # Sends keystrokes to server as a bool list.
    def move(self):
        keys = pygame.key.get_pressed()
        arrow_keys = [False, False, False, False] # up down left right

        if keys[pygame.K_UP]:
            arrow_keys[0] = True

        if keys[pygame.K_DOWN]:
            arrow_keys[1] = True

        if keys[pygame.K_LEFT]:
            arrow_keys[2] = True
        
        if keys[pygame.K_RIGHT]:
            arrow_keys[3] = True

        return bytes(arrow_keys)

    # Update player rcet to be drawn on canvas.
    def update_draw(self):
        self.rect = (self.x, self.y, self.width, self.height)

    # Updates position of player after getting new coords from server.
    def update_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]