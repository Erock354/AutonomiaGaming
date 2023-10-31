import json
import socket
import threading
from player import *

PORT = 5054
SERVER = "192.168.10.65"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
HEADERSIZE = 10
IP = "192.168.10.65"

running = True
online_players = []
addr_online_players = []


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
            player_data = {"addr": IP, "x": player.rect.x, "y": player.rect.y}
            data = json.dumps(player_data)
            client.send(bytes(data, encoding="utf-8"))
            player_before.rect.x = player.rect.x
            player_before.rect.y = player.rect.y


def receive(conn, sus):
    print("RECEIVING DATA")
    while True:
        data = conn.recv(1024)
        data = data.decode("utf-8")

        # Contrast overload of data
        divider = data.find(']')
        data = data[:divider + 1]
        data = json.loads(data)

        for player in data:

            if player['addr'] not in addr_online_players:
                addr_online_players.append(player['addr'])
                new_player = Player(int(player['x']), int(player['y']), 64, 64)
                new_player.addr = player['addr']
                online_players.append(new_player)

            for online_player in online_players:
                if player['addr'] == online_player.addr:
                    online_player.rect.x = player['x']
                    online_player.rect.y = player['y']
                    break
