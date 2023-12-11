import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        # Variable to track the current player (X or O)
        self.current_player = "X"

        # Variable to track the AI difficulty level
        self.difficulty_level = tk.StringVar()
        self.difficulty_level.set("easy")

        # Create buttons for the Tic-Tac-Toe grid
        self.buttons = [[None, None, None] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(root, text="", font=("Helvetica", 24), width=6, height=3,
                                              command=lambda i=i, j=j: self.on_button_click(i, j))
                self.buttons[i][j].grid(row=i, column=j)

        # Create buttons for difficulty level
        easy_button = tk.Button(root, text="Easy", command=lambda: self.set_difficulty("easy"))
        easy_button.grid(row=0, column=3, padx=10, pady=10)

        hard_button = tk.Button(root, text="Hard", command=lambda: self.set_difficulty("hard"))
        hard_button.grid(row=1, column=3, padx=10, pady=10)

    def on_button_click(self, i, j):
        # Check if the button is already clicked or if the game is over
        if self.buttons[i][j]["text"] == "" and not self.check_winner():
            # Update the button text with the current player
            self.buttons[i][j]["text"] = self.current_player

            # Check for a winner after each move
            winner = self.check_winner()
            if winner:
                messagebox.showinfo("Tic-Tac-Toe", f"Player {winner} wins!")
                self.reset_game()
            elif self.is_board_full():
                messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                self.reset_game()
            else:
                # Switch to the other player
                self.current_player = "O"

                # Computer's move (AI)
                self.computer_move()

                # Check for a winner after the computer's move
                winner = self.check_winner()
                if winner:
                    messagebox.showinfo("Tic-Tac-Toe", f"Player {winner} wins!")
                    self.reset_game()
                elif self.is_board_full():
                    messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
                    self.reset_game()
                else:
                    # Switch back to the player
                    self.current_player = "X"

    def computer_move(self):
        if self.difficulty_level.get() == "easy":
            self.computer_move_easy()
        elif self.difficulty_level.get() == "hard":
            self.computer_move_hard()

    def computer_move_easy(self):
        # Basic AI: Randomly choose an empty cell for the computer's move
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]["text"] == ""]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.buttons[i][j]["text"] = "O"

    def computer_move_hard(self):
        best_score, best_move = self.minimax_alpha_beta(float('-inf'), float('inf'), True)
        if best_move:
            i, j = best_move
            self.buttons[i][j]["text"] = "O"

    def minimax_alpha_beta(self, alpha, beta, is_maximizing):
        winner = self.check_winner()

        if winner == "O":
            return 1, None
        elif winner == "X":
            return -1, None
        elif self.is_board_full():
            return 0, None

        best_move = None

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = "O"
                        score, _ = self.minimax_alpha_beta(alpha, beta, False)
                        self.buttons[i][j]["text"] = ""  # Undo the move

                        if score > best_score:
                            best_score = score
                            best_move = (i, j)

                        alpha = max(alpha, best_score)
                        if alpha >= beta:
                            break  # Beta cut-off
            return best_score, best_move
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = "X"
                        score, _ = self.minimax_alpha_beta(alpha, beta, True)
                        self.buttons[i][j]["text"] = ""  # Undo the move

                        if score < best_score:
                            best_score = score
                            best_move = (i, j)

                        beta = min(beta, best_score)
                        if alpha >= beta:
                            break  # Alpha cut-off
            return best_score, best_move

    def check_winner(self):
        # Check rows, columns, and diagonals for a winner
        for i in range(3):
            if self.buttons[i][0]["text"] == self.buttons[i][1]["text"] == self.buttons[i][2]["text"] != "":
                return self.buttons[i][0]["text"]
            if self.buttons[0][i]["text"] == self.buttons[1][i]["text"] == self.buttons[2][i]["text"] != "":
                return self.buttons[0][i]["text"]

        if self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != "":
            return self.buttons[0][0]["text"]
        if self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != "":
            return self.buttons[0][2]["text"]

        return None

    def is_board_full(self):
        # Check if the board is full (a draw)
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    return False
        return True

    def reset_game(self):
        # Reset the game by clearing button texts
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""

        # Reset the current player to "X"
        self.current_player = "X"

    def set_difficulty(self, level):
        self.difficulty_level.set(level)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
