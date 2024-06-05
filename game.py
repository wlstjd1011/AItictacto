# Tic-Tac-Toe 게임 진행을 위한 함수들
# 게임 진행은 유저가 사용할 때, 컴퓨터 스스로 학습할 때 진행

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