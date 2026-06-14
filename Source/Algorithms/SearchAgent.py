from Algorithms.BFS import BFS
from Algorithms.LocalSearch import *

from Algorithms.Minimax import *

class SearchAgent:
    """Lớp quản lý đóng vai trò trung gian gọi thuật toán di chuyển do người chơi chọn ở menu (Strategy Pattern)"""
    def __init__(self, _map, _food_Position, start_row, start_col, N, M):
        # Lưu trữ trạng thái hiện tại của ván game để truyền vào các thuật toán AI
        self.map = _map.copy()
        self.food_Position = _food_Position.copy()
        self.start_row = start_row
        self.start_col = start_col
        self.N = N
        self.M = M

    def execute(self, ALGORITHMS, visited=None, depth=4, Score=0):
        # Điều phối tới thuật toán tương ứng dựa trên string được chọn
        if ALGORITHMS == "BFS":
            return BFS(self.map, self.food_Position, self.start_row, self.start_col, self.N, self.M)
        if ALGORITHMS == "Local Search":
            return greedy_local_step(self.map, self.start_row, self.start_col, self.N, self.M, visited.copy())
        if ALGORITHMS == "Minimax":
            return minimaxAgent(self.map, self.start_row, self.start_col, self.N, self.M, depth, Score)
