import pygame
from train import get_level4boards
import random

level4boards=get_level4boards()

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# 화면 크기 설정
allsize = 1000
size = 600
cell_size = size // 3
screen = pygame.display.set_mode((allsize, size))
pygame.display.set_caption('Tic Tac Toe')

# 글꼴 설정
font = pygame.font.Font(None, 200)
small_font = pygame.font.Font(None, 40)

def draw_board(board, show_score, first, show_turn, your_turn):    
    screen.fill(WHITE)
    # 수직선 그리기
    pygame.draw.line(screen, BLACK, (cell_size, 0), (cell_size, size), 3)
    pygame.draw.line(screen, BLACK, (2 * cell_size, 0), (2 * cell_size, size), 3)
    # 수평선 그리기
    pygame.draw.line(screen, BLACK, (0, cell_size), (size, cell_size), 3)
    pygame.draw.line(screen, BLACK, (0, 2 * cell_size), (size, 2 * cell_size), 3)
    pygame.draw.line(screen, BLACK, (size, 0), (size, size), 3)

    for row in range(3):
        for col in range(3):
            if board[row][col] != '':
                text = font.render(board[row][col], True, RED if board[row][col] == 'X' else BLUE)
                screen.blit(text, (col * cell_size + 30, row * cell_size + 10))
    restart_message_display = small_font.render("'B' return to start screen", True, BLACK)
    screen.blit(restart_message_display, (size + 20, 300))
    chance_message_display = small_font.render("'C' AI moves for you", True, BLACK)
    screen.blit(chance_message_display, (size + 20, 340))

    ##########################################
    ################ PHASE 2 #################
    ##########################################
    if show_turn:   # display whose turn it is
        turn_font = pygame.font.Font(None, 70)
        if your_turn:
            whose_turn_display = turn_font.render("YOUR TURN", True, RED)
        else:
            whose_turn_display = turn_font.render("ENEMY TURN", True, BLACK)
        screen.blit(whose_turn_display, (size + 20, 420))
    ##########################################
    ################ PHASE 2 #################
    ##########################################

    if show_score:
        board_tuple = tuple(tuple(row) for row in board)  # 현재 보드 상태를 튜플로 변환
        Owincase=level4boards[(board_tuple,first)][0]
        Olosecase=level4boards[(board_tuple,first)][1]
        Odrawcase=level4boards[(board_tuple,first)][2]

        Owincase_text = small_font.render("'O'wincase", True, BLACK)  # "Board Scores" 텍스트 추가
        screen.blit(Owincase_text, (size + 20, 20)) 

        wincase_display = small_font.render(str(Owincase), True, BLACK)  # 점수를 텍스트로 변환
        screen.blit(wincase_display, (size + 20, 60))  # 점수 텍스트 위치 지정

        Olosecase_text = small_font.render("'O'losecase", True, BLACK)  
        screen.blit(Olosecase_text, (size + 20, 100))

        losecase_display = small_font.render(str(Olosecase), True, BLACK)  # 점수를 텍스트로 변환
        screen.blit(losecase_display, (size + 20, 140))

        drawcase_text = small_font.render("drawcase", True, BLACK)  
        screen.blit(drawcase_text, (size + 20, 180))

        drawcase_display = small_font.render(str(Odrawcase), True, BLACK)  # 점수를 텍스트로 변환
        screen.blit(drawcase_display, (size + 20, 220))  # 점수 텍스트 위치 지정

    score_message_display = small_font.render("'S' to show/hide score.", True, BLACK)
    screen.blit(score_message_display, (size + 20, 260))



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
    ################ PHASE 2 #################
    onlin_text = small_font.render("Press 3 for online 2Players", True, BLACK)
    onlin_rect = onlin_text.get_rect(center=(size // 2, 400))
    screen.blit(onlin_text, onlin_rect)

##########################################
################ PHASE 2 #################
##########################################
def inputname(player_name):
    names = ['Thor','Captain America','Iron Man','Black Widow','Scarlet Witch',
    'Black Panther','Hawkeye','Quicksilver','Vision','Ant-Man','Captain Marvel',
    'Loki','Wolverine','Doctor Strange','Winter Soldier','Wasp','Hulk','Mantis',
    'Falcon','War Machine','Moon Knight','Spider-Man','Valkyrie','Storm',
    'Deadpool','Yondu','Star-Lord','Gamora','Rocket','Drax','Groot','Nebula',
    'Cyclops','Iceman','Beast','Phoenix','Rogue','Professor X','Colossus',
    'Nightcrawler','Beast','Kitty Pride','Angel','Havok','Magneto','Mystique',
    'Toad','Chipper','Charlie','Merlin','Wolfman','Cougar','Hollywood','Slider',
    'Jester','Stinger','Sundown','Goose','Viper','Maverick','Cyclone','Warlock',
    'Hangman','Fanboy','Payback','Hammer','Coyote','Omaha','Halo']

    random.shuffle(names)
    if player_name == '':
        player_name = names[0]

    screen.fill(WHITE)
    # 게임 제목 표시
    title_text = small_font.render("Tic Tac Toe", True, BLACK)
    title_rect = title_text.get_rect(center=(size // 2, 100))
    screen.blit(title_text, title_rect)
    # 플레이어 이름 입력
    player_name_text = small_font.render("Player name", True, BLACK)
    player_name_rect = player_name_text.get_rect(center=(size // 2, 200))
    screen.blit(player_name_text, player_name_rect)
    # Input box
    input_name_text = small_font.render(player_name, True, BLACK)
    input_name_rect = input_name_text.get_rect(center=(size // 2, 250))
    screen.blit(input_name_text, input_name_rect)
    # Go to game room
    goto_text = small_font.render("Press Return to enter the game room ...", True, BLACK)
    goto_rect = goto_text.get_rect(center=(size // 2, 400))
    screen.blit(goto_text, goto_rect)

    return player_name

def gameroom(player1_name, player2_name):
    screen.fill(WHITE)
    # 게임 제목 표시
    title_text = small_font.render("Tic Tac Toe", True, BLACK)
    title_rect = title_text.get_rect(center=(size // 2, 100))
    screen.blit(title_text, title_rect)
    # 플레이어1
    player1_text = small_font.render("Player1", True, BLACK)
    player1_rect = player1_text.get_rect(center=(size // 4, 200))
    screen.blit(player1_text, player1_rect)
    player1_name_text = small_font.render(player1_name, True, BLACK)
    player1_name_rect = player1_name_text.get_rect(center=(size // 4, 250))
    screen.blit(player1_name_text, player1_name_rect)
    if player2_name != '' and player2_name is not None:
        # 플레이어2
        player2_text = small_font.render("Player2", True, BLACK)
        player2_rect = player2_text.get_rect(center=(size // 4 * 3, 200))
        screen.blit(player2_text, player2_rect)
        player2_name_text = small_font.render(player2_name, True, BLACK)
        player2_name_rect = player2_name_text.get_rect(center=(size // 4 * 3, 250))
        screen.blit(player2_name_text, player2_name_rect)
        msg = "Starting game ..."
    else:
        msg = "Waiting for another player ..."    
        # Go to main menu
        home_text = small_font.render("Press B to return to start screen", True, BLACK)
        home_rect = home_text.get_rect(center=(size // 2, 450))
        screen.blit(home_text, home_rect)

    # Waiting Or Start
    msg_text = small_font.render(msg, True, BLACK)
    msg_rect = msg_text.get_rect(center=(size // 2, 400))
    screen.blit(msg_text, msg_rect)
##########################################
################ PHASE 2 #################
##########################################