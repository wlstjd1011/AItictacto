import pygame
import sys
from game import is_board_full, make_move, check_winner
from interface import draw_board, selectfirst, selectlevel, selectplayer
from level import level1, level2, level3, level4

################ PHASE 2 #################
from interface import inputname, gameroom, gamelist, draw_replay
from client import Client
from database import Database
import time
from datetime import datetime
import copy

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
game_save = False
boards = []
your_turn = False
goto_net = False # Online Mode
player_name = ''
client_instance = None
game_type = ''
replay_moves = []
move_cnt = 0 
start_time = time.time()
move_idx = 0
enemy_saved = False
you_saved = False

# 글꼴 설정
font = pygame.font.Font(None, 200)
small_font = pygame.font.Font(None, 40)

################ PHASE 2 #################
db = Database()

################ PHASE 2 #################
def close_game():
    global db

    db.close()
    pygame.quit()
    sys.exit()

def main_menu():
    global player, game_type, board, boards, game_over, game_save, your_turn, goto_net
    your_turn = False
    goto_net = False
    # 1 player or 2 players
    player = 0
    while player == 0:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    player = 1
                    game_type = 'vs computer'
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    player = 2
                    game_type = '2Players'
                ################ PHASE 2 #################
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    player = 3
                    game_type = 'Online 2Players'
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    player = 4
                elif event.key == pygame.K_q:
                    close_game()
            elif event.type == pygame.QUIT:
                close_game()
        selectplayer()
        pygame.display.flip()

    ################ PHASE 2 #################
    if player == 1:
        selectlevel_menu()
    elif player == 3:
        inputname_menu()
    elif player == 4:
        gamelist_menu()

    # Board initialization
    board = [['' for _ in range(3)] for _ in range(3)]

    ################ PHASE 2 #################
    boards = []
    boards.append(copy.deepcopy(board))

    game_over = False
    game_save = False

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
                    close_game()
            elif event.type == pygame.QUIT:
                close_game()
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
                    close_game()
            elif event.type == pygame.QUIT:
                close_game()
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
                close_game()
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
                close_game()

        if client_instance.current_player in ('W','O'): # Current player is first
            gameroom(player_name, client_instance.enemy_name)
        else:                                           # Current player is second
            gameroom(client_instance.enemy_name, player_name)
        pygame.display.flip()

        if client_instance.current_player != 'W':
            time.sleep(1)   # Wait a second to show the room for a moment
            inc += 1    # Iterate one more time to show the room

def gamelist_menu():
    # Recorded games
    global db, replay_moves, move_cnt, start_time, move_idx
    PAGE_SIZE = 5
    pg_num = 1
    game_count = db.get_game_count()
    max_pg = game_count // PAGE_SIZE + 1
    games = db.list_plays(pg_num,PAGE_SIZE)
    exit_loop = False
    while not exit_loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    replay_moves = db.get_plays(games[0][0])
                    exit_loop = True
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:                    
                    replay_moves = db.get_plays(games[1][0])
                    exit_loop = True
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    replay_moves = db.get_plays(games[2][0])
                    exit_loop = True
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    replay_moves = db.get_plays(games[3][0])
                    exit_loop = True
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    replay_moves = db.get_plays(games[4][0])
                    exit_loop = True
                elif event.key == pygame.K_n:
                    if pg_num < max_pg:    # If page is beyond max page, stop going to next
                        pg_num += 1
                        games = db.list_plays(pg_num,PAGE_SIZE)
                    else:
                        games = []
                elif event.key == pygame.K_p:
                    # print(f"pg_num : {pg_num}")
                    if pg_num > 1:    # If page is beyond min page, stop going to prev
                        pg_num -= 1
                        games = db.list_plays(pg_num,PAGE_SIZE)
                    else:
                        games = []
                elif event.key == pygame.K_b:   # go to Main Menu
                    main_menu()
                    return
            elif event.type == pygame.QUIT:
                close_game()
        gamelist(games)
        pygame.display.flip()

        move_cnt = len(replay_moves)
        start_time = time.time()
        move_idx = 0

# Function to shut down the client
def shutdown_client(client):
    print("Shutting down client...")
    client.shutdown()

# Function to save game moves
def save_game_play(game_type, boards):
    global db
    game_id = db.get_next_game_id()
    game_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    temp_bd = None
    for i, bd in enumerate(boards):
        # print(f"{bd} // {temp_bd}")
        if i > 0:            
            if bd == temp_bd:
                continue    # If duplicate then skip

        db.save_play(game_id, game_type, bd, game_datetime)
        temp_bd = bd
