from typing import Optional

import chess
import chess.engine
import time
import chess.svg
from IPython.display import SVG, display
from chess import engine

def static_eval(board: chess.Board):
    i = 0
    evaluation = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        evaluation = evaluation + (get_piece_val(str(board.piece_at(i))) if x else -get_piece_val(str(board.piece_at(i))))
    return evaluation

def get_piece_val(piece: Optional[str]):
    if(piece == None):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == 'K' or piece == 'k':
        value = 900
    #value = value if (board.piece_at(place)).color else -value
    return value


def minmax(board_instance: chess.Board, max_depth: int, current_depth: int, is_max_player: bool, nodes_per_depth: dict):
    # This if else code block is only used for analysis of algorithm, by counting number of nodes explored
    if max_depth - current_depth in nodes_per_depth:
        nodes_per_depth[max_depth - current_depth] += 1
    else:
        nodes_per_depth[max_depth - current_depth] = 1

    # This is the base case, depth == 0 means it is a leaf node
    if current_depth == 0:
        leaf_node_score = static_eval(board_instance)
        return (leaf_node_score, nodes_per_depth)

    if is_max_player:

        # set absurdly high negative value such that none of the static evaluation result less than this value
        best_score = -100000

        for legal_move in board_instance.legal_moves:
            move = chess.Move.from_uci(str(legal_move))

            # pushing the current move to the board
            board_instance.push(move)

            # calculating node score, if the current node will be the leaf node, then score will be calculated by static evaluation;
            # score will be calculated by finding max value between node score and current best score.
            node_score, nodes_per_depth = minmax(board_instance, max_depth, current_depth - 1, False, nodes_per_depth)

            # calculating the max value for the particular node
            best_score = max(best_score, node_score)

            # undoing the last move, so that we can evaluate next legal moves
            board_instance.pop()

        return (best_score, nodes_per_depth)
    else:

        # set absurdly high positive value such that none of the static evaluation result more than this value
        best_score = 100000

        for legal_move in board_instance.legal_moves:
            move = chess.Move.from_uci(str(legal_move))

            # pushing the current move to the board
            board_instance.push(move)

            # calculating node score, if the current node will be the leaf node, then score will be calculated by static evaluation;
            # score will be calculated by finding min value between node score and current best score.
            node_score, nodes_per_depth = minmax(board_instance, max_depth, current_depth - 1, True, nodes_per_depth)

            # calculating the min value for the particular node
            best_score = min(best_score, node_score)

            # undoing the last move, so that we can evaluate next legal moves
            board_instance.pop()

        return (best_score, nodes_per_depth)


def best_move_using_minmax(board_instance: chess.Board, depth: int, is_max_player: bool):
    best_move_score = -1000000
    best_move = None

    nodes_per_depth = dict()

    for legal_move in board_instance.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        board_instance.push(move)
        move_score, nodes_per_depth = minmax(board_instance, depth, depth, False, nodes_per_depth)
        score = max(best_move_score, move_score)
        board_instance.pop()
        if score > best_move_score:
            best_move_score = score
            best_move = move
    return (best_move, nodes_per_depth)


def game_between_two_computer(depth:int=3):
    board = chess.Board()

    for n in range(0, 10):
        start = time.time()
        if n % 2 == 0:
            print("WHITE Turn")
            move, nodes_per_depth = best_move_using_minmax(board, depth, False)
        else:

            print("BLACK Turn")
            move, nodes_per_depth = best_move_using_minmax(board, depth, True)
        end = time.time()

        print("Move in UCI format:", move)
        print("Nodes per depth:", nodes_per_depth)
        print("Time taken by Move:", end - start)
        board.push(move)
        display(SVG(chess.svg.board(board, size=400)))
        print("\n")

game_between_two_computer()