import unittest
from othello_logic import initialize_board, is_valid_move, make_move, get_valid_moves, get_score, check_winner

class TestOthelloLogic(unittest.TestCase):

    def test_initialize_board(self):
        board = initialize_board()
        self.assertEqual(len(board), 8, "Board should have 8 rows")
        for row in board:
            self.assertEqual(len(row), 8, "Each row should have 8 columns")

        self.assertEqual(board[3][3], 'O', "Initial piece at (3,3) should be 'O'")
        self.assertEqual(board[3][4], 'X', "Initial piece at (3,4) should be 'X'")
        self.assertEqual(board[4][3], 'X', "Initial piece at (4,3) should be 'X'")
        self.assertEqual(board[4][4], 'O', "Initial piece at (4,4) should be 'O'")

        empty_count = 0
        for r in range(8):
            for c in range(8):
                if (r, c) not in [(3,3), (3,4), (4,3), (4,4)]:
                    self.assertEqual(board[r][c], ' ', f"Cell ({r},{c}) should be empty")
                if board[r][c] == ' ':
                    empty_count +=1
        self.assertEqual(empty_count, 60, "There should be 60 empty cells initially")

    def test_is_valid_move_initial_board(self):
        board = initialize_board()
        # Valid moves for 'X'
        self.assertTrue(is_valid_move(board, 'X', 2, 3), "X should have a valid move at (2,3)")
        self.assertTrue(is_valid_move(board, 'X', 3, 2), "X should have a valid move at (3,2)")
        self.assertTrue(is_valid_move(board, 'X', 4, 5), "X should have a valid move at (4,5)")
        self.assertTrue(is_valid_move(board, 'X', 5, 4), "X should have a valid move at (5,4)")

        # Invalid moves for 'X' (occupied)
        self.assertFalse(is_valid_move(board, 'X', 3, 3), "X cannot move to occupied (3,3)")
        self.assertFalse(is_valid_move(board, 'X', 3, 4), "X cannot move to occupied (3,4)")

        # Invalid moves for 'X' (no flip)
        self.assertFalse(is_valid_move(board, 'X', 0, 0), "X cannot move to (0,0) - no flip")
        self.assertFalse(is_valid_move(board, 'X', 2, 2), "X cannot move to (2,2) - no flip")

        # Valid moves for 'O'
        self.assertTrue(is_valid_move(board, 'O', 2, 4), "O should have a valid move at (2,4)")
        self.assertTrue(is_valid_move(board, 'O', 3, 5), "O should have a valid move at (3,5)")
        self.assertTrue(is_valid_move(board, 'O', 4, 2), "O should have a valid move at (4,2)")
        self.assertTrue(is_valid_move(board, 'O', 5, 3), "O should have a valid move at (5,3)")

    def test_is_valid_move_custom_board(self):
        # Board:
        # O O O . . . . .
        # . X . . . . . .
        # . . . . . . . .
        # . . . . . . . .
        # . . . . . . . .
        # . . . . . . . .
        # . . . . . . . .
        # . . . . . . . .
        board = [[' ' for _ in range(8)] for _ in range(8)]
        board[0][0] = 'O'
        board[0][1] = 'O'
        board[0][2] = 'O'
        board[1][1] = 'X'

        self.assertTrue(is_valid_move(board, 'X', 0, 3), "X should be able to place at (0,3) to flip O's horizontally")
        
        board[2][1] = 'O'
        board[3][1] = 'O'
        # Board:
        # O O O . . . . .
        # . X . . . . . .
        # . O . . . . . .
        # . O . . . . . .
        # . . . . . . . .
        self.assertTrue(is_valid_move(board, 'X', 4, 1), "X should be able to place at (4,1) to flip O's vertically")

        board[2][2] = 'O'
        board[3][3] = 'O'
        # Board:
        # O O O . . . . .
        # . X . . . . . .
        # . O O . . . . . (O at 2,1 and 2,2)
        # . O . O . . . . (O at 3,1 and 3,3)
        # . . . . . . . .
        self.assertTrue(is_valid_move(board, 'X', 4, 4), "X should be able to place at (4,4) to flip O diagonally from (1,1)")

        # Test invalid: no pieces to flip
        self.assertFalse(is_valid_move(board, 'X', 7, 7), "X cannot move to (7,7) - no flip")
        # Test invalid: occupied
        self.assertFalse(is_valid_move(board, 'X', 1, 1), "X cannot move to occupied (1,1)")
        # Test invalid: out of bounds (is_valid_move assumes valid indices, get_valid_moves filters)
        # Not explicitly testing out of bounds here as the function's guard clause handles it.
        # self.assertFalse(is_valid_move(board, 'X', -1, 0))

        # Test edge case: flipping a single piece on the edge
        board = [[' ' for _ in range(8)] for _ in range(8)]
        board[0][0] = 'O'
        board[0][1] = 'X'
        self.assertTrue(is_valid_move(board, 'O', 0, 2), "O should be able to place at (0,2) on edge")

    def test_make_move_initial_board(self):
        board = initialize_board()
        # X plays at (2,3)
        make_move(board, 'X', 2, 3)
        self.assertEqual(board[2][3], 'X', "X should be placed at (2,3)")
        self.assertEqual(board[3][3], 'X', "O at (3,3) should be flipped to X")
        self.assertEqual(board[3][4], 'X', "Original X at (3,4) should remain X") # Unrelated piece
        self.assertEqual(board[4][3], 'X', "Original X at (4,3) should remain X") # Unrelated piece
        self.assertEqual(board[4][4], 'O', "Original O at (4,4) should remain O") # Unrelated piece

    def test_make_move_horizontal_flip(self):
        # O O O . . .
        # . X . . . .
        board = [[' ' for _ in range(8)] for _ in range(8)]
        board[0][0] = 'O'
        board[0][1] = 'O'
        board[0][2] = 'X' # This X will make the move
        make_move(board, 'X', 0, 3) # X places at (0,3)
        # Expected: X X X X . . .
        self.assertEqual(board[0][0], 'X', "Piece at (0,0) should be flipped to X")
        self.assertEqual(board[0][1], 'X', "Piece at (0,1) should be flipped to X")
        self.assertEqual(board[0][2], 'X', "Original piece at (0,2) should remain X")
        self.assertEqual(board[0][3], 'X', "New piece should be at (0,3)")

    def test_make_move_vertical_flip(self):
        # O . .
        # O . .
        # X . .
        # . . . (X will place here)
        board = [[' ' for _ in range(8)] for _ in range(8)]
        board[0][0] = 'O'
        board[1][0] = 'O'
        board[2][0] = 'X'
        make_move(board, 'X', 3, 0)
        # Expected:
        # X . .
        # X . .
        # X . .
        # X . .
        self.assertEqual(board[0][0], 'X', "Piece at (0,0) should be flipped to X")
        self.assertEqual(board[1][0], 'X', "Piece at (1,0) should be flipped to X")
        self.assertEqual(board[2][0], 'X', "Piece at (2,0) should remain X")
        self.assertEqual(board[3][0], 'X', "New piece should be at (3,0)")

    def test_make_move_diagonal_flip(self):
        # O . . .
        # . O . .
        # . . X .
        # . . . . (X will place here)
        board = [[' ' for _ in range(8)] for _ in range(8)]
        board[0][0] = 'O'
        board[1][1] = 'O'
        board[2][2] = 'X'
        make_move(board, 'X', 3, 3)
        # Expected:
        # X . . .
        # . X . .
        # . . X .
        # . . . X
        self.assertEqual(board[0][0], 'X', "Piece at (0,0) should be flipped to X")
        self.assertEqual(board[1][1], 'X', "Piece at (1,1) should be flipped to X")
        self.assertEqual(board[2][2], 'X', "Piece at (2,2) should remain X")
        self.assertEqual(board[3][3], 'X', "New piece should be at (3,3)")

    def test_make_move_multiple_directions_flip(self):
        # O O O
        # O X O
        # O O O (X will place at 1,1, this is a setup for a center move)
        board = [['O' for _ in range(3)] for _ in range(3)] # Fill 3x3 with O
        board.extend([[' '] * 8 for _ in range(5)]) # Pad rows
        for i in range(3): board[i].extend([' '] * 5) # Pad columns

        board[1][1] = 'X' # Center piece for X
        # Now, make a move that flips in multiple directions
        # Let's say board is:
        # X . X . . .
        # . O . . . .
        # X O X . . .
        # . O . . . .
        # . . X . . .
        # Player 'O' plays at (2,1)
        custom_board = [[' ' for _ in range(8)] for _ in range(8)]
        custom_board[0][0] = 'X'
        custom_board[0][2] = 'X'
        custom_board[1][1] = 'O' # Original O
        custom_board[2][0] = 'X'
        custom_board[2][2] = 'X'
        custom_board[3][1] = 'O' # Original O
        custom_board[4][2] = 'X'

        # Player 'O' places piece at (2,1). Should flip (1,1) and (3,1)
        make_move(custom_board, 'O', 2, 1)
        self.assertEqual(custom_board[2][1], 'O', "New piece for O at (2,1)")
        self.assertEqual(custom_board[1][1], 'O', "X at (1,1) should be flipped to O vertically")
        self.assertEqual(custom_board[3][1], 'O', "X at (3,1) should be flipped to O vertically")
        
        # Check that other pieces are untouched
        self.assertEqual(custom_board[0][0], 'X')
        self.assertEqual(custom_board[0][2], 'X')
        self.assertEqual(custom_board[2][0], 'X')
        self.assertEqual(custom_board[2][2], 'X')
        self.assertEqual(custom_board[4][2], 'X')

    def test_get_valid_moves_initial_board(self):
        board = initialize_board()
        # Player X
        expected_moves_x = [(2, 3), (3, 2), (4, 5), (5, 4)]
        valid_moves_x = get_valid_moves(board, 'X')
        self.assertCountEqual(valid_moves_x, expected_moves_x, "Valid moves for X on initial board are incorrect")

        # Player O
        expected_moves_o = [(2, 4), (3, 5), (4, 2), (5, 3)]
        valid_moves_o = get_valid_moves(board, 'O')
        self.assertCountEqual(valid_moves_o, expected_moves_o, "Valid moves for O on initial board are incorrect")

    def test_get_valid_moves_no_moves(self):
        # X X X
        # X O X
        # X X X
        # O has no moves
        board = [['X' for _ in range(3)] for _ in range(3)]
        board[1][1] = 'O'
        # Pad the board to 8x8
        for row in board:
            row.extend([' '] * 5)
        board.extend([[' '] * 8 for _ in range(5)])
        
        valid_moves_o = get_valid_moves(board, 'O')
        self.assertEqual(len(valid_moves_o), 0, "O should have no valid moves")

        # Test for X as well, who also has no moves on this specific 3x3 setup if it were their turn
        valid_moves_x = get_valid_moves(board, 'X')
        self.assertEqual(len(valid_moves_x), 0, "X should also have no valid moves in this configuration")


    def test_get_valid_moves_multiple_options(self):
        # O X . .
        # X X . .
        # . . . .
        # . . . .
        # Player O's turn
        board = [[' ' for _ in range(8)] for _ in range(8)]
        board[0][0] = 'O'
        board[0][1] = 'X'
        board[1][0] = 'X'
        board[1][1] = 'X'
        # Valid moves for O: (0,2) (horizontal), (2,0) (vertical), (2,2) (diagonal)
        expected_moves_o = [(0, 2), (2, 0), (2,2)]
        valid_moves_o = get_valid_moves(board, 'O')
        self.assertCountEqual(valid_moves_o, expected_moves_o, "Valid moves for O are incorrect")

    def test_get_score(self):
        board = initialize_board()
        score = get_score(board)
        self.assertEqual(score['X'], 2, "Initial score for X should be 2")
        self.assertEqual(score['O'], 2, "Initial score for O should be 2")

        # After X plays at (2,3) -> X:4, O:1
        # Board state:
        # . . . . . . . .
        # . . . . . . . .
        # . . . X . . . . (New X at 2,3)
        # . . . X X . . . (Flipped O at 3,3; Original X at 3,4)
        # . . . X O . . . (Original X at 4,3; Original O at 4,4)
        # . . . . . . . .
        make_move(board, 'X', 2, 3)
        score = get_score(board)
        self.assertEqual(score['X'], 4, "Score for X after one move should be 4")
        self.assertEqual(score['O'], 1, "Score for O after one move should be 1")

        # O plays at (2,4) -> X:3, O:3
        # Board state after X's move:
        # . . . . . . . .
        # . . . . . . . .
        # . . . X . . . . (X at 2,3)
        # . . . X X . . . (X at 3,3; X at 3,4)
        # . . . X O . . . (X at 4,3; O at 4,4)
        # O plays at (2,4). Flips X at (3,4)
        # New Board:
        # . . . . O . . . (New O at 2,4)
        # . . . X O . . . (X at 2,3; Flipped X at 3,4 to O)
        # . . . X O . . . (X at 3,3; Original O at 4,4)
        # . . . X O . . . (X at 4,3)
        make_move(board, 'O', 2, 4)
        score = get_score(board)
        self.assertEqual(score['X'], 3, "Score for X after O's move should be 3") # (2,3), (3,3), (4,3)
        self.assertEqual(score['O'], 3, "Score for O after O's move should be 3") # (2,4), (3,4), (4,4)


        # Test on a nearly full board
        full_board = [['X' for _ in range(8)] for _ in range(8)]
        full_board[0][0] = 'O'
        full_board[7][7] = ' '
        score_full = get_score(full_board)
        self.assertEqual(score_full['X'], 64 - 2, "Score for X on nearly full board")
        self.assertEqual(score_full['O'], 1, "Score for O on nearly full board")

    def test_check_winner(self):
        board = initialize_board()
        self.assertIsNone(check_winner(board), "Game should not be over on initial board")

        # Scenario: X wins
        board_x_wins = [['X' for _ in range(8)] for _ in range(8)]
        board_x_wins[0][0] = 'O' # O has 1 piece
        # Ensure no valid moves for O (e.g., surround O or fill board such that O cannot play)
        # For simplicity, assume X filled the board mostly.
        # We need to ensure get_valid_moves for both players returns empty.
        # This setup guarantees X has more pieces. We just need to ensure no moves are possible.
        # A completely full board is the easiest way to ensure no moves.
        for r in range(8):
            for c in range(8):
                if board_x_wins[r][c] == ' ': board_x_wins[r][c] = 'X' # Fill remaining with X
        
        # Double check no moves (though a full board implies this)
        self.assertEqual(get_valid_moves(board_x_wins, 'X'), [])
        self.assertEqual(get_valid_moves(board_x_wins, 'O'), [])
        self.assertEqual(check_winner(board_x_wins), 'X', "X should be the winner")

        # Scenario: O wins
        board_o_wins = [['O' for _ in range(8)] for _ in range(8)]
        board_o_wins[0][0] = 'X' # X has 1 piece
        for r in range(8):
            for c in range(8):
                if board_o_wins[r][c] == ' ': board_o_wins[r][c] = 'O'
        self.assertEqual(check_winner(board_o_wins), 'O', "O should be the winner")

        # Scenario: Draw
        board_draw = [['X' for _ in range(4)] + ['O' for _ in range(4)] for _ in range(8)] # 32 X, 32 O
        # Ensure the board is full to stop moves
        for r in range(8):
            for c in range(8): #This will make it full, X:32, O:32
                if (r*8+c) % 2 == 0: board_draw[r][c] = 'X'
                else: board_draw[r][c] = 'O'

        self.assertEqual(get_valid_moves(board_draw, 'X'), [])
        self.assertEqual(get_valid_moves(board_draw, 'O'), [])
        self.assertEqual(check_winner(board_draw), 'Draw', "Game should be a draw")

        # Scenario: Game ends because no player has moves (X wins by having more pieces)
        # X X X
        # X X X
        # X O .  (O has 1 piece, X has 8. No moves for O. No moves for X.)
        board_no_moves = [['X' for _ in range(3)] for _ in range(3)]
        board_no_moves[2][1] = 'O'
        board_no_moves[2][2] = ' ' # Empty space
        # Pad to 8x8
        for row in board_no_moves: row.extend([' '] * 5)
        board_no_moves.extend([[' '] * 8 for _ in range(5)])
        # Fill remaining with X to ensure X has more and O cannot move
        for r in range(8):
            for c in range(8):
                if board_no_moves[r][c] == ' ' and not (r==2 and c==2): # keep (2,2) empty for a moment
                     board_no_moves[r][c] = 'X'
        
        # Check actual valid moves based on this specific board
        # At this point, board_no_moves is almost full of X, with one O and one empty.
        # O is at (2,1). (2,2) is empty.
        # (2,0) is X. (1,1) is X. (1,2) is X. (0,2) is X.
        # O cannot move to (2,2) because it's not flanked by X.
        # X cannot move to (2,2) because it doesn't flip O.
        self.assertEqual(get_valid_moves(board_no_moves, 'O'), [], "O should have no moves")
        self.assertEqual(get_valid_moves(board_no_moves, 'X'), [], "X should have no moves")
        self.assertNotEqual(get_score(board_no_moves)['X'], get_score(board_no_moves)['O'])
        self.assertEqual(check_winner(board_no_moves), 'X', "X wins when no one can move and X has more pieces")

if __name__ == '__main__':
    unittest.main()
