import socket
import codes

SIZE = 256

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1" # ip of server.
        self.port = 8888 # port of server.

        self.client.connect((self.server, self.port))


    ##### PLAYER METHODS #####

    # (Optional) Takes player 1:s keystrokes as boollist. 
    # Updates position on server side if argument passed.
    # Returns formatted position to be used when drawing on client side.
    # Gets a formated position as ((x1,y1), (x2,y2))
    def get_players_pos(self, directions=b""):
        try:      
            self.client.send(codes.player_pos + directions)

            pos = self.client.recv(SIZE).decode()
            pos = pos.split()
            p1_pos_tup = self.__str_to_tup(pos[0])
            p2_pos_tup = self.__str_to_tup(pos[1])
            
            return p1_pos_tup, p2_pos_tup # ((x1,y1), (x2,y2))
        except:
            pass

    def get_player_direction(self,direction):
        try:
            direction =str(direction)
            direction = direction.encode()
            self.client.send(codes.player_direction + direction)
            direction = self.client.recv(SIZE).decode()
            p1_direction, p2_direction = direction.split()
            return int(p1_direction), int(p2_direction)

        except:
            pass

    def get_players_hp(self):
        try:
            self.client.send(codes.player_hp)
            hp = self.client.recv(SIZE).decode()
            p1_hp, p2_hp = hp.split()

            return int(p1_hp), int(p2_hp)
        except:
            pass

    ##### ENEMY METHODS #####

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

    ##### PRIVATE METHODS #####

    # Takes a string and format it into a int tuple.
    # Returns tuple.
    def __str_to_tup(self, tup):
        tup = tup.split(",")
        return int(tup[0]), int(tup[1])