import pygame
import sys
from game import is_board_full, make_move, check_winner
from interface import draw_board, selectfirst, selectlevel, selectplayer
from level import level1, level2, level3, level4

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

# 글꼴 설정
font = pygame.font.Font(None, 200)
small_font = pygame.font.Font(None, 40)


player = 0
while player == 0:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                player = 1
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                player = 2
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    selectplayer()
    pygame.display.flip()

level = 0

while level == 0 and player == 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                level = 1
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                level = 2
            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                level = 3
            elif event.key == pygame.K_4 or event.key == pygame.K_K_KP4:
                level = 4
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    selectlevel()
    pygame.display.flip()

user_choice = ''
while user_choice not in ['U', 'C'] and player == 1:
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

board = [['' for _ in range(3)] for _ in range(3)]
if user_choice == 'C':
    first = 'X'
    current_player = 'X'
else:
    first = 'O'
    current_player = 'O'
game_over = False

def reset_game():
    global board, current_player, game_over
    board = [['' for _ in range(3)] for _ in range(3)]
    if user_choice == 'C':
        current_player = 'X'
    else:
        current_player = 'O'
    game_over = False

# 메인 루프
while True:
    if(player==1):
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                if event.key == pygame.K_q:
                    exit()
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
                    player = 0
                    level = 0
                    user_choice = ''
                    game_over=False
                    board = [['' for _ in range(3)] for _ in range(3)]
                    # 초기 상태로 되돌아가 선택 화면을 다시 표시
                    while player == 0:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                                    player = 1
                                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                                    player = 2
                                elif event.key == pygame.K_q:
                                    pygame.quit()
                                    sys.exit()
                            elif event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        selectplayer()
                        pygame.display.flip()

                    while level == 0 and player == 1:
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
                                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                                    level=5
                                elif event.key == pygame.K_q:
                                    pygame.quit()
                                    sys.exit()
                            elif event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        selectlevel()
                        pygame.display.flip()
                    while user_choice not in ['U', 'C'] and player == 1:
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
                    if user_choice == 'C':
                        first='X'
                        current_player = 'X'
                    else:
                        first='O'
                        current_player = 'O'
    else:
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
                        exit()
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
                        player = 0
                        level = 0
                        user_choice = ''
                        game_over=False
                        board = [['' for _ in range(3)] for _ in range(3)]
                        # 초기 상태로 되돌아가 선택 화면을 다시 표시
                        while player == 0:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                                        player = 1
                                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                                        player = 2
                                    elif event.key == pygame.K_q:
                                        pygame.quit()
                                        sys.exit()
                                elif event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                            selectplayer()
                            pygame.display.flip()

                        while level == 0 and player == 1:
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
                                    elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                                        level=5
                                    elif event.key == pygame.K_q:
                                        pygame.quit()
                                        sys.exit()
                                elif event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                            selectlevel()
                            pygame.display.flip()
                        while user_choice not in ['U', 'C'] and player == 1:
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
                        if user_choice == 'C':
                            first='X'
                            current_player = 'X'
                        else:
                            first='O'
                            current_player = 'O'
                
    draw_board(board,show_score,first)
    if game_over:
        winner = check_winner(board)
        if winner:
            text = small_font.render(f'{winner} wins! Press R to restart, Press Q to exit', True, BLACK)
        else:
            text = small_font.render('Draw! Press R to restart, Press Q to exit', True, BLACK)
        screen.blit(text, (20, size // 2 - 20))

    pygame.display.flip()