import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
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
TEXT_COLOR = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Fonts
font = pygame.font.Font(None, 80)
small_font = pygame.font.Font(None, 40)

# Initialize board
def initialize_board():
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Draw lines on the board
def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Draw figures (X and O)
def draw_figures(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), 
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

# Display message on screen
def display_message(message):
    text = font.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    subtext = small_font.render('Press R to Restart', True, TEXT_COLOR)
    subtext_rect = subtext.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(subtext, subtext_rect)

# Check for a win
def check_win(board, player):
    # Vertical and Horizontal
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[2][0] == board[1][1] == board[0][2] == player:
        return True
    return False

# Check for a draw
def check_draw(board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_win(board, 'O'):
        return 1
    if check_win(board, 'X'):
        return -1
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ' '
                    best_score = min(score, best_score)
        return best_score

# AI move
def ai_move(board):
    best_score = -math.inf
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                score = minimax(board, 0, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move:
        board[move[0]][move[1]] = 'O'

# Restart the game
def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    return initialize_board()

# Main game loop
def play_game():
    board = restart()
    draw_lines()
    player_turn = True
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] == ' ' and player_turn:
                    board[clicked_row][clicked_col] = 'X'
                    player_turn = False
                    draw_figures(board)

                    if check_win(board, 'X'):
                        display_message("You Win!")
                        game_over = True
                    elif check_draw(board):
                        display_message("It's a Draw!")
                        game_over = True

                    if not game_over:
                        # AI move
                        ai_move(board)
                        draw_figures(board)

                        if check_win(board, 'O'):
                            display_message("AI Wins!")
                            game_over = True
                        elif check_draw(board):
                            display_message("It's a Draw!")
                            game_over = True

                    player_turn = True

            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                board = restart()
                game_over = False
                player_turn = True

        pygame.display.update()

if __name__ == '__main__':
    play_game()
