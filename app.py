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

dir = os.path.dirname(os.path.abspath(__file__)) # set dir dynamically so that we can utilize images and other scripts when necessary
image_path = os.path.join(dir, 'images', 'wooden_board.png') # location of the background for our board
black_game_piece_image = os.path.join(dir, 'images', 'black_game_piece.png') # location of the black game piece
white_game_piece_image = os.path.join(dir, 'images', 'white_game_piece.png') # location of the white game piece

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


try:
    black_stone_image = Image.open(black_game_piece_image).resize((stone_size * 3, stone_size * 3))
    white_stone_image = Image.open(white_game_piece_image).resize((stone_size * 3, stone_size * 3))

    # conversion to PhotoImage for Tkinter to handle the images
    black_stone = ImageTk.PhotoImage(black_stone_image)
    white_stone = ImageTk.PhotoImage(white_stone_image)
except FileNotFoundError:
    print("Error: Stone images not found")
    black_stone = None
    white_stone = None


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

    if color == black and black_stone:
        stone_image = black_stone
    elif color == white and white_stone:
        stone_image = white_stone
    else:
        return
    

    canvas.create_image(
        cell_size // 2 + x * cell_size,
        cell_size // 2 + y * cell_size,
        image=stone_image,
        tags="stone_{}_{}".format(x,y)
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


# identify the group a stone belongs to by searching all adjacent stones of the same color
def dfs(x, y, color):
    group = [(x, y)]
    visited = set(group)

    stack = [(x, y)]

    while stack:
        cx, cy = stack.pop()

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < board_size and 0 <= ny < board_size and (nx, ny) not in visited:
                if board[ny][nx] == color:
                    group.append((nx, ny))
                    visited.add((nx, ny))
                    stack.append((nx, ny))
    
    return group


# check liberties of a group.
def check_liberties(group):
    liberties = set()

    for x, y in group:
        # check the adjacent cells
        for dx, dy in [(-1,0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < board_size and 0 <= ny < board_size:
                if board[ny][nx] is None: # Empty space liberty
                    liberties.add((nx, ny))
    
    return liberties


# check if any opponent's group is surrounded (has no liberties left)
def capture_stones():
    captured_stones = []
    for y in range(board_size):
        for x in range(board_size):
            if board[y][x] is not None:
                color = board[y][x]

                group = dfs(x, y, color)

                liberties = check_liberties(group)

                if not liberties:
                    captured_stones.extend(group)
    
    for x, y in captured_stones:
        board[y][x] = None
        canvas.delete("stone_{}_{}".format(x,y))

    return captured_stones


# execute the placing of the stones
def place_stones(x, y):

    global current_player

    print(f"Placing stone at ({x}, {y})")

    if is_valid_move(x, y):
        board[y][x] = current_player
        draw_stone(x, y, current_player)

        captured = capture_stones()

        if captured:
            print(f"Captured stones: {captured}")

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