import pygame

font_path = "assets/fonts/pixelFont.ttf"

base_sizes = {
    "header": 48,
    "large": 28,
    "small": 23,
    "verysmall": 21,
}

def load_fonts(scale=1.0):
    s = lambda size: max(12, int(size * scale))

    return {
        name: pygame.font.Font(font_path, s(size))
        for name, size in base_sizes.items()
    }