#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import numpy as np
import time
from copy import deepcopy
import time
import sys

## Some useful functions that convert boards to string or list of list

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def get_board_list (board, N):
    return [[j for j in board[i:i+N]] for i in range(0, len(board), N)]

def string_to_board(board):
    return "".join(["".join(i) for i in board])


# Check if a row,col index pair is on the board to find valid range of moves
def valid_index(pos,N):
        return 0 <= pos[0] < N  and 0 <= pos[1] < N

def get_piece_positions(board):
    '''
    This function scans entire board and find relative position of each piece.
    '''
    positions = {'@' : [], '$' : [], 'w' : [], 'W' : [], 'b' : [], 'B' : []}

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != '.':
                if board[i][j] not in positions.keys():
                    positions[board[i][j]] = [(i,j)]
                else:
                    positions[board[i][j]].append((i,j))
    return positions

def skip_spot_check(start, end, board):
    '''
    This function checks simple moves. Simple moves are moves where piece can 
    move but there is no opportunity to capture.
    With given start and end location, it checks if any piece in between as 
    well as whereever pieces lands should be empty square.
    '''
    if board[end[0]][end[1]] == '.':
        delta = (end[0]-start[0], end[1] - start[1])
        if delta[1] == 0 and delta[0] > 0:
            for i in range(1, delta[0]):
                spot_x = start[0] + i
                spot_y = start[1]
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
        elif delta[1] == 0 and delta[0] < 0:
            for i in range(-1, delta[0], -1):
                spot_x = start[0] + i
                spot_y = start[1]
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True

        elif delta[0] == 0 and delta[1] > 0:
            for i in range(1, delta[1]):
                spot_x = start[0]
                spot_y = start[1] + i
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
        elif delta[0] == 0 and delta[1] < 0:
            for i in range(-1, delta[1], -1):
                spot_x = start[0]
                spot_y = start[1] + i
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
    
        elif delta[0] > 0 and delta[1] > 0:
            for (i, j) in zip(range(1, delta[0]), range(1, delta[1])):
                spot_x = start[0] + i
                spot_y = start[1] + j
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
        elif delta[0] < 0 and delta[1] < 0:
            for (i, j) in zip(range(-1, delta[0], -1), range(-1, delta[1], -1)):
                spot_x = start[0] + i
                spot_y = start[1] + j
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
        elif delta[0] > 0 and delta[1] < 0:
            for (i, j) in zip(range(1, delta[0]), range(-1, delta[1], -1)):
                spot_x = start[0] + i
                spot_y = start[1] + j
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
        elif delta[0] < 0 and delta[1] > 0:
            for (i, j) in zip(range(-1, delta[0],-1), range(1, delta[1])):
                spot_x = start[0] + i
                spot_y = start[1] + j
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
    
    return False


def capture_spot_check(start, end, board, capature_piece):
    '''
    This function checks capture moves. Capture moves are moves where piece can 
    move band there is opportunity to capture.
    With given start and end location, it checks if any piece in between as 
    well as whereever pieces lands should be empty square. It makes sure it can 
    capture only one piece at a time. 
    '''

    capture_string = ''
    if board[end[0]][end[1]] == '.':
        delta = (end[0]-start[0], end[1] - start[1])
        if delta[1] == 0 and delta[0] > 0:
            for i in range(1, delta[0]):
                spot_x = start[0] + i
                spot_y = start[1]
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
        elif delta[1] == 0 and delta[0] < 0:
            for i in range(-1, delta[0], -1):
                spot_x = start[0] + i
                spot_y = start[1]
                capture_string += board[spot_x][spot_y]
            l1 = [i for i in capture_string if i != '.']    
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True

        elif delta[0] == 0 and delta[1] > 0:
            for i in range(1, delta[1]):
                spot_x = start[0]
                spot_y = start[1] + i
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
        elif delta[0] == 0 and delta[1] < 0:
            for i in range(-1, delta[1], -1):
                spot_x = start[0]
                spot_y = start[1] + i
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
    
        elif delta[0] > 0 and delta[1] > 0:
            for (i, j) in zip(range(1, delta[0]), range(1, delta[1])):
                spot_x = start[0] + i
                spot_y = start[1] + j
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
        elif delta[0] < 0 and delta[1] < 0:
            for (i, j) in zip(range(-1, delta[0], -1), range(-1, delta[1], -1)):
                spot_x = start[0] + i
                spot_y = start[1] + j
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
        elif delta[0] > 0 and delta[1] < 0:
            for (i, j) in zip(range(1, delta[0]), range(-1, delta[1], -1)):
                spot_x = start[0] + i
                spot_y = start[1] + j
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
        elif delta[0] < 0 and delta[1] > 0:
            for (i, j) in zip(range(-1, delta[0],-1), range(1, delta[1])):
                spot_x = start[0] + i
                spot_y = start[1] + j
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
    
    return False

