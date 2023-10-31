import json
import threading
import socket
from time import sleep

PORT = 5054
SERVER = "172.20.10.2"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()
HEADERSIZE = 10
players = []


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")
    joined_p = {"addr": addr[0], "x": None, "y": None}
    players.append(joined_p)
    try:
        connected = True
        while connected:
            data = conn.recv(1024*10)
            data = data.decode("utf-8")
            data = data.split('}')
            data = [item for item in data if item != ""]
            data = [item + '}' for item in data]
            json_data = []
            for d in data:
                json_data.append(json.loads(d))

            for d in json_data:
                for player in players:
                    if player['addr'] == d['addr']:
                        player['x'] = d['x']
                        player['y'] = d['y']

    finally:
        with clients_lock:
            players.remove(joined_p)
            clients.remove(conn)
        conn.close()


def send_data(conn, addr):
    try:
        while conn:
            sleep(0.01)
            data = json.dumps(players)
            conn.send(bytes(data, encoding="utf-8"))
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()


def start():
    print('[SERVER STARTED]!')
    server.listen()

    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)

        thread1 = threading.Thread(target=handle_client, args=(conn, addr))
        thread2 = threading.Thread(target=send_data, args=(conn, addr))
        thread1.start()
        thread2.start()


start()
