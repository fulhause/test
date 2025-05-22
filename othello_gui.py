import pygame
from othello_logic import initialize_board, get_valid_moves, is_valid_move, make_move, check_winner, get_score

# Initialize Pygame
pygame.init()

# --- Constants ---
# Window size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650 # Increased height for score display
WINDOW_TITLE = "Othello"

# Colors
BOARD_COLOR = (0, 128, 0)  # Green
GRID_COLOR = (0, 0, 0)     # Black
PLAYER_X_COLOR = (30, 30, 30)   # Dark Gray / Black
PLAYER_O_COLOR = (220, 220, 220) # Light Gray / White
HIGHLIGHT_COLOR = (255, 255, 0) # Yellow for valid moves

# Board dimensions
BOARD_ROWS = 8
BOARD_COLS = 8

# Calculate square size and piece radius
SQUARE_SIZE = SCREEN_WIDTH // BOARD_COLS # Assuming width and height are same for board area
PIECE_RADIUS = SQUARE_SIZE // 2 - 5 # A little padding
HIGHLIGHT_RADIUS = SQUARE_SIZE // 4 # For highlighting valid moves

# --- Pygame Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

if __name__ == '__main__':
    running = True
    # Game state variables
    current_board = initialize_board()
    current_player = 'X' # Player X starts
    game_over = False
    winner = None
    message_font = pygame.font.SysFont(None, 48) # Font for game over messages
    score_font = pygame.font.SysFont(None, 36) # Font for score display
    button_font = pygame.font.SysFont(None, 30) # Font for button text

    # "New Game" Button properties
    button_color = (100, 100, 100) # Grey
    button_hover_color = (150, 150, 150) # Lighter Grey
    button_text_color = (255, 255, 255) # White
    button_width = 150
    button_height = 40
    # Position button above the score area
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = SCREEN_HEIGHT - 70 # Adjusted to be above scores
    new_game_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)


    while running:
        mouse_pos = pygame.mouse.get_pos() # Get mouse position for hover effect

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                # Check if "New Game" button was clicked
                if new_game_button_rect.collidepoint(mouseX, mouseY):
                    # Reset game state
                    current_board = initialize_board()
                    current_player = 'X'
                    game_over = False
                    winner = None
                elif not game_over: # Process board clicks only if game is not over
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    # Ensure click is within board area before processing game move
                    if 0 <= clicked_row < BOARD_ROWS and 0 <= clicked_col < BOARD_COLS:
                        if is_valid_move(current_board, current_player, clicked_row, clicked_col):
                            make_move(current_board, current_player, clicked_row, clicked_col)
                            
                            # Switch player logic
                            next_player = 'O' if current_player == 'X' else 'X'
                            if get_valid_moves(current_board, next_player):
                                current_player = next_player
                            elif not get_valid_moves(current_board, current_player):
                                game_over = True
                                winner = check_winner(current_board)
                            
                            # Check for game over condition if not already set by player switch logic
                            if not game_over:
                                potential_winner = check_winner(current_board)
                                if potential_winner:
                                    game_over = True
                                    winner = potential_winner
        
        # --- Drawing ---
        screen.fill(BOARD_COLOR) 
        draw_board(screen, current_board, current_player if not game_over else None)

        # Draw "New Game" button
        current_button_color = button_hover_color if new_game_button_rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, current_button_color, new_game_button_rect)
        new_game_text = button_font.render("New Game", True, button_text_color)
        text_rect_button = new_game_text.get_rect(center=new_game_button_rect.center)
        screen.blit(new_game_text, text_rect_button)

        if game_over:
            message = ""
            if winner == 'Draw':
                message = "It's a Draw!"
            else:
                message = f"Player {winner} wins!"
            
            text_surface = message_font.render(message, True, (255, 0, 0))
            text_rect_msg = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 110)) # Position above button
            screen.blit(text_surface, text_rect_msg)
        
        # Display scores
        scores = get_score(current_board)
        score_text = f"Player X: {scores['X']}  Player O: {scores['O']}"
        score_surface = score_font.render(score_text, True, GRID_COLOR)
        score_rect_disp = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25))
        screen.blit(score_surface, score_rect_disp)

        pygame.display.flip()

def draw_board(screen, board_state, current_player):
    """
    Draws the Othello board and pieces onto the screen.

    Args:
        screen (pygame.Surface): The Pygame screen surface.
        board_state (list): The 2D list representing the Othello board.
    """
    screen.fill(BOARD_COLOR)

    # Draw grid lines
    for x in range(0, SCREEN_WIDTH, SQUARE_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, SQUARE_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    # Draw pieces
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            center_x = c * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = r * SQUARE_SIZE + SQUARE_SIZE // 2
            if board_state[r][c] == 'X':
                pygame.draw.circle(screen, PLAYER_X_COLOR, (center_x, center_y), PIECE_RADIUS)
            elif board_state[r][c] == 'O':
                pygame.draw.circle(screen, PLAYER_O_COLOR, (center_x, center_y), PIECE_RADIUS)

    # Highlight valid moves for the current_player, if game is not over
    if current_player: # current_player can be None if game is over
        valid_moves = get_valid_moves(board_state, current_player)
        for r, c in valid_moves:
            center_x = c * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = r * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(screen, HIGHLIGHT_COLOR, (center_x, center_y), HIGHLIGHT_RADIUS, 2) # Draw a thin circle

    pygame.quit()
