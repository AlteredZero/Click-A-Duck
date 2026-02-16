import pygame
import math

class FloatingText:
    def __init__(self, text, pos, critical=False):
        self.text = text
        self.x, self.y = pos
        self.timer = 0
        self.scale = 0.0
        self.alpha = 255
        self.critical = critical

        self.angle = 0

        if self.critical:
            self.scale = 1.3

    def update(self):
        self.timer += 1

        if self.scale < 1:
            self.scale += 0.08

        self.y -= 2

        if self.timer > 20:
            self.alpha -= 10
            if self.alpha < 0:
                self.alpha = 0

        if self.critical:
            self.angle = math.sin(self.timer * 0.4) * 20

    def draw(self, screen, font):

        if self.critical:
            r = 255
            g = int(100 + 80 * math.sin(self.timer * 0.3))
            b = 180
            color = (r, g, b)
        else:
            color = (255, 255, 255)

        surf = font.render(self.text, True, color)

        surf = pygame.transform.scale(
            surf,
            (
                int(surf.get_width() * self.scale),
                int(surf.get_height() * self.scale)
            )
        )

        if self.critical:
            surf = pygame.transform.rotate(surf, self.angle)

        surf.set_alpha(self.alpha)

        rect = surf.get_rect(center=(self.x, self.y))
        screen.blit(surf, rect)

    def dead(self):
        return self.timer >= 60
