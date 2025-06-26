import time
import importlib
from typing import List

class Referee:
    def __init__(self):
        self.ROWS = 6
        self.COLS = 12
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        
        # Force reload of both AIs
        self.reload_ais()

    def reload_ais(self):
        """Reload AI modules to take into account any changes"""
        # Reload AI A
        import ia_a
        importlib.reload(ia_a)
        from ia_a import ai_decision as ia_a_decision
        self.ia_a_func = ia_a_decision
        
        # Reload AI B
        import ia_b
        importlib.reload(ia_b)
        from ia_b import ai_decision as ia_b_decision
        self.ia_b_func = ia_b_decision

    def display_board(self):
        """Display the game board."""
        print("\n" + "=" * 50)
        print("     0  1  2  3  4  5  6  7  8  9 10 11")
        print("   " + "-" * 38)
        for row in range(self.ROWS):
            print(f"{row} |", end=" ")
            for col in range(self.COLS):
                if self.board[row][col] == 0:
                    print(" .", end=" ")
                elif self.board[row][col] == 1:
                    print(" A", end=" ")
                else:
                    print(" B", end=" ")
            print(" |")
        print("   " + "-" * 38)
        print("=" * 50 + "\n")

    def make_move(self, col: int, player: int) -> bool:
        """Play a move on the board."""
        if col is None or col < 0 or col >= self.COLS or self.board[0][col] != 0:
            return False
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return True
        return False

    def check_winner(self):
        """Check the 4 possible directions for a winner"""
        # Horizontal
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if (self.board[row][col] != 0 and 
                    self.board[row][col] == self.board[row][col+1] == 
                    self.board[row][col+2] == self.board[row][col+3]):
                    return self.board[row][col]
        
        # Vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if (self.board[row][col] != 0 and 
                    self.board[row][col] == self.board[row+1][col] == 
                    self.board[row+2][col] == self.board[row+3][col]):
                    return self.board[row][col]
        
        # Downward diagonal
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if (self.board[row][col] != 0 and 
                    self.board[row][col] == self.board[row+1][col+1] == 
                    self.board[row+2][col+2] == self.board[row+3][col+3]):
                    return self.board[row][col]
        
        # Upward diagonal
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                if (self.board[row][col] != 0 and 
                    self.board[row][col] == self.board[row-1][col+1] == 
                    self.board[row-2][col+2] == self.board[row-3][col+3]):
                    return self.board[row][col]
        
        return 0

    def is_board_full(self) -> bool:
        """Check if the board is full."""
        return all(self.board[0][col] != 0 for col in range(self.COLS))

    def run_match(self):
        """Run a match between the two AIs."""
        print("=== STARTING MATCH: AI A vs AI B ===")
        current_player = -1
        turn_number = 1

        while True:
            self.display_board()
            if self.check_winner() != 0 or self.is_board_full():
                break

            start_time = time.time()
            print(f"Turn {turn_number}")
            turn_number += 1
            
            if current_player == 1:
                col = self.ia_a_func(self.board)
                print(f"AI A plays column {col} (time: {time.time() - start_time:.2f}s)")
            else:
                col = self.ia_b_func(self.board)
                print(f"AI B plays column {col} (time: {time.time() - start_time:.2f}s)")

            if not self.make_move(col, current_player):
                print(f"Error: invalid move in column {col}!")
                break
            current_player *= -1

        # Final result
        winner = self.check_winner()
        self.display_board()
        if winner == 1:
            print("AI A wins!")
        elif winner == -1:
            print("AI B wins!")
        else:
            print("It's a draw!")

if __name__ == "__main__":
    referee = Referee()
    referee.run_match()