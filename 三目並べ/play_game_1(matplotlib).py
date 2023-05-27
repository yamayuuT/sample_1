import matplotlib.pyplot as plt
import numpy as np
import random

# Game board
board = np.zeros((3,3), dtype=int)

def draw_board(board):
    plt.clf()
    plt.grid(True)
    plt.xticks([0,1,2])
    plt.yticks([0,1,2])
    for i in range(3):
        for j in range(3):
            if board[i,j] == 1:
                plt.text(j, i, 'X', fontsize=30, ha='center', va='center')
            elif board[i,j] == -1:
                plt.text(j, i, 'O', fontsize=30, ha='center', va='center')
    plt.pause(0.01)

def check_win(board):
    for i in range(3):
        if abs(sum(board[i,:])) == 3:
            return True
        if abs(sum(board[:,i])) == 3:
            return True
    if abs(board[0,0] + board[1,1] + board[2,2]) == 3:
        return True
    if abs(board[0,2] + board[1,1] + board[2,0]) == 3:
        return True
    return False

def cpu_move(board):
    while True:
        move = random.randint(0, 8)
        if board[move//3, move%3] == 0:
            board[move//3, move%3] = -1
            break

def onclick(event):
    x = int(round(event.xdata))
    y = int(round(event.ydata))
    if board[y,x] == 0:
        board[y,x] = 1
        draw_board(board)
        if check_win(board):
            print("Player 1 wins!")
            plt.close()
        elif 0 not in [board[i,j] for i in range(3) for j in range(3)]:
            print("The game is a draw!")
            plt.close()
        else:
            cpu_move(board)
            draw_board(board)
            if check_win(board):
                print("CPU wins!")
                plt.close()
            elif 0 not in [board[i,j] for i in range(3) for j in range(3)]:
                print("The game is a draw!")
                plt.close()

# Game loop
fig = plt.figure()
fig.canvas.mpl_connect('button_press_event', onclick)
draw_board(board)
plt.show()
