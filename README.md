# Sudoku Solver with Visual Backtracking

A Python application that visualizes the backtracking algorithm solving Sudoku puzzles.

## Features

- Modern, dark-themed GUI using CustomTkinter
- Option to input your own Sudoku puzzle or use a default one
- Visual representation of the backtracking algorithm in action
- Step-by-step logging of the solving process
- Input validation to ensure valid Sudoku puzzles
- Centered window that maintains consistent appearance

## Requirements

- Python 3.7+
- CustomTkinter 5.1.2+

## Installation

1. Clone the repository or download the source code
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python sudoku_solver.py
   ```

## How to Use

1. Launch the application
2. Choose whether to use the default puzzle or input your own
3. If inputting your own puzzle:
   - Enter numbers 1-9 in the cells you want to prefill
   - Leave empty cells blank
4. Click "Solve Sudoku" to start the solving process
5. Watch as the algorithm works through the puzzle
6. Use "Reset / New Board" to start over or try a different puzzle

## How It Works

The application uses a backtracking algorithm to solve Sudoku puzzles:

1. Find an empty cell on the board
2. Try placing digits 1-9 in that cell
3. Check if the placement is valid according to Sudoku rules
4. If valid, recursively try to solve the rest of the board
5. If unsuccessful, backtrack and try the next digit
6. Repeat until the puzzle is solved or determined to be unsolvable

The solving process is visualized in real-time with color-coded feedback and step-by-step logging.

## Project Structure

- `sudoku_solver.py` - Main application file
- `README.md` - Project documentation
