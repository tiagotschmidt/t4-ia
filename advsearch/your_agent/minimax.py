import random
from typing import Tuple, Callable

def minimax_move(state, max_depth: int, eval_func: Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.

    Args:
        state: The current game state (instance of GameState).
        max_depth: The maximum depth of the search (-1 for unlimited).
        eval_func: The evaluation function to evaluate terminal or leaf states.

    Returns:
        A tuple (x, y) representing the coordinates of the best move.
    """

    def minimax_value(state, depth, alpha, beta, maximizing_player):
        if depth == 0 or state.is_terminal():            
            return eval_func(state, maximizing_player), None

        if maximizing_player:
            value = float('-inf')
            best_move = None
            for move in state.legal_moves():
                new_state = state.next_state(move)
                value_of_move, _ = minimax_value(new_state, depth - 1, alpha, beta, False)
                alpha = max(alpha, value_of_move)
                if value_of_move > value:
                    value = value_of_move
                    best_move = move
                #print("tupla atual:",value,best_move)
                if beta <= alpha:
                    break  # Pruning
            print("valor:",value,best_move)
            return value, best_move
        else:
            value = float('inf')
            best_move = None
            for move in state.legal_moves():
                new_state = state.next_state(move)
                value_of_move, _ = minimax_value(new_state, depth - 1, alpha, beta, True)
                beta = min(beta, value_of_move)
                if value_of_move < value:
                    value = value_of_move
                    best_move = move
                if beta <= alpha:
                    break  # Pruning
            return value, best_move

    _, best_move = minimax_value(state, max_depth, float('-inf'), float('inf'), True)
    return best_move
