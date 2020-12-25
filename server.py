import socket
import threading

ADDRESS = "127.0.0.1"
PORT = 8888
SIZE = 128

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ADDRESS, PORT))
server.listen(2)
print("server started...")

players_pos = [(0, 0), (400, 400)]

def update_pos(direction, player):
    movement_speed = 5

    # left
    if direction[2]:
        x, y = players_pos[player]
        x -= movement_speed
        players_pos[player] = (x, y)
    
    # right
    if direction[3]:
        x, y = players_pos[player]
        x += movement_speed
        players_pos[player] = (x, y)

    # up
    if direction[0]:
        x, y = players_pos[player]
        y -= movement_speed
        players_pos[player] = (x, y)

    # down
    if direction[1]:
        x, y = players_pos[player]
        y += movement_speed
        players_pos[player] = (x, y)


def tup_to_str(tup):
    return str(tup[0]) + "," + str(tup[1])


def pos_to_str(player):
    player1_coords = tup_to_str(players_pos[0])
    player2_coords = tup_to_str(players_pos[1])

    if player == 0:
        return f"{player1_coords};{player2_coords}"
    else:
        return f"{player2_coords};{player1_coords}"


def client_thread(conn, player):
    # need to call pos_to_string before sending data to client

    reply = pos_to_str(player).encode()
    conn.send(reply)

    while True:
        try:
            data = conn.recv(SIZE)

            if not data:
                print("disconnected")
                break

            update_pos(data, player)
            reply = pos_to_str(player).encode()
            conn.send(reply)
        except:
            break

    print("lost connection")
    conn.close()


player_number = 0
while True:
    conn, addr = server.accept()
    print("new connection from", addr)

    thread = threading. Thread(target=client_thread, args=(conn, player_number))
    thread.start()

    player_number += 1
    if player_number == 2: # not the best way...  
        player_number = 0