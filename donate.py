import pygame

base_width = 2560
base_height = 1440


def draw_donate(screen, mouse_pos, fonts):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    background = (60, 60, 60)

    rect = pygame.Rect(sx(20), sy(160), sx(200), sy(60))

    pygame.draw.rect(screen, background, rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, s(3))

    donate_text = fonts["large"].render("Support", False, (255, 255, 255))
    screen.blit(donate_text, donate_text.get_rect(center=rect.center))

    return rect


def open_donate(screen, fonts, game_data, draw_animated_text):

    clickable_rects = []

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(250), sy(20), sx(750), sy(360))

    pygame.draw.rect(screen, (60, 60, 60), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)


    draw_animated_text(
        screen,
        "Support",
        fonts["large"],
        (255, 255, 255),
        (menu_rect.centerx, sy(60)),
        "support_title"
    )

    draw_animated_text(
        screen,
        "If you're enjoying the game, consider supporting me!",
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, sy(100)),
        "support_desc"
    )

    draw_animated_text(
        screen,
        "Every little bit helps me keep making more fun stuff.",
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, sy(140)),
        "support_desc2"
    )

    draw_animated_text(
        screen,
        "Cashapp: $AlteredDan",
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, sy(180)),
        "cashapp_desc"
    )

    draw_animated_text(
        screen,
        "Venmo: @Altered_Stuff",
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, sy(220)),
        "venmo_desc"
    )

    return clickable_rects

"""
    draw_animated_text(
        screen,
        "(opens in a new tab)",
        fonts["verysmall"],
        (255, 255, 255),
        (menu_rect.centerx, sy(260)),
        "support_desc3"
    )

    support_center_y = menu_rect.bottom - sy(70) + fonts["small"].get_height() // 2

    support_rect = pygame.Rect(
        menu_rect.centerx - sx(120),
        support_center_y - sy(20),
        sx(240),
        sy(40)
    )

    pygame.draw.rect(
        screen,
        (4, 207, 116),
        support_rect
    )

    draw_animated_text(
        screen,
        "SUPPORT!",
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, support_center_y),
        "support_button"
    )

    clickable_rects.append((support_rect, "support_button"))

    return clickable_rects"""