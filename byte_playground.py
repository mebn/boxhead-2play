# test send bytes

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "127.0.0.1"
port = 8888

client.connect((server, port))

a = [False, True]
b = bytearray(a)
client.send(b)

data = client.recv(128)
print(data)
