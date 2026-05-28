import pygame

from Source.Constants.constants import  *


class Food:
    """
    Class biểu diễn thức ăn trong trò chơi Pacman.
    Thức ăn có thể là điểm nhỏ hoặc điểm lớn (màu vàng).
    """
    def __init__(self, row, col, width, height, color):
        """
        Khởi tạo đối tượng Food.
        
        Args:
            row: Vị trí hàng trên lưới.
            col: Vị trí cột trên lưới.
            width: Chiều rộng của thức ăn.
            height: Chiều cao của thức ăn.
            color: Màu sắc của thức ăn.
        """
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)  # Đặt màu trong suốt
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        self.row = row
        self.col = col

        # Thiết lập vị trí hình chữ nhật
        self.rect = self.image.get_rect()
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]
        # Điều chỉnh vị trí cho thức ăn lớn (màu vàng) để căn giữa
        if color == FOOD_ORANGE:
            self.rect.top += SIZE_WALL // 2 - height // 2
            self.rect.left += SIZE_WALL // 2 - width // 2

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))

    def getRC(self):
        return [self.row, self.col]