##########################################
################ PHASE 2 #################
##########################################

def reset_game():
    global board, boards, current_player, game_over
    global game_save
    board = [['' for _ in range(3)] for _ in range(3)]

    ################ PHASE 2 #################
    boards = []
    boards.append(copy.deepcopy(board))

    if user_choice == 'C':
        current_player = 'X'
    else:
        current_player = 'O'
    game_over = False
    game_save = False

        
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
            ################ PHASE 2 #################
            boards.append(copy.deepcopy(board))

            winner = check_winner(board)
            if winner:
                game_over = True
            elif is_board_full(board):
                game_over = True
            else:
                current_player = 'X' if current_player == 'O' else 'O'
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == 'O':
                x, y = event.pos
                col = x // cell_size
                row = y // cell_size
                if(col>=3):
                    continue
                if board[row][col] == '':
                    board[row][col] = current_player
                    ################ PHASE 2 #################
                    boards.append(copy.deepcopy(board))

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
                    close_game()
                if event.key == pygame.K_s:
                    show_score = not show_score
                if event.key == pygame.K_c and not game_over:
                    row, col = level4(first,board,current_player)
                    board[row][col] = current_player
                    ################ PHASE 2 #################
                    boards.append(copy.deepcopy(board))

                    winner = check_winner(board)
                    if winner:
                        game_over = True
                    elif is_board_full(board):
                        game_over = True
                    else:
                        current_player = 'X' if current_player == 'O' else 'O'
                if event.key == pygame.K_b:
                    # set_game()
                    main_menu()

    elif player == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                col = x // cell_size
                row = y // cell_size
                if(col>=3):
                    continue
                if board[row][col] == '':
                    board[row][col] = current_player
                    ################ PHASE 2 #################
                    boards.append(copy.deepcopy(board))

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
                    close_game()
                if event.key == pygame.K_s:
                    show_score = not show_score
                if event.key == pygame.K_c and not game_over:
                    row, col = level4(first,board,current_player)
                    board[row][col] = current_player
                    ################ PHASE 2 #################
                    boards.append(copy.deepcopy(board))

                    winner = check_winner(board)
                    if winner:
                        game_over = True
                    elif is_board_full(board):
                        game_over = True
                    else:
                        current_player = 'X' if current_player == 'O' else 'O'
                if event.key == pygame.K_b:
                    # set_game()
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
        if your_turn:
            if not you_saved: # Save only once per user's turn
                boards.append(copy.deepcopy(board))
                you_saved = True
            enemy_saved = False
        else:
            if not enemy_saved: # Save only once per enemy turn
                boards.append(copy.deepcopy(board))
                enemy_saved = True
            you_saved = False

        if client_instance.enemy_drop: # Enemy exits
            game_over = True
            draw_board(board,show_score,first,False,False)  # refresh screen
            text = small_font.render('The other player has disconnected. Ending the game...', True, BLACK)
            screen.blit(text, (20, size // 2 - 20))
            pygame.display.flip()
            time.sleep(2)
            # set_game()
            main_menu()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                shutdown_client(client_instance)
                close_game()

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
                    close_game()
                if event.key == pygame.K_s:
                    show_score = not show_score
                if event.key == pygame.K_c and not game_over:
                    row, col = level4(first,board,client_instance.current_player)
                    board[row][col] = client_instance.current_player
                    boards.append(copy.deepcopy(board))
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
                    # set_game()
                    main_menu()

    elif player == 4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close_game()
                if event.key == pygame.K_b:
                    # set_game()
                    main_menu()

    if player == 4:
        new_time = time.time()
        elapsed_time = new_time - start_time
        if elapsed_time > 1 and move_idx < move_cnt-1:    # 1 move per 1 second
            move_idx += 1
            start_time = new_time
        replay_board = eval(replay_moves[move_idx][0])
        draw_replay(replay_board)

        if move_idx == move_cnt-1:  # replay complete
            text = small_font.render(f'Replay ends! Press B to return to start screen, Press Q to exit', True, BLACK)
            screen.blit(text, (20, size // 2 - 20))
    ##########################################
    ################ PHASE 2 #################
    ##########################################

    else:
        draw_board(board,show_score,first,False if game_over else goto_net,your_turn)

        if game_over:
            if not game_save:   # Save only once per game
                print("Saving game ...")
                save_game_play(game_type, boards)  # Save game on game over
                game_save = True

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
