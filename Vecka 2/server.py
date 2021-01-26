import socket
import threading
import dimensions
import codes
import random

ADDRESS = "127.0.0.1"
PORT = 8888
SIZE = 128

# keep track of important stuff to be sent to clients.
class Entity:
    def __init__(self, type, pos, hp):
        self.type = type
        self.x = pos[0]
        self.y = pos[1]
        self.hp = hp
        self.direction = 0
        self.pos = [self.x, self.y]

    # Used to turn a list of 2 elements into a comma seperated list.
    def get_pos_as_str(self):
        return str(self.pos[0]) + "," + str(self.pos[1])

    # Takes a list with bools and player (1 or 2).
    # Moves the player on server side.
    # Includes wall detection.
    def update_player_pos(self, direction):
        if self.type != "player":
            return

        movement_speed = 5

        # up
        if direction[0] and self.y >= 0:
            self.y -= movement_speed

        # down
        if direction[1] and self.y <= dimensions.HEIGHT - dimensions.PLAYER_HEIGHT:
            self.y += movement_speed

        # left
        if direction[2] and self.x >= 0:
            self.x -= movement_speed
        
        # right
        if direction[3] and self.x <= dimensions.WIDTH - dimensions.PLAYER_WIDTH:
            self.x += movement_speed
        
        self.pos = [self.x, self.y]


    # This is kinda buggy atm.
    def update_enemy_pos(self, players):
        if self.type != "enemy":
            return

        movement_speed = 1 # less then player m. speed

        # enemies move toward the closest player.
        # handle movement in x direction.
        if self.x <= players[0].x or self.x <= players[1].x:
            self.x += movement_speed
        else:
            self.x -= movement_speed
        
        # handle movement in y direction.
        if self.y <= players[0].y or self.y <= players[1].y:
            self.y += movement_speed
        else:
            self.y -= movement_speed

        self.pos = [self.x, self.y]


def generate_enemies(amount, players):
    enemies_list = []
    radius = 60

    for _ in range(amount):
        x = random.randint(0, dimensions.WIDTH)
        y = random.randint(0, dimensions.HEIGHT)

        # TODO: Spawn radius around players.
        while [x, y] == players[0].pos or [x, y] == players[1].pos:
            x = random.randint(0, dimensions.WIDTH)
            y = random.randint(0, dimensions.HEIGHT)

        enemies_list.append(Entity("enemy", [x, y], 100))

    return enemies_list


# Returns "x1,y1 x2,y2" and makes sure every client is player 1.
def players_pos_to_str(player, players):
    player1_coords = players[0].get_pos_as_str()
    player2_coords = players[1].get_pos_as_str()

    if player == 0:
        return f"{player1_coords} {player2_coords}"
    else:
        return f"{player2_coords} {player1_coords}"


# formattes hp of players to "100 100"
def players_hp_as_str(player, players):
    if player == 0:
        return f"{players[0].hp} {players[1].hp}"
    else:
        return f"{players[1].hp} {players[0].hp}"


# formattes enemies pos to a string like "x1 y1;x2 y2;x3 y3;"
def enemies_pos_to_str(enemies):
    pos_str = ""

    for enemy in enemies:
        pos_str += f"{enemy.x} {enemy.y};"

    return pos_str[:-1]


def players_direction_as_str(player, players, direction):
    players[player].direction = direction.decode()
    if player == 0:
        return f"{players[0].direction} {players[1].direction}"
    else:
        return f"{players[1].direction} {players[0].direction}"


# A thread that starts when a new clients connects.
def client_thread(conn, player, all_entites):
    while True:
        try:
            data = conn.recv(SIZE)
            if not data:
                print("disconnected")
                break

            code = data[:2] # can be between 00 and 99 codes. (100 events)
            data = data[2:]

            # handle player movement
            if code == codes.player_pos:
                if data:
                    players[player].update_player_pos(data)

                reply = players_pos_to_str(player, all_entites["players"]).encode()
                conn.send(reply)

            if code == codes.player_direction:

                reply = players_direction_as_str(player, all_entites["players"], data).encode()
                conn.send(reply)

            # handle enemies position
            if code == codes.enemies_position:
                for enemy in enemies:
                    enemy.update_enemy_pos(players)

                reply = enemies_pos_to_str(enemies).encode()
                conn.send(reply)

            if code == codes.player_hp:
                reply = players_hp_as_str(player, players).encode()
                conn.send(reply)

            if code == codes.bullets_position:
                pass

        except:
            break

    print("lost connection")
    conn.close()



if __name__ == "__main__":
    # server setup stuff
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ADDRESS, PORT))
    server.listen(2)
    print("server started...")

    players = [
        Entity("player", [0, 0], 100),
        Entity("player", [400, 400], 100)
    ]
    enemies = generate_enemies(5, players) # starting game with 5 enemies.

    # pass 1 big object as paramater.
    all_entites = {
        "players": players,
        "enemies": enemies
    }


    player_number = 0
    while True:
        conn, addr = server.accept()
        print("new connection from", addr)

        thread = threading.Thread(target=client_thread,
            args=(conn, player_number, all_entites))
        thread.start()
        print(threading.active_count())

        player_number += 1
        if player_number == 2: # not the best way...  
            player_number = 0