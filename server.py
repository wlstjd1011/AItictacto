##########################################
################ PHASE 2 #################
##########################################
import socket
import threading
import signal
import sys

# Create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the server on port 5555
server.bind(('localhost', 5555))
# Listen for incoming connections
server.listen()
print("Server started, waiting for connections...")

# Data structures of clients, rooms, and games
clients = []
waiting_rooms = []
games = {}

# Function to broadcast a message to both players in a game
def broadcast(game_id, message):
    game = games[game_id]
    # print(f"Current games: {games}")
    player1, player2 = game[0], game[1]
    print(f"Broadcast message: {message}")
    try:
        player1.send((message + "\n").encode('utf-8'))
        player2.send((message + "\n").encode('utf-8'))
    except:
        pass

def handle_client(client, room_id):
    global waiting_rooms, games
    # room_id = None
    # client_name = None

    try:
        while True:
            message = client.recv(1024).decode('utf-8')
            print(f"Got message: {message}")
            if not message:
                break

            # Handle game moves
            game_id, play_turn, board = eval(message)
            game = games[game_id]  
            if game[3] == play_turn:
                game_temp = (game[0],game[1],board,'X' if game[3] == 'O' else 'O')
                games[game_id] = game_temp
                broadcast(game_id, str((game_temp[2], game_temp[3])))

    except Exception as e:
        print(f"Client error: {e}")

    finally:
        clients.remove(client)
        for room in waiting_rooms:
            if room[0] == room_id:
                print(f"Remove #{room_id} from waiting room")
                waiting_rooms.remove(room)
                break
        if room_id in games:
            enemy = games[room_id][1] if games[room_id][0] == client else games[room_id][0]
            try:
                enemy.send("END\n".encode('utf-8'))
            except:
                pass
            del games[room_id]
        client.close()
        print("Client disconnected")

# Function to start a new game with two players
def start_new_game(client1, client2, room_id, name1, name2):
    # Initialize the game board
    board = [['' for _ in range(3)] for _ in range(3)]
    games[room_id] = (client1, client2, board, 'O')  # (player1, player2, board, turn)

    # notify the other player's name
    try:
        client1.send((str((room_id, 'O', name2)) + "\n").encode('utf-8'))
        client2.send((str((room_id, 'X', name1)) + "\n").encode('utf-8'))
    except:
        pass

    # go game
    broadcast(room_id, str((board, 'O')))
    print(f"Game started in room {room_id} between {name1} and {name2}")

# Function to handle server shutdown
def signal_handler(sig, frame):
    print("Server is shutting down...")
    for client in clients:
        client.close()
    server.close()
    sys.exit(0)

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Main loop to accept new client connections and pair them for games
room_counter = 1
while True:
    client, address = server.accept()
    clients.append(client)
    
    client_name = client.recv(1024).decode('utf-8')
    print(f"New connection from {address} with name {client_name}")

    if waiting_rooms:
        print(f"Waiting rooms {waiting_rooms}")
        # Pair with a waiting player
        room_id, waiting_client, waiting_name = waiting_rooms.pop(0)
        print(f"Enter the room #{room_id}")
        start_new_game(waiting_client, client, room_id, waiting_name, client_name)
        threading.Thread(target=handle_client, args=(client, room_id)).start()
    else:
        # Create a new room and wait for another player
        room_id = room_counter
        print(f"Create a new room #{room_id}")
        room_counter += 1
        waiting_rooms.append((room_id, client, client_name))
        client.send((str((room_id, 'W', "")) + "\n").encode('utf-8'))
        threading.Thread(target=handle_client, args=(client,room_id)).start()
##########################################
################ PHASE 2 #################
##########################################