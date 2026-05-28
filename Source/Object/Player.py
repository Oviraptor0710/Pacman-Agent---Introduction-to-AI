import pygame

from Source.Constants.constants import SIZE_WALL, MARGIN


class Player:
    def __init__(self, row, col, fileImage):
        # Tải và điều chỉnh kích thước hình ảnh người chơi
        self.image = pygame.image.load(fileImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE_WALL, SIZE_WALL))

        # Thiết lập vị trí ban đầu của người chơi
        self.rect = self.image.get_rect()
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]
        self.row = row
        self.col = col

    def change_state(self, rotate, fileImage):
        # Thay đổi trạng thái và hướng của người chơi
        self.image = pygame.image.load(fileImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE_WALL, SIZE_WALL))
        self.image = pygame.transform.rotate(self.image, rotate)

        # Cập nhật hình chữ nhật và vị trí
        self.rect = self.image.get_rect()
        self.rect.top = self.row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = self.col * SIZE_WALL + MARGIN["LEFT"]

    def draw(self, screen):
        # Vẽ người chơi lên màn hình
        screen.blit(self.image, (self.rect.left, self.rect.top))

    def getRC(self):
        # Lấy tọa độ hàng và cột hiện tại
        return [self.row, self.col]

    def setRC(self, row, col):
        # Đặt tọa độ hàng và cột mới
        self.row = row
        self.col = col
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]

    def move(self, d_R, d_C):
        # Di chuyển người chơi theo một khoảng cách nhất định
        self.rect.top += d_R
        self.rect.left += d_C

    def touch_New_RC(self, row, col):
        # Kiểm tra xem người chơi đã chạm đến vị trí mới chưa
        return self.rect.top == row * SIZE_WALL + MARGIN["TOP"] and self.rect.left == col * SIZE_WALL + MARGIN["LEFT"]