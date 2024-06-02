import pygame
import sys
import random
import itertools

board = [['' for _ in range(3)] for _ in range(3)]


def generate_alltictactoe_boards():
    symbols = ['O', 'X', '']
    all_comb = list(itertools.product(symbols, repeat=9))
    all_boards={}
    for first in ['O', 'X']:
        for comb in all_comb:
            board_tuple = tuple(tuple(comb[i:i+3]) for i in range(0, 9, 3))
            all_boards[(board_tuple, first)] = 0
    return all_boards

def make_move(row, col, current,board):
    board[row][col] = current

def check_winner(board):
    # 행, 열, 대각선 검사
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '':
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def is_board_full(board):
    for row in board:
        if '' in row:
            return False
    return True

def level1(board):
    # 가능한 모든 빈 칸의 위치를 찾습니다.
    available_positions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    # 가능한 위치 중에서 랜덤하게 선택합니다.
    row, col = random.choice(available_positions)
    return row, col

def level2(board,current):
    # 가능한 모든 빈 칸의 위치를 찾습니다.
    available_positions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    # 당장 승리할 수 있다면, 승리합니다.
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                board[row][col] = current
                if check_winner(board) == current:
                    board[row][col] = ''  # 보드 상태 복원
                    return row, col
                board[row][col] = ''  # 보드 상태 복원
                
    row, col = random.choice(available_positions)
    return row, col

def create_random_weight():
    weight=[[random.uniform(0,1) for i in range(3)] for j in range(3)]
    return weight

def normalization_weight(weight):
    weightsum=sum(sum(row) for row in weight)
    result_weight = [[element/weightsum for element in row] for row in weight]
    return result_weight

def average_weights(weight0, weight1):
    average = [[(weight0[row][col] + weight1[row][col]) / 2 for col in range(3)] for row in range(3)]
    return average

def playTTTself_noob(weight0, weight1,current,board):
    current_weight = weight0 if current == 'O' else weight1
    best_score = -1
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                if current_weight[row][col] > best_score:
                    best_score = current_weight[row][col]
                    best_move = (row, col)

    if best_move:
        make_move(best_move[0], best_move[1], current,board)
        winner = check_winner(board)
        if winner:
            return weight0 if winner == 'O' else weight1
        else:
            next_player = 'X' if current == 'O' else 'O'
            return playTTTself_noob(weight0, weight1, next_player,board)
    else:
        return average_weights(weight0, weight1) 

