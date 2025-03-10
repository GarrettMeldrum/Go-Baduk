import tkinter as tk

board_size = 19 # Size of the board, 19x19 is standard for the game of Go.
cell_size = 40 # size of each cell, represented in pixels
stone_size = 18 # radius of the stone piece, represented in pixels
black, white = 'black', 'white' # Color of pieces

board = [[None for _ in range(board_size)] for _ in range(board_size)]
current_player = black

root = tk.Tk()
root.title("Go Game")
canvas = tk.Canvas(root, width=cell_size * board_size, height=cell_size * board_size, bg='green')
canvas.pack()

def draw_board():
    for i in range(BOARD_SIZE):
        # Draw horizontal lines
        canvas.create_line(CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE,
                          CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE, CELL_SIZE // 2 + i * CELL_SIZE)
        # Draw vertical lines
        canvas.create_line(CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2,
                           CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE)



root.mainloop()