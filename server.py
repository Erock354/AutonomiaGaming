import json
import socket
import threading
from time import sleep

# Server setup
PORT = 5054
SERVER = "172.20.10.2"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

# Server binding
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Keep track of clients
clients = set()
clients_lock = threading.Lock()
HEADERSIZE = 10
players = []


# Handle client connections
def handle_client(conn, addr):
    # Message for every new connection
    print(f"[NEW CONNECTION]: {addr} Connected")
    # Initializing a new player object containing the address of the client
    joined_p = {"addr": addr[0], "x": None, "y": None}
    # Appending the player object to the list of players
    players.append(joined_p)
    try:
        # Setting the connection to true
        # While the connection is set to true, the client is still connected to the server
        connected = True
        while connected:
            data = conn.recv(1024 * 10)  # The amount of data in bytes that the server will receive
            data = data.decode("utf-8")  # The decoding format of the data

            # Handling possible data overflow by splitting the data into a list of strings
            data = data.split('}')
            data = [item for item in data if item != ""]
            data = [item + '}' for item in data]

            # Converting strings into a JSON objects and storing them into a list
            json_data = []
            for d in data:
                json_data.append(json.loads(d))

            # For each object in the list of JSON objects, check if the address of the object matches the address of the
            # player object. If it does, update the x and y coordinates of the player object
            for d in json_data:
                for player in players:
                    if player['addr'] == d['addr']:
                        player['x'] = d['x']
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
