import socket
import pickle

PORT = 5050
SERVER = "192.168.134.161"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
HEADERSIZE = 10
IP = socket.gethostbyname(socket.gethostname())


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client


def send(client, player):
    player_coordinates = {"addr": IP, "x": player.rect.x, "y": player.rect.y}
    msg = pickle.dumps(player_coordinates)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
    print(msg)
    client.send(msg)


def receive(connection):
    msg = connection.recv(1024).decode(FORMAT)
    return msg
