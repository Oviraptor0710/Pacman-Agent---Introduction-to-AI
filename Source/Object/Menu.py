import os
import sys

import pygame

from Source.Constants.constants import *

BLUE_LIGHT = (135, 206, 250)
clock = pygame.time.Clock()
bg = pygame.image.load(os.path.join(IMAGE_DIR, "intro_bg.png"))
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
pygame.init()
font = pygame.font.SysFont('Arial', 30)
my_font = pygame.font.SysFont('Impact', 45)



_N = _M = 0
__map = 0
SIZE_WALL = 20

menu_bg = pygame.image.load(os.path.join(IMAGE_DIR, "algo_bg.png"))  # Create this image
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

algo_bg_path = os.path.join(IMAGE_DIR, "algo_bg.png")
if os.path.exists(algo_bg_path):
    algo_bg = pygame.image.load(algo_bg_path)
    algo_bg = pygame.transform.scale(algo_bg, (WIDTH, HEIGHT))
else:
    algo_bg = menu_bg  # Fallback nếu chưa tải ảnh vào



class Button:
    def __init__(self, x, y, width, height, screen, buttonText="Button", onClickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction
        self.screen = screen

        self.fillColors = {
            'normal': '#FF9900',  # Cam
            'hover': '#E68A00',  # Cam đậm hơn (hover)
            'pressed': '#CC7A00',  # Cam đậm nhất (click)
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (255, 255, 255))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.onClickFunction()

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        pygame.draw.rect(self.buttonSurface, ORANGE, (0, 0, self.width, self.height), 5)
        self.screen.blit(self.buttonSurface, self.buttonRect)


class Menu:
    def __init__(self, screen):
        self.current_level = 0
        self.current_algorithm = ""  # New variable to store algorithm selection
        self.clicked = False
        self.map_name = []
        self.current_map = 0
        self.done = False
        self.current_screen = 1
        self.screen = screen
        self.btnStart = Button(WIDTH // 2 - 100 + 5, HEIGHT - 170, 200, 100, screen, "Start", self.myFunction)
        
        # Button layout variables cho Screen 2 và Screen 5
        button_width = 200
        center_x = WIDTH // 2 - button_width // 2
        start_y = HEIGHT // 2 - 160
        gap = 125

        # Level buttons
        self.btnLevel1 = Button(center_x, start_y, button_width, 80, screen, "No Moving",
                                self._load_level_1)
        self.btnLevel2 = Button(center_x, start_y + gap, button_width, 80, screen, "Random",
                                self._load_level_2)
        self.btnLevel3 = Button(center_x, start_y + 2 * gap, button_width, 80, screen, "A*",
                                self._load_level_3)

        # Algorithm buttons
        self.btnBFS = Button(center_x, start_y, button_width, 80, screen, "BFS",
                             lambda: self._set_algorithm("BFS"))
        self.btnLocalSearch = Button(center_x, start_y + gap, button_width, 80, screen, "Local Search",
                                    lambda: self._set_algorithm("Local Search"))
        self.btnMinimax = Button(center_x, start_y + 2 * gap, button_width, 80, screen, "Minimax",
                                lambda: self._set_algorithm("Minimax"))

        # Map navigation buttons
        self.btnPrev = Button(WIDTH // 2 - 250, HEIGHT // 4 * 3 + 35, 100, 100, screen, "<", self.prevMap)
        self.btnNext = Button(WIDTH // 2 + 150, HEIGHT // 4 * 3 + 35, 100, 100, screen, ">", self.nextMap)
        self.btnPlay = Button(WIDTH // 2 - 75, HEIGHT // 4 * 3 + 35, 150, 100, screen, "PLAY", self.selectMap)
        self.btnBack = Button(40, HEIGHT // 4 * 3 + 35, 150, 100, screen, "BACK", self.goBack)

        # Back buttons for Level and Algorithm screens (centered, smaller height)
        self.btnLevelBack = Button(WIDTH // 2 - 75, start_y + 3 * gap, 150, 60, screen, "BACK", self.goBackToMenu)
        self.btnAlgoBack = Button(WIDTH // 2 - 75, start_y + 3 * gap, 150, 60, screen, "BACK", self.goBackToLevel)

    def myFunction(self):
        """Callback for the Start button"""
        if self.clicked:
            self.current_screen = 2  # Move to level selection screen
        self.clicked = False

    def goBackToMenu(self):
        """Go back to main menu from level selection"""
        if self.clicked:
            self.current_screen = 1
        self.clicked = False

    def _set_algorithm(self, algorithm):
        if self.clicked:
            self.current_algorithm = algorithm
            self._load_maps_for_level()
            self.current_screen = 3
        self.clicked = False

    def _load_level_1(self):
        if self.clicked:
            self.current_level = 1
            self.current_screen = 5  # Go to algorithm selection
        self.clicked = False

    def _load_level_2(self):
        if self.clicked:
            self.current_level = 2
            self.current_screen = 5  # Go to algorithm selection
        self.clicked = False

    def _load_level_3(self):
        if self.clicked:
            self.current_level = 3
            self.current_screen = 5  # Go to algorithm selection
        self.clicked = False

    def _load_level_4(self):
        if self.clicked:
            self.current_level = 4
            self.current_screen = 5  # Go to algorithm selection
        self.clicked = False

    def _load_maps_for_level(self):
        """Load maps for the current level"""
        self.map_name = []
        self.current_map = 0
        level_dir = os.path.join(os.path.dirname(BASE_DIR), "Map")
        for file in os.listdir(level_dir):
            self.map_name.append(os.path.join(level_dir, file))

    def goBack(self):
        """Go back to algorithm selection"""
        self.current_screen = 5

    def goBackToLevel(self):
        """Go back to level selection"""
        self.current_screen = 2

    def prevMap(self):
        """Navigate to the previous map"""
        if self.clicked:
            if len(self.map_name) > 0:
                self.current_map = (self.current_map - 1) % len(self.map_name)
                self.current_screen = 3  # Refresh map display
        self.clicked = False

    def nextMap(self):
        """Navigate to the next map"""
        if self.clicked:
            if len(self.map_name) > 0:
                self.current_map = (self.current_map + 1) % len(self.map_name)
                self.current_screen = 3  # Refresh map display
        self.clicked = False

    def selectMap(self):
        if self.clicked:
            self.done = True

    def draw_map(self, map_path):

        f = open(map_path, "r")
        x = f.readline().split()
        count_ghost = 0
        N, M = int(x[0]), int(x[1])

        MARGIN_TOP = 100
        MARGIN_LEFT = (WIDTH - M * SIZE_WALL) // 2
        
        # Tối ưu hóa: Load ảnh tường một lần duy nhất vào bộ nhớ (Preload)
        wall_image_path = os.path.join(IMAGE_DIR, "wall.png")
        if os.path.exists(wall_image_path):
            wall_surf = pygame.image.load(wall_image_path).convert()
            wall_surf = pygame.transform.scale(wall_surf, (SIZE_WALL, SIZE_WALL))
        else:
            wall_surf = pygame.Surface([SIZE_WALL, SIZE_WALL])
            wall_surf.fill(WALL_DEEP_BLUE)

        for i in range(N):
            line = f.readline().split()
            for j in range(M):
                cell = int(line[j])
                if cell == WALL:
                    top = i * SIZE_WALL + MARGIN_TOP
                    left = j * SIZE_WALL + MARGIN_LEFT
                    self.screen.blit(wall_surf, (left, top))
                elif cell == FOOD:
                    image = pygame.Surface([SIZE_WALL // 2, SIZE_WALL // 2])
                    image.fill(WHITE)
                    image.set_colorkey(WHITE)
                    pygame.draw.ellipse(image, FOOD_ORANGE, [0, 0, SIZE_WALL // 2, SIZE_WALL // 2])

                    top = i * SIZE_WALL + MARGIN_TOP + SIZE_WALL // 2 - SIZE_WALL // 4
                    left = j * SIZE_WALL + MARGIN_LEFT + SIZE_WALL // 2 - SIZE_WALL // 4
                    self.screen.blit(image, (left, top))
                elif cell == MONSTER:
                    image = pygame.image.load(IMAGE_GHOST[count_ghost]).convert_alpha()
                    image = pygame.transform.scale(image, (SIZE_WALL, SIZE_WALL))
                    top = i * SIZE_WALL + MARGIN_TOP
                    left = j * SIZE_WALL + MARGIN_LEFT
                    count_ghost = (count_ghost + 1) % len(IMAGE_GHOST)
                    self.screen.blit(image, (left, top))

        # Draw Pacman
        x = f.readline().split()
        image = pygame.image.load(IMAGE_PACMAN[0]).convert_alpha()
        image = pygame.transform.scale(image, (SIZE_WALL, SIZE_WALL))
        top = int(x[0]) * SIZE_WALL + MARGIN_TOP
        left = int(x[1]) * SIZE_WALL + MARGIN_LEFT
        self.screen.blit(image, (left, top))

        f.close()

    def run(self):
        while not self.done:
            self.clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            if self.current_screen == 1:
                # Main menu
                self.screen.blit(bg, (0, 0))
                self.btnStart.process()

            elif self.current_screen == 2:
                # Level selection
                self.screen.blit(algo_bg, (0, 0))
                text_surface = my_font.render('SELECT GHOST MOVE', False, WHITE)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
                self.screen.blit(text_surface, text_rect)
                self.btnLevel1.process()
                self.btnLevel2.process()
                self.btnLevel3.process()
                self.btnLevelBack.process()

            elif self.current_screen == 5:
                # Algorithm selection (new screen)
                self.screen.blit(algo_bg, (0, 0))
                text_surface = my_font.render('SELECT PACMAN ALGORITHMS', False, WHITE)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
                self.screen.blit(text_surface, text_rect)
                self.btnBFS.process()
                self.btnLocalSearch.process()
                self.btnMinimax.process()
                #self.btnMCTS.process()
                self.btnAlgoBack.process()

            elif self.current_screen == 3:
                # Load map display
                self.screen.fill((20, 30, 48)) # Màu Xanh Lam Đậm (Dark Navy) hợp với Cam
                self.current_screen = 4
                self.draw_map(self.map_name[self.current_map])

            elif self.current_screen == 4:
                # Map navigation
                if self.current_level == 1:
                    X= 'No Moving'
                elif self.current_level == 2:
                    X= 'Random Move'
                else :
                    X= 'A* Move'
                text = f'{X} - {self.current_algorithm}'
                text_surface = my_font.render(text, False, WHITE) # Đổi sang chữ trắng
                self.screen.blit(text_surface, (WIDTH // 2 - 200, 0))
                
                # Draw Map Name centered below the map
                map_filename = os.path.basename(self.map_name[self.current_map])
                map_name_str = map_filename.replace('.txt', '').capitalize()
                map_name_str = map_name_str.replace('Map', 'Map ')
                map_name_surface = my_font.render(map_name_str, False, ORANGE)
                text_rect = map_name_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 90))
                self.screen.blit(map_name_surface, text_rect)
                
                self.btnNext.process()
                self.btnPrev.process()
                self.btnPlay.process()
                self.btnBack.process()

            pygame.display.flip()
            clock.tick(FPS)

        # Return level, map and algorithm
        return [self.current_level, self.map_name[self.current_map], self.current_algorithm]