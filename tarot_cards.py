import pygame
import random
import time
import math

base_width = 2560
base_height = 1440

float_time = 0


def draw_tarot_cards_button(screen, tarot_card_icon):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)
    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    background = (70, 70, 255)
    border = (255, 255, 255)

    rect = pygame.Rect(sx(20), screen_height - sy(460), sx(80), sy(80))

    pygame.draw.rect(screen, background, rect)
    pygame.draw.rect(screen, border, rect, s(3))

    icon = pygame.transform.scale(tarot_card_icon, (sx(50), sy(50)))
    icon_rect = icon.get_rect(center=rect.center)
    screen.blit(icon, icon_rect)

    return rect

def draw_exclamation(screen, icon, rect):
    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    scale = min(scale_x, scale_y)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    icon = pygame.transform.scale(icon, (sx(30), sy(30)))

    icon_rect = icon.get_rect(center=(rect.right - sx(10), rect.top + sy(10)))

    screen.blit(icon, icon_rect)



def sping_the_wheel_reward_frame(screen, fonts, draw_animated_text, reward):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    popup_width = sx(600)
    popup_height = sy(300)

    main_rect = pygame.Rect(0, 0, popup_width, popup_height)
    main_rect.center = (screen_width // 2, screen_height // 2)

    pygame.draw.rect(screen, (60, 60, 60), main_rect)
    pygame.draw.rect(screen, (255, 255, 255), main_rect, 3)

    reward_title = fonts["large"].render("You Landed On..", True, (255, 255, 255))
    reward_title_rect = reward_title.get_rect(
        center=(main_rect.centerx, main_rect.top + sy(40))
    )

    reward_description = fonts["small"].render(f"{reward}!", True, (255, 255, 255))

    reward_description_rect = reward_description.get_rect(
        center=(main_rect.centerx, main_rect.top + sy(100))
    )

    button_width = sx(180)
    button_height = sy(50)

    claim_button_rect = pygame.Rect(0, 0, button_width, button_height)
    claim_button_rect.center = (main_rect.centerx, main_rect.bottom - sy(60))

    pygame.draw.rect(screen, (4, 207, 116), claim_button_rect)

    claim_text = fonts["small"].render("CLAIM", True, (255, 255, 255))
    claim_text_rect = claim_text.get_rect(center=claim_button_rect.center)

    draw_animated_text(
        screen,
        "You Landed On..",
        fonts["verylarge"],
        (255, 255, 255),
        reward_title_rect.center,
        "reward_title"
    )

    draw_animated_text(
        screen,
        f"{reward}!",
        fonts["small"],
        (255, 255, 255),
        reward_description_rect.center,
        "reward_name"
    )

    draw_animated_text(
        screen,
        "CLAIM",
        fonts["small"],
        (255, 255, 255),
        claim_text_rect.center,
        "claim_button"
    )


    return claim_button_rect



def open_tarot_card_frame(screen, fonts, game_data, draw_animated_text, background_cards_icon, tarot_card_icon):
    global float_time

    clickable_rects = []

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(135), sy(500), sx(500), sy(650))

    pygame.draw.rect(screen, (70, 70, 255), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

    float_time += 0.03

    x_offset = math.sin(float_time) * sx(10)
    y_offset = math.cos(float_time * 0.8) * sy(10)

    scale_pulse = math.sin(float_time * 1.5) * 5

    background_cards = pygame.transform.scale(background_cards_icon, (sx(200), sy(200)))
    background_cards_rect = background_cards.get_rect(center=(menu_rect.centerx, menu_rect.centery))
    screen.blit(background_cards, background_cards_rect)

    icon = pygame.transform.scale(tarot_card_icon, (sx(200) + int(scale_pulse), sy(200) + int(scale_pulse)))
    icon_rect = icon.get_rect(
    center=(menu_rect.centerx + x_offset, menu_rect.centery + y_offset))
    screen.blit(icon, icon_rect)

    draw_animated_text(
        screen,
        "Tarot Cards",
        fonts["large"],
        (255, 255, 255),
        (menu_rect.centerx, menu_rect.top + sy(30)),
        "tarot_cards_title"
    )

    support_center_y = menu_rect.bottom - sy(70) + fonts["small"].get_height() // 2
    support_rect = pygame.Rect(menu_rect.centerx - sx(120), support_center_y - sy(20), sx(240), sy(40))
    pygame.draw.rect(screen, (4, 207, 116), support_rect)

    remaining = True

    if remaining:
        button_text = f"PULL CARD ({str(game_data["extras"]["tarrot_cards_available"])})"
    else:
        pass
        #button_text = format_time(remaining)
    
    draw_animated_text(
        screen,
        button_text,
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, support_center_y),
        "pull_card_button"
    )

    help_button_y = menu_rect.top + sy(20) + fonts["large"].get_height() // 2
    help_button_center = (menu_rect.centerx + sx(215), help_button_y)

    help_button_rect = pygame.Rect(0, 0, sx(35), sy(35))
    help_button_rect.center = help_button_center

    pygame.draw.rect(screen, (102, 102, 255), help_button_rect)

    draw_animated_text(
        screen,
        "?",
        fonts["large"],
        (255, 255, 255),
        help_button_center,
        "help_info"
    )

    if game_data["extras"]["tarrot_cards_ready"]:
        clickable_rects.append((support_rect, "pull_card_button"))
        clickable_rects.append((help_button_rect, "help_info"))


    return clickable_rects