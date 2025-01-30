import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.axes import Axes

from domain.game_state import GameState
from interface.abstract_presenter import AbstractPresenter

class CharacterPresenter(AbstractPresenter):

    def draw(self, state: GameState):
        self.display_chessboard()

    # Define the chessboard setup
    def draw_chessboard(self):
        board = np.zeros((8, 8))
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row, col] = 0.5
        return board

    # Define the pieces and their initial positions
    def add_pieces(self, ax: Axes):
        pieces = {
            "R": "♜",  # Rook
            "N": "♞",  # Knight
            "B": "♝",  # Bishop
            "Q": "♛",  # Queen
            "K": "♚",  # King
            "P": "♟",  # Pawn
        }

        # Initial chess positions (simplified for demonstration)
        initial_positions = {
            (0, 0): "R", (0, 7): "R", (7, 0): "R", (7, 7): "R",  # Rooks
            (0, 1): "N", (0, 6): "N", (7, 1): "N", (7, 6): "N",  # Knights
            (0, 2): "B", (0, 5): "B", (7, 2): "B", (7, 5): "B",  # Bishops
            (0, 3): "Q", (0, 4): "K", (7, 3): "Q", (7, 4): "K",  # Queen and King
        }

        for col in range(8):
            initial_positions[(1, col)] = "P"  # Black Pawns
            initial_positions[(6, col)] = "P"  # White Pawns

        for (row, col), piece in initial_positions.items():
            ax.text(col + 0.5, 7 - row + 0.5, pieces[piece], fontsize=24, ha='center', va='center', color='k' if row < 2 else 'white')

    # Main function to display the board
    def display_chessboard(self):
        board = self.draw_chessboard()
        fig, ax = plt.subplots(figsize=(8, 8))

        # Draw the chessboard
        ax.imshow(board, cmap="Accent", extent=(0, 8, 0, 8))

        # Add grid lines
        for x in range(9):
            ax.axhline(x, color='black', linewidth=0.5)
            ax.axvline(x, color='black', linewidth=0.5)

        # Add pieces to the board
        self.add_pieces(ax)

        highlight_rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='none', visible=False)
        ax.add_patch(highlight_rect)

        def on_press(event):
            if event.inaxes == ax:
                x, y = int(event.xdata), int(event.ydata)
                print(x,y)

                xy = (float(x), float(y))

                highlight_rect.set_xy(xy)  # Move the rectangle to the clicked square
                highlight_rect.set_visible(True)  # Make the rectangle visible
                fig.canvas.draw()

        fig.canvas.mpl_connect("button_press_event", on_press)

        plt.show()