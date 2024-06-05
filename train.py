import random
import itertools
from game import make_move, check_winner, is_board_full

randomplay=100000
reinforceplay=100000

board = [['' for _ in range(3)] for _ in range(3)]

def create_random_weight():
    weight=[[random.uniform(0,1) for i in range(3)] for j in range(3)]
    return weight

def normalization_weight(weight):
    weightsum=sum(sum(row) for row in weight)
    result_weight = [[element/weightsum for element in row] for row in weight]
    return result_weight

def average_weights(weight0, weight1):
    nweight0=normalization_weight(weight0)
    nweight1=normalization_weight(weight1)
    average = [[(nweight0[row][col] + nweight1[row][col]) / 2 for col in range(3)] for row in range(3)]
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


def generate_allboards_boards():
    symbols = ['O', 'X', '']
    all_comb = list(itertools.product(symbols, repeat=9))
    all_boards={}
    for first in ['O', 'X']:
        for comb in all_comb:
            board_tuple = tuple(tuple(comb[i:i+3]) for i in range(0, 9, 3))
            all_boards[(board_tuple, first)]=[0, 0, 0] #'O' win, lose, draw
    return all_boards

def playTTTself_play_random(first, weight, current, board, allboards, history=None):
    if history is None:
        history = [(('','',''),('','',''),('','',''))]
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
            update_allboards(first, history, winner, allboards)
            return
        if is_board_full(board):
            update_allboards(first, history, None, allboards)
            return
        else:
            next_player = 'X' if current == 'O' else 'O'
            playTTTself_play_random(first, weight, next_player, board, allboards, history)
    else:
        return 

def update_allboards(first,history, winner,allboards):
    # tictactoe의 모든 단계의 보드 상태를 추적하여 allboards 값을 업데이트
    for board_tuple in history:
        if winner == 'O':
            allboards[board_tuple,first][0]+=1
        elif winner == 'X':
            allboards[board_tuple,first][1]+=1
        else:
            allboards[board_tuple,first][2]+=1
        

def train_play_random(allboards):
    for i in range(0,randomplay):
        weight=create_random_weight()
        board = [['' for _ in range(3)] for _ in range(3)]
        playTTTself_play_random('O',weight, 'O', board,allboards)
        board = [['' for _ in range(3)] for _ in range(3)]
        playTTTself_play_random('X',weight, 'X', board,allboards)

def playTTTself_play_reinforce(first, current, board, allboards, history=None):
    if history is None:
        history = [(('','',''),('','',''),('','',''))]
    best_score = float('-inf') if current == 'O' else float('inf')
    best_move = None

    if(random.uniform(0,1)<0.2):
        available_positions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    # 가능한 위치 중에서 랜덤하게 선택합니다.
        best_move = random.choice(available_positions)
    else:
        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    board[row][col] = current
                    board_tuple = tuple(tuple(r) for r in board)
                    numthisposition=allboards[board_tuple,first][0]+allboards[board_tuple,first][1]+allboards[board_tuple,first][2]
                    if numthisposition==0:
                        score=0
                    else:
                        score = (allboards[board_tuple,first][0]-allboards[board_tuple,first][1])/numthisposition
                    if current == 'O':
                        if score > best_score:
                            best_score = score
                            best_move = (row, col)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (row, col)
                    board[row][col] = ''  
    if best_move:
        make_move(best_move[0], best_move[1], current, board)
        history.append(tuple(tuple(row) for row in board))  # 현재 보드 상태를 기록
        winner = check_winner(board)
        if winner:
            update_allboards(first, history, winner, allboards)
            return
        if is_board_full(board):
            update_allboards(first, history, None, allboards)
            return
        else:
            next_player = 'X' if current == 'O' else 'O'
            playTTTself_play_reinforce(first, next_player, board, allboards, history)
    else:
        return
    
def train_play_reinforce(allboards):
    for i in range(0,reinforceplay):
        board = [['' for _ in range(3)] for _ in range(3)]
        playTTTself_play_reinforce('O', 'O', board,allboards)
        board = [['' for _ in range(3)] for _ in range(3)]
        playTTTself_play_reinforce('X', 'X', board,allboards)

level3boards=generate_allboards_boards()
level4boards=generate_allboards_boards()
    
level2weight=train_noob()
train_play_random(level3boards)
train_play_reinforce(level4boards)

def get_level2weight():
    return level2weight

def get_level3boards():
    return level3boards

def get_level4boards():
    return level4boards