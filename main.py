#---------------------#
#-------IMPORTS-------#
#---------------------#

import pygame
import random
import math
import time
import json
import webbrowser
import os
import sys
import subprocess
from save_manager import load_game, save_game
from fonts import load_fonts
from options import draw_options, open_options    
from stats import draw_stats, open_stats
from donate import draw_donate, open_donate
from spin_the_wheel import draw_SpinTheWheel, open_SpinTheWheel, spin_the_wheel, sping_the_wheel_reward_frame
from tarot_cards import draw_tarot_cards_button, open_tarot_card_frame, pull_tarot_card, add_tarot_progress, get_tarot_goal, update_tarot_reset
from floating_text import FloatingText
from duck import Duck
from pool import Pool
from upgrade_buttons import UpgradeManager
from magical_auto_clicker import MagicalAutoClicker
from duck_pop_effect import DuckPopEffect
from console import Console


#---------------------#
#--------INIT---------#
#---------------------#

def loading_screen(screen, screen_width, screen_height, scale, fonts):
    clock = pygame.time.Clock()

    duck_image = pygame.image.load("assets/Images/Duck1.png").convert_alpha()
    duck_image = pygame.transform.scale(duck_image, (int(80 * scale), int(80 * scale)))

    loading_steps = [
        lambda: pygame.mixer.Sound("assets/audio/DuckQuack.mp3"),
        lambda: pygame.mixer.Sound("assets/audio/MouseClick.mp3"),
        lambda: pygame.mixer.Sound("assets/audio/PurchaseSound.mp3"),
        lambda: pygame.mixer.Sound("assets/audio/HoverSound.mp3"),
        lambda: pygame.mixer.Sound("assets/audio/ErrorSound.mp3"),
        lambda: pygame.image.load("assets/Images/BackgroundBlue.png").convert_alpha(),
        lambda: pygame.image.load("assets/Images/Pool1.png").convert_alpha(),
        lambda: pygame.image.load("assets/Images/YellowPool.png").convert_alpha(),
        lambda: pygame.image.load("assets/Images/HotPinkPool.png").convert_alpha(),
        lambda: pygame.image.load("assets/Images/CoralPool.png").convert_alpha(),
        lambda: pygame.image.load("assets/Images/CyanPool.png").convert_alpha(),
    ]

    total_steps = len(loading_steps)
    completed = 0

    displayed_percent = 0
    target_percent = 0

    start_time = pygame.time.get_ticks()
    minimum_time = 4000
    hold_time = 500

    t = 0

    running = True
    while running:

        current_time = pygame.time.get_ticks()
        elapsed = current_time - start_time

        if completed < total_steps:
            loading_steps[completed]()
            completed += 1
            target_percent = int((completed / total_steps) * 100)

        if displayed_percent < target_percent:
            displayed_percent += 0.5
            
        elif completed == total_steps and elapsed < minimum_time:

            displayed_percent += 0.3

        if displayed_percent > 100:
            displayed_percent = 100

        screen.fill((0, 0, 0))

        loading_text = fonts["large"].render(
            f"LOADING {int(displayed_percent)}%",
            False,
            (255, 255, 255)
        )
        screen.blit(loading_text, (20, screen_height - 80))

        t += 0.1
        angle = math.sin(t) * 10
        rotated = pygame.transform.rotate(duck_image, angle)
        rect = rotated.get_rect(bottomright=(screen_width - 40, screen_height - 40))
        screen.blit(rotated, rect)

        pygame.display.flip()
        global_time = clock.tick(60)

        if displayed_percent >= 100 and elapsed >= minimum_time:
            pygame.time.delay(hold_time)
            running = False

    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill((0, 0, 0))

    for alpha in range(255, -1, -8):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(15)


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
screen_width, screen_height = screen.get_size()

base_width = 2560
base_height = 1440

scale_x = screen_width / base_width
scale_y = screen_height / base_height

scale = min(scale_x, scale_y)

fonts = load_fonts(scale)

loading_screen(screen, screen_width, screen_height, scale, fonts)

pygame.display.set_caption("Click-A-Duck")
pygame.display.set_icon(pygame.image.load("assets/Images/Duck1.png").convert_alpha())

with open("data/upgrade_data.json", "r") as f:
    upgrade_data = json.load(f)


#---------------------#
#-------SCALING-------#
#---------------------#

def sx(x): return int(x * scale)
def sy(y): return int(y * scale)
def sr(rect):
    return pygame.Rect(sx(rect.x), sy(rect.y), sx(rect.w), sy(rect.h))


def load_scaled(path, width, height):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (sx(width), sy(height)))


#---------------------#
#------VARIABLES------#
#---------------------#

original_pool_image = pygame.image.load("assets/Images/Pool1.png").convert_alpha()

