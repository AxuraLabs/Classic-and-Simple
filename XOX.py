import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)    
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def check_winner(board, player):
    # Check rows, columns, and diagonals
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    if board[0][0] == board[1][1] == board[2][2] == player:
        draw_diagonal_line(player)
        return True

    if board[2][0] == board[1][1] == board[0][2] == player:
        draw_anti_diagonal_line(player)
        return True

    return False

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)

def draw_diagonal_line(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)

def draw_anti_diagonal_line(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)

def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    return [[0, 0, 0] for _ in range(3)]

def available_square(board, row, col):
    return board[row][col] == 0

def is_board_full(board):
    return all(board[row][col] != 0 for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

def minimax(board, depth, is_maximizing, max_depth):
    if check_winner(board, 2):
        return 1
    if check_winner(board, 1):
        return -1
    if is_board_full(board):
        return 0

    if depth >= max_depth:  # Limit the depth of recursion for the AI
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(board, row, col):
                    board[row][col] = 2
                    score = minimax(board, depth + 1, False, max_depth)
                    board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(board, row, col):
                    board[row][col] = 1
                    score = minimax(board, depth + 1, True, max_depth)
                    board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    if random.random() < 0.2:  # 20% chance to make a random move
        empty_squares = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if available_square(board, row, col)]
        return random.choice(empty_squares)

    best_score = float('-inf')
    move = (0, 0)
    max_depth = 2  # Depth-limit for less optimal AI
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(board, row, col):
                board[row][col] = 2
                score = minimax(board, 0, False, max_depth)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

# Main function
board = restart_game()  # Initialize board and draw the grid
player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if available_square(board, mouseY, mouseX):
                board[mouseY][mouseX] = player
                if check_winner(board, player):
                    game_over = True
                player = 2

        if player == 2 and not game_over:
            row, col = best_move(board)
            if available_square(board, row, col):
                board[row][col] = 2
                if check_winner(board, 2):
                    game_over = True
                player = 1

        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            board = restart_game()
            player = 1
            game_over = False

    if not game_over:
        screen.fill(BG_COLOR)  # Clear the screen
        draw_lines()  # Redraw the grid
        draw_figures(board)  # Redraw the figures
        pygame.display.update()