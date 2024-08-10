import math

# Initialize board
def initialize_board():
    return [' ' for _ in range(9)]

# Print the board
def print_board(board):
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

# Check for a win
def check_win(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
                      (0, 3, 6), (1, 4, 7), (2, 5, 8), 
                      (0, 4, 8), (2, 4, 6)]
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_conditions)

# Check for a draw
def check_draw(board):
    return ' ' not in board

# Get available moves
def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == ' ']

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
        for move in available_moves(board):
            board[move] = 'O'
            score = minimax(board, depth + 1, False)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in available_moves(board):
            board[move] = 'X'
            score = minimax(board, depth + 1, True)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

# AI move
def ai_move(board):
    best_score = -math.inf
    move = None
    for possible_move in available_moves(board):
        board[possible_move] = 'O'
        score = minimax(board, 0, False)
        board[possible_move] = ' '
        if score > best_score:
            best_score = score
            move = possible_move
    board[move] = 'O'

# Player move
def player_move(board):
    move = None
    while move not in available_moves(board):
        try:
            move = int(input("Enter your move (1-9): ")) - 1
        except ValueError:
            continue
    board[move] = 'X'

# Main game loop
def play_game():
    board = initialize_board()
    print("Tic-Tac-Toe")
    print_board(board)

    while True:
        # Player move
        player_move(board)
        print_board(board)
        if check_win(board, 'X'):
            print("You win!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

        # AI move
        ai_move(board)
        print_board(board)
        if check_win(board, 'O'):
            print("AI wins!")
            break
        if check_draw(board):
            print("It's a draw!")
            break

if __name__ == '__main__':
    play_game()