pool = Pool(
    image=original_pool_image,
    center=(screen_width // 2, screen_height // 2),
    scale=scale
)

background = pygame.image.load("assets/Images/BackgroundBlue.png").convert_alpha()
background = pygame.transform.scale(background, (screen_width, screen_height))

cursor_image = load_scaled("assets/Images/CursorImageDefault.png", 40, 40)
cursor_hover_image = load_scaled("assets/Images/CursorImage.png", 40, 40)

magical_auto_clicker_image = load_scaled("assets/Images/MagicalAutoClicker.png", 40, 40)

pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
t = 0
respawn_time = None

cannot_afford_message = ""
cannot_afford_timer = 0

save_message = "Game has been saved."
save_message_timer = 0

last_duck_sound_time = 0
last_save_time = 0

tick_time = pygame.time.get_ticks()

shiny_active = False
shiny_timer = 0
shiny_duration = 30000

shiny_dpc_multiplier = 3
shiny_dps_multiplier = 2

shiny_duck_icon = load_scaled("assets/Images/ShinyDuck.png", 40, 40)

shiny_hover_rect = None

show_options = False
show_stats = False
show_donate = False

show_spin_the_wheel = False

show_tarot_card_frame = False

show_warning_clear_data = False

clear_button_rect = None
cancel_button_rect = None

save_cooldown_until = 0

support_url = "https://ko-fi.com/altered_games" # CHANGE URL

support_button = None

spin_the_wheel_icon = pygame.image.load("assets/Images/Spin-The-Wheel.png").convert_alpha()
spin_the_wheel_info_icon = pygame.image.load("assets/Images/Spin-The-WheelInfo.png").convert_alpha()
spin_the_wheel_arrow_icon = pygame.image.load("assets/Images/Spin-The-WheelArrow.png").convert_alpha()

tarot_card_icon = pygame.image.load("assets/Images/TarotCardsIcon.png").convert_alpha()
tarot_card_background_icon = pygame.image.load("assets/Images/TarrotCardsBackgroundCards.png").convert_alpha()
tarot_card_single_icon = pygame.image.load("assets/Images/SingleTarrotCard.png").convert_alpha()

the_sun_tarot_card = pygame.image.load("assets/Images/TheSunTarotCard.png").convert_alpha() # +x ducks
the_devil_tarot_card = pygame.image.load("assets/Images/TheDevilTarotCard.png").convert_alpha() # -x ducks
the_empress_tarot_card = pygame.image.load("assets/Images/TheEmpressTarotCard.png").convert_alpha() # x1.5 total ducks
death_tarot_card = pygame.image.load("assets/Images/TheDeathTarotCard.png").convert_alpha() # x0.5 total ducks
wheel_of_fortune_tarot_card = pygame.image.load("assets/Images/ThWheelOfFortuneTarotCard.png").convert_alpha() # x2 total ducks
the_tower_tarot_card = pygame.image.load("assets/Images/TheTowerTarotCard.png").convert_alpha() # x0.1 total ducks
the_fool_tarot_card = pygame.image.load("assets/Images/TheFoolTarotCard.png").convert_alpha() # does nothing
the_world_tarot_card = pygame.image.load("assets/Images/TheWorldTarotCards.png").convert_alpha() # simulate 5 minutes
page_of_cups_tarot_card = pygame.image.load("assets/Images/PageOfCupsTarotCards.png").convert_alpha() # gives huge reward but turns out to be a fake
ace_of_pentacles_tarot_card = pygame.image.load("assets/Images/AceOfPentaclesTaroCard.png").convert_alpha() # gives 2 tarot cards
tarot_card_background_design = pygame.image.load("assets/Images/TarotCardBackgroundDesign.png").convert_alpha()
sping_the_wheel_background_design = pygame.image.load("assets/Images/spin_the_wheel_background_design.png").convert_alpha()

the__tarot_card = pygame.image.load("assets/Images/TheSunTarotCard.png").convert_alpha()

exclamation_icon = pygame.image.load("assets/Images/ExclamationIcon.png").convert_alpha()

spin_the_wheel_rect = None

tarot_cards_rect = None

help_button_rect = None

show_spin_the_wheel_frame = False

spin_the_wheel_boost_active = False

tarot_cards_list = []


#---------------------#
#--------AUDIO--------#
#---------------------#

duck_click_sound = pygame.mixer.Sound("assets/audio/DuckQuack.mp3")
click_sound = pygame.mixer.Sound("assets/audio/MouseClick.mp3")
purchase_sound = pygame.mixer.Sound("assets/audio/PurchaseSound.mp3")
hover_sound = pygame.mixer.Sound("assets/audio/HoverSound.mp3")
error_sound = pygame.mixer.Sound("assets/audio/ErrorSound.mp3")

##################################################
# SET MUSIC OPTION ONCE MUSIC IS ADDED!!!!!
##################################################
music_sound = pygame.mixer.Sound("assets/audio/DuckQuack.mp3")


#---------------------#
#----DICTIONARIES-----#
#---------------------#

default_data = {
    "ducks": 0,
    "ducksPerClick": 1,
    "ducksPerSecond": 0,
    "maxDucksInPool": 1,
    "spawnTime": 3, 
    "DPCUpgradeBought": 0,
    "reainforcedCursorB": 0,
    "poolSize": 1,
    "playtime": 0,
    "cursorSize": 1,
    "duckColor": "yellow",
    "poolColor": "green",
    "magicalAutoClickers": 0,
    "magicalAutoClickerSpeed": 1,
    "multiplierDPC": 1.0,
    "multiplierDPS": 1.0,
    "twoDuckSpawnChance": 0.0,
    "shinyDuckChance": 0.0,
    "criticalChance": 0.0,
    "criticalPower": 1.1,
    "duckNests": 0,
    "goldenDuckStatue": 0,
    "quakingSpeaker": 0,
    "duckCoop": 0,
    "duckBeacon": 0,
    "globalGameSpeed": 1,
    "allTimeDucks": 0,
    "purchases":{
        "orangeDuckB": False,
        "yellowPoolB": False,
        "magicalAutoClickerB": False,
        "megaDuckFeederB": False,
        "radiantPlungeB": False,
        "GoldenStrongCursorB": False,
        "LuxuryNestGroundB": False,
        "fortuneFeathersB": False,
        "autoClickerSpeedB": False,
        "purpleDuckB": False,
        "featherFountainB": False,
        "quackAmplifierB": False,
        "duckMagnetB": False,
        "hotPinkPoolB": False,
        "rubberDuckArmyB": False,
        "radiantPlungeIIB": False,
        "TurquoiseDuckB": False,
        "spinTheWheelB": False,
        "fortuneFeathersIIB": False,
        "DuckHeaterB": False,
        "BreadStormMachineB": False,
        "coralPoolB": False,
        "duckDlc": False,
        "magicalAutoClickerB2": False,
        "duckCeoB": False,
        "hydroQuackPumpB": False,
        "flockRouterB": False,
        "pondOverclockerB": False,
        "autoClickerSpeedB2": False,
        "fortuneFeathersIIIB": False,
        "limeDuckB": False,
        "duckIndustriesB": False,
        "duckHotelB": False,
        "crumbTrailsB": False,
        "cyanPoolB": False,
        "radiantPlungeIIIB": False,
        "pondLanternB": False,
        "tarotCardsB": False,
        "decorativePondArchB": False,
        "enchantedWaterWheelB": False,
        "platinumStrongCursorB": False,
        "opulentNestingGroundsB": False,
        "fortuneFeathersIVB": False,
        "duck2.0B": False,
        "duckMultiversePortalB": False,
        "orangeBlueDuckB": False,
        "friendlyButterflyB": False,
        "magicalAutoClickerB3": False,
        "grayPoolB": False,
        "mechanicalBreakShaker": False,
        "duckPythonTerminalB": False,
        "nestSkyscrapperB": False,
        "nestExpansionPermitB": False,
        "thermalNestingStonesB": False,
        "theDuckCompanyStockB": False,
        "radiantPlungeIVB": False,
        "duckLogisticsBoardB": False,
        "flockSupervisorPostB": False,
        "waterLevelRegulatorB": False,
        "heavyDutyBreadCratesB": False,
        "fortuneFeathersVB": False,
        "redBlueDuckB": False,
        "advancedFlockConditioningB": False,
        "sophisticatedWaterFilterB": False,
        "scarlettpoolB": False,
        "duckMatrixB": False
    },
    "settings": {
        "volume": 0.5,
        "music": True,
        "sfx": True,
        "duckText": True,
        "magicalAutoClickers": True
    },
    "extras": {
        "spin_the_wheel_ready": True,
        "spin_the_wheel_next_time": 0,
        "tarrot_cards_ready": True,
        "tarrot_cards_available": 0,
        "tarot_progress": 0,
        "tarot_goal": 0,
        "tarot_cards_earned_today": 0,
        "tarot_last_reset_time": 0
    }
}

duck_images = {
    "yellow": load_scaled("assets/Images/Duck1.png", 60, 60),
    "shiny": load_scaled("assets/Images/ShinyDuck.png", 60, 60),
    "orange": load_scaled("assets/Images/OrangeDuck.png", 60, 60),
    "purple": load_scaled("assets/Images/PurpleDuck.png", 60, 60),
    "turquoise": load_scaled("assets/Images/TurquoiseDuck1.png", 60, 60),
    "lime": load_scaled("assets/Images/LimeDuck.png", 60, 60),
    "orangeBlue": load_scaled("assets/Images/OrangeBlueDuck.png", 60, 60),
    "redblue": load_scaled("assets/Images/RedBlueDuck.png", 60, 60),
}

pool_images = {
    "green": pygame.image.load("assets/Images/Pool1.png").convert_alpha(),
    "yellow": pygame.image.load("assets/Images/YellowPool.png").convert_alpha(),
    "hotPink": pygame.image.load("assets/Images/HotPinkPool.png").convert_alpha(),
    "coral": pygame.image.load("assets/Images/CoralPool.png").convert_alpha(),
    "cyan": pygame.image.load("assets/Images/CyanPool.png").convert_alpha(),
    "gray": pygame.image.load("assets/Images/GrayPool.png").convert_alpha(),
    "scarlett": pygame.image.load("assets/Images/ScarlettPool.png").convert_alpha(),
}

enhancement_icons = {
    "megaDuckFeederB": load_scaled("assets/Images/MegaDuckFeeder.png", 50, 50),
    "featherFountainB": load_scaled("assets/Images/FeatherFountain.png", 50, 50),
    "quackAmplifierB": load_scaled("assets/Images/QuackAmplifier.png", 50, 50),
    "duckMagnetB": load_scaled("assets/Images/DuckMagnet.png", 50, 50),
    "rubberDuckArmyB": load_scaled("assets/Images/DuckArmy.png", 50, 50),
    "DuckHeaterB": load_scaled("assets/Images/DuckHeater.png", 50, 50),
    "BreadStormMachineB": load_scaled("assets/Images/BreadStormMachine.png", 50, 50),
    "duckDlc": load_scaled("assets/Images/DuckDLC.png", 50, 50),
    "duckCeoB": load_scaled("assets/Images/DuckCEO.png", 50, 50),
    "hydroQuackPumpB": load_scaled("assets/Images/Hydro-Quack Pump.png", 50, 50),
    "flockRouterB": load_scaled("assets/Images/FlockRouter.png", 50, 50),
    "pondOverclockerB": load_scaled("assets/Images/PondOverclock.png", 50, 50),
    "duckIndustriesB": load_scaled("assets/Images/DuckIndustries.png", 50, 50),
    "duckHotelB": load_scaled("assets/Images/DuckHotel.png", 50, 50),
    "crumbTrailsB": load_scaled("assets/Images/BreadcrumbsDuck.png", 50, 50),
    "pondLanternB": load_scaled("assets/Images/PondLantern.png", 50, 50),
    "decorativePondArchB": load_scaled("assets/Images/DecorativeDuckArch.png", 50, 50),
    "enchantedWaterWheelB": load_scaled("assets/Images/EnhantedWaterWheel.png", 50, 50),
    "duck2.0B": load_scaled("assets/Images/Duck2.0.png", 50, 50),
    "duckMultiversePortalB": load_scaled("assets/Images/DuckMultiversePortal.png", 50, 50),
    "friendlyButterflyB": load_scaled("assets/Images/monarchButterfly.png", 50, 50),
    "mechanicalBreakShaker": load_scaled("assets/Images/MechanicalBreadShaker.png", 50, 50),
    "duckPythonTerminalB": load_scaled("assets/Images/DuckPythonTerminal.png", 50, 50),
    "nestSkyscrapperB": load_scaled("assets/Images/NestSkyscrapper.png", 50, 50),
    "nestExpansionPermitB": load_scaled("assets/Images/NestExpansionPermit.png", 50, 50),
    "thermalNestingStonesB": load_scaled("assets/Images/ThermalStones.png", 50, 50),
    "duckLogisticsBoardB": load_scaled("assets/Images/DuckLogisitcsBoard.png", 50, 50),
    "flockSupervisorPostB": load_scaled("assets/Images/FlockSupervisor.png", 50, 50),
    "waterLevelRegulatorB": load_scaled("assets/Images/WaterLevelRegulator.png", 50, 50),
    "heavyDutyBreadCratesB": load_scaled("assets/Images/HeavyBreadCrates.png", 50, 50),
    "advancedFlockConditioningB": load_scaled("assets/Images/DuckConditioning.png", 50, 50),
    "sophisticatedWaterFilter": load_scaled("assets/Images/SophisticatedWaterFilter.png", 50, 50),
    "duckMatrixB": load_scaled("assets/Images/DuckMatrix.png", 50, 50),
}

enhancement_positions = {
    "megaDuckFeederB": (sx(850), sy(900)),
    "featherFountainB": (sx(1800), sy(700)),
    "quackAmplifierB": (sx(1000), sy(300)),
    "duckMagnetB": (sx(1570), sy(1070)),
    "rubberDuckArmyB": (sx(1500), sy(300)),
    "DuckHeaterB": (sx(800), sy(650)),
    "BreadStormMachineB": (sx(1020), sy(1100)),
    "duckDlc": (sx(1230), sy(250)),
    "duckCeoB": (sx(860), sy(400)),
    "hydroQuackPumpB": (sx(1700), sy(430)),
    "flockRouterB": (sx(1730), sy(900)),
    "pondOverclockerB": (sx(1300), sy(1150)),
    "duckHotelB": (sx(717),  sy(395)),
    "crumbTrailsB": (sx(1843), sy(395)),
    "pondLanternB": (sx(1930), sy(720)),
    "decorativePondArchB": (sx(1843), sy(1045)),
    "enchantedWaterWheelB": (sx(717),  sy(1045)),
    "duckIndustriesB": (sx(630),  sy(720)),
    "duck2.0B": (sx(1610), sy(380)),
    "duckMultiversePortalB": (sx(1780), sy(620)),
    "friendlyButterflyB": (sx(1300), sy(250)),
    "mechanicalBreakShaker": (sx(1780), sy(820)),
    "duckPythonTerminalB": (sx(1650), sy(1000)),
    "nestSkyscrapperB": (sx(1400), sy(1120)),
    "nestExpansionPermitB": (sx(1160), sy(1120)),
    "thermalNestingStonesB": (sx(910),  sy(1000)),
    "duckLogisticsBoardB": (sx(780),  sy(820)),
    "flockSupervisorPostB": (sx(780),  sy(750)),
    "waterLevelRegulatorB": (sx(830),  sy(500)),
    "heavyDutyBreadCratesB": (sx(1130), sy(270)),
    "advancedFlockConditioningB": (sx(1400), sy(270)),
    "sophisticatedWaterFilter": (sx(1530), sy(430)),
    "duckMatrixB": (sx(1750), sy(540)),
}

special_tooltips = {
    "shiny": "The entire pool is filled with riches now. Ducks give 3x Ducks per click and 2x Ducks per second for 30 seconds.",
    "tarot_cards_help": "Tarot cards are special items that grant random buffs or debuffs. They are purely luck-based and can lead to massive earnings or total loss. Earn a card by filling your earnings meter. You are limited to eight cards every 24 hours. Play at your own risk.",
    "spin_the_wheel_bonus": f"The spin-the-wheel rewarded you with .",
}

tooltip_hover_start = {}
enhancements_info = {}


#---------------------#
#--------LISTS--------#
#---------------------#

ducks = []
floating_texts = []
magical_auto_clickers = []
duck_pop_effects = []
option_hover_rects = []
donate_hover_rects = []
spin_the_wheel_rects = []
tarot_card_rects = []


#---------------------#
#------FUNCTIONS------#
#---------------------#

def spawn_duck(pool, duck_image, shrink_x = 0.75, shrink_y = 0.65, offset=(0, -30)):
    duck_radius = duck_image.get_width() // 2
    
    a = pool.rect.width / 2 * shrink_x - duck_radius
    b = pool.rect.height / 2 * shrink_y - duck_radius
    
    h, k = pool.get_center()
    h += offset[0]
    k += offset[1]

    while True:
        x = random.randint(int(h - a), int(h + a))
        y = random.randint(int(k - b), int(k + b))
        
        if ((x - h) ** 2) / (a ** 2) + ((y - k) ** 2) / (b ** 2) <= 1:
            return duck_image.get_rect(center=(x, y))
        

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "

        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return lines


def draw_upgrade_rows(screen, game_data, manager):
    start_x = sx(20)
    start_y = screen_height - sy(270)
    spacing_x = sx(50)
    spacing_y = sy(50)

    hover_rects = []

    row = 0

    for key in ["duckNests","goldenDuckStatue","quakingSpeaker","duckCoop","duckBeacon"]:

        level = game_data.get(key, 0)
        icon = manager.get_upgrade_icon(key)
        description = manager.get_upgrade_description(key)

        if not icon:
            continue

        if not description:
            continue

        for i in range(level):
            x = start_x + i * spacing_x
            y = start_y + row * spacing_y

            rect = icon.get_rect(topleft=(x, y))
            screen.blit(icon, rect)

            hover_rects.append((rect, f"{key}_{i}"))

        row += 1

    return hover_rects


def draw_enhancements(screen, game_data, icons, positions):
    purchases = game_data["purchases"]
    hover_rects = []

    for key, icon in icons.items():
        if purchases.get(key, False):
            position = positions[key]
            rect = icon.get_rect(center=position)
            screen.blit(icon, rect)

            hover_rects.append((rect, key))

    return hover_rects


def get_clicker_position(index, total, pool):
    center = pygame.Vector2(pool.rect.center)

    radius = max(pool.rect.width, pool.rect.height) // 2 + 80

    angle = (index / total) * math.tau

    x = center.x + math.cos(angle) * radius
    y = center.y + math.sin(angle) * radius

    return x, y


def get_current_dps():
    dps = game_data["ducksPerSecond"]
    multiplerDPS = game_data["multiplierDPS"]

    dps *= multiplerDPS

    if shiny_active:
        dps *= shiny_dps_multiplier

    if spin_the_wheel_boost_active:
        dps *= reward_bonus

    return int(dps)


def get_current_dpc():
    dpc = game_data["ducksPerClick"]
    multiplierDPC = game_data["multiplierDPC"]
    critical_chance = game_data["criticalChance"]
    critical_power = game_data["criticalPower"]

    roll = random.uniform(0.0, 1.0)

    dpc *= multiplierDPC

    if shiny_active:
        dpc *= shiny_dpc_multiplier

    if spin_the_wheel_boost_active:
        dpc *= reward_bonus

    crit = False

    if roll < critical_chance:
        dpc *= critical_power
        crit = True

    return int(dpc), crit


def get_duck_spawn_count(game_data):
    base = 1

    beacon_level = game_data.get("duckBeacon", 0)

    chance_percent = beacon_level * 0.5

    extra = chance_percent / 100
    guaranteed = int(extra)
    remainder = extra - guaranteed

    count = base + guaranteed

    if random.random() < remainder:
        count += 1

    return count


def draw_animated_tooltip(screen, text, font, rect, mouse_pos, key, offset_x, offset_y):
    global tooltip_hover_start

    if not rect.collidepoint(mouse_pos):
        tooltip_hover_start.pop(key, None)
        return

    if key not in tooltip_hover_start:
        tooltip_hover_start[key] = pygame.time.get_ticks()

    hover_start_time = tooltip_hover_start[key]

    padding = sx(8)
    max_width = sx(600)

    lines = wrap_text(text, font, max_width)

    line_height = font.get_height()

    surfaces = [font.render(line, True, (255,255,255)) for line in lines]
    box_width = max(s.get_width() for s in surfaces) + padding * 2
    box_height = line_height * len(lines) + padding * 2

    x = rect.right + offset_x
    y = rect.top + offset_y

    pygame.draw.rect(screen, (30, 30, 30), (x, y, box_width, box_height))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, box_width, box_height), sx(2))

    current_time = pygame.time.get_ticks()
    elapsed = current_time - hover_start_time
    letter_delay = 5

    for i, line in enumerate(lines):
        x_offset = 0

        for index, letter in enumerate(line):

            appear_time = index * letter_delay

            if elapsed > appear_time:

                progress = min(1, (elapsed - appear_time) / 150)

                scale = 1 + (1 - progress) * 0.6

                letter_surface = font.render(letter, True, (255,255,255))
                scaled_surface = pygame.transform.scale_by(letter_surface, scale)

                y_pos = y + padding + i * line_height

                screen.blit(
                    scaled_surface,
                    (
                        x + padding + x_offset,
                        y_pos - (scaled_surface.get_height() - line_height) / 2
                    )
                )

                x_offset += letter_surface.get_width()


