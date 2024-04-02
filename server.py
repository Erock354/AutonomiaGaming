import json
import socket
import threading
from time import sleep


class Server:

    def __init__(self, server):
        # Server setup: Define the PORT and IP address for the server
        self.PORT = 63425

        self.ADDR = (server, self.PORT)
        self.FORMAT = "utf-8"

        # Server binding: Create a TCP socket and bind it to the defined address
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        # Keep track of clients: Maintain a threadsafe set of currently connected clients and an associated lock
        # Also set up a variable for the size of the message header, and a list for storing player data
        self.clients = set()
        self.clients_lock = threading.Lock()
        self.HEADERSIZE = 10
        self.players = []
        self.bullets = []
        self.lock = threading.Lock()

    # Handle client connections: Manage client and receive data
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION]: {addr} Connected")  # Message for every new connection

        # Initializing a new player object containing the client address
        joined_p = {"obj": "player", "addr": addr[0], "x": 64, "y": 720 - 64, "color": "white"}

        self.players.append(joined_p)  # Appending the player object to the list of players
        try:
            connected = True  # Setting the connection to true
            while connected:
                sleep(0.008)
                # While the connection is set to true, the server stays connected & receiving data from the client
                data = conn.recv(2048)  # The amount of data in bytes that the server will receive
                data = data.decode("utf-8")  # The decoding format of the data
                # Handling possible data overflow by splitting the data into a list of strings
                data = data.split('}')
                data = [item for item in data if item != ""]
                data = [item + '}' for item in data]
                # Converting strings into JSON objects and storing them into a list
                json_data = []
                for d in data:
                    json_data.append(json.loads(d))

                for d in json_data:
                    if d['obj'] == "player":
                        # For each JSON object, check the client's address and update player's coordinates if there's a
                        # match
                        for player in self.players:
                            if player['addr'] == d['addr']:
                                player['x'] = d['x']
                                player['y'] = d['y']
                                player['color'] = d['color']
                    if d['obj'] == "bullet":
                        self.send_bullet([json_data[0]])
        finally:
            # If the connection is lost, remove the player and connection from their respective tracking structures
            with self.clients_lock:
                self.players.remove(joined_p)
                self.clients.remove(conn)
            conn.close()  # Close the connection

    # Send data to clients: Handling the sending of current game state to connected clients
    def send_player_data(self, conn, addr):
        try:
            # While connections exist, consistently send updated player data to all clients
            while conn:
                data = json.dumps(self.players)
                conn.send(bytes(data, encoding="utf-8"))  # Encode the data and send it to the client
                sleep(0.008)  # Sleep for 8 milliseconds to avoid overloading the server

        finally:
            # If the connection is lost, remove it from the client tracking structure
            with self.clients_lock:
                self.clients.remove(conn)
            conn.close()  # Close the connection

    def send_bullet(self, bullet):
        for conn in self.clients:  # For every client connected
            data = json.dumps(bullet)
            conn.send(bytes(data, encoding="utf-8"))  # Send bullet data

    def start(self):
        print(f'[SERVER STARTED]! ({self.server.getsockname()})')  # Notify the server has started
        self.server.listen()  # Begin listening for incoming connections

        # Communication
        # Accept connections and start a new thread for each incoming client
        while True:
            conn, addr = self.server.accept()
            with self.clients_lock:
                self.clients.add(conn)
            # Start two threads - one for handling incoming data from the client, another for sending data to them
            thread1 = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread2 = threading.Thread(target=self.send_player_data, args=(conn, addr))
            thread1.start()
            thread2.start()
