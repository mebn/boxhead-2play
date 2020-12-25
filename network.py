import socket

SIZE = 128

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 8888

        self.pos = self.connect()

    def get_pos(self):
        pos = self.pos.split(";")
        return pos[0], pos[1]

    def connect(self):
        try:
            self.client.connect((self.server, self.port))
            return self.client.recv(SIZE).decode()
        except:
            pass

    def get_players_updated_pos(self, direction):
        try:
            self.client.send(direction)

            xy = self.client.recv(SIZE).decode()
            xy = xy.split(";")
            return xy[0], xy[1] # ("x1,y1", "x2,y2")
        except:
            pass