def remove_piece(start, end, board):
    '''
    This function remove piece from board once it is captured. 
    '''
    
    board1 = deepcopy(board)
    delta = (end[0]-start[0], end[1] - start[1])
    if delta[1] == 0 and delta[0] > 0:
        for i in range(1, delta[0]):
            spot_x = start[0] + i
            spot_y = start[1]

            board1[spot_x][spot_y] = '.'

    elif delta[1] == 0 and delta[0] < 0:
        for i in range(-1, delta[0], -1):
            spot_x = start[0] + i
            spot_y = start[1]
            board1[spot_x][spot_y] = '.'

    elif delta[0] == 0 and delta[1] > 0:
        for i in range(1, delta[1]):
            spot_x = start[0]
            spot_y = start[1] + i
            board1[spot_x][spot_y] = '.'


    elif delta[0] == 0 and delta[1] < 0:
        for i in range(-1, delta[1], -1):
            spot_x = start[0]
            spot_y = start[1] + i
            board1[spot_x][spot_y] = '.'


    elif delta[0] > 0 and delta[1] > 0:
        for (i, j) in zip(range(1, delta[0]), range(1, delta[1])):
            spot_x = start[0] + i
            spot_y = start[1] + j
            board1[spot_x][spot_y] = '.'

    elif delta[0] < 0 and delta[1] < 0:
        for (i, j) in zip(range(-1, delta[0], -1), range(-1, delta[1], -1)):
            spot_x = start[0] + i
            spot_y = start[1] + j
            board1[spot_x][spot_y] = '.'

    elif delta[0] > 0 and delta[1] < 0:
        for (i, j) in zip(range(1, delta[0]), range(-1, delta[1], -1)):
            spot_x = start[0] + i
            spot_y = start[1] + j
            board1[spot_x][spot_y] = '.'


    elif delta[0] < 0 and delta[1] > 0:
        for (i, j) in zip(range(-1, delta[0],-1), range(1, delta[1])):
            spot_x = start[0] + i
            spot_y = start[1] + j
            board1[spot_x][spot_y] = '.'
    
    return board1

def get_promoted(move, player, N):
    '''
    Check if piece can be promoted to Raichu
    '''
    if (player == 'w' and move[0] == N-1) or (player == 'b' and move[0] == 0):
        return True
    else:
        return False


def skip_spot_check(start, end, board):
    '''
    This function checks simple moves. Simple moves are moves where piece can 
    move but there is no opportunity to capture.
    With given start and end location, it checks if any piece in between as 
    well as whereever pieces lands should be empty square.
    '''
    if board[end[0]][end[1]] == '.':
        delta = (end[0]-start[0], end[1] - start[1])
        if delta[1] == 0 and delta[0] > 0:
            for i in range(1, delta[0]):
                spot_x = start[0] + i
                spot_y = start[1]
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
        elif delta[1] == 0 and delta[0] < 0:
            for i in range(-1, delta[0], -1):
                spot_x = start[0] + i
                spot_y = start[1]
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True

        elif delta[0] == 0 and delta[1] > 0:
            for i in range(1, delta[1]):
                spot_x = start[0]
                spot_y = start[1] + i
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
        elif delta[0] == 0 and delta[1] < 0:
            for i in range(-1, delta[1], -1):
                spot_x = start[0]
                spot_y = start[1] + i
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
    
        elif delta[0] > 0 and delta[1] > 0:
            for (i, j) in zip(range(1, delta[0]), range(1, delta[1])):
                spot_x = start[0] + i
                spot_y = start[1] + j
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
        elif delta[0] < 0 and delta[1] < 0:
            for (i, j) in zip(range(-1, delta[0], -1), range(-1, delta[1], -1)):
                spot_x = start[0] + i
                spot_y = start[1] + j
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
        elif delta[0] > 0 and delta[1] < 0:
            for (i, j) in zip(range(1, delta[0]), range(-1, delta[1], -1)):
                spot_x = start[0] + i
                spot_y = start[1] + j
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
        elif delta[0] < 0 and delta[1] > 0:
            for (i, j) in zip(range(-1, delta[0],-1), range(1, delta[1])):
                spot_x = start[0] + i
                spot_y = start[1] + j
                if board[spot_x][spot_y] != '.' or board[end[0]][end[1]] != '.':
                    return False
            else:
                return True
    
    return False


