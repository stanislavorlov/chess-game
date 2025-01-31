import os
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.patches as patches

from domain.chessboard.file import File
from domain.chessboard.position import Position
from domain.chessboard.rank import Rank
from domain.game.game_state import GameState
from domain.pieces.piece import Piece
from interface.abstract_presenter import AbstractPresenter

class ImagePresenter(AbstractPresenter):

    BOARD_SIZE = 8

    def __init__(self):
        #square_size = Presenter.get_square_size()
        square_size = 1.2
        fig_size = self.BOARD_SIZE * square_size
        self.fig, self.ax = plt.subplots(figsize=(fig_size, fig_size))

    def draw(self, state: GameState):

        # ToDo: should rotate the board based on player side
        chessboard = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE))
        chessboard[1::2, ::2] = 1  # Black squares in odd rows
        chessboard[::2, 1::2] = 1  # Black squares in even rows

        # Create the plot
        self.ax.imshow(chessboard, cmap="gray", origin="upper", extent=(0, self.BOARD_SIZE, 0, self.BOARD_SIZE))

        # Add gridlines
        self.ax.set_xticks(np.arange(0, self.BOARD_SIZE, 1))
        self.ax.set_yticks(np.arange(0, self.BOARD_SIZE, 1))
        self.ax.grid(which="major", color="black", linestyle="-", linewidth=1)
        self.ax.tick_params(axis="both", which="both", length=0, labelsize=0)

        self.draw_pieces(state)

        # Add rank and file labels
        self.ax.set_xticks(np.arange(0.0, self.BOARD_SIZE, 1), minor=True)
        self.ax.set_xticklabels(['a','b','c','d','e','f','g','h'], minor=True, fontsize=12)
        self.ax.set_yticks(np.arange(0.0, self.BOARD_SIZE, 1), minor=True)
        self.ax.set_yticklabels([1,2,3,4,5,6,7,8], minor=True, fontsize=12)

        # Hide major tick labels
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        # Add a rectangle to highlight the clicked square
        highlight_rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='none', visible=False)
        self.ax.add_patch(highlight_rect)

        # Display the chessboard with pieces
        plt.show()

    def onclick_handler(self, callback):
        # Add a rectangle to highlight the clicked square
        highlight_rect = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='none', visible=False)
        self.ax.add_patch(highlight_rect)

        # Mouse click handler
        def on_click(event):
            if event.inaxes == self.ax:  # Check if the click is inside the chessboard
                x, y = int(event.xdata), int(event.ydata)
                highlight_rect.set_xy((x, y))  # Move the rectangle to the clicked square
                highlight_rect.set_visible(True)  # Make the rectangle visible
                self.fig.canvas.draw()  # Redraw the canvas
                print(File.from_index(x), Rank.from_index(7 - y))
                callback(Position(File.from_index(x), Rank.from_index(7 - y)))

        # Connect the click handler
        self.fig.canvas.mpl_connect("button_press_event", on_click)

    def draw_pieces(self, state: GameState):
        piece_state = state.get_state()

        for position, piece in piece_state.items():
            col, row = position.file.to_index(), position.rank.to_index()
            image = mpimg.imread(ImagePresenter.get_image(piece))  # Load the piece image
            self.ax.imshow(image, extent=(col, col + 1, 6 - row, 7 - row))  # Position the image

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