import random
from typing import Tuple, Callable

def minimax_max(state, alpha, beta, depth, eval_func: Callable):    
    if depth == 0 or state.is_terminal():            
            return eval_func(state, state.player),None
    current_value = float('-inf')
    current_action = None

    legal_moves = state.legal_moves()
    next_states = [(state.next_state(move),move) for move in legal_moves]
    print(legal_moves,depth)
    for next_state,move in next_states:
        new_value, _ = minimax_min(next_state,alpha,beta,depth-1,eval_func)
        if new_value > current_value:            
            current_value = new_value
            current_action = move
            alpha = max(alpha,current_value)
            if(alpha >= beta):
                break    
    return current_value,current_action

def minimax_min(state, alpha, beta, depth, eval_func: Callable):
    if depth == 0 or state.is_terminal():            
            return eval_func(state,state.player),None
    current_value = float('inf')
    current_action = None

    legal_moves = state.legal_moves()
    next_states = [(state.next_state(move),move) for move in legal_moves]
    print(legal_moves,depth)
    for next_state,move in next_states:
        new_value, _ = minimax_max(next_state,alpha,beta,depth-1,eval_func)
        if new_value < current_value:
            current_value = new_value
            current_action = move
            beta = min(beta,current_value)
            if(beta <= alpha):
                break
    return current_value,current_action

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
    _, best_move = minimax_max(state, float('-inf'), float('inf'), max_depth,eval_func)
    return best_move