def capture_spot_check(start, end, board, capature_piece):
    '''
    This function checks capture moves. Capture moves are moves where piece can 
    move band there is opportunity to capture.
    With given start and end location, it checks if any piece in between as 
    well as whereever pieces lands should be empty square. It makes sure it can 
    capture only one piece at a time. 
    '''

    capture_string = ''
    if board[end[0]][end[1]] == '.':
        delta = (end[0]-start[0], end[1] - start[1])
        if delta[1] == 0 and delta[0] > 0:
            for i in range(1, delta[0]):
                spot_x = start[0] + i
                spot_y = start[1]
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
        elif delta[1] == 0 and delta[0] < 0:
            for i in range(-1, delta[0], -1):
                spot_x = start[0] + i
                spot_y = start[1]
                capture_string += board[spot_x][spot_y]
            l1 = [i for i in capture_string if i != '.']    
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True

        elif delta[0] == 0 and delta[1] > 0:
            for i in range(1, delta[1]):
                spot_x = start[0]
                spot_y = start[1] + i
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
        elif delta[0] == 0 and delta[1] < 0:
            for i in range(-1, delta[1], -1):
                spot_x = start[0]
                spot_y = start[1] + i
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
    
        elif delta[0] > 0 and delta[1] > 0:
            for (i, j) in zip(range(1, delta[0]), range(1, delta[1])):
                spot_x = start[0] + i
                spot_y = start[1] + j
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
        elif delta[0] < 0 and delta[1] < 0:
            for (i, j) in zip(range(-1, delta[0], -1), range(-1, delta[1], -1)):
                spot_x = start[0] + i
                spot_y = start[1] + j
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
        elif delta[0] > 0 and delta[1] < 0:
            for (i, j) in zip(range(1, delta[0]), range(-1, delta[1], -1)):
                spot_x = start[0] + i
                spot_y = start[1] + j
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
        elif delta[0] < 0 and delta[1] > 0:
            for (i, j) in zip(range(-1, delta[0],-1), range(1, delta[1])):
                spot_x = start[0] + i
                spot_y = start[1] + j
                capture_string += board[spot_x][spot_y]

            l1 = [i for i in capture_string if i != '.']
            if len(l1) != 1 or l1[0] not in capature_piece :
                return False
            else:
                return True
    
    return False

def remove_piece(start, end, board):
    '''
    This function remove piece from board once it is captured. 
    '''
    
    board1 = deepcopy(board)
    delta = (end[0]-start[0], end[1] - start[1])
    if delta[1] == 0 and delta[0] > 0:
        for i in range(1, delta[0]):
            spot_x = start[0] + i
            spot_y = start[1]

            board1[spot_x][spot_y] = '.'

    elif delta[1] == 0 and delta[0] < 0:
        for i in range(-1, delta[0], -1):
            spot_x = start[0] + i
            spot_y = start[1]
            board1[spot_x][spot_y] = '.'

    elif delta[0] == 0 and delta[1] > 0:
        for i in range(1, delta[1]):
            spot_x = start[0]
            spot_y = start[1] + i
            board1[spot_x][spot_y] = '.'


    elif delta[0] == 0 and delta[1] < 0:
        for i in range(-1, delta[1], -1):
            spot_x = start[0]
            spot_y = start[1] + i
            board1[spot_x][spot_y] = '.'


    elif delta[0] > 0 and delta[1] > 0:
        for (i, j) in zip(range(1, delta[0]), range(1, delta[1])):
            spot_x = start[0] + i
            spot_y = start[1] + j
            board1[spot_x][spot_y] = '.'

    elif delta[0] < 0 and delta[1] < 0:
        for (i, j) in zip(range(-1, delta[0], -1), range(-1, delta[1], -1)):
            spot_x = start[0] + i
            spot_y = start[1] + j
            board1[spot_x][spot_y] = '.'

    elif delta[0] > 0 and delta[1] < 0:
        for (i, j) in zip(range(1, delta[0]), range(-1, delta[1], -1)):
            spot_x = start[0] + i
            spot_y = start[1] + j
            board1[spot_x][spot_y] = '.'


    elif delta[0] < 0 and delta[1] > 0:
        for (i, j) in zip(range(-1, delta[0],-1), range(1, delta[1])):
            spot_x = start[0] + i
            spot_y = start[1] + j
            board1[spot_x][spot_y] = '.'
    
    return board1

