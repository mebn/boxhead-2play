import socket
import codes

SIZE = 256

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1" # ip of server.
        self.port = 8888 # port of server.

        self.pos = self.connect()

    # Connects to server, gets starting pos of both players and stores it in self.pos.
    def connect(self):
        try:
            self.client.connect((self.server, self.port))
            return self.client.recv(SIZE).decode()
        except:
            pass

    # Gets a formated position as ((x1,y1), (x2,y2))
    def get_starting_pos(self):
        pos = self.pos.split()
        p1_pos_tup = str_to_tup(pos[0])
        p2_pos_tup = str_to_tup(pos[1])
        
        return p1_pos_tup, p2_pos_tup # ((x1,y1), (x2,y2))

    # Takes player 1:s keystrokes as boollist. 
    # Updates position on server side.
    # Returns formatted position to be used when drawing on client side.
    def get_players_updated_pos(self, direction):
        try:
            self.client.send(codes.player_movement + direction)

            pos = self.client.recv(SIZE).decode()
            pos = pos.split()
            p1_pos_tup = str_to_tup(pos[0])
            p2_pos_tup = str_to_tup(pos[1])

            return p1_pos_tup, p2_pos_tup # ((x1,y1), (x2,y2))
        except:
            pass

    def get_enemies_pos(self):
        try:
            self.client.send(codes.enemies_position)
            all_enemies_pos = self.client.recv(SIZE).decode() # as "x1 y1;x2 y2;x3 y3;"
            all_enemies_pos = all_enemies_pos.split(";") # as ["x1 y1", "x2 y2", "x3 y3"]
            
            formatted_pos = []
            for pos in all_enemies_pos:
                x, y = pos.split()
                formatted_pos.append( (int(x), int(y)) )

            return formatted_pos # as [(x1, y1), (x2, y2), (x3, y3)]
        except:
            pass

    ##### private functions #####

    # Takes a string and format it into a int tuple.
    # Returns tuple.
    def str_to_tup(self, xy):
        xy = xy.split(",")
        return int(xy[0]), int(xy[1])