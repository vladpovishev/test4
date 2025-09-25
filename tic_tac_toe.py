"""Simple Tic Tac Toe game with a Tkinter GUI.

The application renders a 3x3 grid of buttons that players use to place
X and O marks.  The game announces wins or draws and allows users to
start a fresh match with a reset button.
"""

from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MoveResult:
    """Information about the outcome of a move."""

    winner: Optional[str] = None
    draw: bool = False

    @property
    def is_finished(self) -> bool:
        return self.winner is not None or self.draw


class TicTacToeGame:
    """Encapsulates the UI and logic for a Tic Tac Toe game."""

    SIZE: int = 3

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)

        self.current_player: str = "X"
        self.board: List[List[str]] = [["" for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.buttons: List[List[tk.Button]] = []
        self.game_over: bool = False

        self.status_label = tk.Label(self.root, text=self._status_text(), font=("Helvetica", 16))
        self.status_label.grid(row=0, column=0, columnspan=self.SIZE, pady=(10, 5))

        self._create_board()

        reset_button = tk.Button(
            self.root,
            text="Reset",
            font=("Helvetica", 12),
            command=self.reset,
            width=10,
        )
        reset_button.grid(row=self.SIZE + 1, column=0, columnspan=self.SIZE, pady=(10, 10))

    def _create_board(self) -> None:
        board_frame = tk.Frame(self.root)
        board_frame.grid(row=1, column=0, columnspan=self.SIZE)

        for row in range(self.SIZE):
            button_row: List[tk.Button] = []
            for col in range(self.SIZE):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Helvetica", 20, "bold"),
                    width=4,
                    height=2,
                    command=lambda r=row, c=col: self.handle_move(r, c),
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

    def _status_text(self) -> str:
        return f"Current player: {self.current_player}" if not self.game_over else "Game over"

    def handle_move(self, row: int, col: int) -> None:
        if self.game_over or self.board[row][col]:
            return

        self.board[row][col] = self.current_player
        self.buttons[row][col]["text"] = self.current_player

        result = self.evaluate_game()
        if result.winner:
            self.status_label.config(text=f"Player {result.winner} wins!")
            self._highlight_winner(result.winner)
            self.game_over = True
        elif result.draw:
            self.status_label.config(text="It's a draw!")
            self.game_over = True
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=self._status_text())

        if result.is_finished:
            self._disable_all_buttons()

    def _disable_all_buttons(self) -> None:
        for row in self.buttons:
            for button in row:
                button.config(state=tk.DISABLED)

    def _highlight_winner(self, winner: str) -> None:
        winning_cells = self._find_winning_cells(winner)
        for row, col in winning_cells:
            self.buttons[row][col].config(bg="#b3ffb3")

    def _find_winning_cells(self, player: str) -> List[tuple[int, int]]:
        lines = self._winning_lines()
        for line in lines:
            if all(self.board[row][col] == player for row, col in line):
                return line
        return []

    def evaluate_game(self) -> MoveResult:
        lines = self._winning_lines()
        for line in lines:
            values = {self.board[row][col] for row, col in line}
            if len(values) == 1 and "" not in values:
                (row, col) = line[0]
                return MoveResult(winner=self.board[row][col])

        if all(self.board[row][col] for row in range(self.SIZE) for col in range(self.SIZE)):
            return MoveResult(draw=True)

        return MoveResult()

    def _winning_lines(self) -> List[List[tuple[int, int]]]:
        lines: List[List[tuple[int, int]]] = []

        # Rows and columns
        for index in range(self.SIZE):
            lines.append([(index, col) for col in range(self.SIZE)])
            lines.append([(row, index) for row in range(self.SIZE)])

        # Diagonals
        lines.append([(i, i) for i in range(self.SIZE)])
        lines.append([(i, self.SIZE - 1 - i) for i in range(self.SIZE)])

        return lines

    def reset(self) -> None:
        self.current_player = "X"
        self.board = [["" for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.game_over = False
        self.status_label.config(text=self._status_text())

        for row in self.buttons:
            for button in row:
                button.config(text="", bg=self.root.cget("bg"), state=tk.NORMAL)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    TicTacToeGame().run()


if __name__ == "__main__":
    main()