def get_promoted(move, player, N):
    '''
    Check if piece can be promoted to Raichu
    '''
    if (player == 'w' and move[0] == N-1) or (player == 'b' and move[0] == 0):
        return True
    else:
        return False


## Movement
### Movement for each piece is divided into two categories. Simple moves
### which does moves pieces but it does not have opportunity to capture.
### Capture moves which does have opportunity to capture.

def get_pichu_simple_moves(current_position, current_board, player):
    x = current_position[0]
    y = current_position[1]
    board = current_board.copy()
    if player == 'w':
    ## Possible moves (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)
        moves = ((x+1, y-1), (x+1, y+1))
    else:
    ## Possible moves (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)
        moves = ((x-1, y-1), (x-1, y+1))
    

    return [[current_position, move] for move in moves if valid_index(move, len(current_board)) and (board[move[0]][move[1]] in "." )]

def get_pichu_capture_moves(current_position, current_board, player):
    x = current_position[0]
    y = current_position[1]
    board = current_board.copy()
    if player == 'w':
        opposition = 'b'
        moves = ((x+2, y-2), (x+2, y+2))
    else:
        opposition = 'w'
        moves = ((x-2, y-2), (x-2, y+2))

    capture_moves = [[current_position, move] for move in moves if valid_index(move, len(current_board))
         and capture_spot_check(current_position, move, current_board, opposition)]
    return capture_moves


def get_pikachu_simple_moves(current_position, current_board, player):
    x = current_position[0]
    y = current_position[1]
    board = current_board.copy()

    if player == 'w':
        moves = ((x, y-1), (x, y+1), (x+1, y), (x, y-2), (x, y+2), (x+2, y))
    else:
        moves = ((x, y-1), (x, y+1), (x-1, y), (x, y-2), (x, y+2), (x-2, y))

    return [[current_position, move] for move in moves if valid_index(move, len(current_board)) and 
            skip_spot_check(current_position, move, current_board)]

def get_pikachu_capture_moves(current_position, current_board, player):
    x = current_position[0]
    y = current_position[1]
    board = current_board.copy()

    if player == 'w':
        opposition = 'bB'
        moves = ((x, y-2), (x, y+2), (x+2, y), (x, y-3), (x, y+3), (x+3, y))
     
    else:
        opposition = 'wW'
        moves = ((x, y-2), (x, y+2), (x-2, y), (x, y-3), (x, y+3), (x-3, y))

    capture_moves = [[current_position, move] for move in moves if valid_index(move, len(current_board))
         and capture_spot_check(current_position, move, current_board, opposition)]
    return capture_moves


def get_Raichu_simple_moves(current_position, current_board, player):
    x = current_position[0]
    y = current_position[1]
    board = current_board.copy()

    moves =  [(i,y) for i in range(x-1, -1, -1)]+\
        [(i,y) for i in range(x+1, len(current_board), 1)]+\
        [(x,i) for i in range(y-1, -1, -1)]+\
        [(x,i) for i in range(y+1, len(current_board), 1)]+\
        [(i,j) for i,j in zip(range(x-1, -1, -1), range(y-1, -1, -1))]+\
        [(i,j) for i,j in zip(range(x+1, len(current_board), 1), range(y+1, len(current_board), 1))]+\
        [(i,j) for i,j in zip(range(x-1, -1, -1), range(y+1, len(current_board), 1))]+\
        [(i,j) for i,j in zip(range(x+1, len(current_board), 1), range(y-1, -1, -1))]

    return [[current_position, move] for move in moves if valid_index(move, len(current_board)) and 
            skip_spot_check(current_position, move, current_board)]

