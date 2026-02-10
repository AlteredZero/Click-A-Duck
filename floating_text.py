import pygame

class FloatingText:
    def __init__(self, text, pos, color=(255, 255, 255)):
        self.text = text
        self.x, self.y = pos
        self.timer = 0
        self.scale = 0.0
        self.alpha = 255
        self.color = color

    def update(self):
        self.timer += 1

        if self.scale < 1:
            self.scale += 0.08

        self.y -= 2

        if self.timer > 15 * 0.5:
            self.alpha -= 8
            if self.alpha < 0:
                self.alpha = 0

    def draw(self, screen, font):
        surf = font.render(self.text, True, self.color)
        surf = pygame.transform.scale(
            surf,
            (
                int(surf.get_width() * self.scale),
                int(surf.get_height() * self.scale)
            )
        )

        surf.set_alpha(self.alpha)
        rect = surf.get_rect(center=(self.x, self.y))
        screen.blit(surf, rect)

    def dead(self):
        return self.timer >= 60