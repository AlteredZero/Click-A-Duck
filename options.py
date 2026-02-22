import pygame

base_width = 2560
base_height = 1440

def draw_options(screen, mouse_pos, fonts):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    rect = pygame.Rect(sx(20), sy(20), sx(200), sy(60))

    pygame.draw.rect(screen, (60, 60, 60), rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, s(3))

    options_button = fonts["large"].render("Options", False, (255, 255, 255))
    screen.blit(options_button, options_button.get_rect(center=rect.center))

    return rect


def open_options(screen, fonts, game_data):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(250), sy(20), sx(300), sy(500))

    pygame.draw.rect(screen, (60, 60, 60), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

    title = fonts["large"].render("Options", False, (255, 255, 255))
    screen.blit(title, title.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(40)))

    music_text = fonts["small"].render("Music: ON", False, (255, 255, 255))
    screen.blit(music_text, music_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(90)))

    sfx_text = fonts["small"].render("SFX: ON", False, (255, 255, 255))
    screen.blit(sfx_text, sfx_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(130)))

    duck_text = fonts["small"].render("Duck Text: ON", False, (255, 255, 255))
    screen.blit(duck_text, duck_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(170)))