def get_Raichu_capture_moves(current_position, current_board, player):
    x = current_position[0]
    y = current_position[1]
    board = current_board.copy()

    opposition = 'bB$' if player == 'w' else 'wW@'

    moves =  [(i,y) for i in range(x-1, -1, -1)]+\
        [(i,y) for i in range(x+1, len(current_board), 1)]+\
        [(x,i) for i in range(y-1, -1, -1)]+\
        [(x,i) for i in range(y+1, len(current_board), 1)]+\
        [(i,j) for i,j in zip(range(x-1, -1, -1), range(y-1, -1, -1))]+\
        [(i,j) for i,j in zip(range(x+1, len(current_board), 1), range(y+1, len(current_board), 1))]+\
        [(i,j) for i,j in zip(range(x-1, -1, -1), range(y+1, len(current_board), 1))]+\
        [(i,j) for i,j in zip(range(x+1, len(current_board), 1), range(y-1, -1, -1))]

    capture_moves = [[current_position, move] for move in moves if valid_index(move, len(current_board))
         and capture_spot_check(current_position, move, current_board, opposition)]
    return capture_moves



def hieuristic_score(board):

    white_score = board.count('w') + 3*board.count('W') + 5*board.count('@')
    black_score = board.count('b') + 3*board.count('B') + 5*board.count('$')

    return white_score -  black_score + bonus_points(board)

def bonus_points(board):



    positions = get_piece_positions(get_board_list(board, N))

    white_raichu_current_positions = positions["@"]
    white_pichu_current_positions = positions['w']
    white_pikachu_current_positions = positions['W']

    black_raichu_current_positions = positions["$"]
    black_pichu_current_positions = positions['b']
    black_pikachu_current_positions = positions['B']    

    edge_score = sum([-2 for p in white_raichu_current_positions if p[1]  == 0 or p[1] == len(board)/N-1]) - sum([-2 for p in black_raichu_current_positions if p[1]  == 0 or p[1] == len(board)/N-1])
    pichu_center = sum([1 for p in white_pichu_current_positions if p[1]>1 and p[1]<len(board)/N-2 and p[0] > 2]) - sum([1 for p in black_pichu_current_positions if p[1]>2 and p[1]<len(board)/N-2 and p[0] < len(board)/N-3])
    pikachu_center = sum([2 for p in white_pikachu_current_positions if p[1]>0 and p[1]<len(board)/N-1 and p[0] > 2]) - sum([2 for p in black_pikachu_current_positions if p[1]>0 and p[1]<len(board)/N-1 and p[0] < len(board)/N-3])

    return edge_score + pichu_center + pikachu_center


