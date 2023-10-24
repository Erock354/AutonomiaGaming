import json
import socket
import threading
from player import *
from time import *
from main import set_other_players

PORT = 5054
SERVER = "192.168.124.161"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
HEADERSIZE = 10
IP = socket.gethostbyname(socket.gethostname())

running = True


def connect(player):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(ADDR)

    thread1 = threading.Thread(target=send, args=(conn, player), daemon=True)
    thread2 = threading.Thread(target=receive, args=(conn, None), daemon=True)
    thread1.start()
    thread2.start()
    return


def send(client, player):
    player_before = Player(0, 0, 0, 0)
    while True:
        if player_before.rect.x != player.rect.x or player_before.rect.y != player.rect.y:
            sleep(1/1000)
            player_data = {"addr": IP, "x": player.rect.x, "y": player.rect.y}
            data = json.dumps(player_data)
            client.send(bytes(data, encoding="utf-8"))
            player_before.rect.x = player.rect.x
            player_before.rect.y = player.rect.y


def receive(conn, sus):
    while True:
        data = conn.recv(1024)
        data = data.decode("utf-8")
        data = json.loads(data)
        print(data, "\n")
        other_players = []
        for player in data:
            other_players.append(Player(player['x'], player['y'], 64, 64))
        set_other_players(other_players)
