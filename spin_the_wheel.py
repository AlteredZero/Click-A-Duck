import pygame
import random
import time

base_width = 2560
base_height = 1440

wheel_angle = 0
wheel_velocity = 0
wheel_spinning = False
wheel_idle = True

spin_time = 0
spin_duration = 7
start_angle = 0

landed = False

reward_name = None

slices = {
    "15min x1.2": 292,
    "30min x1.2": 245,
    "60min x1.2": 203,
    "15min x1.5": 70,
    "30min x1.5": 24,
    "60min x1.5": 340,
    "15min x2": 158,
    "30min x2": 112
}

chances = {
    "15min x1.2": 26,
    "30min x1.2": 18,
    "60min x1.2": 8,
    "15min x1.5": 17,
    "30min x1.5": 12,
    "60min x1.5": 3,
    "15min x2": 11,
    "30min x2": 5
}


def draw_SpinTheWheel(screen, spin_the_wheel_icon):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)
    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    background = (255, 70, 70)
    border = (255, 255, 255)

    rect = pygame.Rect(sx(20), screen_height - sy(370), sx(80), sy(80))

    pygame.draw.rect(screen, background, rect)
    pygame.draw.rect(screen, border, rect, s(3))

    icon = pygame.transform.scale(spin_the_wheel_icon, (sx(50), sy(50)))
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



def spin_the_wheel():
    global wheel_spinning, wheel_idle
    global reward_name, target_angle, spin_time, start_angle, wheel_angle

    reward_name = random.choices(
        list(chances.keys()),
        weights=list(chances.values())
    )[0]

    reward_angle = slices[reward_name]

    wheel_angle = wheel_angle % 360
    start_angle = wheel_angle

    rotations = random.randint(6, 10)

    target_angle = start_angle - (360 * rotations + (start_angle % 360) - reward_angle)

    wheel_spinning = True
    wheel_idle = False

    spin_time = time.time()

    print("Chosen:", reward_name)



def update_wheel(show_spin_the_wheel_frame):
    global wheel_angle, wheel_spinning, target_angle
    global spin_time, spin_duration, start_angle

    if wheel_spinning:
        elapsed = time.time() - spin_time
        t = min(elapsed / spin_duration, 1)

        ease = 1 - (1 - t) ** 5
        wheel_angle = start_angle + (target_angle - start_angle) * ease

        if t >= 1:
            wheel_angle = target_angle
            wheel_spinning = False

            print("Landed on:", reward_name)

            return True, reward_name

    return show_spin_the_wheel_frame, reward_name


def open_SpinTheWheel(screen, fonts, game_data, draw_animated_text, spin_the_wheel_icon, spin_the_wheel_arrow_icon, show_spin_the_wheel_frame, get_spin_time_remaining, format_time, sping_the_wheel_background_design):
    global wheel_angle

    clickable_rects = []

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(135), sy(550), sx(600), sy(600))

    pygame.draw.rect(screen, (255, 70, 70), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

    show_spin_the_wheel_frame, reward_name = update_wheel(show_spin_the_wheel_frame)

    sping_the_wheel_background_design = pygame.transform.scale(sping_the_wheel_background_design, (sx(550), sy(550)))
    sping_the_wheel_background_design_rect = sping_the_wheel_background_design.get_rect(center=(menu_rect.centerx, menu_rect.centery))
    screen.blit(sping_the_wheel_background_design, sping_the_wheel_background_design_rect)

    if wheel_idle:
        wheel_angle -= 0.1

    icon = pygame.transform.scale(spin_the_wheel_icon, (sx(400), sy(400)))

    rotated_icon = pygame.transform.rotate(icon, wheel_angle)
    icon_rect = rotated_icon.get_rect(center=menu_rect.center)
    screen.blit(rotated_icon, icon_rect)


    arrow_icon = pygame.transform.scale(spin_the_wheel_arrow_icon, (sx(80), sy(80)))

    arrow_icon_rect = arrow_icon.get_rect(center=(menu_rect.centerx + sx(180), menu_rect.centery))
    screen.blit(arrow_icon, arrow_icon_rect)


    draw_animated_text(
        screen,
        "SPIN-THE-WHEEL",
        fonts["large"],
        (255, 255, 255),
        (menu_rect.centerx, menu_rect.top + sy(30)),
        "SPIN-THE-WHEEL_title"
    )

    support_center_y = menu_rect.bottom - sy(70) + fonts["small"].get_height() // 2

    support_rect = pygame.Rect(
        menu_rect.centerx - sx(120),
        support_center_y - sy(20),
        sx(240),
        sy(40)
    )

    remaining = get_spin_time_remaining(game_data)

    if remaining == 0:
        button_text = "SPIN!"
        pygame.draw.rect(screen, (4, 207, 116), support_rect)
    else:
        button_text = format_time(remaining)
        pygame.draw.rect(screen, (60, 60, 60), support_rect)
    
    draw_animated_text(
        screen,
        button_text,
        fonts["small"],
        (255, 255, 255),
        (menu_rect.centerx, support_center_y),
        "spin_button"
    )

    if game_data["extras"]["spin_the_wheel_ready"]:
        clickable_rects.append((support_rect, "spin_button"))


    return clickable_rects, show_spin_the_wheel_frame, reward_name