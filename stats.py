import pygame

base_width = 2560
base_height = 1440


def draw_stats(screen, mouse_pos, fonts):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    background = (60, 60, 60)

    rect = pygame.Rect(sx(20), sy(90), sx(200), sy(60))

    pygame.draw.rect(screen, background, rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, s(3))

    stats_text = fonts["large"].render("Stats", False, (255, 255, 255))
    screen.blit(stats_text, stats_text.get_rect(center=rect.center))

    return rect


def open_stats(screen, fonts, game_data, draw_animated_text):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(250), sy(20), sx(400), sy(955))

    pygame.draw.rect(screen, (60, 60, 60), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

    stats_lines = [
        f"Ducks: {int(game_data['ducks']):,}",
        f"Ducks per click: {int(game_data['ducksPerClick']):,}",
        f"Ducks per second: {int(game_data['ducksPerSecond']):,}",
        f"Max ducks in pool: {int(game_data['maxDucksInPool']):,}",
        f"Duck spawn time: {game_data['spawnTime']}s",
        f"Strong cursors: {game_data['DPCUpgradeBought']:,}",
        f"Duck nests: {game_data['duckNests']:,}",
        f"Golden duck statues: {game_data['goldenDuckStatue']:,}",
        f"Quaking speakers: {game_data['quakingSpeaker']:,}",
        f"Reinforced cursors: {game_data['reainforcedCursorB']:,}",
        f"Duck coops: {game_data['duckCoop']:,}",
        f"Duck beacons: {game_data['duckBeacon']:,}",
        f"Critical chance: {game_data['criticalChance']*100}%",
        f"Critical power: x{game_data['criticalPower']}",
        f"DPC multiplier: x{game_data['multiplierDPC']}",
        f"DPS multiplier: x{game_data['multiplierDPS']}",
        f"Shiny duck chance: {game_data['shinyDuckChance']*100}%",
        f"Two duck spawn chance: {game_data['twoDuckSpawnChance']*100}%",
        f"Magical auto clickers: {game_data['magicalAutoClickers']:,}",
        f"Auto clicker speed: {game_data['magicalAutoClickerSpeed']:,}",
        f"All time ducks: {int(game_data['allTimeDucks']):,}",
        f"Playtime: {game_data['playtime']}s"
    ]

    draw_animated_text(
        screen,
        "Stats",
        fonts["large"],
        (255, 255, 255),
        (menu_rect.centerx, sy(60)),
        "stats_title"
    )

    start_y = sy(100)

    for i, line in enumerate(stats_lines):
        center_y = start_y + i * sy(40)

        draw_animated_text(
            screen,
            line,
            fonts["small"],
            (255,255,255),
            (menu_rect.centerx, center_y),
            f"stats_line_{i}"
        )