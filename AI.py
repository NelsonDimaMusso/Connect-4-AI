import time
import math
import random
from typing import List, Tuple, Optional

ROWS = 6
COLS = 12
WIN_COUNT = 4
MAX_TIME = 9.96  # Time limit in seconds

def is_terminal(board: List[List[int]]) -> bool:
    if check_winner(board) != 0:
        return True
    return is_board_full(board)

def ai_decision(board: List[List[int]]) -> int:
    start_time = time.time()
    
    # Iterative deepening with Alpha-Beta pruning
    best_column = 0
    depth = 1
    
    while depth <= 6:  # MAX_DEPTH
        if time.time() - start_time > MAX_TIME * 0.4:
            break
                
        try:
            column = alpha_beta_search(board, depth, start_time)
            if column is not None:
                best_column = column
            depth += 1
        except TimeoutError:
            break
                
    return best_column

def alpha_beta_search(board: List[List[int]], max_depth: int, start_time: float) -> Optional[int]:
    if time.time() - start_time >= MAX_TIME:
        raise TimeoutError()
    
    _, best_column = max_value(board, -math.inf, math.inf, 0, max_depth, start_time)
    return best_column

def max_value(board: List[List[int]], alpha: float, beta: float, 
              depth: int, max_depth: int, start_time: float) -> Tuple[float, Optional[int]]:
    
    if time.time() - start_time >= MAX_TIME:
        raise TimeoutError()

    if is_terminal(board) or depth >= max_depth:
        return evaluate_utility(board, depth), None
        
    value = -math.inf
    best_column = None
    
    for column in get_valid_columns(board):
        new_board = make_move(board, column, 1)  # PLAYER_1
        min_val, _ = min_value(new_board, alpha, beta, depth + 1, max_depth, start_time)
        
        if min_val > value:
            value = min_val
            best_column = column
            
        if value >= beta:
            return value, best_column
            
        alpha = max(alpha, value)
        
    return value, best_column

def min_value(board: List[List[int]], alpha: float, beta: float,
              depth: int, max_depth: int, start_time: float) -> Tuple[float, Optional[int]]:
    
    if time.time() - start_time >= MAX_TIME:
        raise TimeoutError()

    if is_terminal(board) or depth >= max_depth:
        return evaluate_utility(board, depth), None
        
    value = math.inf
    best_column = None
    
    for column in get_valid_columns(board):
        new_board = make_move(board, column, -1)  # PLAYER_2
        max_val, _ = max_value(new_board, alpha, beta, depth + 1, max_depth, start_time)
        
        if max_val < value:
            value = max_val
            best_column = column
            
        if value <= alpha:
            return value, best_column
            
        beta = min(beta, value)
        
    return value, best_column

def evaluate_utility(board: List[List[int]], depth: int) -> float:
    winner = check_winner(board)
    
    if winner == 1:  # PLAYER_1
        return 1000 - depth  # Prefer quick wins
    elif winner == -1:  # PLAYER_2
        return -1000 + depth  # Prefer delayed losses
    elif is_board_full(board):
        return 0  # Draw
    else:
        return evaluate_board(board)  # Heuristic evaluation

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
    center_column = COLS // 2
    for row in range(ROWS):
        if board[row][center_column] == 1:  # PLAYER_1
            score += 3
    
    return score

def evaluate_window(window: List[int]) -> float:
    score = 0
    player1_count = window.count(1)
    player2_count = window.count(-1)
    empty_count = window.count(0)
    
    # If both players are in the window, it's neutral
    if player1_count > 0 and player2_count > 0:
        return 0
    
    # Evaluation for our player
    if player1_count == 4:
        score += 1000
    elif player1_count == 3 and empty_count == 1:
        score += 50
    elif player1_count == 2 and empty_count == 2:
        score += 10
    elif player1_count == 1 and empty_count == 3:
        score += 1
    
    # Defensive evaluation for opponent
    if player2_count == 4:
        score -= 1000
    elif player2_count == 3 and empty_count == 1:
        score -= 80  # Important to block
    elif player2_count == 2 and empty_count == 2:
        score -= 15
    elif player2_count == 1 and empty_count == 3:
        score -= 2
    
    return score

def get_valid_columns(board: List[List[int]]) -> List[int]:
    valid_columns = []
    for col in range(COLS):
        if board[0][col] == 0:  # EMPTY
            valid_columns.append(col)
    return valid_columns

def make_move(board: List[List[int]], col: int, player: int) -> List[List[int]]:
    new_board = [row[:] for row in board]
    
    # Find the lowest available row
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
    
    # Check positive diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] != 0 and
                board[row][col] == board[row+1][col+1] == 
                board[row+2][col+2] == board[row+3][col+3]):
                return board[row][col]
    
    # Check negative diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] != 0 and
                board[row][col] == board[row-1][col+1] == 
                board[row-2][col+2] == board[row-3][col+3]):
                return board[row][col]
    
    return 0

def is_board_full(board: List[List[int]]) -> bool:
    return all(board[0][col] != 0 for col in range(COLS))
