import pygame

base_width = 2560
base_height = 1440


def draw_socials(screen, mouse_pos, fonts):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    rect = pygame.Rect(sx(20), sy(160), sx(200), sy(60))

    pygame.draw.rect(screen, (60, 60, 60), rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, s(3))

    donate_text = fonts["large"].render("Socials", False, (255, 255, 255))
    screen.blit(donate_text, donate_text.get_rect(center=rect.center))

    return rect


def open_socials(screen, fonts, draw_animated_text, youtube_logo, discord_logo, x_logo, cashapp_logo, venmo_logo):

    clickable_rects = []

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(250), sy(20), sx(755), sy(320))

    pygame.draw.rect(screen, (60, 60, 60), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

    draw_animated_text(
        screen,
        "Socials",
        fonts["large"],
        (255, 255, 255),
        (menu_rect.centerx, sy(60)),
        "support_title"
    )

    draw_animated_text(
        screen,
        "Stay connected with us!",
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, sy(120)),
        "support_desc"
    )

    draw_animated_text(
        screen,
        "Follow our official channels for",
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, sy(175)),
        "support_desc2"
    )

    draw_animated_text(
        screen,
        "updates, gameplay, and community chat.",
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, sy(200)),
        "support_desc3"
    )

    youtube_logo = pygame.transform.scale(youtube_logo, (55, 55))
    youtube_logo_rect = youtube_logo.get_rect(center=(menu_rect.centerx - 160, sy(280)))
    screen.blit(youtube_logo, youtube_logo_rect)

    discord_logo = pygame.transform.scale(discord_logo, (55, 55))
    discord_logo_rect = discord_logo.get_rect(center=(menu_rect.centerx - 80, sy(280)))
    screen.blit(discord_logo, discord_logo_rect)

    x_logo = pygame.transform.scale(x_logo, (55, 55))
    x_logo_rect = x_logo.get_rect(center=(menu_rect.centerx, sy(280)))
    screen.blit(x_logo, x_logo_rect)

    cashapp_logo = pygame.transform.scale(cashapp_logo, (55, 55))
    cashapp_logo_rect = cashapp_logo.get_rect(center=(menu_rect.centerx + 80, sy(280)))
    screen.blit(cashapp_logo, cashapp_logo_rect)

    venmo_logo = pygame.transform.scale(venmo_logo, (55, 55))
    venmo_logo_rect = venmo_logo.get_rect(center=(menu_rect.centerx + 160, sy(280)))
    screen.blit(venmo_logo, venmo_logo_rect)

    clickable_rects.append((youtube_logo_rect, "youtube_logo"))
    clickable_rects.append((discord_logo_rect, "discord_logo"))
    clickable_rects.append((x_logo_rect, "x_logo"))
    clickable_rects.append((cashapp_logo_rect, "cashapp_logo"))
    clickable_rects.append((venmo_logo_rect, "venmo_logo"))

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
        sx(255),
        sy(55)
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