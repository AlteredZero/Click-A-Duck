import pygame
import random
import time
import math

base_width = 2560
base_height = 1440

float_time = 0

is_flipping = False
flip_progress = 0
selected_card = None
flip_speed = 0.08
fade_alpha = 255
is_fading = False
reveal_scale = 1.0
reveal_timer = 0


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


def pull_tarot_card(tarot_cards_list):
    global is_flipping, flip_progress, selected_card
    global is_fading, fade_alpha

    if selected_card and not is_flipping:
        is_fading = True
        fade_alpha = 255
        return

    if not is_flipping:
        selected_card = random.choice(tarot_cards_list)
        flip_progress = 0
        is_flipping = True



def open_tarot_card_frame(screen, fonts, game_data, draw_animated_text, background_cards_icon, tarot_card_icon, the_sun_tarot_card, the_devil_tarot_card, the_empress_tarot_card, death_tarot_card, wheel_of_fortune_tarot_card, the_tower_tarot_card, the_fool_tarot_card, the_world_tarot_card, page_of_cups_tarot_card, ace_of_pentacles_tarot_card):

    global float_time, is_flipping, flip_progress, selected_card, is_fading, fade_alpha, reveal_scale, reveal_timer

    tarot_cards = [
        the_sun_tarot_card,
        the_devil_tarot_card,
        the_empress_tarot_card,
        death_tarot_card,
        wheel_of_fortune_tarot_card,
        the_tower_tarot_card,
        the_fool_tarot_card,
        the_world_tarot_card,
        page_of_cups_tarot_card,
        ace_of_pentacles_tarot_card
    ]

    tarot_cards_rewards = {
        the_sun_tarot_card: f"+{random.randint(1, 5000000)} ducks",
        the_devil_tarot_card: f"-{random.randint(1, 5000000)} ducks",
        the_empress_tarot_card: "x1.5 total ducks",
        death_tarot_card: "x0.5 total ducks",
        wheel_of_fortune_tarot_card: "x2 total ducks",
        the_tower_tarot_card: "x0.1 total ducks",
        the_fool_tarot_card: "Nothing!",
        the_world_tarot_card: "simulate 5 minutes",
        page_of_cups_tarot_card: f"+{random.randint(18203192, 172919082731)}",  # FAKE REWARD! ITS ACTUALLY NOTHING!!!!
        ace_of_pentacles_tarot_card: "+2 tarot cards"
    }

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

    background_cards = pygame.transform.scale(background_cards_icon, (sx(300), sy(300)))
    background_cards_rect = background_cards.get_rect(center=(menu_rect.centerx, menu_rect.centery))
    screen.blit(background_cards, background_cards_rect)

    if is_fading:
        fade_alpha -= 15

        if fade_alpha <= 0:
            fade_alpha = 0
            is_fading = False

            selected_card = random.choice(tarot_cards)
            flip_progress = 0
            is_flipping = True
            fade_alpha = 255

    card_width = sx(300)
    card_height = sy(300)

    if is_flipping:
        flip_progress += flip_speed

    if flip_progress >= 1:
        flip_progress = 1
        is_flipping = False
        reveal_timer = 1.0

    flip_scale = abs(math.cos(flip_progress * math.pi))

    if reveal_timer > 0:
        reveal_timer -= 0.08
        reveal_scale = 1.0 + 0.4 * reveal_timer
    else:
        reveal_scale = 1.0

    current_width = max(1, int(card_width * flip_scale * reveal_scale))
    current_height = int(card_height * reveal_scale)

    if flip_progress < 0.5:
        card_image = tarot_card_icon
    else:
        card_image = selected_card if selected_card else tarot_card_icon

    scaled_card = pygame.transform.scale(card_image, (current_width, current_height)).convert_alpha()
    scaled_card.set_alpha(fade_alpha)

    card_rect = scaled_card.get_rect(center=(
        menu_rect.centerx + x_offset,
        menu_rect.centery + y_offset
    ))

    screen.blit(scaled_card, card_rect)

    draw_animated_text(
        screen,
        "Tarot Cards",
        fonts["large"],
        (255, 255, 255),
        (menu_rect.centerx, menu_rect.top + sy(30)),
        "tarot_cards_title"
    )

    tarot_card_reward = ""

    if not is_flipping and selected_card:
        if not is_flipping and selected_card:
            tarot_card_reward = tarot_cards_rewards.get(selected_card, "")
            text_alpha = int(255 * (1 - reveal_timer))
        else:
            tarot_card_reward = ""
            text_alpha = 0

    draw_animated_text(
        screen,
        tarot_card_reward,
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, menu_rect.top + sy(500)),
        "tarot_cards_title"
    )

    support_center_y = menu_rect.bottom - sy(70) + fonts["small"].get_height() // 2
    support_rect = pygame.Rect(menu_rect.centerx - sx(120), support_center_y - sy(20), sx(240), sy(40))
    pygame.draw.rect(screen, (4, 207, 116), support_rect)

    button_text = f"PULL CARD ({str(game_data['extras']['tarrot_cards_available'])})"

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

    return clickable_rects, help_button_rect, tarot_cards