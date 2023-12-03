"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Flatten the board to make counting easier
    flat_board = [cell for row in board for cell in row]

    # Count the number of X's and O's
    x_count = flat_board.count('X')
    o_count = flat_board.count('O')

    # Decide whose turn it is
    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):  # is_terminal is a function to check if the game has ended
        return set()  # Return an empty set for a terminal board

    available_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                available_actions.add((i, j))

    return available_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action!")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != None:  # Row check
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != None:  # Column check
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != None:  # Top-left to bottom-right
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != None:  # Top-right to bottom-left
        return board[0][2]

    return None  # No winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        if None in row:
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def board_to_key(board):
        return tuple(tuple(row) for row in board)

    def max_value(board, memo):
        board_key = board_to_key(board)
        if board_key in memo:
            return memo[board_key]

        if terminal(board):
            return utility(board), None

        v = float('-inf')
        best_action = None
        for action in actions(board):
            val, _ = min_value(result(board, action), memo)
            if val > v:
                v = val
                best_action = action

        memo[board_key] = (v, best_action)
        return v, best_action

    def min_value(board, memo):
        board_key = board_to_key(board)
        if board_key in memo:
            return memo[board_key]

        if terminal(board):
            return utility(board), None

        v = float('inf')
        best_action = None
        for action in actions(board):
            val, _ = max_value(result(board, action), memo)
            if val < v:
                v = val
                best_action = action

        memo[board_key] = (v, best_action)
        return v, best_action

    memo = {}
    current_player = player(board)
    if current_player == X:
        _, action = max_value(board, memo)
    else:
        _, action = min_value(board, memo)

    return action
