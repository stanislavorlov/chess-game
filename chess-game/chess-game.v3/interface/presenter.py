import os
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.patches as patches
from domain.pieces.piece import Piece
from domain.chess_game import ChessGame

class Presenter(object):
    
    def __init__(self, game: ChessGame):
        self._game = game
      
    def draw(self):
        board_size = 8
        chessboard = np.zeros((board_size, board_size))
        chessboard[1::2, ::2] = 1  # Black squares in odd rows
        chessboard[::2, 1::2] = 1  # Black squares in even rows

        board = self._game.get_board()
        files = board.get_files()
        ranks = board.get_ranks()

        square_size = self.get_square_size()
        fig_size = board_size * square_size
        fig, ax = plt.subplots(figsize=(fig_size, fig_size))
        
        selected_square = None  # Keep track of the selected square

        # Create the plot
        # fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(chessboard, cmap="gray", origin="upper", extent=(0, board_size, 0, board_size))

        # Add gridlines
        ax.set_xticks(np.arange(0, board_size + 1, 1))
        ax.set_yticks(np.arange(0, board_size + 1, 1))
        ax.grid(which="major", color="black", linestyle="-", linewidth=1)
        ax.tick_params(axis="both", which="both", length=0, labelsize=0)

        self.draw_pieces(ax, board_size)

        # Add rank and file labels
        ax.set_xticks(np.arange(0.5, board_size, 1), minor=True)
        ax.set_xticklabels(files, minor=True, fontsize=12)
        ax.set_yticks(np.arange(0.5, board_size, 1), minor=True)
        ax.set_yticklabels(ranks, minor=True, fontsize=12)

        # Hide major tick labels
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        
        # Add a rectangle to highlight the clicked square
        highlight_rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='none', visible=False)
        ax.add_patch(highlight_rect)

        # Mouse click handler
        def on_click(event):
            if event.inaxes == ax:  # Check if the click is inside the chessboard
                x, y = int(event.xdata), int(event.ydata)
                highlight_rect.set_xy((x, y))  # Move the rectangle to the clicked square
                highlight_rect.set_visible(True)  # Make the rectangle visible
                fig.canvas.draw()  # Redraw the canvas
                square = f"{files[x]}{ranks[7 - y]}"  # Convert to chess notation
                print(f"Clicked square: {square}")

                self._game.click_square(files[x], ranks[7 - y])

        # Connect the click handler
        fig.canvas.mpl_connect("button_press_event", on_click)

        # Display the chessboard with pieces
        plt.show()

    def draw_pieces(self, ax, board_size):
        initial_board = self._game.get_state()

        # Place chess pieces on the board
        for row in range(board_size):
            for col in range(board_size):
                piece: Piece = initial_board[row][col]
                if piece:
                    image = mpimg.imread(Presenter.get_pieces()[piece.get_acronym()])  # Load the piece image
                    ax.imshow(image, extent=(col, col + 1, 7 - row, 8 - row))  # Position the image

    @staticmethod
    def get_pieces():
        return {
            "wp": "./interface/Content/wp.png",
            "wr": "./interface/Content/wr.png",
            "wn": "./interface/Content/wn.png",
            "wb": "./interface/Content/wb.png",
            "wq": "./interface/Content/wq.png",
            "wk": "./interface/Content/wk.png",
            "bp": "./interface/Content/bp.png",
            "br": "./interface/Content/br.png",
            "bn": "./interface/Content/bn.png",
            "bb": "./interface/Content/bb.png",
            "bq": "./interface/Content/bq.png",
            "bk": "./interface/Content/bk.png",
        }

    def get_square_size(self):
        sample_piece_path = next(iter(self.get_pieces().values()))
        if not os.path.exists(sample_piece_path):
            raise FileNotFoundError(f"Image file not found: {sample_piece_path}")
        sample_image = mpimg.imread(sample_piece_path)
        piece_height, piece_width = sample_image.shape[:2]  # Get the dimensions of the image
        
        # Set the figure size based on piece dimensions
        square_size = max(piece_width, piece_height) / 100  # Scale to figure units
        
        return square_size