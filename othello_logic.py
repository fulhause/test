def initialize_board():
    """
    Initializes an 8x8 Othello board with the standard starting position.
    Player 1 is 'X', Player 2 is 'O'. Empty cells are ' '.

    Returns:
        list: A 2D list representing the Othello board.
    """
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[3][3] = 'O'
    board[3][4] = 'X'
    board[4][3] = 'X'
    board[4][4] = 'O'
    return board

if __name__ == '__main__':
    # Example usage (can be removed or commented out):
    # board = initialize_board()
    # for row in board:
    #     print(row)

def is_valid_move(board, player, row, col):
    """
    Checks if placing a piece for `player` at `(row, col)` is a valid move.
    A move is valid if the cell is empty and placing a piece there flips at least one opponent piece.

    Args:
        board (list): The Othello board.
        player (str): The player making the move ('X' or 'O').
        row (int): The row to place the piece.
        col (int): The column to place the piece.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    if not (0 <= row < 8 and 0 <= col < 8 and board[row][col] == ' '):
        return False

    opponent = 'O' if player == 'X' else 'X'
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            # Potential line to flip
            r_check, c_check = r + dr, c + dc
            while 0 <= r_check < 8 and 0 <= c_check < 8:
                if board[r_check][c_check] == player:
                    return True  # Found a piece to flip
                elif board[r_check][c_check] == ' ':
                    break  # Empty space, no flip in this direction
                r_check += dr
                c_check += dc
    return False

def make_move(board, player, row, col):
    """
    Places the `player`'s piece at `(row, col)` and flips opponent pieces.
    Assumes the move is valid. Modifies the board in place.

    Args:
        board (list): The Othello board.
        player (str): The player making the move ('X' or 'O').
        row (int): The row to place the piece.
        col (int): The column to place the piece.
    """
    board[row][col] = player
    opponent = 'O' if player == 'X' else 'X'
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        pieces_to_flip = []
        while 0 <= r < 8 and 0 <= c < 8:
            if board[r][c] == opponent:
                pieces_to_flip.append((r, c))
            elif board[r][c] == player:
                for flip_r, flip_c in pieces_to_flip:
                    board[flip_r][flip_c] = player
                break 
            else: # Empty cell or out of bounds
                break
            r += dr
            c += dc

def get_valid_moves(board, player):
    """
    Returns a list of (row, col) tuples representing all valid moves for the `player`.

    Args:
        board (list): The Othello board.
        player (str): The player to find moves for ('X' or 'O').

    Returns:
        list: A list of (row, col) tuples for valid moves.
    """
    valid_moves = []
    for r in range(8):
        for c in range(8):
            if is_valid_move(board, player, r, c):
                valid_moves.append((r, c))
    return valid_moves

def get_score(board):
    """
    Calculates the score for each player.

    Args:
        board (list): The Othello board.

    Returns:
        dict: A dictionary with piece counts, e.g., {'X': count_X, 'O': count_O}.
    """
    score = {'X': 0, 'O': 0}
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'X':
                score['X'] += 1
            elif board[r][c] == 'O':
                score['O'] += 1
    return score

def check_winner(board):
    """
    Determines the winner of the game.
    The game ends when no player has any valid moves.
    The player with more pieces wins.

    Args:
        board (list): The Othello board.

    Returns:
        str or None: 'X' if player X wins, 'O' if player O wins, 
                     'Draw' if it's a draw, or None if the game is not over.
    """
    player_x_moves = get_valid_moves(board, 'X')
    player_o_moves = get_valid_moves(board, 'O')

    if not player_x_moves and not player_o_moves:
        # Game is over
        score = get_score(board)
        if score['X'] > score['O']:
            return 'X'
        elif score['O'] > score['X']:
            return 'O'
        else:
            return 'Draw'
    else:
        # Game is not over
        return None
