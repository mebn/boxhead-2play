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
players_pos = [[0, 0], [400, 400]]
player_hp = [100, 100]
enemies_pos = [[100, 200], [200, 100]] # ex. 2 enemies from the beginning.

# Takes a list with bools and player (1 or 2).
# Moves the player on server side.
# Includes wall detection.
def update_pos(direction, player):
    movement_speed = 5
    x = players_pos[player][0]
    y = players_pos[player][1]

    # up
    if direction[0] and y >= 0:
        y -= movement_speed

    # down
    if direction[1] and y <= dimensions.HEIGHT - dimensions.PLAYER_HEIGHT:
        y += movement_speed

    # left
    if direction[2] and x >= 0:
        x -= movement_speed
    
    # right
    if direction[3] and x <= dimensions.WIDTH - dimensions.PLAYER_WIDTH:
        x += movement_speed

    players_pos[player][0] = x
    players_pos[player][1] = y


# Used to turn a list of 2 elements into a comma seperated list.
# Used in all_pos_to_str()
def player_pos_to_str(player_pos):
    return str(player_pos[0]) + "," + str(player_pos[1])

# Returns "x1,y1;x2,y2" and makes sure every client is player 1.
def all_pos_to_str(player):
    player1_coords = player_pos_to_str(players_pos[0])
    player2_coords = player_pos_to_str(players_pos[1])

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
                update_pos(data, player)
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

    player_number += 1
    if player_number == 2: # not the best way...  
        player_number = 0