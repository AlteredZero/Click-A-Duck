#---------------------#
#-------IMPORTS-------#
#---------------------#

import pygame
import random
import math
import time
from save_manager import load_game, save_game
from fonts import load_fonts
from options import draw_options    
from stats import draw_stats
from floating_text import FloatingText
from duck import Duck
from pool import Pool
from upgrade_buttons import UpgradeManager
from magical_auto_clicker import MagicalAutoClicker
from duck_pop_effect import DuckPopEffect


#---------------------#
#--------INIT---------#
#---------------------#

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
screen_width, screen_height = screen.get_size()

pygame.display.set_caption("Click-A-Duck")
pygame.display.set_icon(pygame.image.load("assets/Images/Duck1.png").convert_alpha())


#---------------------#
#-------SCALING-------#
#---------------------#

base_width = 2560
base_height = 1440

scale_x = screen_width / base_width
scale_y = screen_height / base_height

scale = min(scale_x, scale_y)

fonts = load_fonts(scale)

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

cursor_image = load_scaled("assets/Images/CursorImage.png", 40, 40)

magical_auto_clicker_image = load_scaled("assets/Images/MagicalAutoClicker.png", 40, 40)

pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
t = 0
respawn_time = None

cannot_afford_message = ""
cannot_afford_timer = 0

last_duck_sound_time = 0
last_save_time = 0

last_duck_second = pygame.time.get_ticks()

shiny_active = False
shiny_timer = 0
shiny_duration = 30000

shiny_dpc_multiplier = 3
shiny_dps_multiplier = 2

shiny_duck_icon = load_scaled("assets/Images/ShinyDuck.png", 40, 40)


#---------------------#
#--------AUDIO--------#
#---------------------#

duck_click_sound = pygame.mixer.Sound("assets/audio/DuckQuack.mp3")
click_sound = pygame.mixer.Sound("assets/audio/MouseClick.mp3")
purchase_sound = pygame.mixer.Sound("assets/audio/PurchaseSound.mp3")
hover_sound = pygame.mixer.Sound("assets/audio/HoverSound.mp3")
error_sound = pygame.mixer.Sound("assets/audio/ErrorSound.mp3")


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
    "multiplier": 1.0,
    "twoDuckSpawnChance": 0,
    "shinyDuckChance": 0.0,
    "duckNests": 0,
    "goldenDuckStatue": 0,
    "quakingSpeaker": 0,
    "duckCoop": 0,
    "duckBeacon": 0,
    "purchases":{
        "orangeDuckB": False,
        "yellowPoolB": False,
        "magicalAutoClickerB": False,
        "megaDuckFeederB": False,
        "radiantPlungeB": False,
        "autoClickerSpeedB": False,
        "purpleDuckB": False,
        "featherFountainB": False,
        "quackAmplifierB": False,
        "duckMagnetB": False,
        "rubberDuckArmyB": False,
        "radiantPlungeIIB": False
    }
}

upgrade_info = {
    "duckNests": {
        "description": "A cozy duck nest raising little ducklings, who happily multiply. Grants +1 Duck per second (DPS)."
    },
    "goldenDuckStatue": {
        "description": "A golden duck statue ducks can admire, inspiring them to appear faster, increasing Duck spawn speed by +5%."
    },
    "quakingSpeaker": {
        "description": "A quaking speaker that ducks cannot resist, attracting more friends. Increases the maximum number of Ducks in the pool by 1."
    },
    "duckCoop": {
        "description": "Keeps the duck population growing more steadily, giving +3 Ducks per second (DPS)."
    },
    "duckBeacon": {
        "description": "A glowing marker visible to ducks from far away, grants +0.5% chance for 2 ducks to spawn per spawn time instead of just 1."
    },
}

