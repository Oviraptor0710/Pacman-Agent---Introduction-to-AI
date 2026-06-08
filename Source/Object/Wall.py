import pygame
import os

from Source.Constants.constants import SIZE_WALL, MARGIN, IMAGE_DIR


class Wall:
    def __init__(self, row, col, color):
        # Load hình ảnh tường thay vì vẽ màu
        wall_image_path = os.path.join(IMAGE_DIR, "wall.png")
        if os.path.exists(wall_image_path):
            self.image = pygame.image.load(wall_image_path)
            self.image = pygame.transform.scale(self.image, (SIZE_WALL, SIZE_WALL))
        else:
            self.image = pygame.Surface([SIZE_WALL, SIZE_WALL])
            self.image.fill(color)

        # Lưu vị trí của bức tường trên lưới
        self.row = row
        self.col = col

        # Tạo hình chữ nhật để xác định vị trí trên màn hình
        self.rect = self.image.get_rect()
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]

    def draw(self, screen):
        # Vẽ bức tường lên màn hình tại vị trí đã định
        screen.blit(self.image, (self.rect.left, self.rect.top))