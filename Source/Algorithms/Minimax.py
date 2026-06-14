from Utils.Utils import *
from Constants.constants import *

_food_pos = []

def evaluationFunction(_map, pac_row, pac_col, N, M, score):
    """Hàm đánh giá (Heuristic): Tính điểm dựa vào trạng thái hiện tại của bàn cờ"""
    ghost_pos = []
    distancesToFoodList = []
    # Lấy tọa độ toàn bộ food và ghost
    for row in range(N):
        for col in range(M):
            if _map[row][col] == FOOD:
                # Tính khoảng cách Manhattan từ pacman tới thức ăn
                distancesToFoodList.append(Manhattan(row, col, pac_row, pac_col))
            if _map[row][col] == MONSTER:
                ghost_pos.append([row, col])
            if _map[row][col] == EMPTY:
                score += 5 # Thưởng nhỏ nếu ô trống (khuyến khích pacman đi qua nhiều ô)

    INF = 100000000.0  # Đại diện cho vô cùng lớn
    WEIGHT_FOOD = 100.0  # Trọng số cho mức độ quan trọng của food
    WEIGHT_GHOST = -150.0  # Trọng số cho mức độ nguy hiểm của ma

    _score = score
    # Khuyến khích pacman đi về phía viên thức ăn gần nhất (khoảng cách càng ngắn điểm càng cao)
    if len(distancesToFoodList) > 0:
        _score += WEIGHT_FOOD / (min(distancesToFoodList) if min(distancesToFoodList) != 0 else 1)
    else:
        _score += WEIGHT_FOOD # Nếu không còn food

    # Trừ điểm nếu có ghost gần pacman, ghost càng gần điểm trừ càng nặng
    for [g_r, g_c] in ghost_pos:
        distance = Manhattan(pac_row, pac_col, g_r, g_c)
        if distance > 0:
            _score += WEIGHT_GHOST / distance
        else:
            return -INF # Nếu chạm ma, điểm là âm vô cực (xấu nhất)

    return _score

def is_game_over(_map, _pac_row, _pac_col, _N, _M, _depth) -> bool:
        """Kiểm tra xem trò chơi đã đến trạng thái dừng chưa: hết cây tìm kiếm (depth=0), bị ma bắt, hoặc ăn hết mồi"""
        if _map[_pac_row][_pac_col] == MONSTER or _depth == 0:
            return True

        for row in range(_N):
            for col in range(_M):
                if _map[row][col] == FOOD:
                    return False # Vẫn còn mồi trên bản đồ

        return True

def minimaxAgent(_map, pac_row, pac_col, N, M, depth, Score):
    """Khởi tạo quá trình duyệt cây Minimax, Pacman đóng vai trò là hàm MAX (tối đa hoá điểm số)"""
    def max_value(_map, _pac_row, _pac_col, _N, _M, _depth, score):
        # Hàm MAX: Lượt của Pacman
        if is_game_over(_map, _pac_row, _pac_col, _N, _M, _depth):
            return evaluationFunction(_map, _pac_row, _pac_col, _N, _M, score)

        v = -10000000000000000
        for [_d_r, _d_c] in moving:
            _new_r, _new_c = _pac_row + _d_r, _pac_col + _d_c
            if isValid(_map, _new_r, _new_c, _N, _M):
                state = _map[_new_r][_new_c]
                _map[_new_r][_new_c] = EMPTY # Di chuyển tạm thời (Mô phỏng Pacman di chuyển)
                if state == FOOD:
                    score += 40
                    _food_pos.pop(_food_pos.index((_new_r, _new_c)))
                else:
                    score -= 2
                
                # Gọi hàm MIN cho lượt tiếp theo của ma quái
                v = max(v, min_value(_map, _new_r, _new_c, _N, _M, _depth - 1, score))
                
                # Hoàn tác lại nước đi để mô phỏng các hướng khác (Backtracking)
                _map[_new_r][_new_c] = state
                if state == FOOD:
                    score -= 40
                    _food_pos.append((_new_r, _new_c))
                else:
                    score += 2
        return v


    def min_value(_map, _pac_row, _pac_col, _N, _M, _depth, score):
        # Hàm MIN: Lượt của ma quái (cố gắng làm điểm Pacman tệ nhất có thể)
        if is_game_over(_map, _pac_row, _pac_col, _N, _M, _depth):
            return evaluationFunction(_map, _pac_row, _pac_col, _N, _M, score)

        v = 10000000000000000
        for row in range(_N):
            for col in range(_M):
                if _map[row][col] == MONSTER:
                    for [_d_r, _d_c] in moving:
                        _new_r, _new_c = _d_r + row, _d_c + col
                        if isWall(_map, _new_r, _new_c, _N, _M):
                            state = _map[_new_r][_new_c]
                            _map[_new_r][_new_c] = MONSTER # Mô phỏng Ghost di chuyển
                            _map[row][col] = EMPTY
                            
                            # Chuyển về lượt của Pacman
                            v = min(v, max_value(_map, _pac_row, _pac_col, _N, _M, _depth - 1, score))
                            
                            # Hoàn tác
                            _map[_new_r][_new_c] = state
                            _map[row][col] = MONSTER
        return v

    # Phần code khởi tạo (Gốc của cây Minimax)
    res = []
    global _food_pos
    _food_pos = []
    for _row in range(N):
        for _col in range(M):
            if _map[_row][_col] == FOOD:
                _food_pos.append((_row, _col))

    # Khảo sát từng nước đi có thể của Pacman từ vị trí ban đầu
    for [d_r, d_c] in moving:
        new_r, new_c = pac_row + d_r, pac_col + d_c
        if isValid(_map, new_r, new_c, N, M):
            _state = _map[new_r][new_c]
            _map[new_r][new_c] = EMPTY
            if _state == FOOD:
                Score += 40
                _food_pos.pop(_food_pos.index((new_r, new_c)))
            else:
                Score -= 2
            
            # Tính điểm (tệ nhất có thể) mà Ghost có thể gây ra nếu Pacman đi hướng này
            res.append(([new_r, new_c], min_value(_map, new_r, new_c, N, M, depth, Score)))
            
            _map[new_r][new_c] = _state
            if _state == FOOD:
                Score -= 40
                _food_pos.append((new_r, new_c))
            else:
                Score += 2

    # Sắp xếp kết quả dựa trên điểm số (tăng dần)
    res.sort(key=lambda k: k[1])
    # Trả về tọa độ nước đi có giá trị cao nhất
    if len(res) > 0:
        return res[-1][0]
    return []