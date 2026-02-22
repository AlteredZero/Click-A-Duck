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

    options_text = fonts["large"].render("Stats", False, (255, 255, 255))
    screen.blit(options_text, options_text.get_rect(center=rect.center))

    return rect


def open_stats(screen, fonts, game_data):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height

    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(250), sy(20), sx(400), sy(955))

    pygame.draw.rect(screen, (60, 60, 60), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

    title = fonts["large"].render("Stats", False, (255, 255, 255))
    screen.blit(title, title.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(40)))

    ducks_text = fonts["small"].render(f"Ducks: {int(game_data["ducks"]):,}", False, (255, 255, 255))
    screen.blit(ducks_text, ducks_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(90)))

    dpc_text = fonts["small"].render(f"Ducks per click: {int(game_data["ducksPerClick"]):,}", False, (255, 255, 255))
    screen.blit(dpc_text, dpc_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(130)))

    dps_text = fonts["small"].render(f"Ducks per second: {int(game_data["ducksPerSecond"]):,}", False, (255, 255, 255))
    screen.blit(dps_text, dps_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(170)))

    max_duck_text = fonts["small"].render(f"Max ducks in pool: {int(game_data["maxDucksInPool"]):,}", False, (255, 255, 255))
    screen.blit(max_duck_text, max_duck_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(210)))

    spawn_time_text = fonts["small"].render(f"Duck spawn time: {game_data["spawnTime"]:,}s", False, (255, 255, 255))
    screen.blit(spawn_time_text, spawn_time_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(250)))

    strong_cursor_text = fonts["small"].render(f"Strong cursors: {game_data["DPCUpgradeBought"]:,}", False, (255, 255, 255))
    screen.blit(strong_cursor_text, strong_cursor_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(290)))

    nests_text = fonts["small"].render(f"Duck nests: {game_data["duckNests"]:,}", False, (255, 255, 255))
    screen.blit(nests_text, nests_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(330)))

    gold_statue_text = fonts["small"].render(f"Golden duck statues: {game_data["goldenDuckStatue"]:,}", False, (255, 255, 255))
    screen.blit(gold_statue_text, gold_statue_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(370)))

    quacking_speaker_text = fonts["small"].render(f"Quaking speakers: {game_data["quakingSpeaker"]:,}", False, (255, 255, 255))
    screen.blit(quacking_speaker_text, quacking_speaker_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(410)))

    reinforced_cursor_text = fonts["small"].render(f"Reinforced cursors: {game_data["reainforcedCursorB"]:,}", False, (255, 255, 255))
    screen.blit(reinforced_cursor_text, reinforced_cursor_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(450)))

    duck_coop_text = fonts["small"].render(f"Duck coops: {game_data["duckCoop"]:,}", False, (255, 255, 255))
    screen.blit(duck_coop_text, duck_coop_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(490)))

    duck_beacon_text = fonts["small"].render(f"Duck beacons: {game_data["duckBeacon"]:,}", False, (255, 255, 255))
    screen.blit(duck_beacon_text, duck_beacon_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(530)))

    crit_chance_text = fonts["small"].render(f"Critical chance: {game_data["criticalChance"]*100}%", False, (255, 255, 255))
    screen.blit(crit_chance_text, crit_chance_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(570)))

    crit_power_text = fonts["small"].render(f"Critical power: x{game_data["criticalPower"]}", False, (255, 255, 255))
    screen.blit(crit_power_text, crit_power_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(610)))

    multiplier_dpc_text = fonts["small"].render(f"DPC multiplier: x{game_data["multiplierDPC"]}", False, (255, 255, 255))
    screen.blit(multiplier_dpc_text, multiplier_dpc_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(650)))

    multiplier_dps_text = fonts["small"].render(f"DPS multiplier: x{game_data["multiplierDPS"]}", False, (255, 255, 255))
    screen.blit(multiplier_dps_text, multiplier_dps_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(690)))

    shiny_duck_text = fonts["small"].render(f"Shiny duck chance: {game_data["shinyDuckChance"]*100}%", False, (255, 255, 255))
    screen.blit(shiny_duck_text, shiny_duck_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(730)))

    two_duck_spawn_text = fonts["small"].render(f"Two duck spawn chance: {game_data["twoDuckSpawnChance"]*100}%", False, (255, 255, 255))
    screen.blit(two_duck_spawn_text, two_duck_spawn_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(770)))

    magic_auto_clicker_text = fonts["small"].render(f"Magical auto clickers: {game_data["magicalAutoClickers"]:,}", False, (255, 255, 255))
    screen.blit(magic_auto_clicker_text, magic_auto_clicker_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(810)))

    auto_clicker_speed_text = fonts["small"].render(f"Auto clicker speed: {game_data["magicalAutoClickerSpeed"]:,}", False, (255, 255, 255))
    screen.blit(auto_clicker_speed_text, auto_clicker_speed_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(850)))

    all_time_duck_text = fonts["small"].render(f"All time ducks: {int(game_data["allTimeDucks"]):,}", False, (255, 255, 255))
    screen.blit(all_time_duck_text, all_time_duck_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(890)))

    playtime_text = fonts["small"].render(f"Playtime: {game_data["playtime"]}s", False, (255, 255, 255))
    screen.blit(playtime_text, playtime_text.get_rect(centerx=menu_rect.x + menu_rect.width // 2, y=sy(930)))