enhancements_info = {
    "megaDuckFeederB": {
        "description": "A massive feeder that no Duck can resist, permanently increases Ducks per second by +25."
    },
    "featherFountainB": {
        "description": "A fountain of magical feathers keeps the Ducks entertained, increasing Ducks per second by +65."
    },
    "quackAmplifierB": {
        "description": "Every quack resonates across the pond with extra force, granting x2 Ducks per click permanently."
    },
    "duckMagnetB": {
        "description": "Ducks from nearby ponds mysteriously find their way here, permanently increases Ducks per second by +200."
    },
    "rubberDuckArmyB": {
        "description": "Here to serve and protect the duck empire, granting +300 DPS and +300 DPC permanently."
    },
    "DuckHeaterB": {
        "description": "Makes the ducks feel nice and warm, especially perfect for the winter season. Gives +900 DPS."
    },
    "BreadStormMachineB": {
        "description": "A magical machine that makes it literally rain bread, though the ducks aren't complaining. Gives +500 DPS and +500 DPC"
    },
    "duckDlc": {
        "description": "Adds more ducks. That's it. Gives +1150 DPS."
    },
    "duckCeoB": {
        "description": "The ducks elected a leader. things got organized fast. Grants +750 DPS and +750 DPC"
    },
    "hydroQuackPumpB": {
        "description": ""
    },
    "flockRouterB": {
        "description": ""
    },
    "pondOverclockerB": {
        "description": ""
    },
}

duck_images = {
    "yellow": load_scaled("assets/Images/Duck1.png", 60, 60),
    "shiny": load_scaled("assets/Images/ShinyDuck.png", 60, 60),
    "orange": load_scaled("assets/Images/OrangeDuck.png", 60, 60),
    "purple": load_scaled("assets/Images/PurpleDuck.png", 60, 60),
    "turquoise": load_scaled("assets/Images/TurquoiseDuck1.png", 60, 60),
}

pool_images = {
    "green": pygame.image.load("assets/Images/Pool1.png").convert_alpha(),
    "yellow": pygame.image.load("assets/Images/YellowPool.png").convert_alpha(),
    "hotPink": pygame.image.load("assets/Images/HotPinkPool.png").convert_alpha(),
    "coral": pygame.image.load("assets/Images/CoralPool.png").convert_alpha(),
}

upgrade_icons = {
    "duckNests": load_scaled("assets/Images/DuckNest.png", 45, 45),
    "goldenDuckStatue": load_scaled("assets/Images/DuckStatue.png", 45, 45),
    "quakingSpeaker": load_scaled("assets/Images/DuckSpeaker.png", 45, 45),
    "duckCoop": load_scaled("assets/Images/DuckCoop.png", 45, 45),
    "duckBeacon": load_scaled("assets/Images/DuckBeacon.png", 45, 45),
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
}


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
    start_y = screen_height - sy(255)
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

            hover_rects.append((rect, key))

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


game_data = load_game(default_data)

upgade_manager = UpgradeManager(screen_width, screen_height, game_data, scale)

display_ducks = float(game_data["ducks"])

#---------------------#
#--------LISTS--------#
#---------------------#

ducks = []
floating_texts = []
magical_auto_clickers = []
duck_pop_effects = []


#---------------------#
#------FOR LOOPS------#
#---------------------#

