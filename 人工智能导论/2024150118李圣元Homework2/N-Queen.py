import tkinter as tk
from tkinter import messagebox
def solve_n_queens(num):
    solutions = []
    n = num
    #判断是否合法
    def is_valid(queens, row, col):
        for i in range(row):
            if queens[i] == col or (row - i) == abs(col - queens[i]):
                return False
        return True
    def backtrack(row, queens):
        # 所有行放置完成，记录解
        if row == n:
            solutions.append(queens.copy())
            return
        # 遍历当前行的所有列
        for col in range(n):
            if is_valid(queens, row, col):
                queens.append(col)
                # 递归下一行
                backtrack(row + 1, queens)
                #回溯然后尝试下一列
                queens.pop(-1)
    backtrack(0, [])
    return solutions
class QueenNGUI:
    def __init__(self, root,n:int):
        self.root = root
        self.root.title(str(n)+"皇后问题 - 回溯法")
        self.root.resizable(False, False)
        # 初始化参数
        self.solutions = solve_n_queens(n)
        self.current_idx =-1
        self.cell_size = 60
        self.n = n           # n皇后
        self.canvas = tk.Canvas(root, width=self.n*self.cell_size, height=self.n*self.cell_size)
        self.canvas.pack(pady=10)
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        self.next_btn = tk.Button(btn_frame, text="下一个解", command=self.show_next_solution, font=("Arial", 12))
        self.next_btn.grid(row=0, column=0, padx=10)
        self.draw_board(None)

    def draw_board(self, queen_pos):
        self.canvas.delete("all")
        for row in range(self.n):
            for col in range(self.n):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                # 黑白交替颜色
                color = "#f0f0f0" if (row + col) % 2 == 0 else "#606060"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        if queen_pos:
            for row in range(self.n):
                col = queen_pos[row]
                x = col * self.cell_size + self.cell_size//2
                y = row * self.cell_size + self.cell_size//2
                self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="yellow", outline="red", width=2)
                self.canvas.create_text(x, y, text="Q", font=("Arial", 20, "bold"))

    def show_next_solution(self):
        self.current_idx += 1
        if self.current_idx >= len(self.solutions):
            messagebox.showinfo("提示", "已显示所有解（共"+str(len(self.solutions))+"个）！")
            self.current_idx = len(self.solutions) - 1
            return
        current_sol = self.solutions[self.current_idx]
        self.draw_board(current_sol)
        self.next_btn.config(text=f"下一个解（当前：{self.current_idx+1}/{(len(self.solutions))}")
if __name__ == "__main__":
    n=int(input("N="))
    root = tk.Tk()
    app = QueenNGUI(root,n)
    root.mainloop()