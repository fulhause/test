# Python Othello Game

This is an Othello (Reversi) game implemented in Python with a graphical user interface using Pygame.

## Files

*   `othello_logic.py`: Contains the core game logic (board representation, move validation, piece flipping, etc.).
*   `othello_gui.py`: Implements the Pygame-based GUI, event handling, and game flow.
*   `test_othello_logic.py`: Contains unit tests for the game logic.

## Requirements

*   Python 3
*   Pygame library

To install Pygame:
```bash
pip install pygame
```

## How to Play

1.  Ensure you have Python 3 and Pygame installed.
2.  Run the game using:
    ```bash
    python othello_gui.py
    ```
3.  Click on a highlighted square to place your piece.
4.  The game will indicate the current player, scores, and valid moves.
5.  Use the "New Game" button to restart the game.

## How to Run Tests

To run the unit tests for the game logic:
```bash
python -m unittest test_othello_logic.py
```