def quit_game():
    global running
    running = False


def reset_game(game_data, default_data):
    game_data.clear()
    game_data.update(default_data)
    magical_auto_clickers.clear()
    ducks.clear()


def reset_game_callback():
    reset_game(game_data, default_data)
    save_game(game_data)

    pygame.quit()

    if getattr(sys, 'frozen', False):
        # Compiled executable
        subprocess.Popen([sys.executable])
    else:
        # Python script
        subprocess.Popen([sys.executable] + sys.argv)

    sys.exit()


def draw_animated_text(screen, text, font, color, center_pos, key):
    global tooltip_hover_start

    if key not in tooltip_hover_start:
        tooltip_hover_start[key] = pygame.time.get_ticks()

    start_time = tooltip_hover_start[key]
    current_time = pygame.time.get_ticks()
    elapsed = current_time - start_time

    letter_delay = 5
    line_height = font.get_height()

    x_offset_total = 0
    letters = []

    for letter in text:
        surf = font.render(letter, True, color)
        letters.append(surf)
        x_offset_total += surf.get_width()

    start_x = center_pos[0] - x_offset_total // 2
    y = center_pos[1]

    x_offset = 0

    for index, letter_surface in enumerate(letters):
        appear_time = index * letter_delay

        if elapsed > appear_time:
            progress = min(1, (elapsed - appear_time) / 150)
            scale = 1 + (1 - progress) * 0.6

            scaled_surface = pygame.transform.scale_by(letter_surface, scale)

            screen.blit(
                scaled_surface,
                (
                    start_x + x_offset,
                    y - scaled_surface.get_height() // 2
                )
            )

        x_offset += letter_surface.get_width()


