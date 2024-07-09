#Kindly install tkinter module in order to use the gui form
import tkinter as tk

# Colors
COLORS = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'orange', 'purple', 'teal', 'pink', 'brown']

class NQueensGUI:
    def __init__(self, root, n):
        self.root = root
        self.n = n
        self.board = [-1] * n
        self.current_solution_index = -1
        
        self.canvas_size = 400
        self.square_size = self.canvas_size // n
        
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.canvas_clicked)  
        self.canvas.focus_set()  
        
        self.next_button = tk.Button(self.root, text="Next", command=self.next_solution)
        self.next_button.pack(side=tk.LEFT, padx=10)
        
        self.previous_button = tk.Button(self.root, text="Previous", command=self.previous_solution)
        self.previous_button.pack(side=tk.LEFT, padx=10)
        
        self.resize_label = tk.Label(self.root, text="Resize board:")
        self.resize_label.pack(side=tk.LEFT, padx=10)
        
        self.resize_entry = tk.Entry(self.root)
        self.resize_entry.pack(side=tk.LEFT, padx=10)
        
        self.resize_button = tk.Button(self.root, text="Resize", command=self.resize_board)
        self.resize_button.pack(side=tk.LEFT, padx=10)
        
        self.solution_counter_label = tk.Label(self.root, text="Solution: 0 / 0")
        self.solution_counter_label.pack()
        
        self.solve_n_queens()
        self.draw_board()
        self.update_solution_counter()
    
        self.canvas.bind("<Left>", lambda event: self.previous_solution())
        self.canvas.bind("<Right>", lambda event: self.next_solution())
    
    def solve_n_queens(self):
        def is_safe(board, row, col):
            for r in range(row):
                if board[r] == col or abs(board[r] - col) == row - r:
                    return False
            return True
        
        def solve(row):
            if row == self.n:
                yield self.board[:]
            else:
                for col in range(self.n):
                    if is_safe(self.board, row, col):
                        self.board[row] = col
                        yield from solve(row + 1)
        
        self.solutions = list(solve(0))
    
    #function to create the board
    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.n):
            for j in range(self.n):
                color = 'white' if (i + j) % 2 == 0 else 'black'
                self.canvas.create_rectangle(i * self.square_size, j * self.square_size,
                                             (i + 1) * self.square_size, (j + 1) * self.square_size,
                                             fill=color)
        
        if self.current_solution_index != -1:
            for row, col in enumerate(self.board):
                x = col * self.square_size + self.square_size // 2
                y = row * self.square_size + self.square_size // 2
                radius = self.square_size // 3
                color = COLORS[row % len(COLORS)]
                # Draw queen as a circle in the middle of the square
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
    
    def update_solution_counter(self):
        total_solutions = len(self.solutions)
        self.solution_counter_label.config(text=f"Solution: {self.current_solution_index + 1} / {total_solutions}")
    
    def next_solution(self, event=None):
        if self.solutions:
            self.current_solution_index = (self.current_solution_index + 1) % len(self.solutions)
            self.board = self.solutions[self.current_solution_index]
            self.draw_board()
            self.update_solution_counter()
    
    def previous_solution(self, event=None):
        if self.solutions:
            self.current_solution_index = (self.current_solution_index - 1) % len(self.solutions)
            self.board = self.solutions[self.current_solution_index]
            self.draw_board()
            self.update_solution_counter()
    
    def resize_board(self):
        try:
            new_size = int(self.resize_entry.get())
            if new_size < 4:
                raise ValueError("Minimum size must be 4.")
        except ValueError as e:
            print(f"Error: {e}")
            return
        
        self.n = new_size
        self.board = [-1] * self.n
        self.current_solution_index = -1
        self.square_size = self.canvas_size // self.n
        
        self.solve_n_queens()
        self.draw_board()
        self.update_solution_counter()
    
    def canvas_clicked(self, event):
        # Allow clicking on the canvas to navigate between solutions
        self.next_solution()

#Main function
def main():
    while True:
        try:
            n = int(input("Enter the number of queens (minimum 4): "))
            if n < 4:
                print("Error: Minimum number of queens must be 4.")
                print()
            else:
                break
        except ValueError:
            print("Error: Please enter a valid integer.")
    
    root = tk.Tk()
    root.title("N-Queens")
    
    app = NQueensGUI(root, n)
    
    root.mainloop()

if __name__ == "__main__":
    main()