def train_noob():
    weight10240=[[normalization_weight(create_random_weight()) for k in range(1024)] for l in range(10)]
    for l in range(0,10):
        k=1024
        while(k>0):
            k//=2
            for j in range (0,k):
                board = [['' for _ in range(3)] for _ in range(3)]
                weight0=playTTTself_noob(weight10240[l][2*j],weight10240[l][2*j+1],'O',board)
                board = [['' for _ in range(3)] for _ in range(3)]
                weight1=playTTTself_noob(weight10240[l][2*j+1],weight10240[l][2*j],'O',board)
                weight10240[l][j]=average_weights(weight0,weight1)
    weight=[[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            for l in range(10):
                weight[i][j]+=weight10240[l][0][i][j]
            weight[i][j]/=10
    return weight

level3weight=train_noob()
print(level3weight)

def level3(board):
    best_score = -1
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                if level3weight[row][col] > best_score:
                    best_score = level3weight[row][col]
                    best_move = (row, col)
    return best_move

# 학습을 위한 board들 준비
level4boards=generate_alltictactoe_boards()
level5boards=generate_alltictactoe_boards()


def playTTTself_play_random(first, weight, current, board,allboards, history=None):
    if history is None:
        history = []
    best_score = 0
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                if weight[row][col] > best_score:
                    best_score = weight[row][col]
                    best_move = (row, col)

    if best_move:
        make_move(best_move[0], best_move[1], current, board)
        history.append(tuple(tuple(row) for row in board))  # 현재 보드 상태를 기록
        winner = check_winner(board)
        if winner:
            update_allboards(first,history, winner,allboards)
        else:
            next_player = 'X' if current == 'O' else 'O'
            playTTTself_play_random(first,weight, next_player, board,allboards, history)
    else:
        return

def update_allboards(first,history, winner,allboards):
    # tictactoe의 모든 단계의 보드 상태를 추적하여 allboards 값을 업데이트
    for board_state in history:
        if winner == 'O':
            allboards[board_state,first] += 1
        elif winner == 'X':
            allboards[board_state,first] -= 1

def train_play_random(allboards):
    for i in range(0,100000):
        weight=create_random_weight()
        board = [['' for _ in range(3)] for _ in range(3)]
        playTTTself_play_random('O',weight, 'O', board,allboards)
        board = [['' for _ in range(3)] for _ in range(3)]
        playTTTself_play_random('X',weight, 'X', board,allboards)
        if(i%10000==0):
            print(i)

train_play_random(level4boards)

def level4(first,board,current):
    global level4boards
    best_score = float('-inf') if current == 'O' else float('inf')
    best_move = None
        # 가능한 모든 움직임을 시뮬레이션하여 최선의 움직임을 찾음
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                board[row][col] = current
                board_tuple = tuple(tuple(r) for r in board)
                score = level4boards[board_tuple,first]
                if current == 'O':
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = (row, col)
                board[row][col] = ''  # 보드 상태 복원
    return best_move

def level5(board,current):
    global level5boards
    best_score = float('-inf') if current == 'O' else float('inf')
    best_move = None
        # 가능한 모든 움직임을 시뮬레이션하여 최선의 움직임을 찾음
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                board[row][col] = current
                board_tuple = tuple(tuple(r) for r in board)
                score = level5boards[board_tuple,first]
                if current == 'O':
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = (row, col)
                board[row][col] = ''  # 보드 상태 복원
    return best_move

# 색상 정의
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
score_message = "Press 'S' to show/hide scoreboard."

# 글꼴 설정
font = pygame.font.Font(None, 200)
small_font = pygame.font.Font(None, 40)

def draw_board():
    screen.fill(WHITE)
    # 수직선 그리기
    pygame.draw.line(screen, BLACK, (cell_size, 0), (cell_size, size), 3)
    pygame.draw.line(screen, BLACK, (2 * cell_size, 0), (2 * cell_size, size), 3)
    # 수평선 그리기
    pygame.draw.line(screen, BLACK, (0, cell_size), (size, cell_size), 3)
    pygame.draw.line(screen, BLACK, (0, 2 * cell_size), (size, 2 * cell_size), 3)

    for row in range(3):
        for col in range(3):
            if board[row][col] != '':
                text = font.render(board[row][col], True, RED if board[row][col] == 'X' else BLUE)
                screen.blit(text, (col * cell_size + 30, row * cell_size + 10))

    if show_score:
        # 점수판 그리기
        pygame.draw.line(screen, BLACK, (size, 0), (size, size), 3)  # 보드 오른쪽에 구분선 그리기
        score_text = small_font.render("Board Scores", True, BLACK)  # "Board Scores" 텍스트 추가
        screen.blit(score_text, (size + 20, 20))  # "Board Scores" 텍스트 위치 지정

        board_tuple = tuple(tuple(row) for row in board)  # 현재 보드 상태를 튜플로 변환
        score = level4boards[board_tuple,first]  # 현재 보드 상태의 점수 가져오기
        score_display = small_font.render(str(score), True, BLACK)  # 점수를 텍스트로 변환
        screen.blit(score_display, (size + 20, 60))  # 점수 텍스트 위치 지정

    score_message_display = small_font.render(score_message, True, BLACK)
    screen.blit(score_message_display, (size + 20, 100))

def selectfirst():
    screen.fill(WHITE)
    # 게임 제목 표시
    title_text = small_font.render("Tic Tac Toe", True, BLACK)
    title_rect = title_text.get_rect(center=(size // 2, 100))
    screen.blit(title_text, title_rect)
    # 누가 먼저 시작할지 안내 문구 표시
    who_first_text = small_font.render("Who goes first?", True, BLACK)
    who_first_rect = who_first_text.get_rect(center=(size // 2, 200))
    screen.blit(who_first_text, who_first_rect)
    # 사용자 또는 컴퓨터 선택 안내 문구 표시
    user_text = small_font.render("Press U for User", True, BLACK)
    user_rect = user_text.get_rect(center=(size // 2, 300))
    screen.blit(user_text, user_rect)
    comp_text = small_font.render("Press C for Computer", True, BLACK)
    comp_rect = comp_text.get_rect(center=(size // 2, 350))
    screen.blit(comp_text, comp_rect)

def selectlevel():
    screen.fill(WHITE)
    # 게임 제목 표시
    title_text = small_font.render("Tic Tac Toe", True, BLACK)
    title_rect = title_text.get_rect(center=(size // 2, 100))
    screen.blit(title_text, title_rect)
    # 플레이어 수를 묻는 질문
    who_first_text = small_font.render("Choose level", True, BLACK)
    who_first_rect = who_first_text.get_rect(center=(size // 2, 200))
    screen.blit(who_first_text, who_first_rect)
    # 1명 또는 2명
    user_text = small_font.render("Press 1 for vs level1", True, BLACK)
    user_rect = user_text.get_rect(center=(size // 2, 300))
    screen.blit(user_text, user_rect)
    comp_text = small_font.render("Press 2 for level2", True, BLACK)
    comp_rect = comp_text.get_rect(center=(size // 2, 350))
    screen.blit(comp_text, comp_rect)
    comp_text = small_font.render("Press 3 for level3", True, BLACK)
    comp_rect = comp_text.get_rect(center=(size // 2, 400))
    screen.blit(comp_text, comp_rect)
    comp_text = small_font.render("Press 4 for level4", True, BLACK)
    comp_rect = comp_text.get_rect(center=(size // 2, 450))
    screen.blit(comp_text, comp_rect)


def selectplayer():
    screen.fill(WHITE)
    # 게임 제목 표시
    title_text = small_font.render("Tic Tac Toe", True, BLACK)
    title_rect = title_text.get_rect(center=(size // 2, 100))
    screen.blit(title_text, title_rect)
    # 플레이어 수를 묻는 질문
    who_first_text = small_font.render("How many players?", True, BLACK)
    who_first_rect = who_first_text.get_rect(center=(size // 2, 200))
    screen.blit(who_first_text, who_first_rect)
    # 1명 또는 2명
    user_text = small_font.render("Press 1 for vs computer", True, BLACK)
    user_rect = user_text.get_rect(center=(size // 2, 300))
    screen.blit(user_text, user_rect)
    comp_text = small_font.render("Press 2 for 2Players", True, BLACK)
    comp_rect = comp_text.get_rect(center=(size // 2, 350))
    screen.blit(comp_text, comp_rect)

player=0
while player==0:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                player=1
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                player=2
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    selectplayer()
    pygame.display.flip()

level=0

while level==0 and player==1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                level=1
            elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                level=2
            elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                level=3
            elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                level=4
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    selectlevel()
    pygame.display.flip()  

user_choice = ''
while user_choice not in ['U', 'C'] and player==1:
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
    first='X'
    current_player = 'X'
else:
    first='O'
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

# 게임 루프
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
                    row, col = level2(board,current_player)
                elif(level==3):
                    row, col = level3(board)
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
                



    draw_board()
    if game_over:
        winner = check_winner(board)
        if winner:
            text = small_font.render(f'{winner} wins! Press R to restart, Press Q to exit', True, BLACK)
        else:
            text = small_font.render('Draw! Press R to restart, Press Q to exit', True, BLACK)
        screen.blit(text, (20, size // 2 - 20))

    pygame.display.flip()