def clear_data_warning():

    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    popup_width = sx(600)
    popup_height = sy(300)

    main_rect = pygame.Rect(0, 0, popup_width, popup_height)
    main_rect.center = (screen_width // 2, screen_height // 2)

    pygame.draw.rect(screen, (60, 60, 60), main_rect)
    pygame.draw.rect(screen, (255, 255, 255), main_rect, 3)

    clear_data_warning = fonts["large"].render("WARNING!", True, (255, 255, 255))
    clear_data_warning_rect = clear_data_warning.get_rect(
        center=(main_rect.centerx, main_rect.top + sy(40))
    )

    clear_data_description = fonts["small"].render(
        "You are about to clear ALL DATA!",
        True,
        (255, 255, 255)
    )

    clear_data_description_rect = clear_data_description.get_rect(
        center=(main_rect.centerx, main_rect.top + sy(100))
    )

    clear_data_description2 = fonts["small"].render(
        "This cannot be undone.",
        True,
        (255, 255, 255)
    )

    clear_data_description_rect2 = clear_data_description2.get_rect(
        center=(main_rect.centerx, main_rect.top + sy(130))
    )

    clear_data_description3 = fonts["verysmall"].render(
        "(Game will close and restart)",
        True,
        (255, 255, 255)
    )

    clear_data_description_rect3 = clear_data_description3.get_rect(
        center=(main_rect.centerx, main_rect.top + sy(160))
    )

    button_width = sx(180)
    button_height = sy(50)

    clear_button_rect = pygame.Rect(0, 0, button_width, button_height)
    cancel_button_rect = pygame.Rect(0, 0, button_width, button_height)

    clear_button_rect.center = (main_rect.centerx - sx(120), main_rect.bottom - sy(60))
    cancel_button_rect.center = (main_rect.centerx + sx(120), main_rect.bottom - sy(60))

    pygame.draw.rect(screen, (80, 0, 0), clear_button_rect)
    pygame.draw.rect(screen, (4, 207, 116), cancel_button_rect)

    clear_text = fonts["small"].render("CLEAR DATA", True, (255, 0, 0))
    cancel_text = fonts["small"].render("CANCEL", True, (255, 255, 255))

    clear_text_rect = clear_text.get_rect(center=clear_button_rect.center)
    cancel_text_rect = cancel_text.get_rect(center=cancel_button_rect.center)

    draw_animated_text(
        screen,
        "WARNING!",
        fonts["verylarge"],
        (255, 255, 255),
        clear_data_warning_rect.center,
        "clear_warning_title"
    )

    draw_animated_text(
        screen,
        "You are about to clear ALL DATA!",
        fonts["small"],
        (255, 255, 255),
        clear_data_description_rect.center,
        "clear_warning_desc1"
    )

    draw_animated_text(
        screen,
        "This cannot be undone.",
        fonts["small"],
        (255, 255, 255),
        clear_data_description_rect2.center,
        "clear_warning_desc2"
    )

    draw_animated_text(
        screen,
        "(Game will close and restart)",
        fonts["small"],
        (255, 255, 255),
        clear_data_description_rect3.center,
        "clear_warning_desc3"
    )

    draw_animated_text(
        screen,
        "CLEAR DATA",
        fonts["small"],
        (255, 0, 0),
        clear_text_rect.center,
        "clear_warning_button"
    )

    draw_animated_text(
        screen,
        "CANCEL",
        fonts["small"],
        (255, 255, 255),
        cancel_text_rect.center,
        "cancel_warning_button"
    )


    return clear_button_rect, cancel_button_rect


def get_spin_time_remaining(game_data):
    extras = game_data["extras"]

    if extras.get("spin_the_wheel_ready", True):
        return 0

    next_time = extras.get("spin_the_wheel_next_time", 0)
    remaining = int(next_time - time.time())

    if remaining <= 0:
        extras["spin_the_wheel_ready"] = True
        extras["spin_the_wheel_next_time"] = 0
        save_game(game_data)
        return 0

    return remaining


def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02}"


