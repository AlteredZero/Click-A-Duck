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

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(250), sy(20), sx(500), sy(850))

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

    center_y = start_y + len(options) * sy(60)

    draw_animated_text(
        screen,
        f"Volume: {vol_percent}%",
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, center_y),
        "volume_text"
    )

    vol_rect = pygame.Rect(
        menu_rect.centerx - sx(120),
        center_y - sy(20),
        sx(240),
        sy(40)
    )

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

        center_y = start_y + i * sy(60)

        text_string = f"{label}: {'ON' if is_on else 'OFF'}"

        text_surface = fonts["small"].render(text_string, False, color)

        text_rect = text_surface.get_rect(center=(menu_rect.centerx, center_y))

        if text_rect.collidepoint(mouse_pos):

            bg_rect = text_rect.inflate(sx(20), sy(10))

            pygame.draw.rect(
                screen,
                (100, 100, 100),
                bg_rect,
            )

        draw_animated_text(
            screen,
            text_string,
            fonts["small"],
            color,
            (menu_rect.centerx, center_y),
            f"options_line_{i}"
        )

        clickable_rects.append((text_rect, key))

    settings = game_data["settings"]

    mode = settings["window_mode"]

    fullscreen_text = f"Window Mode: {mode.title()}"

    fullscreen_surface = fonts["small"].render(fullscreen_text, False, (255,255,255))

    fullscreen_rect = fullscreen_surface.get_rect(
        center=(menu_rect.centerx, vol_rect.bottom + sy(70))
    )

    if fullscreen_rect.collidepoint(mouse_pos):

        bg_rect = fullscreen_rect.inflate(sx(20), sy(10))

        pygame.draw.rect(
            screen,
            (100, 100, 100),
            bg_rect,
        )

    draw_animated_text(
        screen,
        fullscreen_text,
        fonts["small"],
        (255,255,255),
        fullscreen_rect.center,
        "fullscreen_text"
    )

    clickable_rects.append((fullscreen_rect, "window_mode"))

    resolutions = [
        [1280, 720],
        [1600, 900],
        [1920, 1080],
        [2560, 1440]
    ]

    current_resolution = settings["resolution"]

    res_text = f"Resolution: {current_resolution[0]}x{current_resolution[1]}"

    res_surface = fonts["small"].render(res_text, False, (255,255,255))

    res_rect = res_surface.get_rect(
        center=(menu_rect.centerx, fullscreen_rect.bottom + sy(40))
    )

    if res_rect.collidepoint(mouse_pos):

        bg_rect = res_rect.inflate(sx(20), sy(10))

        pygame.draw.rect(
            screen,
            (100, 100, 100),
            bg_rect,
        )

    draw_animated_text(
        screen,
        res_text,
        fonts["small"],
        (255,255,255),
        res_rect.center,
        "resolution_text"
    )

    clickable_rects.append((res_rect, "change_resolution"))

    draw_animated_text(
        screen,
        "*Changing resolution or",
        fonts["tiny"],
        (255,255,255),
        (res_rect.centerx, res_rect.bottom + sy(30)),
        "warning_text_1"
    )

    draw_animated_text(
        screen,
        "window mode will restart the game*",
        fonts["tiny"],
        (255,255,255),
        (res_rect.centerx, res_rect.bottom + sy(55)),
        "warning_text_2"
    )

    save_center_y = res_rect.bottom + sy(80)

    save_rect = pygame.Rect(
        menu_rect.centerx - sx(120),
        save_center_y - sy(0),
        sx(240),
        sy(40)
    )

    pygame.draw.rect(screen, (4, 207, 116), save_rect)

    draw_animated_text(
        screen,
        "SAVE GAME",
        fonts["small"],
        (255,255,255),
        save_rect.center,
        "save_game_text"
    )

    quit_rect = pygame.Rect(
        menu_rect.centerx - sx(120),
        save_rect.bottom + sy(40),
        sx(240),
        sy(40)
    )

    pygame.draw.rect(screen, (255,0,0), quit_rect)

    draw_animated_text(
        screen,
        "QUIT GAME",
        fonts["small"],
        (255,255,255),
        quit_rect.center,
        "quit_game_text"
    )

    wipe_rect = pygame.Rect(
        menu_rect.centerx - sx(120),
        quit_rect.bottom + sy(80),
        sx(240),
        sy(40)
    )

    pygame.draw.rect(screen, (80,0,0), wipe_rect)

    draw_animated_text(
        screen,
        "CLEAR DATA",
        fonts["small"],
        (255,0,0),
        wipe_rect.center,
        "wipe_save_text"
    )

    clickable_rects.append((save_rect, "save_game"))
    clickable_rects.append((quit_rect, "quit_game"))
    clickable_rects.append((wipe_rect, "wipe_save"))

    draw_animated_text(
        screen,
        "v1.1",
        fonts["verysmall"],
        (255,255,255),
        (wipe_rect.centerx, wipe_rect.bottom + sy(30)),
        "version_text"
    )

    return clickable_rects