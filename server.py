import json
import socket
import threading
from time import sleep

# Server setup: Define the PORT and IP address for the server
PORT = 5054
SERVER = "172.20.10.2"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

# Server binding: Create a TCP socket and bind it to the defined address
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Keep track of clients: Maintain a threadsafe set of currently connected clients and an associated lock
# Also set up a variable for the size of the message header, and a list for storing player data
clients = set()
clients_lock = threading.Lock()
HEADERSIZE = 10
players = []


# Handle client connections: Manage client and receive data
def handle_client(conn, addr):
    print(f"[NEW CONNECTION]: {addr} Connected")  # Message for every new connection
    joined_p = {"addr": addr[0], "x": None, "y": None}  # Initializing a new player object containing the client address
    players.append(joined_p)  # Appending the player object to the list of players
    try:
        connected = True  # Setting the connection to true
        while connected:
            # While the connection is set to true, the server stays connected & receiving data from the client
            data = conn.recv(1024 * 10)  # The amount of data in bytes that the server will receive
            data = data.decode("utf-8")  # The decoding format of the data
            # Handling possible data overflow by splitting the data into a list of strings
            data = data.split('}')
            data = [item for item in data if item != ""]
            data = [item + '}' for item in data]
            # Converting strings into JSON objects and storing them into a list
            json_data = []
            for d in data:
                json_data.append(json.loads(d))
            # For each JSON object, check the client's address and update player's coordinates if there's a match
            for d in json_data:
                for player in players:
                    if player['addr'] == d['addr']:
                        player['x'] = d['x']
                        player['y'] = d['y']
    finally:
        # If the connection is lost, remove the player and connection from their respective tracking structures
        with clients_lock:
            players.remove(joined_p)
            clients.remove(conn)
        conn.close()  # Close the connection


# Send data to clients: Handling the sending of current game state to connected clients
def send_data(conn, addr):
    try:
        # While connections exist, consistently send updated player data to all clients
        while conn:
            sleep(0.01)  # Sleep for 0.01 seconds to avoid overloading the server
            data = json.dumps(players)
            conn.send(bytes(data, encoding="utf-8"))  # Encode the data and send it to the client
    finally:
        # If the connection is lost, remove it from the client tracking structure
        with clients_lock:
            clients.remove(conn)
        conn.close()  # Close the connection


def start():
    print('[SERVER STARTED]!')  # Notify the server has started
    server.listen()  # Begin listening for incoming connections

    # Accept connections and start a new thread for each incoming client
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)

        # Start two threads - one for handling incoming data from the client, another for sending data to them
        thread1 = threading.Thread(target=handle_client, args=(conn, addr))
        thread2 = threading.Thread(target=send_data, args=(conn, addr))
        thread1.start()
        thread2.start()


# Start the server
start()
