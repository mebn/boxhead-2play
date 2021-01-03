import socket
import threading
import dimensions
import codes

ADDRESS = "127.0.0.1"
PORT = 8888
SIZE = 128

# server setup stuff
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ADDRESS, PORT))
server.listen(2)
print("server started...")

# keep track of important stuff to be sent to clients.
class Entity:
    def __init__(self, type, pos, hp):
        self.type = type
        self.x = pos[0]
        self.y = pos[1]
        self.hp = hp

        self.pos = [self.x, self.y]

    # Used to turn a list of 2 elements into a comma seperated list.
    def get_pos_as_str(self):
        return str(self.pos[0]) + "," + str(self.pos[1])

    # Takes a list with bools and player (1 or 2).
    # Moves the player on server side.
    # Includes wall detection.
    def update_pos(self, direction):
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


players = [
    Entity("player", [0, 0], 100),
    Entity("player", [400, 400], 100)
]
enemies = [
    Entity("enemy", [100, 200], 100),
    Entity("enemy", [200, 100], 100)
]


# Returns "x1,y1;x2,y2" and makes sure every client is player 1.
def all_pos_to_str(player):
    player1_coords = players[0].get_pos_as_str()
    player2_coords = players[1].get_pos_as_str()

    if player == 0:
        return f"{player1_coords};{player2_coords}"
    else:
        return f"{player2_coords};{player1_coords}"


# A thread that starts when a new clients connects.
def client_thread(conn, player):
    # this only send one time, when connecting.
    reply = all_pos_to_str(player).encode()
    conn.send(reply) # sends starting pos.

    while True:
        try:
            data = conn.recv(SIZE)
            if not data:
                print("disconnected")
                break

            code = data[:2] # can be between 00 and 99 codes. (100 events)
            data = data[2:]

            # handle movement
            if code == codes.player_movement:
                players[player].update_pos(data)
                reply = all_pos_to_str(player).encode()
                conn.send(reply)

            if code == codes.enemies_position:
                pass

            if code == codes.player_hp:
                pass

            if code == codes.bullets_position:
                pass

        except:
            break

    print("lost connection")
    conn.close()


player_number = 0
while True:
    conn, addr = server.accept()
    print("new connection from", addr)

    thread = threading.Thread(target=client_thread, args=(conn, player_number))
    thread.start()
    print(threading.active_count())

    player_number += 1
    if player_number == 2: # not the best way...  
        player_number = 0