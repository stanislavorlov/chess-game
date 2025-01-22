import os
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.patches as patches

from domain.chessboard.chess_board import ChessBoard
from domain.game_state import GameState
from domain.pieces.piece import Piece

class Presenter:

    BOARD_SIZE = 8

    def __init__(self, board: ChessBoard):
        square_size = Presenter.get_square_size()
        fig_size = self.BOARD_SIZE * square_size
        self.fig, self.ax = plt.subplots(figsize=(fig_size, fig_size))
        self._board = board

    def draw(self, state: GameState):
        chessboard = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE))
        chessboard[1::2, ::2] = 1  # Black squares in odd rows
        chessboard[::2, 1::2] = 1  # Black squares in even rows

        files = self._board.get_files()
        ranks = self._board.get_ranks()

        #square_size = self.get_square_size()
        #fig_size = board_size * square_size
        #fig, ax = plt.subplots(figsize=(fig_size, fig_size))
        
        selected_square = None  # Keep track of the selected square

        # Create the plot
        # fig, ax = plt.subplots(figsize=(6, 6))
        self.ax.imshow(chessboard, cmap="gray", origin="upper", extent=(0, self.BOARD_SIZE, 0, self.BOARD_SIZE))

        # Add gridlines
        self.ax.set_xticks(np.arange(0, self.BOARD_SIZE + 1, 1))
        self.ax.set_yticks(np.arange(0, self.BOARD_SIZE + 1, 1))
        self.ax.grid(which="major", color="black", linestyle="-", linewidth=1)
        self.ax.tick_params(axis="both", which="both", length=0, labelsize=0)

        self.draw_pieces(state)

        # Add rank and file labels
        self.ax.set_xticks(np.arange(0.5, self.BOARD_SIZE, 1), minor=True)
        self.ax.set_xticklabels(files, minor=True, fontsize=12)
        self.ax.set_yticks(np.arange(0.5, self.BOARD_SIZE, 1), minor=True)
        self.ax.set_yticklabels(ranks, minor=True, fontsize=12)

        # Hide major tick labels
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        
        # Add a rectangle to highlight the clicked square
        highlight_rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='none', visible=False)
        self.ax.add_patch(highlight_rect)

        # Mouse click handler
        #def on_click(event):
        #    if event.inaxes == self.ax:  # Check if the click is inside the chessboard
        #        x, y = int(event.xdata), int(event.ydata)
        #        highlight_rect.set_xy((x, y))  # Move the rectangle to the clicked square
        #        highlight_rect.set_visible(True)  # Make the rectangle visible
        #        self.fig.canvas.draw()  # Redraw the canvas
        #        square = f"{files[x]}{ranks[7 - y]}"  # Convert to chess notation
        #        print(f"Clicked square: {square}")
        #
        #        self._game.click_square(files[x], ranks[7 - y])

        # Connect the click handler
        # self.fig.canvas.mpl_connect("button_press_event", on_click)

        # Display the chessboard with pieces
        plt.show()

    def bind_canvas_click_function(self, onclick_callback):
        # Add a rectangle to highlight the clicked square
        highlight_rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='none', visible=False)
        self.ax.add_patch(highlight_rect)

        files = self._board.get_files()
        ranks = self._board.get_ranks()

        # Mouse click handler
        def on_click(event):
            if event.inaxes == self.ax:  # Check if the click is inside the chessboard
                x, y = int(event.xdata), int(event.ydata)
                highlight_rect.set_xy((x, y))  # Move the rectangle to the clicked square
                highlight_rect.set_visible(True)  # Make the rectangle visible
                self.fig.canvas.draw()  # Redraw the canvas
                onclick_callback(files[x], ranks[7 - y])

        # Connect the click handler
        self.fig.canvas.mpl_connect("button_press_event", on_click)

    def draw_pieces(self, state: GameState):
        piece_state = state.get_state()

        # ToDo: no need to iterate over the all matrix, but iterate just over positions with pieces
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece: Piece = piece_state[row][col]
                if piece:
                    image = mpimg.imread(Presenter.get_image(piece))  # Load the piece image
                    self.ax.imshow(image, extent=(col, col + 1, 7 - row, 8 - row))  # Position the image

    @staticmethod
    def get_image(piece: Piece) -> str:
        return f"./interface/Content/{piece.get_acronym()}.png"

    @staticmethod
    def get_square_size():
        sample_piece_path = "./interface/Content/wp.png"
        if not os.path.exists(sample_piece_path):
            raise FileNotFoundError(f"Image file not found: {sample_piece_path}")
        sample_image = mpimg.imread(sample_piece_path)
        piece_height, piece_width = sample_image.shape[:2]  # Get the dimensions of the image
        
        # Set the figure size based on piece dimensions
        square_size = max(piece_width, piece_height) / 100  # Scale to figure units
        
        return square_size