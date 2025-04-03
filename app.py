import os
import tkinter as tk
from PIL import Image, ImageTk

'''
(1.) I am okay with the click snapping, this could possibly be addressed later though for refinement (04-02-2025)


'''



board_size = 19 # Size of the board, 19x19 is standard for the game of Go.
cell_size = 40 # size of each cell, represented in pixels
stone_size = 18 # radius of the stone piece, represented in pixels
black, white = 'black', 'white' # Color of pieces
background = '' # Background color of the board.
current_player = black # Set the starting player to black

# initiate the board size with a neat line
board = [[None for _ in range(board_size)] for _ in range(board_size)]

dir = os.path.dirname(os.path.abspath(__file__)) # Set dir dynamically so that we can utilize images and other scripts when necessary
image_path = os.path.join(dir, 'images', 'wooden_board.png') # The location of the background for our board

# Attempt to load the background texture
try:
    board_texture = Image.open(image_path)
    board_texture = board_texture.resize((cell_size * board_size, cell_size * board_size))
# If the file is not found -> print error and use the default color for the background
except FileNotFoundError:
    print("Error: Board image not found!")
    board_texture = None

# Create Tkinter(root) window
root = tk.Tk()
root.title("The Game of Go(Baduk)")
canvas = tk.Canvas(root, width=cell_size * board_size, height=cell_size * board_size)

# Display background image if loaded
if board_texture:
    root.board_image = ImageTk.PhotoImage(board_texture)  # Store reference
    canvas.create_image(0, 0, anchor='nw', image=root.board_image)

canvas.pack()


def draw_board():

    for i in range(board_size):

        # Draw horizontal lines
        canvas.create_line(cell_size // 2, cell_size // 2 + i * cell_size,
                          cell_size // 2 + (board_size - 1) * cell_size, cell_size // 2 + i * cell_size)

        # Draw vertical lines
        canvas.create_line(cell_size // 2 + i * cell_size, cell_size // 2,
                           cell_size // 2 + i * cell_size, cell_size // 2 + (board_size - 1) * cell_size)


def draw_stone(x, y, color):

    canvas.create_oval(
        cell_size // 2 + x * cell_size - stone_size,
        cell_size // 2 + y * cell_size - stone_size,
        cell_size // 2 + x * cell_size + stone_size,
        cell_size // 2 + y * cell_size + stone_size,
        fill=color
    )


def is_valid_move(x, y):
    # Extra debugging for clarity
    if not (0 <= x < board_size and 0 <= y < board_size):
        print(f"Invalid Move: Out of bounds at ({x}, {y})")
        return False

    if board[y][x] is not None:
        print(f"Invalid Move: Position ({x}, {y}) already occupied")
        return False

    return True


def place_stones(x, y):
    global current_player
    print(f"Placing stone at ({x}, {y})")
    if is_valid_move(x, y):
        board[y][x] = current_player
        draw_stone(x, y, current_player)
        current_player = white if current_player == black else black


def on_click(event):
    # Calculate grid position based on pixel coordinates
    closest_x = round((event.x - cell_size // 2) / cell_size)
    closest_y = round((event.y - cell_size // 2) / cell_size)
    
    # Calculate the exact pixel position of the closest point
    grid_x = cell_size // 2 + closest_x * cell_size
    grid_y = cell_size // 2 + closest_y * cell_size

    # Add tolerance range around the center of the cell for valid clicks
    click_tolerance = cell_size // 3

    # Check if the click is within the tolerance range of the calculated grid point
    if (abs(event.x - grid_x) <= click_tolerance) and (abs(event.y - grid_y) <= click_tolerance):
        place_stones(closest_x, closest_y)
    else:
        print(f"Click too far from valid point: ({closest_x}, {closest_y})")
    
    print(f"Mouse Click - Pixel Position: ({event.x}, {event.y}) | Grid Position: ({closest_x}, {closest_y})")


draw_board()
canvas.bind("<Button-1>", on_click)
root.mainloop()