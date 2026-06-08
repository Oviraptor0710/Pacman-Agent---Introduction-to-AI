import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Source.Algorithms.Ghost_Move import Ghost_move_A_star
from Source.Object.Player import Player
from Source.Object.Wall import Wall
from Source.Object.Food import Food
from Source.Object.Menu import Menu,Button
import random
from Source.Algorithms.SearchAgent import SearchAgent
import pygame
from Utils.Utils import moving , isWall
from Source.Constants.constants import *
# KHỞI TẠO CÁC BIẾN    -
N = M = Score = _state_PacMan = 0
_map = []
_wall = []
_road = []
_food = []
_ghost = []
_food_Position = []
_ghost_Position = []
_visited = []
PacMan: Player
Level = 1
Map_name = ""
PacMan_Algorithm = "Minimax"

# KHỞI TẠO PYGAME
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PacMan AI')
clock = pygame.time.Clock()

pygame.font.init()
my_font = pygame.font.SysFont('Impact' ,50)    #Score lúc game run
my_font_2 = pygame.font.SysFont('Contrail One', 100) #Your Score ( Hiện lúc end game)

def readMapInFile(map_name: str):
    f = open(map_name, "r")   # Mở file để đọc
    x = f.readline().split()  # Đọc dòng đầu tiên của file, chứa kích thước bản đồ (N và M)
    global N, M, _map
    _map = []                    # Khởi tạo lại bản đồ
    N, M = int(x[0]), int(x[1])  # Gán N và M từ file vào các biến toàn cục (số hàng và số cột của bản đồ)

    for _ in range(N):  # Lặp qua từng hàng của bản đồ
        line = f.readline().split()
        _m = []
        for j in range(M):           # Lặp qua từng cột trong mỗi hàng
            _m.append(int(line[j]))
        _map.append(_m)

    global PacMan
    x = f.readline().split()  # Đọc dòng cuối cùng của file chứa tọa độ của PacMan

    # Tính toán lề (margin) để căn giữa bản đồ trên màn hình
    MARGIN["TOP"] = max(0, (HEIGHT - N * SIZE_WALL) // 2)
    MARGIN["LEFT"] = max(0, (WIDTH - M * SIZE_WALL) // 2)

    # Khởi tạo đối tượng PacMan với tọa độ lấy từ file và ảnh khởi tạo đầu tiên
    PacMan = Player(int(x[0]), int(x[1]), IMAGE_PACMAN[0])

    f.close()


def check_Object(_map, row, col):
    if _map[row][col] == WALL:
        _wall.append(Wall(row, col, WALL_DEEP_BLUE))
    if _map[row][col] == FOOD:
        _food.append(Food(row, col, BLOCK_SIZE, BLOCK_SIZE, FOOD_PINK))
        _food_Position.append([row, col])
    if _map[row][col] == MONSTER:
        _ghost.append(Player(row, col, IMAGE_GHOST[len(_ghost) % len(IMAGE_GHOST)]))
        _ghost_Position.append([row, col])

def initData() -> None:
    global N, M, _map, _food_Position, _food, _road, _wall, _ghost, _visited, Score, _state_PacMan, _ghost_Position
    N = M =  _state_PacMan = 0
    Score = 10
    _map = []
    _wall = []
    _road = []
    _food = []
    _ghost = []
    _food_Position = []
    _ghost_Position = []

    readMapInFile(map_name=Map_name)
    _visited = [[0 for _ in range(M)] for _ in range(N)]

    for row in range(N):
        for col in range(M):
            check_Object(_map, row, col)


def Draw(_screen) -> None:
    for obj_list in [_wall, _road, _food, _ghost]:
        for obj in obj_list:
            obj.draw(_screen)

    PacMan.draw(_screen)

    text_surface = my_font.render(f'Score: {Score}', False, RED)
    screen.blit(text_surface, (WIDTH - text_surface.get_width() - 10, 10))

# 1: Random, 2: A*
def generate_Ghost_new_position(_ghost, _type: int = 0) -> list[list[int]]:
    _ghost_new_position = []
    # Keep track of positions that are already assigned to ghosts
    occupied_positions = []
    if _type == 1:
        for idx in range(len(_ghost)):
            [row, col] = _ghost[idx].getRC()

            rnd = random.randint(0, 3)
            new_row, new_col = row + moving[rnd][0], col + moving[rnd][1]
            while not isWall(_map, new_row, new_col, N, M):
                rnd = random.randint(0, 3)
                new_row, new_col = row + moving[rnd][0], col + moving[rnd][1]

            _ghost_new_position.append([new_row, new_col])
    elif _type == 2:  # A*
        for idx in range(len(_ghost)):
            [start_row, start_col] = _ghost[idx].getRC()
            current_pos = [start_row, start_col]  # Current ghost position
            [end_row, end_col] = PacMan.getRC()

            # Get A* path
            new_pos = Ghost_move_A_star(_map, start_row, start_col, end_row, end_col, N, M)
            # Check if position is already occupied
            if new_pos in occupied_positions:
                # If collision would occur, keep ghost at current position
                _ghost_new_position.append(current_pos)
            else:
                _ghost_new_position.append(new_pos)
                occupied_positions.append(new_pos)

    return _ghost_new_position

def check_collision_ghost(_ghost, pac_row=-1, pac_col=-1) -> bool:
    Pac_pos = [pac_row, pac_col]
    if pac_row == -1:
        Pac_pos = PacMan.getRC()
    for g in _ghost:
        Ghost_pos = g.getRC()
        if Pac_pos == Ghost_pos:
            return True

    return False

def change_direction_PacMan(new_row, new_col):
    global PacMan, _state_PacMan
    [current_row, current_col] = PacMan.getRC()
    _state_PacMan = (_state_PacMan + 1) % len(IMAGE_PACMAN)

    if new_row > current_row:
        PacMan.change_state(-90, IMAGE_PACMAN[_state_PacMan])
    elif new_row < current_row:
        PacMan.change_state(90, IMAGE_PACMAN[_state_PacMan])
    elif new_col > current_col:
        PacMan.change_state(0, IMAGE_PACMAN[_state_PacMan])
    elif new_col < current_col:
        PacMan.change_state(180, IMAGE_PACMAN[_state_PacMan])

def randomPacManNewPos(_map, row, col, _N, _M):
    for [d_r, d_c] in moving:
        new_r, new_c = d_r + row, d_c + col
        if isWall(_map, new_r, new_c, _N, _M):
            return [new_r, new_c]


def startGame() -> None:
    global _map, _visited, Score, PacMan
    _ghost_new_position = []
    result = []
    new_PacMan_Pos = []
    initData()
    pac_can_move = True

    done = False
    is_moving = False
    timer = 0
    delay = 50
    status = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showMenu()
                return

        if delay > 0:
            delay -= 1
        if delay <= 0:
            if is_moving:
                timer += 1
                # Move Ghosts
                if len(_ghost_new_position) > 0:
                    for idx in range(len(_ghost)):
                        old_row_Gho, old_col_Gho = _ghost[idx].getRC()
                        new_row_Gho, new_col_Gho = _ghost_new_position[idx]
                        # Di chuyển ma quái
                        if old_row_Gho < new_row_Gho:
                            _ghost[idx].move(1, 0)
                        elif old_row_Gho > new_row_Gho:
                            _ghost[idx].move(-1, 0)
                        elif old_col_Gho < new_col_Gho:
                            _ghost[idx].move(0, 1)
                        elif old_col_Gho > new_col_Gho:
                            _ghost[idx].move(0, -1)

                        if timer >= SIZE_WALL:
                            _ghost[idx].setRC(new_row_Gho, new_col_Gho)
                            _map[old_row_Gho][old_col_Gho] = EMPTY
                            _map[new_row_Gho][new_col_Gho] = MONSTER

                            # Check va chạm với thức ăn
                            for index in range(len(_food)):
                                [row_food, col_food]= _food[index].getRC()
                                if row_food == old_row_Gho and col_food == old_col_Gho:
                                    _map[row_food][col_food] = FOOD

                # Move PacMan
                if len(new_PacMan_Pos) > 0:
                    [old_row_Pac, old_col_Pac] = PacMan.getRC()
                    [new_row_Pac, new_col_Pac]= new_PacMan_Pos

                    if old_row_Pac < new_row_Pac:
                        PacMan.move(1, 0)
                    elif old_row_Pac > new_row_Pac:
                        PacMan.move(-1, 0)
                    elif old_col_Pac < new_col_Pac:
                        PacMan.move(0, 1)
                    elif old_col_Pac > new_col_Pac:
                        PacMan.move(0, -1)

                    if timer >= SIZE_WALL or PacMan.touch_New_RC(new_row_Pac, new_col_Pac):
                        is_moving = False
                        PacMan.setRC(new_row_Pac, new_col_Pac)
                        Score -= 1

                        # Check va chạm với thức ăn
                        for idx in range(len(_food)):
                            [row_food, col_food] = _food[idx].getRC()
                            if row_food == new_row_Pac and col_food == new_col_Pac:
                                _map[row_food][col_food] = EMPTY
                                _food.pop(idx)
                                _food_Position.pop(idx)
                                Score += 50
                                break
                        new_PacMan_Pos = []

                if check_collision_ghost(_ghost): # Chạm Ma => LOST
                    pac_can_move = False
                    done = True
                    status = -1

                if len(_food_Position) == 0:# Hết food => win
                    status = 1
                    done = True
                if Score == -15 :  # Score = -15  => LOST
                    pac_can_move = False
                    done = True
                    status = -1
                if timer >= SIZE_WALL:
                    is_moving = False
            else:
                # Cập nhật vị trí của ma quái (based on level)
                if Level == 1:
                    _ghost_new_position = generate_Ghost_new_position(_ghost, _type=0) # No Moving
                elif Level == 2:
                    _ghost_new_position = generate_Ghost_new_position(_ghost, _type=1) # Random
                else:
                    _ghost_new_position = generate_Ghost_new_position(_ghost, _type=2) # A*

                is_moving = True
                timer = 0

                if not pac_can_move:
                    continue

                [row, col] = PacMan.getRC()

                # Use the selected PacMan algorithm from menu
                search = SearchAgent(_map, _food_Position, row, col, N, M)

                # Handle different algorithms based on user selection
                if PacMan_Algorithm == "BFS":
                    # Recalculate path when result is empty OR food was just eaten
                    food_eaten = False
                    for idx in range(len(_food)):
                        row_food, col_food = _food[idx].getRC()
                        if row_food == PacMan.getRC()[0] and col_food == PacMan.getRC()[1]:
                            food_eaten = True
                            break

                    if len(result) <= 0 or food_eaten:
                        result = search.execute(ALGORITHMS="BFS")
                        if len(result) > 0:
                            result.pop(0)  # Remove current position
                    elif len(result) > 0:
                        result.pop(0)

                    if len(result) > 0:
                        new_PacMan_Pos = result[0]

                elif PacMan_Algorithm == "Local Search" and len(_food_Position) > 0:
                    new_PacMan_Pos = search.execute(ALGORITHMS="Local Search", visited=_visited)
                    _visited[row][col] += 1

                elif PacMan_Algorithm == "Minimax" and len(_food_Position) > 0:
                    new_PacMan_Pos = search.execute(ALGORITHMS="Minimax", depth=4, Score=Score)

                #If no valid move is found, use random movement
                if len(_food_Position) > 0 and (len(new_PacMan_Pos) == 0 or [row, col] == new_PacMan_Pos):
                    new_PacMan_Pos = randomPacManNewPos(_map, row, col, N, M)

                if len(new_PacMan_Pos) > 0:
                    change_direction_PacMan(new_PacMan_Pos[0], new_PacMan_Pos[1])
                    if check_collision_ghost(_ghost, new_PacMan_Pos[0], new_PacMan_Pos[1]):
                        pac_can_move = False
                        done = True
                        status = -1

        # Vẽ các đối tượng lên màn hình
        screen.fill(BLACK)
        Draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    handleEndGame(status)



done_2 = False


def handleEndGame(status: int):
    global done_2
    done_2 = False
    bg = pygame.image.load(os.path.join(IMAGE_DIR, "Over_bg.jpg"))
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    bg_w = pygame.image.load(os.path.join(IMAGE_DIR, "win_bg.jpg"))
    bg_w = pygame.transform.scale(bg_w, (WIDTH, HEIGHT))

    def clickContinue():
        global done_2
        done_2 = True

    def clickQuit():
        pygame.quit()
        sys.exit(0)

    btnContinue = Button(WIDTH // 2 - 300, HEIGHT // 2 + 100, 200, 100, screen, "CONTINUE", clickContinue)
    btnQuit = Button(WIDTH // 2 + 90, HEIGHT // 2 + 100, 200, 100, screen, "QUIT", clickQuit)

    delay = 50
    while not done_2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if delay > 0:
            delay -= 1
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if status == -1:
            text_surface = my_font_2.render('You lost!! Your Score: {Score}'.format(Score=Score), False, RED)
            screen.blit(bg, (0, 0))
            screen.blit(text_surface, (WIDTH // 4 - 65, 10))
        else:
            screen.blit(bg_w, (0, 0))
            text_surface = my_font_2.render('Your Score: {Score}'.format(Score=Score), False, RED)
            screen.blit(text_surface, (WIDTH // 4 - 65, 10))

        btnQuit.process()
        btnContinue.process()

        pygame.display.flip()
        clock.tick(FPS)

    showMenu()



def showMenu():
    _menu = Menu(screen)
    global Level, Map_name, PacMan_Algorithm  # Add algorithm global
    [Level, Map_name, PacMan_Algorithm] = _menu.run()  # Get algorithm from menu
    startGame()

if __name__ == '__main__':
    showMenu()
    pygame.quit()