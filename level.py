import random
from train import get_level2weight, get_level3boards, get_level4boards

level2weight=get_level2weight()
level3boards=get_level3boards()
level4boards=get_level4boards()

def level1(board):
    # 가능한 모든 빈 칸의 위치를 찾습니다.
    available_positions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    # 가능한 위치 중에서 랜덤하게 선택합니다.
    row, col = random.choice(available_positions)
    return row, col

def level2(board):
    best_score = -1
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                if level2weight[row][col] > best_score:
                    best_score = level2weight[row][col]
                    best_move = (row, col)
    return best_move

def level3(first,board,current):
    best_score = float('-inf') if current == 'O' else float('inf')
    best_move = None
        # 가능한 모든 움직임을 시뮬레이션하여 최선의 움직임을 찾음
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                board[row][col] = current
                board_tuple = tuple(tuple(r) for r in board)
                score = level3boards[board_tuple,first][0]-level3boards[board_tuple,first][1]
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

def level4(first,board,current):
    best_score = float('-inf') if current == 'O' else float('inf')
    best_move = None
        # 가능한 모든 움직임을 시뮬레이션하여 최선의 움직임을 찾음
    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                board[row][col] = current
                board_tuple = tuple(tuple(r) for r in board)
                numthisposition=level4boards[board_tuple,first][0]+level4boards[board_tuple,first][1]+level4boards[board_tuple,first][2]
                if numthisposition==0:
                    score=0
                else:
                    score = (level4boards[board_tuple,first][0]-level4boards[board_tuple,first][1])/numthisposition
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