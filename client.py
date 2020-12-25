import pygame
from player import Player
from network import Network

w = h = 500
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("client")

client_number = 0

def redraw_window(win, player1, player2):
    win.fill((255, 255, 255))
    player1.draw(win)
    player2.draw(win)

    pygame.display.update()


def main():
    network = Network()
    player1_pos, player2_pos = network.get_starting_pos()

    player1 = Player(player1_pos, 100, 100, (0, 255, 0))
    player2 = Player(player2_pos, 100, 100, (255, 0, 0))
    
    clock = pygame.time.Clock()

    is_running = True
    while is_running:
        clock.tick(60)

        response = network.get_players_updated_pos(player1.move())
        if response != None:
            player1_pos, player2_pos = response # every client is player 1.

            player1.update_pos(player1_pos)
            player2.update_pos(player2_pos)
        
        player1.update_draw()
        player2.update_draw()

        redraw_window(win, player1, player2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()



if __name__ == "__main__":
    main()
