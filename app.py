import tkinter as tk

board_size = 19 # Size of the board, 19x19 is standard for the game of Go.
cell_size = 40 # size of each cell, represented in pixels
stone_size = 18 # radius of the stone piece, represented in pixels
black, white = 'black', 'white' # Color of pieces
background = '' # Background color of the board.
click_tolerance = cell_size // 3 # Allow clicks within 1 / value of a cell's size 

board = [[None for _ in range(board_size)] for _ in range(board_size)]
current_player = black

root = tk.Tk() # Generate the TKinter screen
root.title("Go Game") # Title displayed at the top left/right
canvas = tk.Canvas(root, width= cell_size * board_size, height= cell_size * board_size, bg='green')
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
    closest_x = round((event.x - cell_size // 2) / cell_size)
    closest_y = round((event.y - cell_size // 2) / cell_size)
    
    # Calculate the exact pixel position of the closest point
    grid_x = cell_size // 2 + closest_x * cell_size
    grid_y = cell_size // 2 + closest_y * cell_size

    # Check if the click is within the tolerance range of the calculated grid point
    if (abs(event.x - grid_x) <= click_tolerance) and (abs(event.y - grid_y) <= click_tolerance):
        place_stones(closest_x, closest_y)
    else:
        print(f"Click too far from valid point: ({closest_x}, {closest_y})")
    
    print(f"Mouse Click - Pixel Position: ({event.x}, {event.y}) | Grid Position: ({closest_x}, {closest_y})")



draw_board()
canvas.bind("<Button-1>", on_click)
root.mainloop()