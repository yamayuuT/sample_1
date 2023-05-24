import tkinter as tk
import tkinter.messagebox as messagebox
import numpy as np

class ReversiBoard:
    def __init__(self, parent):
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3][3], self.board[4][4] = -1, -1
        self.board[3][4], self.board[4][3] = 1, 1
        self.current_player = 1
        self.parent = parent
        self.buttons = [[None]*8 for _ in range(8)]
        self._init_board_gui()

    def _init_board_gui(self):
        for i in range(8):
            for j in range(8):
                button = tk.Button(self.parent, command=lambda x=i, y=j: self.place_stone(x, y), height=2, width=4)
                button.grid(row=i, column=j)
                self.buttons[i][j] = button
        self._update_buttons()

    def _check_direction(self, x, y, dx, dy):
        tmp_x, tmp_y = x + dx, y + dy
        to_flip = []
        while 0 <= tmp_x < 8 and 0 <= tmp_y < 8 and self.board[tmp_x][tmp_y] == -self.current_player:
            to_flip.append((tmp_x, tmp_y))
            tmp_x += dx
            tmp_y += dy
        if 0 <= tmp_x < 8 and 0 <= tmp_y < 8 and self.board[tmp_x][tmp_y] == self.current_player:
            return to_flip
        else:
            return []

    def _flip(self, x, y):
        to_flip = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0), (-1,-1), (-1,1), (1,-1), (1,1)]:
            to_flip += self._check_direction(x, y, dx, dy)
        for flip_x, flip_y in to_flip:
            self.board[flip_x][flip_y] = self.current_player

    def can_play(self, x, y):
        if self.board[x][y] != 0:
            return False
        to_flip = []
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0), (-1,-1), (-1,1), (1,-1), (1,1)]:
            to_flip += self._check_direction(x, y, dx, dy)
        if not to_flip:
            return False
        return True

    def place_stone(self, x, y):
        if not self.can_play(x, y):
            return
        self.board[x][y] = self.current_player
        self._flip(x, y)
        self.current_player *= -1
        self._update_buttons()
        if not any(self.can_play(i, j) for i in range(8) for j in range(8)):
            self.check_end_game()

    def _update_buttons(self):
        for i in range(8):
            for j in range(8):
                text = ' '
                if self.board[i][j] == 1:
                    text = '●'
                elif self.board[i][j] == -1:
                    text = '○'
                self.buttons[i][j]['text'] = text

    def count_stone(self):
        black_stones = np.count_nonzero(self.board == 1)
        white_stones = np.count_nonzero(self.board == -1)
        return black_stones, white_stones

    def check_end_game(self):
        black_stones, white_stones = self.count_stone()
        message = "Game Over. "
        if black_stones > white_stones:
            message += "Black wins!"
        elif white_stones > black_stones:
            message += "White wins!"
        else:
            message += "It's a draw!"
        messagebox.showinfo("Game Over", message)
        self.parent.after(1000, self.parent.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    ReversiBoard(root)
    root.mainloop()
