import time
import math
import random
from typing import List, Tuple, Optional

ROWS = 6
COLS = 12
WIN_COUNT = 4
MAX_TIME = 9.96  # Time limit in seconds

class ConnectFour:
    def __init__(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.player = 1  # 1 = AI, -1 = human

    def __str__(self):
        s = "  " + "   ".join(str(i) for i in range(COLS)) + "\n"
        s += "┌" + ("───┬" * (COLS - 1)) + "───┐\n"
        for i, row in enumerate(self.board):
            s += "│ " + " │ ".join('R' if cell == 1 else 'Y' if cell == -1 else ' ' for cell in row) + " │\n"
            if i < len(self.board) - 1:
                s += "├" + ("───┼" * (COLS - 1)) + "───┤\n"
        s += "└" + ("───┴" * (COLS - 1)) + "───┘\n"
        return s

def is_terminal(board: List[List[int]]) -> bool:
    if check_winner(board) != 0:
        return True
    return is_board_full(board)

def ai_decision(board: List[List[int]]) -> int:
    start_time = time.time()

    best_col = 0
    depth = 1

    while depth <= 6:  # MAX_DEPTH
        if time.time() - start_time > MAX_TIME * 0.4:
            break

        try:
            col = alpha_beta_search(board, depth, start_time)
            if col is not None:
                best_col = col
            depth += 1
        except TimeoutError:
            break

    return best_col

def alpha_beta_search(board: List[List[int]], max_depth: int, start_time: float) -> Optional[int]:
    if time.time() - start_time >= MAX_TIME:
        raise TimeoutError()

    _, best_col = max_value(board, -math.inf, math.inf, 0, max_depth, start_time)
    return best_col

def max_value(board: List[List[int]], alpha: float, beta: float,
              depth: int, max_depth: int, start_time: float) -> Tuple[float, Optional[int]]:
    if time.time() - start_time >= MAX_TIME:
        raise TimeoutError()

    if is_terminal(board) or depth >= max_depth:
        return utility(board, depth), None

    v = -math.inf
    best_col = None

    for col in get_valid_columns(board):
        new_board = make_move(board, col, 1)  # PLAYER_1
        min_val, _ = min_value(new_board, alpha, beta, depth + 1, max_depth, start_time)

        if min_val > v:
            v = min_val
            best_col = col

        if v >= beta:
            return v, best_col

        alpha = max(alpha, v)

    return v, best_col

def min_value(board: List[List[int]], alpha: float, beta: float,
              depth: int, max_depth: int, start_time: float) -> Tuple[float, Optional[int]]:
    if time.time() - start_time >= MAX_TIME:
        raise TimeoutError()

    if is_terminal(board) or depth >= max_depth:
        return utility(board, depth), None

    v = math.inf
    best_col = None

    for col in get_valid_columns(board):
        new_board = make_move(board, col, -1)  # PLAYER_2
        max_val, _ = max_value(new_board, alpha, beta, depth + 1, max_depth, start_time)

        if max_val < v:
            v = max_val
            best_col = col

        if v <= alpha:
            return v, best_col

        beta = min(beta, v)

    return v, best_col

def utility(board: List[List[int]], depth: int) -> float:
    winner = check_winner(board)

    if winner == 1:  # PLAYER_1
        return 1000 - depth  # Faster win is preferred
    elif winner == -1:  # PLAYER_2
        return -1000 + depth  # Delayed loss is preferred
    elif is_board_full(board):
        return 0  # Draw
    else:
        return evaluate_board(board)

def evaluate_board(board: List[List[int]]) -> float:
    score = 0

    # Evaluate all 4-cell windows
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = [board[row][col + i] for i in range(4)]
            score += evaluate_window(window)

    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            window = [board[row + i][col] for i in range(4)]
            score += evaluate_window(window)

    # Positive diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window)

    # Negative diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window)

    # Bonus for center column
    center_col = COLS // 2
    for row in range(ROWS):
        if board[row][center_col] == 1:  # PLAYER_1
            score += 3

    return score

def evaluate_window(window: List[int]) -> float:
    score = 0
    player1_count = window.count(1)   # PLAYER_1
    player2_count = window.count(-1)  # PLAYER_2
    empty_count = window.count(0)     # EMPTY

    # Ignore windows with both players
    if player1_count > 0 and player2_count > 0:
        return 0

    # Offensive evaluation
    if player1_count == 4:
        score += 1000
    elif player1_count == 3 and empty_count == 1:
        score += 50
    elif player1_count == 2 and empty_count == 2:
        score += 10
    elif player1_count == 1 and empty_count == 3:
        score += 1

    # Defensive evaluation
    if player2_count == 4:
        score -= 1000
    elif player2_count == 3 and empty_count == 1:
        score -= 80  # More important to block
    elif player2_count == 2 and empty_count == 2:
        score -= 15
    elif player2_count == 1 and empty_count == 3:
        score -= 2

    return score

def get_valid_columns(board: List[List[int]]) -> List[int]:
    valid_cols = []
    for col in range(COLS):
        if board[0][col] == 0:  # EMPTY
            valid_cols.append(col)
    return valid_cols

def make_move(board: List[List[int]], col: int, player: int) -> List[List[int]]:
    new_board = [row[:] for row in board]

    # Find lowest empty row
    for row in range(ROWS - 1, -1, -1):
        if new_board[row][col] == 0:  # EMPTY
            new_board[row][col] = player
            break

    return new_board

def check_winner(board: List[List[int]]) -> int:
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] != 0 and
                board[row][col] == board[row][col+1] ==
                board[row][col+2] == board[row][col+3]):
                return board[row][col]

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] != 0 and
                board[row][col] == board[row+1][col] ==
                board[row+2][col] == board[row+3][col]):
                return board[row][col]

    # Check upward diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] != 0 and
                board[row][col] == board[row+1][col+1] ==
                board[row+2][col+2] == board[row+3][col+3]):
                return board[row][col]

    # Check downward diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] != 0 and
                board[row][col] == board[row-1][col+1] ==
                board[row-2][col+2] == board[row-3][col+3]):
                return board[row][col]

    return 0

def is_board_full(board: List[List[int]]) -> bool:
    return all(board[0][col] != 0 for col in range(COLS))

def random_valid_move(board: List[List[int]]) -> Optional[int]:
    valid = get_valid_columns(board)
    return random.choice(valid) if valid else None

def play_game():
    game = ConnectFour()
    print("Connect Four: 1 for AI (R), 2 for human (Y)")
    first = int(input("Choose who starts (1=AI, 2=human): "))
    if first == 2:
        game.player = -1
    print(game)
    turn = 0

    while not is_terminal(game.board):
        turn += 1
        print("Turn:", turn)
        print("\n\n")
        if game.player == -1:
            try:
                action = int(input(f"Human (Y), enter column (0-{COLS - 1}): "))
            except ValueError:
                print("Invalid input. Try again.")
                continue
            if action not in get_valid_columns(game.board):
                print("Invalid move. Try again.")
                continue
            print("Human plays:", action)
        else:
            print("AI is thinking...")
            action = ai_decision(game.board)
            print("AI plays:", action)

        game.board = make_move(game.board, action, game.player)
        game.player = -game.player
        print(game)

    winner = check_winner(game.board)
    if winner == 1:
        print("AI wins!")
    elif winner == -1:
        print("Human wins!")
    else:
        print("Draw!")

if __name__ == "__main__":
    play_game()
