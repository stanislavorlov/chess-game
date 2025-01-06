from Domain.Game.chess_game import ChessGame

import matplotlib.pyplot as plt
import numpy as np

class Painter:
    def __init__(self, chess_game: ChessGame):
        self._game = chess_game
        
    def draw(self):
        self.draw_chessboard()
        self.draw_pieces()

    def draw_pieces(self):
        pass

    def draw_chessboard(self):
        # Define the size of the chessboard
        board_size = 8
        square_size = 1  # Each square's size

        # Create a chessboard pattern
        chessboard = np.zeros((board_size, board_size))
        chessboard[1::2, ::2] = 1  # Black squares in odd rows
        chessboard[::2, 1::2] = 1  # Black squares in even rows

        # Files (columns) and ranks (rows) for labeling
        files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks = list(range(8, 0, -1))

        # Create the plot
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(chessboard, cmap="gray", origin="upper", extent=(0, board_size, 0, board_size))

        # Add gridlines and remove axes
        ax.set_xticks(np.arange(0, board_size + 1, square_size))
        ax.set_yticks(np.arange(0, board_size + 1, square_size))
        ax.set_xticks(np.arange(0.5, board_size, square_size), minor=True)
        ax.set_yticks(np.arange(0.5, board_size, square_size), minor=True)
        ax.grid(which="major", color="black", linestyle="-", linewidth=1)
        ax.tick_params(axis="both", which="both", length=0, labelsize=0)
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Label the files and ranks
        ax.set_xticks(np.arange(0.5, board_size, 1), minor=True)
        ax.set_xticklabels(files, minor=True, fontsize=12)
        ax.set_yticks(np.arange(0.5, board_size, 1), minor=True)
        ax.set_yticklabels(ranks, minor=True, fontsize=12)

        # Rectangle to highlight the square (initially invisible)
        highlight = plt.Rectangle((0, 0), 1, 1, edgecolor='red', facecolor='none', lw=3, zorder=10)
        ax.add_patch(highlight)

        # Mouse click handler
        def on_click(event):
            if event.inaxes == ax:  # Check if click is inside the board
                x, y = int(event.xdata), int(event.ydata)
                file = files[x]
                rank = ranks[board_size - 1 - y]
            
                # Move the highlight rectangle to the clicked square
                highlight.set_xy((x, y))
                highlight.set_visible(True)
                fig.canvas.draw()  # Redraw the canvas to show the highlight

                print(f"Mouse clicked on square: {file}{rank}")

        # Connect the click handler to the figure
        fig.canvas.mpl_connect("button_press_event", on_click)

        # Show the board
        plt.show()