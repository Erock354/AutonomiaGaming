import json
import socket
import threading
from time import sleep
from player import Player


class Client:

    def __init__(self, ip, player):
        # Specifies port and server IP for the connection.
        # FORMAT is used to define the byte encoding format.
        # HEADERSIZE represents the size of headers in bytes.
        # IP defines the IP address of the client.
        self.PORT = 63425
        # getting the IP address using socket.gethostbyname() method
        self.IP = ip

        self.FORMAT = "utf-8"
        self.HEADERSIZE = 10

        # List to hold the information of players currently in game
        self.online_players = []
        # List to hold addresses of players currently in game
        self.addr_online_players = []

        # Binding socket and establish connection
        ADDR = (ip, self.PORT)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a TCP socket
        self.conn.connect(ADDR)  # Connects to the server

        # Reference to the player
        self.player = player

    # Makes a connection to the defined server using the socket module
    def connect(self, player, ip):
        # It starts two threads; one to send player data to the server, and another to receive data from the server
        thread1 = threading.Thread(target=self.send, daemon=True)
        thread2 = threading.Thread(target=self.receive, daemon=True)
        thread1.start()
        thread2.start()

    # Function to send data of the relevant player to the server
    # Sends data anytime when the player's coordinates are changed
    def send(self):
        player_before = Player(0, 0, 0, 0, "white")
        while True:
            if player_before.rect.x != self.player.rect.x or player_before.rect.y != self.player.rect.y:
                player_data = {"obj": "player", "addr": self.IP, "x": self.player.rect.x, "y": self.player.rect.y, "color": self.player.color}
                data = json.dumps(player_data)
                try:
                    self.conn.send(bytes(data, encoding="utf-8"))
                    player_before.rect.x = self.player.rect.x
                    player_before.rect.y = self.player.rect.y
                except:
                    pass
            sleep(0.008)

    def send_bullet(self, bullet):
        bullet_data = {"obj": "bullet", "x": bullet.x, "y": bullet.y, "angle": bullet.angle, "dmg": bullet.dmg}
        data = json.dumps(bullet_data)
        try:
            self.conn.send(bytes(data, encoding="utf-8"))
        except:
            pass

    # Function to receive data - updates on all players from the server
    # Handles network issues gracefully by failing silently
    def receive(self):
        print("RECEIVING DATA")
        while True:
            data = self.conn.recv(1024)
            data = data.decode("utf-8")

            # Handles cases of data overflow
            divider = data.find(']')
            data = data[:divider + 1]
            data = json.loads(data)

            # Upon receiving data of a new player, create a new player instance and add to the list of online players
            for player in data:
                if player['addr'] not in self.addr_online_players:
                    self.addr_online_players.append(player['addr'])  # Add the player's address to the list of online
                    # players
                    new_player = Player(int(player['x']), int(player['y']), 64, 64, player['color'])  # Create a new
                    # player instance
                    new_player.addr = player['addr']  # Set the player's address
                    self.online_players.append(new_player)  # Add the player to the list of online players

                # If received data of an already present player, then update the player's data
                for online_player in self.online_players:
                    if player['addr'] == online_player.addr:
                        online_player.rect.x = player['x']
                        online_player.rect.y = player['y']

            sleep(0.008)