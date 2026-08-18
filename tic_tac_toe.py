import os
import sys


if sys.platform == "win32" and not os.environ.get("TCL_LIBRARY"):
    base = getattr(sys, "base_prefix", sys.prefix)  
    tcl_dir = os.path.join(base, "tcl", "tcl8.6")
    tk_dir = os.path.join(base, "tcl", "tk8.6")
    if os.path.isdir(tcl_dir):
        os.environ["TCL_LIBRARY"] = tcl_dir
    if os.path.isdir(tk_dir):
        os.environ["TK_LIBRARY"] = tk_dir

import tkinter as tk
from tkinter import messagebox

SIZE = 3                 # 棋盘是 3x3
CELL = 150               # 每个格子的边长
PADDING = 30             # 棋盘四周留白）
LINE_WIDTH = 6           # 网格线粗细
PIECE_INSET = 30         # 棋子离格子边线的距离

COLOR_BG = "#fdf6e3"      # 整体背景（米白）
COLOR_GRID = "#34495e"    # 网格线颜色（深灰蓝）
COLOR_X = "#e74c3c"       # 玩家 X 的颜色（红）
COLOR_O = "#2980b9"       # 玩家 O 的颜色（蓝）
COLOR_WIN = "#27ae60"     # 胜利连线高亮色（绿）
COLOR_TEXT = "#2c3e50"    # 状态文字颜色

class TicTacToe:
    """井字棋游戏主体，包含绘制、落子、判胜负等逻辑。"""

    def __init__(self, root):
        self.root = root
        self.root.title("井字棋 Tic-Tac-Toe")
        self.root.resizable(False, False)

        self.board = [[None] * SIZE for _ in range(SIZE)]
        self.current = "X"         
        self.game_over = False     

        self.score = {"X": 0, "O": 0, "平局": 0}

        self.status_var = tk.StringVar()
        self.status_var.set("轮到玩家 X 落子（红色）")
        self.status_label = tk.Label(
            root, textvariable=self.status_var,
            font=("微软雅黑", 18, "bold"), fg=COLOR_TEXT, bg=COLOR_BG,
        )
        self.status_label.pack(pady=(12, 6))

        # 棋盘画布 
        board_size = SIZE * CELL + 2 * PADDING
        self.canvas = tk.Canvas(
            root, width=board_size, height=board_size,
            bg=COLOR_BG, highlightthickness=0,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click) 

        #比分 + 按钮 
        self.score_var = tk.StringVar()
        self.update_score()
        self.score_label = tk.Label(
            root, textvariable=self.score_var,
            font=("微软雅黑", 13), fg=COLOR_TEXT, bg=COLOR_BG,
        )
        self.score_label.pack(pady=6)

        self.restart_btn = tk.Button(
            root, text="重新开始", command=self.reset,
            font=("微软雅黑", 13, "bold"), bg="#f39c12", fg="white",
            activebackground="#e67e22", activeforeground="white",
            padx=16, pady=4,
        )
        self.restart_btn.pack(pady=(0, 16))

        # 空棋盘
        self.draw_board()

    def draw_board(self):
        for i in range(1, SIZE):
            # 竖线
            x = PADDING + i * CELL
            self.canvas.create_line(
                x, PADDING, x, PADDING + SIZE * CELL,
                width=LINE_WIDTH, fill=COLOR_GRID, tags="grid",
            )
            # 横线
            y = PADDING + i * CELL
            self.canvas.create_line(
                PADDING, y, PADDING + SIZE * CELL, y,
                width=LINE_WIDTH, fill=COLOR_GRID, tags="grid",
            )

    def cell_center(self, row, col):
        x = PADDING + col * CELL + CELL // 2
        y = PADDING + row * CELL + CELL // 2
        return x, y

    def draw_x(self, row, col):
        x, y = self.cell_center(row, col)
        half = CELL // 2 - PIECE_INSET  
        self.canvas.create_line(
            x - half, y - half, x + half, y + half,
            width=10, fill=COLOR_X, capstyle=tk.ROUND, tags="piece",
        )
        self.canvas.create_line(
            x - half, y + half, x + half, y - half,
            width=10, fill=COLOR_X, capstyle=tk.ROUND, tags="piece",
        )

    def draw_o(self, row, col):
        x, y = self.cell_center(row, col)
        half = CELL // 2 - PIECE_INSET
        self.canvas.create_oval(
            x - half, y - half, x + half, y + half,
            width=10, outline=COLOR_O, tags="piece",
        )

    def draw_win_line(self, cells):
        points = []
        for row, col in cells:
            x, y = self.cell_center(row, col)
            points.extend([x, y])
        line = self.canvas.create_line(
            *points, width=14, fill=COLOR_WIN, capstyle=tk.ROUND, tags="winline",
        )
        self.canvas.tag_lower(line, "piece")

    def on_click(self, event):
        if self.game_over:
            return
        col = (event.x - PADDING) // CELL
        row = (event.y - PADDING) // CELL
        if not (0 <= row < SIZE and 0 <= col < SIZE):
            return
        if self.board[row][col] is not None:
            return

        self.board[row][col] = self.current
        if self.current == "X":
            self.draw_x(row, col)
        else:
            self.draw_o(row, col)

        # 判断胜负或者平局
        winner, win_cells = self.check_winner()
        if winner:
            self.game_over = True
            self.draw_win_line(win_cells)
            self.score[winner] += 1
            color = COLOR_X if winner == "X" else COLOR_O
            self.set_status(f"🎉 玩家 {winner} 获胜！", color)
            self.update_score()
            return

        if self.is_board_full():
            self.game_over = True
            self.score["平局"] += 1
            self.set_status("🤝 平局！棋盘已下满。", COLOR_TEXT)
            self.update_score()
            return
          
        self.current = "O" if self.current == "X" else "X"
        color = COLOR_X if self.current == "X" else COLOR_O
        name = "红色 X" if self.current == "X" else "蓝色 O"
        self.set_status(f"轮到玩家 {self.current} 落子（{name}）", color)

    def check_winner(self):
        # 所有可能连成一条线的三个格子的组合
        lines = []
        for r in range(SIZE):                    
            lines.append([(r, c) for c in range(SIZE)])
        for c in range(SIZE):                    
            lines.append([(r, c) for r in range(SIZE)])
        lines.append([(0, 0), (1, 1), (2, 2)])      
        lines.append([(0, 2), (1, 1), (2, 0)])     

        for line in lines:
            marks = [self.board[r][c] for r, c in line]
            if marks[0] is not None and marks[0] == marks[1] == marks[2]:
                return marks[0], line
        return None, None

    def is_board_full(self):
        for row in self.board:
            if None in row:
                return False
        return True

    def set_status(self, text, color):
        self.status_var.set(text)
        self.status_label.config(fg=color)

    def update_score(self):
        self.score_var.set(
            f"比分  ——  玩家 X：{self.score['X']}    "
            f"玩家 O：{self.score['O']}    平局：{self.score['平局']}"
        )

    def reset(self):
        self.board = [[None] * SIZE for _ in range(SIZE)]
        self.current = "X"
        self.game_over = False
        self.canvas.delete("piece")    
        self.canvas.delete("winline") 
        self.set_status("轮到玩家 X 落子（红色）", COLOR_X)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg=COLOR_BG)
    game = TicTacToe(root)
    root.mainloop()
