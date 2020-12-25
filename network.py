import socket

SIZE = 128

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1" # ip of server.
        self.port = 8888 # port of server.

        self.pos = self.connect()

    def connect(self):
        try:
            self.client.connect((self.server, self.port))
            return self.client.recv(SIZE).decode()
        except:
            pass

    def get_starting_pos(self):
        pos = self.pos.split(";")
        p1_pos_tup = get_pos(pos[0])
        p2_pos_tup = get_pos(pos[1])
        
        return p1_pos_tup, p2_pos_tup # ((x1,y1), (x2,y2))

    def get_players_updated_pos(self, direction):
        try:
            self.client.send(direction)

            pos = self.client.recv(SIZE).decode()
            pos = pos.split(";")
            p1_pos_tup = get_pos(pos[0])
            p2_pos_tup = get_pos(pos[1])

            return p1_pos_tup, p2_pos_tup # ((x1,y1), (x2,y2))
        except:
            pass

# private functions
def get_pos(xy):
    xy = xy.split(",")
    return int(xy[0]), int(xy[1])