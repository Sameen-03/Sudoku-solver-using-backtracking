import customtkinter as ctk
import time

# Your default board
default_board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver - Visual Backtracking")
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("dark")

        # Set window to fixed size and center it
        self.root.resizable(False, False)  # Disable resizing
        self.center_window(750, 600)  # Set initial size

        # Initialize board as None
        self.board = None

        # Create the main frame
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Show board selection dialog first
        self.show_board_selection()

    def center_window(self, width, height):
        """Center the window on the screen with the given width and height"""
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position coordinates
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set window geometry
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show_board_selection(self):
        # Clear any existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create selection frame
        selection_frame = ctk.CTkFrame(self.main_frame)
        selection_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title label
        title_label = ctk.CTkLabel(selection_frame, text="Sudoku Solver", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        # Question label
        question_label = ctk.CTkLabel(selection_frame, text="Would you like to input your own Sudoku board?",
                                      font=("Arial", 16))
        question_label.pack(pady=10)

        # Buttons frame
        buttons_frame = ctk.CTkFrame(selection_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)

        # Yes button
        yes_button = ctk.CTkButton(buttons_frame, text="Yes, input my own board", command=self.create_empty_board)
        yes_button.grid(row=0, column=0, padx=10)

        # No button
        no_button = ctk.CTkButton(buttons_frame, text="No, use default board", command=self.create_default_board)
        no_button.grid(row=0, column=1, padx=10)

    def create_empty_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.setup_main_interface()

    def create_default_board(self):
        self.board = [row[:] for row in default_board]  # Create a deep copy
        self.setup_main_interface()

    def setup_main_interface(self):
        # Clear any existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Frame for board
        self.board_frame = ctk.CTkFrame(self.main_frame)
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)

        self.entries = []
        for i in range(9):
            row = []
            for j in range(9):
                # Create entry with a slightly larger size
                entry = ctk.CTkEntry(self.board_frame, width=40, height=40, font=('Arial', 20), justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)

                # If using default board and there's a value, display it
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.configure(state="disabled", text_color="white")

                row.append(entry)
            self.entries.append(row)

        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        buttons_frame.grid(row=1, column=0, pady=10)

        # Start button
        self.solve_button = ctk.CTkButton(buttons_frame, text="Solve Sudoku", command=self.start_solving)
        self.solve_button.grid(row=0, column=0, padx=10)

        # Reset button
        self.reset_button = ctk.CTkButton(buttons_frame, text="Reset / New Board", command=self.show_board_selection)
        self.reset_button.grid(row=0, column=1, padx=10)

        # Frame for logging
        self.log_frame = ctk.CTkFrame(self.main_frame)
        self.log_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.log_text = ctk.CTkTextbox(self.log_frame, width=300, height=500, font=("Courier", 12))
        self.log_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.log_frame, command=self.log_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=self.scrollbar.set)

        # Welcome message
        self.log("Welcome to Sudoku Solver!")
        if all(self.board[i][j] == 0 for i in range(9) for j in range(9)):
            self.log("Please input your Sudoku puzzle.")
            self.log("Use numbers 1-9 for filled cells.")
            self.log("Leave empty cells blank.")
            self.log("Then press 'Solve Sudoku'.")

    def start_solving(self):
        # First, update the board from entries
        self.update_board_from_entries()

        # Check if board is valid
        if not self.is_valid_board():
            self.log("Invalid board! Please check your inputs.", color="red")
            return

        self.log("Starting to solve...", color="lightblue")
        self.solve(self.board)

    def update_board_from_entries(self):
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get().strip()
                if value:
                    try:
                        self.board[i][j] = int(value)
                    except ValueError:
                        self.board[i][j] = 0
                else:
                    self.board[i][j] = 0

    def is_valid_board(self):
        # Check that initial placement is valid
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    # Temporarily set cell to 0
                    num = self.board[i][j]
                    self.board[i][j] = 0

                    # Check if the number is valid in this position
                    if not valid(self.board, num, (i, j)):
                        self.board[i][j] = num  # Restore number
                        return False

                    # Restore number
                    self.board[i][j] = num
        return True

    def solve(self, bo):
        find = find_empty(bo)
        if not find:
            self.log("Sudoku Solved!", color="lightgreen")
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(bo, i, (row, col)):
                bo[row][col] = i

                self.entries[row][col].configure(state="normal")
                self.entries[row][col].delete(0, ctk.END)
                self.entries[row][col].insert(0, str(i))
                self.entries[row][col].configure(text_color="lightgreen")
                self.entries[row][col].configure(state="readonly")

                self.log(f"Trying {i} at ({row + 1}, {col + 1})", color="lightgreen")

                self.root.update()
                time.sleep(0.1)  # Slightly faster animation

                if self.solve(bo):
                    return True

                # Backtrack
                bo[row][col] = 0
                self.entries[row][col].configure(state="normal")
                self.entries[row][col].delete(0, ctk.END)
                self.entries[row][col].configure(state="readonly")

                self.log(f"Backtracking from ({row + 1}, {col + 1})", color="red")

                self.root.update()
                time.sleep(0.1)  # Slightly faster animation

        return False

    def log(self, message, color="white"):
        self.log_text.configure(state="normal")
        self.log_text.insert(ctk.END, message + "\n")
        self.log_text.tag_add(color, "end-2l", "end-1l")
        self.log_text.tag_config(color, foreground=color)
        self.log_text.see(ctk.END)
        self.log_text.configure(state="disabled")


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)
    return None


if __name__ == "__main__":
    root = ctk.CTk()
    app = SudokuGUI(root)
    root.mainloop()