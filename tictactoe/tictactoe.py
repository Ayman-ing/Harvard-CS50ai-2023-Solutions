"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None

import copy
def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = 0
    count_O = 0
    for i in board:
        for j in i:
            if j == X:
                count_X = count_X + 1
            elif j == O:
                count_O = count_O + 1
    if count_X == count_O:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.add((i, j))
    
    return action

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    if len(action) != 2 :
        print(action)
    else:

        if player(new_board) == X:
            new_board[action[0]][action[1]] = X
        else:
            new_board[action[0]][action[1]] = O 
    return(new_board)
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and (board[i][0] != EMPTY or  board[i][1]!= EMPTY or board[i][2]!= EMPTY):
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and (board[0][i] != EMPTY or board[1][i]!= EMPTY or board[2][i]!= EMPTY):
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and (board[0][0] != EMPTY or board[1][1]!= EMPTY or board[1][1]!= EMPTY):
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and (board[0][2] != EMPTY or board[2][0]!=EMPTY or board[1][1]!=EMPTY):
        return board[0][2]
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != None:
        return True
    elif actions(board) == set():
        return True 
    else : 
        return False 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else :
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        if terminal(board):
            return utility(board)
        else:
            v = -1
            for action in actions(board):
                value = min_value(result(board, action))
                if value == 1:
                    return 1
                else:
                    v = max(v,value)
            return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        else:
            v = 1
            for action in actions(board):
                value = max_value(result(board, action))
                if value == -1:
                    return -1
                
                else:
                    v = min(v,value)
            return v
    if terminal(board):
        return None
    if board == initial_state():
        return (1,1)
    if player(board) == X:
        v = -1
        
        act = actions(board)
        for action in act:
            if terminal(result(board,action)) and utility(result(board,action))==1:
                return action
        for action in act:
            
            value = min_value(result(board, action))
            if value == 1:
                return action
            elif value > v:
                v = value
                move = action
        return move
    else:
        v = 1
        
        act = actions(board)
        for action in act:
            if terminal(result(board,action)) and utility(result(board,action))==-1:
                return action
        for action in act:
            value = max_value(result(board, action))
            if value == -1:
                return action
            elif value < v:
                v = value
                move = action
        return move
