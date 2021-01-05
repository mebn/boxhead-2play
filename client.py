import pygame
from player import Player
from network import Network
import dimensions

# Clears screen and redraws elements.
def redraw_window(win, player1, player2, enemies_pos):
    win.fill((255, 255, 255))
    player1.draw(win)
    player2.draw(win)

    for enemy_pos in enemies_pos:
        x, y = enemy_pos
        pygame.draw.rect(win, (0,0,255), (x, y, dimensions.ENEMY_WIDTH, dimensions.ENEMY_HEIGHT)) # should be a Enemy class or something

    pygame.display.update()


# Updates positions of players.
def update_players(network, player1, player2):
    # update position
    movement = network.get_players_pos(player1.move())
    if movement != None: # None -> player is not moving
        player1_pos, player2_pos = movement # every client is player 1.

        player1.update_pos(player1_pos)
        player2.update_pos(player2_pos)
    
    # update hp
    p1_hp, p2_hp = network.get_players_hp()
    player1.hp = p1_hp # ok, damage is calculated on server side.
    player2.hp = p2_hp # for graphics on client side.

    # update rect to be drawn
    player1.update_rect()
    player2.update_rect()


def main():
    win = pygame.display.set_mode((dimensions.WIDTH, dimensions.HEIGHT))
    pygame.display.set_caption("client")
    
    network = Network()
    p1_pos, p2_pos = network.get_players_pos()
    p1_hp, p2_hp = network.get_players_hp()

    player1 = Player(p1_pos, p1_hp, dimensions.PLAYER_WIDTH, dimensions.PLAYER_HEIGHT, (0, 255, 0))
    player2 = Player(p2_pos, p2_hp, dimensions.PLAYER_WIDTH, dimensions.PLAYER_HEIGHT, (255, 0, 0))
    
    clock = pygame.time.Clock()

    is_running = True
    while is_running:
        clock.tick(60)

        enemies_pos = network.get_enemies_pos()
        update_players(network, player1, player2)
        redraw_window(win, player1, player2, enemies_pos)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()



if __name__ == "__main__":
    main()
