import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move
from typing import Tuple, Callable

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

# mask template adjusted from https://web.fe.up.pt/~eol/IA/MIA0203/trabalhos/Damas_Othelo/Docs/Eval.html
# could optimize for symmetries but just put all values here for coding speed :P
# DO NOT CHANGE! 
EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

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

    return random.choice([(2, 3), (4, 5), (5, 4), (3, 2)])

def evaluate_mask(state, player: str) -> float:
    """
    Evaluates an othello state from the point of view of the given player.

    Args:
        state: instance of GameState representing the current board state.
        player: player to evaluate the state for (B or W).

    Returns:
        float: Estimate of the value of the state for the given player.
    """

    # Initialize score to 0
    score = 0

    # Loop through each cell in the board
    for row in range(8):
        for col in range(8):
            # Check if the cell has a piece
            if state.board[row][col] != ".":
                # Get the player of the piece on the cell
                piece_player = state.board[row][col]

                # Check if the piece belongs to the player we are evaluating for
                if piece_player == player:
                    # Add the corresponding value from the EVAL_TEMPLATE based on the position
                    score += EVAL_TEMPLATE[row][col]
                else:
                    # Subtract the corresponding value for the opponent's piece
                    score -= EVAL_TEMPLATE[row][col]

    return score

