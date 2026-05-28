import pygame

from Source.Constants.constants import SIZE_WALL, MARGIN


class Wall:
    def __init__(self, row, col, color):
        # Tạo bề mặt hình ảnh cho bức tường với kích thước cố định
        self.image = pygame.Surface([SIZE_WALL, SIZE_WALL])
        # self.image.fill(color)
        # Vẽ hình chữ nhật với viền màu đã chỉ định
        pygame.draw.rect(self.image, color, (0, 0, SIZE_WALL, SIZE_WALL), 1)

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