### This function explores all possible successor moves of current board.       
def successors(current_board, player):
    raichu = '@' if player == 'w' else '$'

    positions = get_piece_positions(current_board)
    

    pichu_current_positions = positions[player]
    pikachu_current_positions = positions[player.upper()]
    raichu_current_positions = positions[raichu]

    


    pichu_simpler_moves = [get_pichu_simple_moves(m, current_board, player) for m in pichu_current_positions]
    pichu_simpler_moves = [item for sublist in pichu_simpler_moves for item in sublist]
    pichu_capture_moves = [get_pichu_capture_moves(m, current_board, player) for m in pichu_current_positions]
    pichu_capture_moves = [item for sublist in pichu_capture_moves for item in sublist]

    pikachu_simpler_moves = [get_pikachu_simple_moves(m, current_board, player) for m in pikachu_current_positions]
    pikachu_simpler_moves = [item for sublist in pikachu_simpler_moves for item in sublist]
    pikachu_capture_moves = [get_pikachu_capture_moves(m, current_board, player) for m in pikachu_current_positions]
    pikachu_capture_moves = [item for sublist in pikachu_capture_moves for item in sublist]

    raichu_simpler_moves = [get_Raichu_simple_moves(m, current_board, player) for m in raichu_current_positions]
    raichu_simpler_moves = [item for sublist in raichu_simpler_moves for item in sublist]
    raichu_capture_moves = [get_Raichu_capture_moves(m, current_board, player) for m in raichu_current_positions]
    raichu_capture_moves = [item for sublist in raichu_capture_moves for item in sublist]

    successor_boards = []

    for m in raichu_capture_moves:

        temp = deepcopy(current_board)
        temp[m[0][0]][m[0][1]] = '.'
        temp[m[1][0]][m[1][1]] = raichu
        temp = remove_piece(m[0], m[1], temp)

        successor_boards.append((temp, m))  

    for m in pikachu_capture_moves:

        temp = deepcopy(current_board)
        temp[m[0][0]][m[0][1]] = '.'
        temp[m[1][0]][m[1][1]] = raichu if get_promoted(m[1], player, len(current_board)) else player.upper()
        temp = remove_piece(m[0], m[1], temp)

        successor_boards.append((temp, m))   

    for m in pichu_capture_moves:

        temp = deepcopy(current_board)
        temp[m[0][0]][m[0][1]] = '.'
        temp[m[1][0]][m[1][1]] = raichu if get_promoted(m[1], player, len(current_board)) else player
        temp = remove_piece(m[0], m[1], temp)

        successor_boards.append((temp, m))

    for m in raichu_simpler_moves:

        temp = deepcopy(current_board)
        temp[m[0][0]][m[0][1]] = '.'
        temp[m[1][0]][m[1][1]] = raichu

        successor_boards.append((temp, m))

    for m in pikachu_simpler_moves:

        temp = deepcopy(current_board)
        temp[m[0][0]][m[0][1]] = '.'
        temp[m[1][0]][m[1][1]] = raichu if get_promoted(m[1], player, len(current_board)) else player.upper()

        successor_boards.append((temp, m))

    for m in pichu_simpler_moves:

        temp = deepcopy(current_board)
        temp[m[0][0]][m[0][1]] = '.'
        temp[m[1][0]][m[1][1]] = raichu if get_promoted(m[1], player, len(current_board)) else player

        successor_boards.append((temp, m))
    return successor_boards

## Check if configuration leads to winning
def winner(board):
    if board.count('b') + board.count('B') + board.count('$') == 0:
        return "white"
    elif board.count('w') + board.count('W') + board.count('@') == 0:
        return "black"
    
    return None 

### Alpha beta pruning 

def alpha_beta(current_board, depth, max_player, alpha, beta):
    player = 'w' if max_player == True else 'b'

    temp_board = deepcopy(current_board)

    if depth == 0 or winner(string_to_board(temp_board)) != None:
        return hieuristic_score(string_to_board(temp_board)), [temp_board]
    
    if max_player:
        maxEval = float('-inf')
        best_board = None
        for child_board in successors(temp_board, player):

            evaluation = alpha_beta(child_board[0], depth-1, False, alpha, beta)[0]

            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)

            if maxEval == evaluation:
                best_board = child_board

            if beta <= alpha:
                break
        
        return maxEval, best_board

    else:
        minEval = float('inf')
        best_board = None
        for child_board in successors(temp_board, 'b'):
            evaluation = alpha_beta(child_board[0], depth-1, True, alpha, beta)[0]

            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            # print("beta is :", beta, "\n")
            if minEval == evaluation:
                best_board = child_board
             
            if beta <= alpha:
                break
        
        return minEval, best_board


### Solve function which runs games and evaluates all possible options
def find_best_move(board, N, player, time_limit):
    max_depth = 1
    end_time = time.time()+float(time_limit)
    if len(board)!=N*N:
        print ("The board does not have correct tiles..")
        print ("#tiles=",len(board))
    else:
        board10 = get_board_list(board, N)

        for depth in range(2,6):

            if(time.time()>=end_time):
                break
            max_depth = depth
            if player == 'w':
                recommended_board = alpha_beta(board10, depth, True, float('-inf'), float('inf'))
            else:
                recommended_board = alpha_beta(board10, depth, False, float('-inf'), float('inf'))


            next_board = recommended_board
            time.sleep(1)
            yield string_to_board(next_board[1][0])


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
