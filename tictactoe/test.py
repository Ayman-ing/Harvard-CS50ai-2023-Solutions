import tictactoe as ttt
X = "X"
O = "O"
EMPTY = None
board=ttt.initial_state()
board=[[X, O,X],
       [EMPTY, X, EMPTY],
       [X, EMPTY, O]]
player=ttt.player(board)
print(player)
actions=ttt.actions(board)
print(actions)
for action in actions:
    print(ttt.result(board,action))
print(ttt.winner(board))
print(ttt.terminal(board))
print(ttt.minimax(board))
