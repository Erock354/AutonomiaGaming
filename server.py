import pickle
import threading
import socket

PORT = 5050
SERVER = "192.168.134.161"
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
    players.append({"addr": addr[0], "x": None, "y": None})
    try:
        full_msg = b''
        connected = True
        while connected:
            msg = conn.recv(1024)
            if not msg:
                break

            full_msg += msg
            player_data = pickle.loads(full_msg[HEADERSIZE:])
            full_msg = b""

            for player in players:
                if player['addr'] == player_data['addr']:
                    player['x'] = player_data['x']
                    player['y'] = player_data['y']

            msg = pickle.dumps(players)
            msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg
            server.send(msg)

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

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()
