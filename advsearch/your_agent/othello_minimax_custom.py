import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from typing import Tuple, Callable
from .minimax import minimax_move


# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

def minimax_max(state, alpha, beta, depth, eval_func: Callable):
    if depth == 0 or state.is_terminal():
        return eval_func(state, state.player), None
    current_value = float('-inf')
    current_action = None

    legal_moves = state.legal_moves()
    next_states = [(state.next_state(move), move) for move in legal_moves]
    print(legal_moves, depth)
    for next_state, move in next_states:
        new_value, _ = minimax_min(next_state, alpha, beta, depth - 1, eval_func)
        if new_value > current_value:
            current_value = new_value
            current_action = move
            alpha = max(alpha, current_value)
            if (alpha >= beta):
                break
    return current_value, current_action


def minimax_min(state, alpha, beta, depth, eval_func: Callable):
    if depth == 0 or state.is_terminal():
        return eval_func(state, state.player), None
    current_value = float('inf')
    current_action = None

    legal_moves = state.legal_moves()
    next_states = [(state.next_state(move), move) for move in legal_moves]
    print(legal_moves, depth)
    for next_state, move in next_states:
        new_value, _ = minimax_max(next_state, alpha, beta, depth - 1, eval_func)
        if new_value < current_value:
            current_value = new_value
            current_action = move
            beta = min(beta, current_value)
            if (beta <= alpha):
                break
    return current_value, current_action


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque uma chamada para o minimax_move (que vc implementara' no modulo minimax).
    # A chamada a minimax_move deve receber sua funcao evaluate como parametro.

    _, best_move = minimax_max(state, float('-inf'), float('inf'), max_depth, evaluate_custom)
    return best_move


def evaluate_custom(state: "GameState", player: str) -> float:
    """
    Evaluates an Othello state from the point of view of the given player.

    Args:
        state: An instance of GameState representing the current board state.
        player: The player whose perspective to evaluate from (either "B" or "W").

    Returns:
        A float representing the estimated value of the state for the given player.
        For terminal states, the exact utility (win: 1.0, loss: -1.0, draw: 0.0) is returned.
        For non-terminal states, an approximation based on the piece count and
        mobility (capturability) is calculated.

    Raises:
        ValueError: If the given player is not "B" or "W".
    """

    if player not in ("B", "W"):
        raise ValueError("Invalid player. Must be either 'B' or 'W'.")

    # Check if the state is terminal (no empty squares and no valid moves for either player)
    if state.is_terminal():
        if state.get_winner() == player:
            return 1.0  # Win for the given player
        elif state.get_winner() is None:
            return 0.0  # Draw
        else:
            return -1.0  # Loss for the given player

    # Calculate player and opponent piece counts
    player_count = state.get_piece_count(player)
    opponent_count = state.get_piece_count(opponent(player))

    # Incorporate mobility by estimating capturable pieces using a capture-based heuristic
    player_capturable = state.estimate_capturable_pieces(player)
    opponent_capturable = state.estimate_capturable_pieces(opponent(player))

    # Normalize piece counts using the maximum possible
    max_pieces = state.get_board_size() ** 2
    player_piece_score = player_count / max_pieces
    opponent_piece_score = opponent_count / max_pieces

    # Normalize capturable pieces using the piece difference
    piece_diff = player_count - opponent_count
    player_capturable_score = player_capturable / (piece_diff + 1)  # Prevent division by zero
    opponent_capturable_score = opponent_capturable / (-piece_diff + 1)

    # Weight and combine piece counts and capturable pieces based on importance
    weighted_piece_score = 0.7 * player_piece_score - 0.3 * opponent_piece_score
    weighted_capturable_score = 0.5 * player_capturable_score - 0.5 * opponent_capturable_score

    # Final evaluation, considering potential corner squares and adjusting weights for higher board sizes
    final_score = weighted_piece_score + weighted_capturable_score + corner_bonus(state, player)
    if state.get_board_size() > 8:
        final_score *= 1.1  # Adjust weights for larger boards

    return final_score


def corner_bonus(state: "GameState", player: str) -> float:
    """
    Calculates a bonus based on the number of corner squares occupied by the given player.

    Args:
        state: An instance of GameState representing the current board state.
        player: The player whose corner occupancy to evaluate (either "B" or "W").

    Returns:
        A float representing the corner bonus (positive for favorable corner occupancy, negative for unfavorable).
    """

    board_size = state.get_board_size()
    corners = [(0, 0), (0, board_size - 1), (board_size - 1, 0), (board_size - 1, board_size - 1)]
    corner_count = sum(state.get_piece_at(pos) == player for pos in corners)

    if corner_count == 4:
        return 0.4  # Significant advantage for owning all corners
    elif corner_count == 3:
        return 0.2  # Moderate advantage for owning 3 corners
    elif corner_count == 2:
        return 0.1  # Slight advantage for owning 2 corners
    elif corner_count == 0:
        return -0.1
