import pygame
import sys
from game import is_board_full, make_move, check_winner
from interface import draw_board, selectfirst, selectlevel, selectplayer
from level import level1, level2, level3, level4

################ PHASE 2 #################
from interface import inputname, gameroom
from client import Client
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# 파이게임 초기화
pygame.init()

# 화면 크기 설정
allsize=1000
size = 600
cell_size = size // 3
screen = pygame.display.set_mode((allsize, size))
pygame.display.set_caption('Tic Tac Toe')

# 게임 보드 초기화
board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'O'
first='O'
game_over = False
show_score = True  # 점수판 표시 여부를 결정하는 변수

################ PHASE 2 #################
your_turn = False
goto_net = False # Online Mode
player_name = ''
client_instance = None

# 글꼴 설정
font = pygame.font.Font(None, 200)
small_font = pygame.font.Font(None, 40)

def main_menu():
    global player, board, game_over, your_turn, goto_net
    your_turn = False
    goto_net = False
    # 1 player or 2 players
    player = 0
    while player == 0:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    player = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    player = 2
                ################ PHASE 2 #################
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    player = 3
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        selectplayer()
        pygame.display.flip()

	################ PHASE 2 #################
    if player == 1:
        selectlevel_menu()
    elif player == 3:
        inputname_menu()

    # Board initialization
    board = [['' for _ in range(3)] for _ in range(3)]

    game_over = False

def selectlevel_menu():
    global level

    # If 1 player is chosen, which level is AI?
    level = 0
    while level == 0:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    level = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    level = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    level = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    level = 4
                elif event.key == pygame.K_q:                    
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        selectlevel()
        pygame.display.flip()

    selectfirst_menu()

def selectfirst_menu():    
    global user_choice, first, current_player

    # If 1 player is chosen, who move first, AI or user?
    user_choice = ''
    while user_choice not in ['U', 'C']:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    user_choice = 'U'
                elif event.key == pygame.K_c:
                    user_choice = 'C'
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        selectfirst()
        pygame.display.flip()

    # If computer move first its mark is X    
    if user_choice == 'C':
        first = 'X'
        current_player = 'X'
    else:
        first = 'O'
        current_player = 'O'
        
##########################################
################ PHASE 2 #################
##########################################
def inputname_menu():
    global goto_net, player_name

    # If online 2 player is chosen, player name is set
    goto_net = False
    while not goto_net:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    goto_net = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        player_name = inputname(player_name)
        pygame.display.flip()

    gameroom_menu()

def gameroom_menu():    
    global client_instance, player_name

    # Game waiting room
    # Create a client instance and connect to the server
    client_instance = Client(name=player_name)
    inc = 0
    while True and inc < 3:    # wait for another player in game room
        if client_instance.current_player is None:
            continue    # Wait until receiving server message

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b: # Go to Main Menu
                    if client_instance.current_player == 'W':   # If in waiting
                        shutdown_client(client_instance)
                        main_menu()
                        return
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if client_instance.current_player in ('W','O'): # Current player is first
            gameroom(player_name, client_instance.enemy_name)
        else:                                           # Current player is second
            gameroom(client_instance.enemy_name, player_name)
        pygame.display.flip()

        if client_instance.current_player != 'W':
            time.sleep(1)   # Wait a second to show the room for a moment
            inc += 1    # Iterate one more time to show the room

# Function to shut down the client
def shutdown_client(client):
    print("Shutting down client...")
    client.shutdown()
##########################################
################ PHASE 2 #################
##########################################

def reset_game():
    global board, current_player, game_over
    board = [['' for _ in range(3)] for _ in range(3)]
    if user_choice == 'C':
        current_player = 'X'
    else:
        current_player = 'O'
    game_over = False

main_menu()

