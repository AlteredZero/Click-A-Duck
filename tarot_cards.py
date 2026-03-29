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

current_reward = ""
reward_value = 0
reward_type = None
reward_applied = False

fake_timer = 0
fake_switching = False
fake_fade_alpha = 255


def get_tarot_goal(game_data):
    return int((game_data["ducksPerClick"] + game_data["ducksPerSecond"]) * 1800)


def add_tarot_progress(game_data, amount):
    if game_data["extras"]["tarot_cards_earned_today"] >= 8:
        return

    game_data["extras"]["tarot_progress"] += amount

    while game_data["extras"]["tarot_progress"] >= game_data["extras"]["tarot_goal"]:
        game_data["extras"]["tarot_progress"] -= game_data["extras"]["tarot_goal"]
        game_data["extras"]["tarot_cards_earned_today"] += 1
        game_data["extras"]["tarrot_cards_available"] += 1
        game_data["extras"]["tarrot_cards_ready"] = True

        game_data["extras"]["tarot_goal"] = get_tarot_goal(game_data)

        if game_data["extras"]["tarot_cards_earned_today"] == 8:
            game_data["extras"]["tarot_progress"] = 0
            game_data["extras"]["tarot_last_reset_time"] = time.time()
            break


def update_tarot_reset(game_data):
    current_time = time.time()
    elapsed = current_time - game_data["extras"]["tarot_last_reset_time"]

    if elapsed >= 86400:
        game_data["extras"]["tarrot_cards_available"] = 0
        game_data["extras"]["tarrot_cards_ready"] = False

        game_data["extras"]["tarot_last_reset_time"] = current_time
        game_data["extras"]["tarot_progress"] = 0
        game_data["extras"]["tarot_goal"] = get_tarot_goal(game_data)


