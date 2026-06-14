from Utils.Utils import find_nearest_food, moving, isValid

def BFS(_map, food_positions, r_start, c_start, N, M):
    # Khởi tạo mảng đánh dấu các ô đã đi qua
    visited = [[False for _ in range(M)] for _ in range(N)]
    # Khởi tạo mảng lưu vết đường đi (parent map) để truy vết lại path
    trace = [[[-1, -1] for _ in range(M)] for _ in range(N)]

    # Tìm viên thức ăn gần nhất theo khoảng cách Manhattan
    [food_row, food_col, index] = find_nearest_food(food_positions, r_start, c_start)

    # Nếu không còn thức ăn, trả về mảng rỗng
    if food_row == -1:
        return []
    
    # Hàng đợi dùng cho duyệt theo chiều rộng (Queue)
    queue = []
    chk = False # Biến cờ kiểm tra xem đã tìm thấy đường chưa
    visited[r_start][c_start] = True # Đánh dấu điểm xuất phát đã được thăm
    queue.append([r_start, c_start]) # Đưa điểm xuất phát vào Queue
    
    # Bắt đầu vòng lặp BFS
    while len(queue) > 0:
        [row, col] = queue.pop(0) # Lấy phần tử đầu tiên ra khỏi Queue

        # Kiểm tra xem đã đến đúng vị trí thức ăn chưa
        if row == food_row and col == food_col:
            chk = True
            break

        # Duyệt qua 4 hướng kề bên (phải, trái, lên, xuống)
        for i in range(4):
            new_row = row + moving[i][0]
            new_col = col + moving[i][1]
            # Nếu vị trí kề hợp lệ (không phải tường) và chưa được thăm
            if isValid(_map, new_row, new_col, N, M) and not visited[new_row][new_col]:
                visited[new_row][new_col] = True # Đánh dấu đã thăm
                trace[new_row][new_col] = [row, col] # Lưu vết cha của ô này
                queue.append([new_row, new_col]) # Đưa ô này vào Queue để duyệt tiếp

    # Nếu không tìm thấy đường đi đến viên thức ăn gần nhất (có thể bị chặn)
    if not chk:
        food_positions.pop(index) # Xóa viên đó khỏi danh sách
        return BFS(_map, food_positions, r_start, c_start, N, M) # Đệ quy tìm viên tiếp theo
    
    # Truy vết ngược từ thức ăn về điểm bắt đầu
    result = [[food_row, food_col]]
    [row, col] = trace[food_row][food_col]
    while row != -1:
        result.insert(0, [row, col]) # Chèn vào đầu danh sách kết quả
        [row, col] = trace[row][col]

    # Trả về đường đi đầy đủ từ Pacman tới thức ăn
    return result