# 메인 루프
while True:
    if(player==1):

        # 컴퓨터가 수를 둘 차례
        if not game_over and current_player == 'X':
            available_positions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
            if(level==1):
                row, col = level1(board)
            elif(level==2):
                row, col = level2(board)
            elif(level==3):
                row, col = level3(first,board,current_player)
            elif(level==4):
                row, col = level4(first,board,current_player)
            board[row][col] = current_player
            winner = check_winner(board)
            if winner:
                game_over = True
            elif is_board_full(board):
                game_over = True
            else:
                current_player = 'X' if current_player == 'O' else 'O'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == 'O':
                x, y = event.pos
                col = x // cell_size
                row = y // cell_size
                if(col>=3):
                    continue
                if board[row][col] == '':
                    board[row][col] = current_player
                    winner = check_winner(board)
                    if winner:
                        game_over = True
                    elif is_board_full(board):
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    show_score = not show_score
                if event.key == pygame.K_c and not game_over:
                    row, col = level4(first,board,current_player)
                    board[row][col] = current_player
                    winner = check_winner(board)
                    if winner:
                        game_over = True
                    elif is_board_full(board):
                        game_over = True
                    else:
                        current_player = 'X' if current_player == 'O' else 'O'
                if event.key == pygame.K_b:
                    main_menu()

    elif player == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                col = x // cell_size
                row = y // cell_size
                if(col>=3):
                    continue
                if board[row][col] == '':
                    board[row][col] = current_player
                    winner = check_winner(board)
                    if winner:
                        game_over = True
                    elif is_board_full(board):
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    show_score = not show_score
                if event.key == pygame.K_c and not game_over:                       
                    row, col = level4(first,board,current_player)
                    board[row][col] = current_player
                    winner = check_winner(board)
                    if winner:
                        game_over = True
                    elif is_board_full(board):
                        game_over = True
                    else:
                        current_player = 'X' if current_player == 'O' else 'O'
                if event.key == pygame.K_b:
                    main_menu()

    ##########################################
    ################ PHASE 2 #################
    ##########################################
    elif player == 3:
        # Change global var
        if client_instance.board is not None:
            board = client_instance.board
            winner = check_winner(board)
            if winner:
                game_over = True
            elif is_board_full(board):
                game_over = True

        your_turn = (client_instance.current_player == client_instance.current_turn)

        if client_instance.enemy_drop: # Enemy exits
            game_over = True
            draw_board(board,show_score,first,False,False)
            text = small_font.render('The other player has disconnected. Ending the game...', True, BLACK)
            screen.blit(text, (20, size // 2 - 20))
            pygame.display.flip()
            time.sleep(2)
            main_menu()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                shutdown_client(client_instance)
                pygame.quit()
                sys.exit()

            # Game move by mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                print(f"current_player : {client_instance.current_player}, current_turn : {client_instance.current_turn}")
                # Only allow move if it's the player's turn
                if client_instance.current_player == client_instance.current_turn:
                    x, y = event.pos
                    col = x // cell_size
                    row = y // cell_size
                    if(col>=3):
                        continue
                    if board[row][col] == '':
                        board[row][col] = client_instance.current_player                        
                        client_instance.board = board
                        client_instance.send_move(board, client_instance.current_player)

            # Control Keys input
            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_r:
                #     reset_game()
                if event.key == pygame.K_q:
                    shutdown_client(client_instance)
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    show_score = not show_score
                if event.key == pygame.K_c and not game_over:
                    row, col = level4(first,board,client_instance.current_player)
                    board[row][col] = client_instance.current_player
                    winner = check_winner(board)
                    if winner:
                        game_over = True
                    elif is_board_full(board):
                        game_over = True
                    # else:
                    #     current_player = 'X' if current_player == 'O' else 'O'                        
                    client_instance.send_move(board, client_instance.current_player)
                if event.key == pygame.K_b:
                    shutdown_client(client_instance)
                    main_menu()
    ##########################################
    ################ PHASE 2 #################
    ##########################################
    
    draw_board(board,show_score,first,False if game_over else goto_net,your_turn)
    if game_over:
        ################ PHASE 2 #################
        if player == 3:   # No restart if online
            str_restart = ''
        else:
            str_restart = 'Press R to restart, '

        winner = check_winner(board)
        if winner:
            text = small_font.render(f'{winner} wins! {str_restart}Press Q to exit', True, BLACK)
        else:
            text = small_font.render(f'Draw! {str_restart}Press Q to exit', True, BLACK)
        screen.blit(text, (20, size // 2 - 20))

    pygame.display.flip()