def get_time_remaining(game_data):
    current_time = time.time()
    elapsed = current_time - game_data["extras"]["tarot_last_reset_time"]
    remaining = max(0, 86400 - elapsed)

    hours = int(remaining // 3600)
    minutes = int((remaining % 3600) // 60)
    seconds = int(remaining % 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"


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


def pull_tarot_card(tarot_cards_list, game_data):
    global is_flipping, flip_progress, selected_card
    global current_reward, reward_value, reward_type, reward_applied, fake_timer, fake_switching, fake_fade_alpha

    if is_flipping:
        return

    reward_applied = False

    fake_timer = 0
    fake_switching = False
    fake_fade_alpha = 255

    selected_card = random.choice(tarot_cards_list)

    dpc = game_data["ducksPerClick"]
    dps = game_data["ducksPerSecond"]
    base = dpc + dps

    low = int(base * 0.5)
    high = int(base * 30)

    if selected_card == tarot_cards_list[0]:
        reward_value = random.randint(low, high)
        reward_type = "add"
        current_reward = f"+{reward_value:,} ducks"

    elif selected_card == tarot_cards_list[1]:
        reward_value = random.randint(low, high)
        reward_type = "subtract"
        current_reward = f"-{reward_value:,} ducks"

    elif selected_card == tarot_cards_list[2]:
        reward_value = 1.5
        reward_type = "multiply"
        current_reward = "x1.5 total ducks"

    elif selected_card == tarot_cards_list[3]:
        reward_value = 0.5
        reward_type = "multiply"
        current_reward = "x0.5 total ducks"

    elif selected_card == tarot_cards_list[4]:
        reward_value = 2
        reward_type = "multiply"
        current_reward = "x2 total ducks"

    elif selected_card == tarot_cards_list[5]:
        reward_value = 0.1
        reward_type = "multiply"
        current_reward = "x0.1 total ducks"

    elif selected_card == tarot_cards_list[6]:
        reward_type = "none"
        current_reward = "Nothing!"

    elif selected_card == tarot_cards_list[7]:
        reward_type = "simulate"
        current_reward = "simulate 5 minutes"

    elif selected_card == tarot_cards_list[8]:
        reward_type = "fake"
        reward_value = random.randint(18203192, 172919082731)
        current_reward = f"+{reward_value:,}"

    elif selected_card == tarot_cards_list[9]:
        reward_type = "cards"
        current_reward = "+2 tarot cards"

    flip_progress = 0
    is_flipping = True



def open_tarot_card_frame(screen, fonts, game_data, draw_animated_text, background_cards_icon, tarot_card_icon, the_sun_tarot_card, the_devil_tarot_card, the_empress_tarot_card, death_tarot_card, wheel_of_fortune_tarot_card, the_tower_tarot_card, the_fool_tarot_card, the_world_tarot_card, page_of_cups_tarot_card, ace_of_pentacles_tarot_card, get_current_dps, tarot_card_background_design):

    global float_time, is_flipping, flip_progress, selected_card, is_fading, fade_alpha, reveal_scale, reveal_timer, current_reward, reward_applied, fake_timer, fake_fade_alpha, fake_switching, get_time_remaining

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
        the_sun_tarot_card: "sun",
        the_devil_tarot_card: "devil",
        the_empress_tarot_card: "empress",
        death_tarot_card: "death",
        wheel_of_fortune_tarot_card: "wheel",
        the_tower_tarot_card: "tower",
        the_fool_tarot_card: "fool",
        the_world_tarot_card: "world",
        page_of_cups_tarot_card: "fake",
        ace_of_pentacles_tarot_card: "ace"
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

    tarot_cards_background_design = pygame.transform.scale(tarot_card_background_design, (sx(450), sy(450)))
    tarot_cards_background_design_rect = tarot_cards_background_design.get_rect(center=(menu_rect.centerx, menu_rect.centery))
    screen.blit(tarot_cards_background_design, tarot_cards_background_design_rect)

    background_cards = pygame.transform.scale(background_cards_icon, (sx(300), sy(300)))
    background_cards_rect = background_cards.get_rect(center=(menu_rect.centerx, menu_rect.centery))
    screen.blit(background_cards, background_cards_rect)

    fade_alpha = 255
    card_width = sx(300)
    card_height = sy(300)

    if is_flipping:
        flip_progress += flip_speed

    if flip_progress >= 1:
        flip_progress = 1
        is_flipping = False
        reveal_timer = 1.0

        if not reward_applied:
            reward_applied = True

            if reward_type == "add":
                game_data["ducks"] += reward_value

            elif reward_type == "subtract":
                game_data["ducks"] = max(0, game_data["ducks"] - reward_value)

            elif reward_type == "multiply":
                game_data["ducks"] = int(game_data["ducks"] * reward_value)

            elif reward_type == "simulate":
                seconds = int(300)

                dps = get_current_dps()
                global_speed = game_data.get("globalGameSpeed", 1)

                dps *= global_speed

                base_dpc = game_data["ducksPerClick"] * game_data["multiplierDPC"]

                crit_chance = game_data.get("criticalChance", 0)
                crit_power = game_data.get("criticalPower", 1)

                total_dps_gain = dps * seconds

                dpc_triggers = seconds // 5

                if crit_chance > 0:
                    avg_multiplier = (1 - crit_chance) + (crit_chance * crit_power)
                else:
                    avg_multiplier = 1

                avg_dpc = base_dpc * avg_multiplier * global_speed

                total_dpc_gain = dpc_triggers * avg_dpc

                total_added = total_dps_gain + total_dpc_gain

                game_data["ducks"] += total_added
                game_data["allTimeDucks"] += total_added
                game_data["playtime"] += seconds

            elif reward_type == "cards":
                game_data["extras"]["tarrot_cards_available"] += 2
                game_data["extras"]["tarrot_cards_ready"] = True

            elif reward_type == "fake":
                fake_timer = 120
                fake_switching = False
                fake_fade_alpha = 255

    if reward_type == "fake":
        if fake_timer > 0:
            fake_timer -= 1
        else:
            fake_switching = True

        if fake_switching:
            fake_fade_alpha -= 15
            if fake_fade_alpha <= 0:
                fake_fade_alpha = 0
                current_reward = "Fake!"

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

    card_rect = pygame.Rect(0, 0, current_width, current_height)
    card_rect.center = (
        menu_rect.centerx + x_offset,
        menu_rect.centery + y_offset
    )

    if reward_type == "fake" and fake_switching:
        old_card = pygame.transform.scale(selected_card, (current_width, current_height)).convert_alpha()
        old_card.set_alpha(fake_fade_alpha)

        fool_card = pygame.transform.scale(the_fool_tarot_card, (current_width, current_height)).convert_alpha()
        fool_card.set_alpha(255 - fake_fade_alpha)

        screen.blit(old_card, card_rect)
        screen.blit(fool_card, card_rect)

    else:
        if flip_progress < 0.5:
            card_image = tarot_card_icon
        else:
            card_image = selected_card if selected_card else tarot_card_icon

        scaled_card = pygame.transform.scale(card_image, (current_width, current_height)).convert_alpha()
        scaled_card.set_alpha(fade_alpha)

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
            tarot_card_reward = current_reward
            text_alpha = int(255 * (1 - reveal_timer))
        else:
            tarot_card_reward = ""
            text_alpha = 0

    draw_animated_text(
        screen,
        tarot_card_reward,
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, menu_rect.top + sy(530)),
        "tarot_cards_title"
    )

    support_center_y = menu_rect.bottom - sy(80) + fonts["small"].get_height() // 2
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

    current_progress = int(game_data["extras"]["tarot_progress"])
    progress_bar_goal = int(game_data["extras"]["tarot_goal"])

    progress_percent = (current_progress / progress_bar_goal) * 100

    progress_bar_center_y = menu_rect.bottom - sy(40) + fonts["small"].get_height() // 2
    progress_bar_rect = pygame.Rect(menu_rect.centerx - sx(200), progress_bar_center_y - sy(14), sx(400), sy(30))
    pygame.draw.rect(screen, (80, 80, 80), progress_bar_rect)

    progress_rect = pygame.Rect(progress_bar_rect.x, progress_bar_rect.y, sx(progress_percent * 4), sy(30))
    pygame.draw.rect(screen, (4, 207, 116), progress_rect)

    pygame.draw.rect(screen, (0, 0, 0), progress_bar_rect, 3)

    if game_data["extras"]["tarot_cards_earned_today"] >= 8:
        progress_bar_text = f"Next 8 card reset in: {get_time_remaining(game_data)}"
    else:
        progress_bar_text = f"{current_progress:,} / {progress_bar_goal:,}"

    draw_animated_text(
        screen,
        progress_bar_text,
        fonts["verysmall"],
        (255, 255, 255),
        (menu_rect.centerx, progress_bar_center_y),
        "progress_bar_text"
    )

    draw_animated_text(
        screen,
        f"Cards: {8 - game_data["extras"]["tarot_cards_earned_today"]}/8",
        fonts["verysmall"],
        (255, 255, 255),
        (menu_rect.centerx, menu_rect.top + sy(60)),
        "daily_cards_counter"
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