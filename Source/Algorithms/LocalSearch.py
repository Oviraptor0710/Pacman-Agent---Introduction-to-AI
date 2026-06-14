from Utils.Utils import moving,isWall
from Source.Constants.constants import FOOD,MONSTER, WALL

def update_cost(_map, pos, current_pos, N, M, depth, visited, item_type, cost):
    """Hàm đệ quy lan truyền điểm số (Influence field) từ một đối tượng (Food/Ghost) ra xung quanh"""
    start_row, start_col = pos
    current_row, current_col = current_pos
    visited.append((current_row, current_col)) # Đánh dấu đã quét qua ô này

    # Dừng lan truyền nếu đạt đến độ sâu quy định hoặc quay lại vị trí bắt đầu
    if depth < 0 or pos == current_pos:
        return

    # Tính điểm dựa vào loại đối tượng và khoảng cách
    point = 0
    if item_type == FOOD: # Đối với mồi (thưởng)
        if depth == 2 :
            point = 40
        elif depth == 1 :
            point = 15
        else:
            point = 5

    elif item_type == MONSTER: # Đối với ma (phạt)
        if depth == 2:
            point = float("-inf") # Quá gần ma -> nguy hiểm tuyệt đối
        if depth == 1:
            point = float("-inf")
        if depth == 0:
            point = -100

    cost[current_row][current_col] += point # Cập nhật điểm cho ô hiện tại

    # Tiếp tục lan truyền ảnh hưởng đến các ô kề bên
    for d_r, d_c in moving:
        new_row, new_col = current_row + d_r, current_col + d_c
        if isWall(_map, new_row, new_col, N, M) and (new_row, new_col) not in visited:
            update_cost(_map, pos, (new_row, new_col), N, M, depth - 1, visited.copy(), item_type, cost)


def scan_surroundings(_map, pos, current_pos, N, M, depth, visited, cost, visited_penalty):
    """Quét xung quanh vị trí hiện tại để phát hiện thức ăn và ma quái, sau đó kích hoạt lan truyền"""
    start_row, start_col = pos
    current_row, current_col = current_pos
    visited.append((current_row, current_col))

    if depth <= 0:
        return

    # Khám phá các hướng có thể đi trong phạm vi depth
    for d_r, d_c in moving:
        new_row, new_col = current_row + d_r, current_col + d_c
        if isWall(_map, new_row, new_col, N, M) and (new_row, new_col) not in visited:
            # Nếu phát hiện thức ăn hoặc ma quái, lan truyền ảnh hưởng (sóng điểm số)
            object_pos = (new_row, new_col)
            if _map[new_row][new_col] == FOOD:
                update_cost(_map, pos, object_pos, N, M, 2, [], FOOD, cost)
            elif _map[new_row][new_col] == MONSTER:
                update_cost(_map, pos, object_pos, N, M, 2, [], MONSTER, cost)

            # Đệ quy tiếp tục khám phá sâu hơn
            scan_surroundings(_map, pos, object_pos, N, M, depth - 1, visited.copy(), cost, visited_penalty)

    # Trừ điểm (phạt) đối với các ô Pacman đã từng đi qua trước đó để tránh lặp (chạy vòng tròn)
    cost[current_row][current_col] -= visited_penalty[current_row][current_col]


def greedy_local_step(_map, start_row, start_col, N, M, visited_penalty):
    """Hàm chính tìm bước đi tiếp theo (chỉ 1 bước) theo hướng có điểm số lợi ích cục bộ cao nhất"""
    cost = [[0 for _ in range(M)] for _ in range(N)] # Ma trận lưu điểm của các ô xung quanh
    visited = []

    # Bắt đầu quét các ô xung quanh Pacman với depth=3 (tầm nhìn 3 ô)
    scan_surroundings(_map, (start_row, start_col), (start_row, start_col), N, M, 3, visited, cost, visited_penalty)

    # Tìm ô kề cạnh (4 hướng) có điểm số (cost) cao nhất
    max_score = float("-inf")
    best_move = []

    for d_r, d_c in moving:
        new_row, new_col = start_row + d_r, start_col + d_c
        if _map[new_row][new_col] != WALL and cost[new_row][new_col] > max_score:
            max_score = cost[new_row][new_col]
            best_move = [new_row, new_col]

    return best_move # Trả về vị trí của nước đi tốt nhất