def apply_bonus_effect(reward_name):
    global spin_the_wheel_boost_active, reward_time, reward_bonus
    spin_the_wheel_boost_active = True


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


game_data = load_game(default_data)

pygame.mixer.music.set_volume(game_data["settings"]["volume"])
if game_data["settings"]["sfx"] == True:
    pygame.mixer.music.set_volume(game_data["settings"]["volume"])
    click_sound.set_volume(game_data["settings"]["volume"])
    duck_click_sound.set_volume(game_data["settings"]["volume"])
    purchase_sound.set_volume(game_data["settings"]["volume"])
    hover_sound.set_volume(game_data["settings"]["volume"])
    error_sound.set_volume(game_data["settings"]["volume"])
                            
if game_data["settings"]["music"] == True:
    music_sound.set_volume(game_data["settings"]["volume"])

console = Console(screen_width, screen_height, scale, quit_game, save_game, reset_game_callback)

upgade_manager = UpgradeManager(screen_width, screen_height, game_data, scale)

display_ducks = float(game_data["ducks"])

floating_texts_enabled = game_data["settings"]["duckText"]


#---------------------#
#------FOR LOOPS------#
#---------------------#

for i in range(game_data["magicalAutoClickers"]):
    pos = get_clicker_position(i, game_data["magicalAutoClickers"], pool)

    magical_auto_clickers.append(
        MagicalAutoClicker(pos, magical_auto_clicker_image)
    ) 

for enhancement in upgrade_data["enhancements"]:
    purchase_key = enhancement.get("purchase_key")

    if purchase_key:
        enhancements_info[purchase_key] = {
            "description": enhancement.get("description", "")
        }


#---------------------#
#----IF STATEMENTS----#
#---------------------#

if game_data["extras"]["tarot_goal"] == 0 and game_data["purchases"]["tarotCardsB"]:
    game_data["extras"]["tarot_goal"] = get_tarot_goal(game_data)


#---------------------#
#-------RUNNING-------#
#---------------------#

