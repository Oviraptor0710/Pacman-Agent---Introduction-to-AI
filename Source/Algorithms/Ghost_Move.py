from queue import PriorityQueue

from Source.Utils.Utils import *

def A_Star(_map, start_row, start_col, end_row, end_col, N, M):
    """Thuật toán A* điều khiển Ma đi tìm đường ngắn nhất để đến ăn Pacman"""
    # Khởi tạo ma trận đánh dấu ô đã thăm
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = {} # Lưu lại node cha để truy vết (came_from)
    cost = {}  # Cost thực tế tính từ điểm bắt đầu: g(n)
    path = []  # Lưu đường đi khi tìm thấy đích
    queue = PriorityQueue() # Open list được sắp xếp dựa trên hàm f(n) = g(n) + h(n)

    start = (start_row, start_col) # Vị trí của Ghost
    end = (end_row, end_col)       # Vị trí của Pacman

    cost[start] = 0
    # Đưa gốc vào Queue (Tuple gồm (f(n), Tọa_độ)), trong đó h(n) là khoảng cách Manhattan
    queue.put((Manhattan(start_row, start_col, end_row, end_col), start))

    # Vòng lặp lấy phần tử có f(n) nhỏ nhất ra xử lý
    while not queue.empty():
        current = queue.get()[1]
        visited[current[0]][current[1]] = True
        
        # Nếu đã tới được vị trí của Pacman
        if current == end:
            path.append([current[0], current[1]])
            # Bắt đầu vòng lặp truy ngược trace để tìm ra đường đi
            while current != start:
                current = trace[current]
                path.append([current[0], current[1]])
            path.reverse() # Đường đi ban đầu là ngược từ đích, cần đảo lại
            # Nếu path lớn hơn 1 (cách pacman >=1 bước), trả về bước đi TIẾP THEO ngay lập tức
            return path[1] if len(path) > 1 else [start_row, start_col]

        # Khám phá các hướng kề
        for [d_r, d_c] in moving:
            new_row, new_col = current[0] + d_r, current[1] + d_c
            # Nếu không phải tường và chưa thăm
            if isWall(_map, new_row, new_col, N, M) and not visited[new_row][new_col]:
                group = (new_row, new_col)
                cost[group] = cost[current] + 1 # Cập nhật g(n) = g(n_cha) + 1
                
                # f(n) = g(n) + h(n) (khoảng cách ước lượng đến đích)
                queue.put((cost[group] + Manhattan(new_row, new_col, end_row, end_col), group))
                trace[group] = current # Lưu vết bước này đến từ đâu

    # Trả về tọa độ hiện tại nếu bị kẹt (đứng yên)
    return [start_row, start_col]