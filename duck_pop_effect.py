import pygame
import random

class DuckPopEffect:
    def __init__(self, image, pos):
        self.original = image
        self.image = image.copy()

        self.pos = pygame.Vector2(pos)

        self.vel = pygame.Vector2(
            random.uniform(-2, 2),
            random.uniform(-8, -5)
        )
        self.gravity = 0.35

        self.angle = 0
        self.spin = random.uniform(-8, 8)

        self.alpha = 255
        self.fade_speed = 6

        self.dead_flag = False

    def update(self):
        self.vel.y += self.gravity
        self.pos += self.vel

        self.angle += self.spin

        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.dead_flag = True

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.original, self.angle)
        rotated.set_alpha(max(0, self.alpha))

        rect = rotated.get_rect(center=self.pos)
        screen.blit(rotated, rect)

    def dead(self):
        return self.dead_flag
