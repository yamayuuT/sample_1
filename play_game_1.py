import pygame
import random
import sys

# Game settings
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH//COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Game board
board = [['' for _ in range(ROWS)] for _ in range(COLS)]

def draw_board():
    WIN.fill(WHITE)
    for i in range(1, ROWS):
        pygame.draw.line(WIN, BLACK, (0, i*SQUARE_SIZE), (WIDTH, i*SQUARE_SIZE))
        pygame.draw.line(WIN, BLACK, (i*SQUARE_SIZE, 0), (i*SQUARE_SIZE, HEIGHT))
    pygame.display.update()

def draw_piece(row, col, piece):
    if piece == 'X':
        pygame.draw.line(WIN, BLACK, (col*SQUARE_SIZE+15, row*SQUARE_SIZE+15), (col*SQUARE_SIZE+SQUARE_SIZE-15, row*SQUARE_SIZE+SQUARE_SIZE-15), 4)
        pygame.draw.line(WIN, BLACK, (col*SQUARE_SIZE+15, row*SQUARE_SIZE+SQUARE_SIZE-15), (col*SQUARE_SIZE+SQUARE_SIZE-15, row*SQUARE_SIZE+15), 4)
    elif piece == 'O':
        pygame.draw.circle(WIN, BLACK, (col*SQUARE_SIZE+SQUARE_SIZE//2, row*SQUARE_SIZE+SQUARE_SIZE//2), 30, 4)
    pygame.display.update()

def check_win(board):
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != '':
            return True
    for col in range(len(board[0])):
        check = []
        for row in board:
            check.append(row[col])
        if check.count(check[0]) == len(check) and check[0] != '':
            return True
    if board[0][0] == board[1][1] == board[2][2] != '':
        return True
    if board[0][2] == board[1][1] == board[2][0] != '':
        return True
    return False

def cpu_move(board):
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == '':
            board[row][col] = 'O'
            draw_piece(row, col, 'O')
            break

def main():
    clock = pygame.time.Clock()
    run = True
    turn = 'X'
    draw_board()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                if board[row][col] == '':
                    board[row][col] = turn
                    draw_piece(row, col, turn)
                    if check_win(board):
                        print(f'{turn} wins!')
                        pygame.time.wait(3000)
                        run = False
                    elif '' not in [board[i][j] for i in range(ROWS) for j in range(COLS)]:
                        print('Draw!')
                        pygame.time.wait(3000)
                        run = False
                    else:
                        turn = 'O' if turn == 'X' else 'X'
                        if turn == 'O':
                            cpu_move(board)
                            if check_win(board):
                                print('O wins!')
                                pygame.time.wait(3000)
                                run = False
                            elif '' not in [board[i][j] for i in range(ROWS) for j in range(COLS)]:
                                print('Draw!')
                                pygame.time.wait(3000)
                                run = False
                            else:
                                turn = 'X'
        pygame.time.wait(100)

    pygame.quit()

if __name__ == "__main__":
    main()
