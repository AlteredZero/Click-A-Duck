import pygame
import random
import time
import math

base_width = 2560
base_height = 1440



def draw_duck_company_stock_button(screen, tarot_card_icon):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)
    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    background = (30, 30, 30)
    border = (255, 255, 255)

    rect = pygame.Rect(sx(20), screen_height - sy(550), sx(80), sy(80))

    pygame.draw.rect(screen, background, rect)
    pygame.draw.rect(screen, border, rect, s(3))

    icon = pygame.transform.scale(tarot_card_icon, (sx(50), sy(50)))
    icon_rect = icon.get_rect(center=rect.center)
    screen.blit(icon, icon_rect)

    return rect


def open_duck_company_stock_frame(screen, fonts, game_data, draw_animated_text):

    clickable_rects = []

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    scale = min(scale_x, scale_y)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(135), sy(500), sx(700), sy(450))
    pygame.draw.rect(screen, (30, 30, 30), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

    draw_animated_text(
        screen,
        "Duck Company Stock",
        fonts["large"],
        (255, 255, 255),
        (menu_rect.centerx, menu_rect.top + sy(30)),
        "duck_company_stock_title"
    )

    draw_animated_text(
        screen,
        "(DUCK)",
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, menu_rect.top + sy(30)),
        "duck_company_stock_symbol"
    )
    
    clickable_rects.append(())

    return clickable_rects