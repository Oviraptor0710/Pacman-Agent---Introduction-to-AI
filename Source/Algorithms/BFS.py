from Utils.Utils import find_nearest_food, moving, isValid

def BFS(_map, food_positions, start_row, start_col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = [[[-1, -1] for _ in range(M)] for _ in range(N)]

    [food_row, food_col, index] = find_nearest_food(food_positions, start_row, start_col)

    if food_row == -1:
        return []
    
    lt = []
    chk = False
    visited[start_row][start_col] = True
    lt.append([start_row, start_col])
    while len(lt) > 0:
        [row, col] = lt.pop(0)

        if row == food_row and col == food_col:
            chk = True
            break

        for i in range(4):
            new_row = row + moving[i][0]
            new_col = col + moving[i][1]
            if isValid(_map, new_row, new_col, N, M) and not visited[new_row][new_col]:
                visited[new_row][new_col] = True
                trace[new_row][new_col] = [row, col]
                lt.append([new_row, new_col]) 

    if not chk:
        food_positions.pop(index)
        return BFS(_map, food_positions, start_row, start_col, N, M)
    
    result = [[food_row, food_col]]
    [row, col] = trace[food_row][food_col]
    while row != -1:
        result.insert(0, [row, col])
        [row, col] = trace[row][col]

    return result