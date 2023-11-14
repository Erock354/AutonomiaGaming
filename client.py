import json
import socket
import threading

from player import *

# Specifies port and server IP for the connection.
# FORMAT is used to define the byte encoding format.
# HEADERSIZE represents the size of headers in bytes.
# IP defines the IP address of the client.
PORT = 5054
SERVER = "192.168.9.161"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
HEADERSIZE = 10
IP = "192.168.9.38"

# List to hold the information of players currently in game
online_players = []
# List to hold addresses of players currently in game
addr_online_players = []


# Makes a connection to the defined server using the socket module
def connect(player):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates a TCP socket
    conn.connect(ADDR)  # Connects to the server

    # It starts two threads; one to send player data to the server, and another to receive data from the server
    thread1 = threading.Thread(target=send, args=(conn, player), daemon=True)
    thread2 = threading.Thread(target=receive, args=(conn, None), daemon=True)
    thread1.start()
    thread2.start()
    return


# Function to send data of the relevant player to the server
# Sends data anytime when the player's coordinates are changed
def send(client, player):
    player_before = Player(0, 0, 0, 0)
    while True:
        if player_before.rect.x != player.rect.x or player_before.rect.y != player.rect.y:
            player_data = {"addr": IP, "x": player.rect.x, "y": player.rect.y}
            data = json.dumps(player_data)
            try:
                client.send(bytes(data, encoding="utf-8"))
                player_before.rect.x = player.rect.x
                player_before.rect.y = player.rect.y
            except:
                pass


# Function to receive data - updates on all players from the server
# Handles network issues gracefully by failing silently
def receive(conn, sus):
    print("RECEIVING DATA")
    while True:
        data = conn.recv(1024)
        data = data.decode("utf-8")

        # Handles cases of data overflow
        divider = data.find(']')
        data = data[:divider + 1]
        data = json.loads(data)

        # Upon receiving data of a new player, create a new player instance and add to the list of online players
        for player in data:
            if player['addr'] not in addr_online_players:
                addr_online_players.append(player['addr'])  # Add the player's address to the list of online players
                new_player = Player(int(player['x']), int(player['y']), 64, 64)  # Create a new player instance
                new_player.addr = player['addr']  # Set the player's address
                online_players.append(new_player)  # Add the player to the list of online players

            # If received data of an already present player, then update the player's data
            for online_player in online_players:
                if player['addr'] == online_player.addr:
                    online_player.rect.x = player['x']
                    online_player.rect.y = player['y']
                    break