for i in range(game_data["magicalAutoClickers"]):
    pos = get_clicker_position(i, game_data["magicalAutoClickers"], pool)

    magical_auto_clickers.append(
        MagicalAutoClicker(pos, magical_auto_clicker_image)
    ) 


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


    mouse_pos = pygame.mouse.get_pos()

    draw_options(screen, mouse_pos, fonts)
    draw_stats(screen, mouse_pos, fonts)


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

    ducks_per_sec_text = fonts["large"].render(f"+{DPS} Ducks Per Second", False, (255, 255, 255))
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                for duck in ducks[:]:
                    if duck.rect.collidepoint(mouse_pos):

                        if duck.shiny:
                            shiny_active = True
                            shiny_timer = shiny_duration
                        
                        DPC = game_data["ducksPerClick"]
                        if shiny_active:
                            DPC *= shiny_dpc_multiplier

                        game_data["ducks"] += DPC
                        
                        ducks.remove(duck)
                        duck_pop_effects.append(DuckPopEffect(duck.image, duck.rect.center))
                        current_time_now = pygame.time.get_ticks()
                        duck_click_sound.play()
                        
                        if shiny_active:
                            floating_texts.append(
                                FloatingText(
                                    f"+{DPC}",
                                    duck.rect.center,
                                    color=(255, 220, 80)
                                )
                            )

                        else:
                            floating_texts.append(
                                FloatingText(
                                    f"+{DPC}",
                                    duck.rect.center
                                )
                            )
                        break

                bought, cost = upgade_manager.clicked(mouse_pos, game_data)

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


    duck_time = clock.get_time()

    if shiny_active:
        shiny_timer -= duck_time
        
        if shiny_timer <= 0:
            shiny_active = False


    if shiny_active:
        size = sx(45)
        padding = sx(8)

        x = screen_width // 2 - size // 2
        y = sy(150)

        pulse = 1 + 0.08 * math.sin(pygame.time.get_ticks() * 0.01)

        icon = pygame.transform.scale_by(shiny_duck_icon, pulse)

        rect = pygame.Rect(x, y, size, size)

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
            
            ducks.append(
                Duck(
                    spawn_duck(pool, duck_image),
                    duck_image,
                    shiny
                )
            )
            respawn_time = None


    #----Ducks per second----#
    if current_time - last_duck_second >= 1000:
        DPS = game_data["ducksPerSecond"]

        if shiny_active:
            DPS *= shiny_dps_multiplier

        game_data["ducks"] += DPS
        last_duck_second += 1000
        

    #----Duck draw / animating----#
    for duck in ducks:
        duck.update()
        duck.draw(screen)


    #----draw magical auto clickers----#
    for clicker in magical_auto_clickers:
        clicker.draw(screen)


    #----floating text----#
    for text in floating_texts[:]:
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
        )

    
    #----duck pop effect----#
    for effect in duck_pop_effects[:]:
        effect.update()
        effect.draw(screen)

        if effect.dead():
            duck_pop_effects.remove(effect)


    #----cannot afford message----#
    if cannot_afford_message and current_time < cannot_afford_timer:
        cannot_afford_text = fonts["large"].render(cannot_afford_message, False, (255, 255, 255))
        screen.blit(cannot_afford_text, cannot_afford_text.get_rect(centerx=screen_width // 2, y=300))


    #----draw enhancements----#
    enhancements_hover_rects = draw_enhancements(screen, game_data, enhancement_icons, enhancement_positions)


    #----upgrade icon tooltips----#
    for rect, key in upgrade_hover_rects:
        if rect.collidepoint(mouse_pos):
            description = upgade_manager.get_upgrade_description(key)\
            
            if description:
                padding = sx(8)
                max_width = sx(600)

                lines = wrap_text(description, fonts["verysmall"], max_width)

                line_height = fonts["verysmall"].get_height()
                surfaces = [fonts["verysmall"].render(line, True, (255,255,255)) for line in lines]

                box_width = max(s.get_width() for s in surfaces) + padding * 2
                box_height = line_height * len(surfaces) + padding * 2

                x = rect.right + sx(10)
                y = rect.top - 30

                pygame.draw.rect(screen, (30, 30, 30), (x, y, box_width, box_height))
                pygame.draw.rect(screen, (255, 255, 255), (x, y, box_width, box_height), sx(2))

                for i, surf in enumerate(surfaces):
                    screen.blit(surf, (x + padding, y + padding + i * line_height))


    #----enhancement icon tooltips----#
    for rect, key in enhancements_hover_rects:
        if rect.collidepoint(mouse_pos):
            info = enhancements_info.get(key)

            if info:
                padding = sx(8)
                max_width = sx(500)

                lines = wrap_text(info["description"], fonts["verysmall"], max_width)

                line_height = fonts["verysmall"].get_height()
                surfaces = [fonts["verysmall"].render(line, True, (255,255,255)) for line in lines]

                box_width = max(s.get_width() for s in surfaces) + padding * 2
                box_height = line_height * len(surfaces) + padding * 2

                x = rect.right + sx(10)
                y = rect.top

                pygame.draw.rect(screen, (30, 30, 30), (x, y, box_width, box_height))
                pygame.draw.rect(screen, (255, 255, 255), (x, y, box_width, box_height), sx(2))

                for i, surf in enumerate(surfaces):
                    screen.blit(surf, (x + padding, y + padding + i * line_height))


    #----upgrde list draw----#
    upgade_manager.draw(screen, fonts["large"], fonts["small"], fonts["verysmall"], game_data)


    #---------------------#
    #-----FINAZLIATION----#
    #---------------------#

    screen.blit(cursor_image, mouse_pos) 
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()