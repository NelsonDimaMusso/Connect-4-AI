import time
import math
import random
from typing import List, Tuple, Optional

ROWS = 6
COLS = 12
WIN_COUNT = 4
MAX_TIME = 9.96  # Limite de temps en secondes

def Terminal_Test(board: List[List[int]]) -> bool:
    if check_winner(board) != 0:
        return True
    return is_board_full(board)

def IA_Decision(board: List[List[int]]) -> int:
    start_time = time.time()
    
    # Recherche Alpha-Beta avec profondeur croissante
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

    if Terminal_Test(board) or depth >= max_depth:
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

    if Terminal_Test(board) or depth >= max_depth:
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
        return 1000 - depth  # Victoire rapide préférée
    elif winner == -1:  # PLAYER_2
        return -1000 + depth  # Défaite retardée préférée
    elif is_board_full(board):
        return 0  # Match nul
    else:
        # Évaluation heuristique
        return evaluate_board(board)

def evaluate_board(board: List[List[int]]) -> float:
    score = 0
    
    # Évaluer toutes les fenêtres de 4 cases
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
    
    # Diagonal positive
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window)
    
    # Diagonal négative
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window)
    
    # Bonus pour les colonnes centrales
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
    
    # Si les deux joueurs sont dans la même fenêtre, pas d'intérêt
    if player1_count > 0 and player2_count > 0:
        return 0
    
    # Évaluation pour notre joueur
    if player1_count == 4:
        score += 1000
    elif player1_count == 3 and empty_count == 1:
        score += 50
    elif player1_count == 2 and empty_count == 2:
        score += 10
    elif player1_count == 1 and empty_count == 3:
        score += 1
    
    # Évaluation pour l'adversaire (défensive)
    if player2_count == 4:
        score -= 1000
    elif player2_count == 3 and empty_count == 1:
        score -= 80  # Plus important de bloquer
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
    
    # Trouver la ligne la plus basse disponible
    for row in range(ROWS - 1, -1, -1):
        if new_board[row][col] == 0:  # EMPTY
            new_board[row][col] = player
            break
            
    return new_board

def check_winner(board: List[List[int]]) -> int:
    # Vérifier horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] != 0 and
                board[row][col] == board[row][col+1] == 
                board[row][col+2] == board[row][col+3]):
                return board[row][col]
    
    # Vérifier vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] != 0 and
                board[row][col] == board[row+1][col] == 
                board[row+2][col] == board[row+3][col]):
                return board[row][col]
    
    # Vérifier diagonal montante
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] != 0 and
                board[row][col] == board[row+1][col+1] == 
                board[row+2][col+2] == board[row+3][col+3]):
                return board[row][col]
    
    # Vérifier diagonal descendante
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