running = True
while running:


    #---------------------#
    #------VARIABLES------#
    #---------------------#

    current_time = pygame.time.get_ticks()

    screen.fill((100, 200, 255))
    screen.blit(background, background.get_rect(center=(screen_width // 2, screen_height // 2)))

    pool.set_level(game_data["poolSize"])
    pool.set_image(pool_images[game_data["poolColor"]])
    pool.draw(screen)

    upgrade_hover_rects = draw_upgrade_rows(screen, game_data, upgade_manager)

    update_tarot_reset(game_data)

    mouse_pos = pygame.mouse.get_pos()

    options_rect = draw_options(screen, mouse_pos, fonts)
    stats_rect = draw_stats(screen, mouse_pos, fonts)
    donate_rect = draw_donate(screen, mouse_pos, fonts)

    if game_data["purchases"]["spinTheWheelB"]:
        spin_the_wheel_rect = draw_SpinTheWheel(screen, spin_the_wheel_icon)

    if game_data["purchases"]["tarotCardsB"]:
        tarot_cards_rect = draw_tarot_cards_button(screen, tarot_card_icon)


    target = game_data["ducks"]

    speed = 12

    display_ducks += (target - display_ducks) * 0.15

    if abs(display_ducks - target) < 0.5:
        display_ducks = target


    #---------------------#
    #---------TEXT--------#
    #---------------------#

    duck_header = fonts["header"].render(f"{int(display_ducks):,} Ducks", False, (255, 255, 255))
    pulse = 1 + min(0.25, abs(target - display_ducks) / 20000)
    duck_header = pygame.transform.scale_by(duck_header, pulse)
    screen.blit(duck_header, duck_header.get_rect(centerx=screen_width // 2, y=sy(40)))

    ducks_per_sec_text = fonts["large"].render(f"{get_current_dps():,} Ducks Per Second", False, (255, 255, 255))
    screen.blit(ducks_per_sec_text, ducks_per_sec_text.get_rect(centerx=screen_width // 2, y=sy(100)))

    store_text_title = fonts["large"].render("Store", False, (255, 255, 255)) 
    screen.blit(store_text_title, store_text_title.get_rect(topright = (screen_width - sx(195), sy(30))))

    store_text_u = fonts["small"].render("Upgrades", False, (255, 255, 255))
    screen.blit(store_text_u, store_text_u.get_rect(topright = (screen_width - sx(183), sy(60))))

    store_text_e = fonts["small"].render("Enhancements", False, (255, 255, 255))
    screen.blit(store_text_e, store_text_e.get_rect(topright = (screen_width - sx(160), sy(715))))


    #---------------------#
    #----FOR LOOPS/IF's---#
    #---------------------#
 

    #----Pygame Event----#
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F9:
                console.toggle()
                
        if console.active:
            console.handle_event(event, game_data, get_current_dps)
            continue


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                mouse_pos = event.pos

                if show_warning_clear_data and clear_button_rect and cancel_button_rect:
                    if clear_button_rect.collidepoint(event.pos):
                        reset_game_callback()
                        save_game(game_data)
                        show_warning_clear_data = False
                        click_sound.play()

                    elif cancel_button_rect.collidepoint(event.pos):
                        show_warning_clear_data = False
                        click_sound.play()

                    continue

                for duck in ducks[:]:
                    if duck.rect.collidepoint(mouse_pos):

                        if duck.shiny:
                            shiny_active = True
                            shiny_timer = shiny_duration
                        
                        DPC, crit = get_current_dpc()

                        game_data["ducks"] += DPC
                        game_data["allTimeDucks"] += DPC
                        add_tarot_progress(game_data, DPC)
                        
                        ducks.remove(duck)
                        duck_pop_effects.append(DuckPopEffect(duck.image, duck.rect.center))
                        current_time_now = pygame.time.get_ticks()
                        duck_click_sound.play()

                        color = (255, 220, 80) if shiny_active else (255,255,255)

                        floating_texts.append(
                            FloatingText(
                                f"+{DPC:,}",
                                duck.rect.center,
                                critical=crit
                            )
                        )
                        break

                bought, cost = upgade_manager.clicked(mouse_pos, game_data)

                if options_rect.collidepoint(event.pos):
                    show_options = not show_options
                    show_stats = False
                    show_donate = False
                    show_spin_the_wheel = False
                    show_tarot_card_frame = False
                    click_sound.play()

                    if show_options:
                        keys_to_reset = ["options_title", "volume_text", "vol_minus", "vol_plus",
                                        "save_game_text", "quit_game_text", "wipe_save_text"]
                        keys_to_reset += [f"options_line_{i}" for i in range(10)]
                        
                        for key in keys_to_reset:
                            tooltip_hover_start.pop(key, None)

                if stats_rect.collidepoint(event.pos):
                    show_stats = not show_stats
                    show_options = False
                    show_donate = False
                    show_spin_the_wheel = False
                    show_tarot_card_frame = False
                    click_sound.play()

                    if show_stats:
                        keys_to_reset = ["stats_title"] + [f"stats_line_{i}" for i in range(23)]
                        for key in keys_to_reset:
                            tooltip_hover_start.pop(key, None)
                
                if donate_rect.collidepoint(event.pos):
                    show_donate = not show_donate
                    show_options = False
                    show_stats = False
                    show_spin_the_wheel = False
                    show_tarot_card_frame = False
                    click_sound.play()

                    if show_donate:
                        keys_to_reset = ["support_title", "support_desc", "support_desc2", "support_desc3", "support_button"]
                        for key in keys_to_reset:
                            tooltip_hover_start.pop(key, None)

                if game_data["purchases"]["spinTheWheelB"]:
                    if spin_the_wheel_rect and spin_the_wheel_rect.collidepoint(event.pos):
                        show_spin_the_wheel = not show_spin_the_wheel
                        show_options = False
                        show_stats = False
                        show_donate = False
                        show_tarot_card_frame = False
                        click_sound.play()

                        if show_spin_the_wheel:
                            keys_to_reset = ["SPIN-THE-WHEEL_title", "spin_button"]
                            for key in keys_to_reset:
                                tooltip_hover_start.pop(key, None)

                if game_data["purchases"]["tarotCardsB"]:
                    if tarot_cards_rect and tarot_cards_rect.collidepoint(event.pos):
                        show_tarot_card_frame = not show_tarot_card_frame
                        show_options = False
                        show_stats = False
                        show_donate = False
                        show_spin_the_wheel = False
                        click_sound.play()

                        if show_tarot_card_frame:
                            keys_to_reset = ["tarot_cards_title", "pull_card_button", "help_info", "tarot_card_reward", "progress_bar_text", "daily_cards_counter"]
                            for key in keys_to_reset:
                                tooltip_hover_start.pop(key, None)

                if show_options:
                    for rect, key in option_hover_rects:
                        if rect.collidepoint(event.pos):

                            if key == "volume_up":
                                game_data["settings"]["volume"] = min(
                                    1.0,
                                    round(game_data["settings"]["volume"] + 0.1, 1)
                                )

                            elif key == "volume_down":
                                game_data["settings"]["volume"] = max(
                                    0.0,
                                    round(game_data["settings"]["volume"] - 0.1, 1)
                                )

                            elif key == "wipe_save":
                                show_warning_clear_data = True
                                for key in [
                                    "clear_warning_title",
                                    "clear_warning_desc1",
                                    "clear_warning_desc2",
                                    "clear_warning_button",
                                    "cancel_warning_button"
                                ]:
                                    tooltip_hover_start.pop(key, None)

                            elif key == "quit_game":
                                quit_game()

                            elif key == "save_game":
                                if current_time > save_cooldown_until:
                                    save_game(game_data)
                                    save_message_timer = current_time + 3000
                                    save_cooldown_until = current_time + 1500
                                    click_sound.play()

                            ##################################################
                            # SET MUSIC OPTION ONCE MUSIC IS ADDED!!!!!
                            ##################################################
                            elif key == "music":
                                game_data["settings"][key] = not game_data["settings"][key]
                                
                                if game_data["settings"]["music"] == True:
                                    music_sound.set_volume(1.0)
                                else:
                                    music_sound.set_volume(0.0)
 
                            elif key == "sfx":
                                game_data["settings"][key] = not game_data["settings"][key]

                                if game_data["settings"]["sfx"] == True:
                                    click_sound.set_volume(1.0)
                                    duck_click_sound.set_volume(1.0)
                                    purchase_sound.set_volume(1.0)
                                    hover_sound.set_volume(1.0)
                                    error_sound.set_volume(1.0)
                                else:
                                    click_sound.set_volume(0.0)
                                    duck_click_sound.set_volume(0.0)
                                    purchase_sound.set_volume(0.0)
                                    hover_sound.set_volume(0.0)
                                    error_sound.set_volume(0.0)

                            elif key == "duckText":
                                game_data["settings"][key] = not game_data["settings"][key]

                                if game_data["settings"]["duckText"] == True:
                                    floating_texts_enabled = game_data["settings"]["duckText"]

                                else:
                                    floating_texts_enabled = game_data["settings"]["duckText"]

                            elif key == "magicalAutoClickers":
                                game_data["settings"][key] = not game_data["settings"][key]

                                if game_data["settings"]["magicalAutoClickers"] == True:
                                    for i in range(game_data["magicalAutoClickers"]):
                                        pos = get_clicker_position(i, game_data["magicalAutoClickers"], pool)

                                        magical_auto_clickers.append(
                                            MagicalAutoClicker(pos, magical_auto_clicker_image)
                                        )

                                else:
                                    magical_auto_clickers.clear()


                            else:
                                game_data["settings"][key] = not game_data["settings"][key]
                            
                            click_sound.play()

                            if game_data["settings"]["sfx"] == True:
                                pygame.mixer.music.set_volume(game_data["settings"]["volume"])
                                click_sound.set_volume(game_data["settings"]["volume"])
                                duck_click_sound.set_volume(game_data["settings"]["volume"])
                                purchase_sound.set_volume(game_data["settings"]["volume"])
                                hover_sound.set_volume(game_data["settings"]["volume"])
                                error_sound.set_volume(game_data["settings"]["volume"])
                            
                            if game_data["settings"]["music"] == True:
                                music_sound.set_volume(game_data["settings"]["volume"])

                            save_game(game_data)

                if show_donate:
                    for rect, key in donate_hover_rects:
                        if rect.collidepoint(event.pos):
                            webbrowser.open(support_url)

                if show_spin_the_wheel:
                    for rect, key in spin_the_wheel_rects:
                        if rect.collidepoint(event.pos):
                            if key == "spin_button":
                                if game_data["extras"]["spin_the_wheel_ready"]:
                                    spin_the_wheel()

                                    game_data["extras"]["spin_the_wheel_ready"] = False
                                    game_data["extras"]["spin_the_wheel_next_time"] = round(time.time() + 86400, 2)

                                    save_game(game_data)

                if show_tarot_card_frame:
                    for rect, key in tarot_card_rects:
                        if rect.collidepoint(event.pos):
                            if key == "pull_card_button":
                                pull_tarot_card(tarot_cards_list, game_data)

                                game_data["extras"]["tarrot_cards_available"] -= 1

                                if game_data["extras"]["tarrot_cards_available"] == 0:
                                    game_data["extras"]["tarrot_cards_ready"] = False
                                else:
                                    game_data["extras"]["tarrot_cards_ready"] = True


                if show_spin_the_wheel_frame:
                    if claim_button_rect.collidepoint(event.pos):
                        show_spin_the_wheel_frame = False

                        spin_the_wheel_boost_active = True
                        active_reward_time = reward_time
                        active_reward_bonus = reward_bonus

                if bought:
                    if game_data["magicalAutoClickers"] > len(magical_auto_clickers):
                        magical_auto_clickers.clear()

                        for i in range(game_data["magicalAutoClickers"]):
                            pos = get_clicker_position(i, game_data["magicalAutoClickers"], pool)

                            magical_auto_clickers.append(
                                MagicalAutoClicker(pos, magical_auto_clicker_image)
                            )
                        
                    save_game(game_data)
                elif cost > 0:
                    cannot_afford_message = f"Cannot afford, need {cost - game_data['ducks']:,} more ducks!"
                    cannot_afford_timer = current_time + 3000


    #----shiny active check----#
    if shiny_active:
        duck_time = clock.get_time()
        shiny_timer -= duck_time
        
        if shiny_timer <= 0:
            shiny_active = False


    #----sping the wheel boost active check----#
    if spin_the_wheel_boost_active:
        duck_time = clock.get_time()
        reward_time -= duck_time

        if reward_time <= 0:
            reward_time = 0
            spin_the_wheel_boost_active = False


    #----shiny active----#
    if shiny_active:
        size = sx(45)
        padding = sx(8)

        x = screen_width // 2 - size // 2
        y = sy(150)

        pulse = 1 + 0.08 * math.sin(pygame.time.get_ticks() * 0.01)

        icon = pygame.transform.scale_by(shiny_duck_icon, pulse)

        rect = pygame.Rect(x, y, size, size)
        shiny_hover_rect = rect

        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((255, 255, 120, 25))
        screen.blit(overlay, (0,0))

        pygame.draw.rect(screen, (255, 215, 0), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, sx(2))

        icon_rect = icon.get_rect(center=rect.center)
        screen.blit(icon, icon_rect)

        seconds = int(shiny_timer / 1000)
        timer_text = fonts["small"].render(f"{seconds}s", False, (255, 255, 255))
        screen.blit(timer_text, timer_text.get_rect(midtop=(rect.centerx, rect.bottom + sy(4))))

        color = (255, 220, 80) if shiny_active else (255,255,255)

        ducks_per_sec_text = fonts["large"].render(
            f"{get_current_dps():,} Ducks Per Second",
            False,
            color
        )


    #----spin the wheel boost active----#
    if spin_the_wheel_boost_active:
        size = sx(45)
        padding = sx(8)

        x = screen_width // 2 - size // 2
        y = sy(150)

        pulse = 1 + 0.08 * math.sin(pygame.time.get_ticks() * 0.01)

        icon = pygame.transform.scale(spin_the_wheel_icon, (sx(35), sy(35)))
        icon = pygame.transform.scale_by(icon, pulse)

        rect = pygame.Rect(x, y, size, size)
        shiny_hover_rect = rect

        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((255, 255, 120, 25))
        screen.blit(overlay, (0,0))

        pygame.draw.rect(screen, (255, 70, 70), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, sx(2))

        icon_rect = icon.get_rect(center=rect.center)
        screen.blit(icon, icon_rect)

        total_seconds = max(0, reward_time // 1000)

        minutes = total_seconds // 60
        seconds = total_seconds % 60

        timer_text = fonts["small"].render(
            f"{minutes:02d}:{seconds:02d}",
            False,
            (255, 255, 255)
        )

        screen.blit(timer_text, timer_text.get_rect(midtop=(rect.centerx, rect.bottom + sy(4))))

        color = (255,255,255)

        ducks_per_sec_text = fonts["large"].render(
            f"{get_current_dps():,} Ducks Per Second",
            False,
            color
        )


    #----Auto Save----#
    if current_time - last_save_time > 5000:
        save_game(game_data)
        last_save_time = current_time


    #----Duck spawn----#
    if len(ducks) < game_data["maxDucksInPool"]:
        if respawn_time is None:
            respawn_delay = game_data["spawnTime"]
            respawn_time = current_time + game_data["spawnTime"] * 1000
        
        elif current_time >= respawn_time:
            shiny_chance = game_data["shinyDuckChance"]
            roll = random.uniform(0.0, 1.0)

            if roll < shiny_chance:
                shiny = True
                duck_image = duck_images["shiny"]
            else:
                shiny = False
                duck_image = duck_images[game_data["duckColor"]]

            spawn_count = get_duck_spawn_count(game_data)

            for _ in range(spawn_count):

                if len(ducks) >= game_data["maxDucksInPool"]:
                    break

                shiny_chance = game_data["shinyDuckChance"]
                roll = random.random()

                if roll < shiny_chance:
                    shiny = True
                    duck_image = duck_images["shiny"]
                else:
                    shiny = False
                    duck_image = duck_images[game_data["duckColor"]]

                ducks.append(
                    Duck(
                        spawn_duck(pool, duck_image),
                        duck_image,
                        shiny
                    )
                )

            respawn_time = None


    #----Ducks per second / playtime----#
    game_speed = game_data.get("globalGameSpeed", 1)

    if current_time - tick_time >= 1000 / game_speed:
        game_data["ducks"] += get_current_dps()
        game_data["allTimeDucks"] += get_current_dps()
        add_tarot_progress(game_data, get_current_dps())
        game_data["playtime"] += 1
        tick_time += 1000 / game_speed
        

    #----Duck draw / animating----#
    for duck in ducks:
        duck.update()
        duck.draw(screen)


    #----draw magical auto clickers----#
    for clicker in magical_auto_clickers:
        clicker.draw(screen)


    #----floating text----#
    for text in floating_texts[:]:
        if floating_texts_enabled:
            text.update()
            text.draw(screen, fonts["large"])

            if text.dead():
                floating_texts.remove(text)


    #----magical auto clicker config----#
    for clicker in magical_auto_clickers:
        clicker.update(
            ducks,
            duck_click_sound,
            speed = 0.1 + game_data["magicalAutoClickerSpeed"],
            game_data=game_data,
            floating_texts=floating_texts,
            duck_pop_effects=duck_pop_effects,
            get_current_dpc = get_current_dpc,
            set_shiny_active = lambda: globals().update({
                "shiny_active": True,
                "shiny_timer": shiny_duration
            })
        )

    
    #----duck pop effect----#
    for effect in duck_pop_effects[:]:
        effect.update()
        effect.draw(screen)

        if effect.dead():
            duck_pop_effects.remove(effect)


    #----draw enhancements----#
    enhancements_hover_rects = draw_enhancements(screen, game_data, enhancement_icons, enhancement_positions)


    #----draw spin the wheel exclamation----#
    if game_data["purchases"]["spinTheWheelB"] and game_data["extras"]["spin_the_wheel_ready"] and spin_the_wheel_rect:
            draw_exclamation(screen, exclamation_icon, spin_the_wheel_rect)


    #----draw tarot cards exclamation----#
    if game_data["purchases"]["tarotCardsB"] and game_data["extras"]["tarrot_cards_ready"] and tarot_cards_rect:
            draw_exclamation(screen, exclamation_icon, tarot_cards_rect)


    #----upgrade icon tooltips----#
    for rect, unique_key in upgrade_hover_rects:

        base_key = unique_key.split("_")[0]

        description = (
            upgade_manager.get_upgrade_description(base_key)
            + f" Owned: {int(game_data[base_key]):,}"
        )

        draw_animated_tooltip(
            screen,
            description,
            fonts["verysmall"],
            rect,
            mouse_pos,
            f"upgrade_{unique_key}",
            sx(10),
            -sy(35)
        )


    #----enhancement icon tooltips----#
    for rect, key in enhancements_hover_rects:
        info = enhancements_info.get(key)

        if info:
            draw_animated_tooltip(
                screen,
                info["description"],
                fonts["verysmall"],
                rect,
                mouse_pos,
                f"enhancement_{key}",
                sx(10),
                0
            )


    #----Shiny icon tooltip----#
    if shiny_hover_rect:
        draw_animated_tooltip(
            screen,
            special_tooltips["shiny"],
            fonts["verysmall"],
            shiny_hover_rect,
            mouse_pos,
            "shiny_tooltip",
            sx(10),
            0
        )
        

    #----options frame----#
    if show_options:
        option_hover_rects = open_options(screen, fonts, game_data, mouse_pos, draw_animated_text)


    #----stats frame----#
    if show_stats:
        open_stats(screen, fonts, game_data, draw_animated_text)


    #----donate frame----#
    if show_donate:
        donate_hover_rects = open_donate(screen, fonts, game_data, draw_animated_text)


    #----spin the wheel frame----#
    if show_spin_the_wheel:
        spin_the_wheel_rects, show_spin_the_wheel_frame, reward_name, reward_bonus, reward_time = open_SpinTheWheel(screen, fonts, game_data, draw_animated_text, spin_the_wheel_info_icon, spin_the_wheel_arrow_icon, show_spin_the_wheel_frame, get_spin_time_remaining, format_time, sping_the_wheel_background_design)


    #----tarot cards frame----#
    if show_tarot_card_frame:
        tarot_card_rects, help_button_rect, tarot_cards_list = open_tarot_card_frame(screen, fonts, game_data, draw_animated_text, tarot_card_background_icon, tarot_card_single_icon, the_sun_tarot_card, the_devil_tarot_card, the_empress_tarot_card, death_tarot_card, wheel_of_fortune_tarot_card, the_tower_tarot_card, the_fool_tarot_card, the_world_tarot_card, page_of_cups_tarot_card, ace_of_pentacles_tarot_card, get_current_dps, tarot_card_background_design)


    #----cannot afford message----#
    if cannot_afford_message and current_time < cannot_afford_timer:
        cannot_afford_text = fonts["large"].render(cannot_afford_message, False, (255, 255, 255))
        screen.blit(cannot_afford_text, cannot_afford_text.get_rect(centerx=screen_width // 2, y=300))


    #----game saved message----#
    if save_message and current_time < save_message_timer:
        save_message_text = fonts["large"].render(save_message, False, (255, 255, 255))
        screen.blit(save_message_text, save_message_text.get_rect(centerx=screen_width // 2, y=300))


    #----upgrde list draw----#
    upgade_manager.draw(screen, fonts["large"], fonts["small"], fonts["verysmall"], game_data)


    #----show clear data warning frame----#
    if show_warning_clear_data:
        clear_button_rect, cancel_button_rect = clear_data_warning()


    #----show spin the wheel reward frame----#
    if show_spin_the_wheel_frame:
        claim_button_rect = sping_the_wheel_reward_frame(screen, fonts, draw_animated_text, reward_name)


    #----tarot card help tooltip----#
    if help_button_rect:
        draw_animated_tooltip(
            screen,
            special_tooltips["tarot_cards_help"],
            fonts["verysmall"],
            help_button_rect,
            mouse_pos,
            "tarot_cards_help_tooltip",
            sx(10),
            0
        )

    #----tarot cards available and ready check----#
    if game_data["extras"]["tarrot_cards_available"] > 0:
        game_data["extras"]["tarrot_cards_ready"] = True


    #----spin the wheel available and ready check----#
    if game_data["extras"]["spin_the_wheel_next_time"] == 0:
        game_data["extras"]["spin_the_wheel_ready"] = True


    # ---------------------#
    # --- CURSOR / HOVER---#
    # ---------------------#

    hovering = False

    for rect, _ in upgrade_hover_rects:
        if rect.collidepoint(mouse_pos):
            hovering = True
            break

    if not hovering:
        for rect, _ in enhancements_hover_rects:
            if rect.collidepoint(mouse_pos):
                hovering = True
                break

    if not hovering:
        for b in upgade_manager.buttons_upgrades:
            if b.rect.collidepoint(mouse_pos):
                hovering = True
                break

    if not hovering:
        for b in upgade_manager.buttons_enhancements[:4]:
            if b.rect.collidepoint(mouse_pos):
                hovering = True
                break

    if not hovering and show_spin_the_wheel_frame:
        if claim_button_rect.collidepoint(mouse_pos):
            hovering = True

    if not hovering:
        if options_rect.collidepoint(mouse_pos):
            hovering = True

    if not hovering:
        if game_data["purchases"]["spinTheWheelB"]:
            if spin_the_wheel_rect.collidepoint(mouse_pos):
                hovering = True

    if not hovering:
        if game_data["purchases"]["tarotCardsB"]:
            if tarot_cards_rect.collidepoint(mouse_pos):
                hovering = True

    if not hovering:
        if stats_rect.collidepoint(mouse_pos):
            hovering = True

    if not hovering:
        if donate_rect.collidepoint(mouse_pos):
            hovering = True

    if show_warning_clear_data and clear_button_rect and cancel_button_rect:
        if clear_button_rect.collidepoint(mouse_pos):
            hovering = True

        elif cancel_button_rect.collidepoint(mouse_pos):
            hovering = True

    if not hovering and shiny_hover_rect and shiny_hover_rect.collidepoint(mouse_pos):
        hovering = True

    if not hovering:
        for duck in ducks:
            if duck.rect.collidepoint(mouse_pos):
                hovering = True
                break

    if not hovering and show_options:
        for rect, _ in option_hover_rects:
            if rect.collidepoint(mouse_pos):
                hovering = True
                break
    
    if not hovering and show_donate:
        for rect, key in donate_hover_rects:
            if rect.collidepoint(mouse_pos):
                hovering = True
                break
    
    if not hovering and show_spin_the_wheel:
        for rect, key in spin_the_wheel_rects:
            if rect.collidepoint(mouse_pos):
                hovering = True
                break

    if not hovering and show_tarot_card_frame:
        for rect, key in tarot_card_rects:
            if rect.collidepoint(mouse_pos):
                hovering = True
                break

    cursor_to_draw = cursor_hover_image if hovering else cursor_image

    rect = cursor_to_draw.get_rect(center=mouse_pos)
    screen.blit(cursor_to_draw, rect)


    #---------------------#
    #-----FINAZLIATION----#
    #---------------------#
    
    console.draw(screen, fonts["small"])
    
    pygame.display.flip()

    clock.tick(int(60 * game_data.get("globalGameSpeed", 1)))

pygame.quit()