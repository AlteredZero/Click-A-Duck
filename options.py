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


def open_options(screen, fonts, game_data, mouse_pos, draw_animated_text):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)
    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(250), sy(20), sx(400), sy(635))

    pygame.draw.rect(screen, (60, 60, 60), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

    draw_animated_text(
        screen,
        "Options",
        fonts["large"],
        (255,255,255),
        (menu_rect.centerx, sy(60)),
        "options_title"
    )

    options = [
        ("Music", "music"),
        ("SFX", "sfx"),
        ("Duck Text", "duckText"),
        ("Magical Auto Clickers", "magicalAutoClickers")
    ]

    clickable_rects = []

    start_y = sy(100)

    vol = game_data["settings"]["volume"]
    vol_percent = int(vol * 100)

    vol_text = fonts["small"].render(
        f"Volume: {vol_percent}%",
        False,
        (255,255,255)
    )

    vol_rect = vol_text.get_rect(
        centerx=menu_rect.centerx,
        y=start_y + len(options) * sy(60)
    )

    screen.blit(vol_text, vol_rect)

    minus_rect = pygame.Rect(
        vol_rect.left - sx(60),
        vol_rect.top,
        sx(40),
        sy(30)
    )

    pygame.draw.rect(screen, (150,150,150), minus_rect)
    screen.blit(
        fonts["small"].render("-", False, (0,0,0)),
        minus_rect.move(sx(12), sy(2))
    )

    plus_rect = pygame.Rect(
        vol_rect.right + sx(20),
        vol_rect.top,
        sx(40),
        sy(30)
    )

    pygame.draw.rect(screen, (150,150,150), plus_rect)
    screen.blit(
        fonts["small"].render("+", False, (0,0,0)),
        plus_rect.move(sx(12), sy(2))
    )

    clickable_rects.append((minus_rect, "volume_down"))
    clickable_rects.append((plus_rect, "volume_up"))


    for i, (label, key) in enumerate(options):

        is_on = game_data["settings"][key]

        color = (0, 220, 0) if is_on else (220, 0, 0)

        center_y = start_y + i * sy(60) + fonts["small"].get_height() // 2

        draw_animated_text(
            screen,
            f"{label}: {'ON' if is_on else 'OFF'}",
            fonts["small"],
            color,
            (menu_rect.centerx, center_y),
            f"options_line_{i}"
        )

        rect = pygame.Rect(
            menu_rect.centerx - 200,
            center_y - 20,
            400,
            40
        )

        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(
                screen,
                (100, 100, 100),
                rect.inflate(s(20), s(10))
        )

        clickable_rects.append((rect, key))


    save_text = fonts["small"].render(
        "SAVE GAME",
        False,
        (255, 255, 255)
    )

    save_rect = save_text.get_rect(
        centerx=menu_rect.centerx,
        y=vol_rect.bottom + sy(60)
    )

    pygame.draw.rect(
        screen,
        (4, 207, 116),
        save_rect.inflate(sx(20), sy(10))
    )


    quit_text = fonts["small"].render(
        "QUIT GAME",
        False,
        (255, 255, 255)
    )

    quit_rect = quit_text.get_rect(
        centerx=menu_rect.centerx,
        y=vol_rect.bottom + sy(120)
    )

    pygame.draw.rect(
        screen,
        (255,0,0),
        quit_rect.inflate(sx(20), sy(10))
    )


    wipe_text = fonts["small"].render(
        "CLEAR DATA",
        False,
        (255, 0, 0)
    )

    wipe_rect = wipe_text.get_rect(
        centerx=menu_rect.centerx,
        y=vol_rect.bottom + sy(245)
    )

    pygame.draw.rect(
        screen,
        (80, 0, 0),
        wipe_rect.inflate(sx(20), sy(10))
    )


    screen.blit(save_text, save_rect)
    screen.blit(quit_text, quit_rect)
    screen.blit(wipe_text, wipe_rect)


    clickable_rects.append((save_rect, "save_game"))
    clickable_rects.append((quit_rect, "quit_game"))
    clickable_rects.append((wipe_rect, "wipe_save"))

    return clickable_rects