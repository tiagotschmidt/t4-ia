import random
from typing import Tuple
from ..tttm.gamestate import GameState
from ..tttm.board import Board
from .minimax import minimax_move


# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state: GameState) -> Tuple[int, int]:
    """
    Calculates the best move using the minimax algorithm with alpha-beta pruning.

    Args:
        state: The current game state.

    Returns:
        A tuple (x, y) representing the coordinates of the best move.
    """

    # Assuming a reasonable default maximum depth and a provided evaluation function
    max_depth = float('+inf')  # Adjust based on game complexity and performance needs

    best_move = minimax_move(state, max_depth, utility)
    return best_move


def utility(state, player):
    b = state.get_board().board
    if (state.is_terminal()):
        current_winner = state.winner()
        if (current_winner == None):
            return 0
        elif (player == current_winner):
            return 10
        else:
            return -10
    else:
        return 0


def check_winner(state):
    """
    Checks if there is a winner in the given tic tac toe state.

    Args:
      state: A list of 9 characters representing the tic tac toe board.

    Returns:
      The winning player ('X' or 'O'), or None if there is no winner.
    """
    board = state.get_board().board
    winning_lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    simple_board = [item for sublist in board for item in sublist]
    for line in winning_lines:
        if simple_board[line[0]] == simple_board[line[1]] == simple_board[line[2]] != '-':
            return simple_board[line[0]]
    return None
