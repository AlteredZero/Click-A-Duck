import pygame

class Pool:
    def __init__(self, image, center, scale, base_size=600):
        self.original_image = image
        self.scale = scale
        self.center = center
        self.base_size = base_size

        self.pool_size_level = 1
        self.image = None
        self.rect = None

        self.update_size()

    def update_size(self):
        growth = 1 + (self.pool_size_level - 1) * 0.1

        size = int(self.base_size * growth * self.scale)

        self.image = pygame.transform.scale(
            self.original_image,
            (size, size)
        )

        self.rect = self.image.get_rect(center=self.center)

    def set_level(self, level):
        self.pool_size_level = level
        self.update_size()

    def get_center(self):
        return self.rect.center

    def get_radius(self):
        return self.rect.width // 2

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_image(self, image):
        self.original_image = image
        self.update_size()