##########################################
################ PHASE 2 #################
##########################################
from interface import draw_board
import socket
import threading

class Client:
    def __init__(self, name, host='localhost', port=5555):
        self.running = True
        self.current_player = None
        self.current_turn = 'O'
        self.board = None
        self.game_id = None
        self.enemy_name = None
        self.enemy_drop = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        # Send my name
        self.client.send(name.encode('utf-8'))

        threading.Thread(target=self.receive_messages).start()

    # Function to receive messages from the server
    def receive_messages(self):
        buffer = ""
        while self.running:
            try:
                buffer = self.client.recv(1024).decode('utf-8')
                print(f"Got message {buffer}")
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    if self.current_player is None or self.current_player == 'W':
                        self.game_id, self.current_player, self.enemy_name = eval(message)                    
                        if self.enemy_name is None or self.enemy_name == '':
                            print(f"Waiting for another player in Room {self.game_id}...")
                        else:
                            print(f"You are Player {self.current_player} in Game {self.game_id}. Your enemy is {self.enemy_name}")
                    elif message == "END":
                        print("The other player has disconnected. Ending the game.")
                        self.enemy_drop = True
                        self.running = False
                        self.shutdown()
                    else:
                        # Receive the updated board state from the server
                        self.board, self.current_turn = eval(message)
            except:
                self.running = False
                break

    def send_move(self, board, current_player):
        try:
            self.client.send(str((self.game_id, current_player, board)).encode('utf-8'))
        except:
            self.running = False

    def shutdown(self):
        self.running = False
        self.client.close()
##########################################
################ PHASE 2 #################
##########################################