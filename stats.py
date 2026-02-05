import pygame

def draw_stats(screen, mouse_pos, fonts):

    base_width = 2560
    base_height = 1440

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    background = (60, 60, 60)

    rect = pygame.Rect(sx(20), sy(90), sx(200), sy(60))

    pygame.draw.rect(screen, background, rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, s(3))

    options_text = fonts["large"].render("Stats", False, (255, 255, 255))
    screen.blit(options_text, options_text.get_rect(center=rect.center))

    return rect