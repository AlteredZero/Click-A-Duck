import pygame
import json

upgrade_data_file_dir = "data/upgrade_data.json"

pygame.mixer.init()

purchase_sound = pygame.mixer.Sound("assets/audio/PurchaseSound.mp3")
click_sound = pygame.mixer.Sound("assets/audio/MouseClick.mp3")
error_sound = pygame.mixer.Sound("assets/audio/ErrorSound.mp3")


enhancement_effects = {
    "GoldenStrongCursorB": {
        "target_upgrade_title": "Stronger Cursor",
        "bonus_dpc": 5,
        "description": "Forged from pure gold, making your cursor even stronger. Grants +7 Ducks per click.",
        "icon": "assets/Images/StrongGoldCursor.png"
    },
    "LuxuryNestGroundB": {
        "target_upgrade_title": "Duck Nest",
        "bonus_dps": 5,
        "description": "A luxurious duck nest raising little ducklings, who happily multiply. Grants +5 Duck per second.",
        "icon": "assets/Images/PremiumDuckNest.png"
    }   
}


def load_icon(path, size):
    icon = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(icon, (size, size))


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


class UpgradeButton:
    def __init__(self, rect, config, scale):
        self.rect = rect
        self.scale = scale
        self.s = lambda v: int(v * scale)

        self.title = config["title"]
        self.base_cost = config["cost"]
        self.cost = self.base_cost

        self.icon = load_icon(config["icon"], self.s(52))
        self.save_key = config["save_key"]
        self.duck_color = config["duck_color"]
        self.bonus = config["bonus"]
        self.description = config["description"]
        self.save_key2 = config["save_key2"]
        self.one_time = config["one_time"]
        self.pool_color = config["pool_color"]
        self.purchase_key = config.get("purchase_key")

    def can_afford(self, game_data):
        return game_data["ducks"] >= self.cost
    
    
    def click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    
    def purchase(self, game_data):
        game_data["ducks"] -= self.cost
        purchase_sound.play()

        if self.save_key == "spawnTime":
            game_data[self.save_key] *= 0.95
            game_data[self.save_key] = max(0, round(game_data[self.save_key], 2))

        elif self.save_key == "shinyDuckChance":
            game_data[self.save_key] += 0.001

        elif self.bonus is not None:
            if self.duck_color is not None:
                game_data[self.save_key] = self.duck_color
                if self.save_key == "duckColor":
                    game_data["ducksPerClick"] += self.bonus

            elif self.pool_color is not None:
                game_data[self.save_key] = self.pool_color
                if self.save_key == "poolColor":
                    game_data["ducksPerClick"] += self.bonus

            elif self.title == "Rubber Duck Army":
                game_data["ducksPerClick"] += self.bonus
                game_data["ducksPerSecond"] += self.bonus
            
            elif self.title == "Bread Storm Machine":
                game_data["ducksPerClick"] += self.bonus
                game_data["ducksPerSecond"] += self.bonus

            elif self.title == "Duck CEO":
                game_data["ducksPerClick"] += self.bonus
                game_data["ducksPerSecond"] += self.bonus

            else:
                game_data[self.save_key] += self.bonus

        elif self.title == "Reinforced Cursor":
            game_data["multiplierDPC"] += 0.01
            game_data["multiplierDPC"] = round(game_data["multiplierDPC"], 3)
        
        elif self.title == "Duck Coop":
            game_data["multiplierDPS"] += 0.01
            game_data["multiplierDPS"] = round(game_data["multiplierDPS"], 3)

        elif self.title == "Auto Clicker Speed +1":
            game_data["magicalAutoClickerSpeed"] += 0.5

        else:
            game_data[self.save_key] += 1

        if self.save_key2 is not None:
            game_data[self.save_key2] += 1

        if self.one_time and self.purchase_key:
            game_data["purchases"][self.purchase_key] = True


    def draw_tooltip(self, screen, font, game_data):
        mouse_pos = pygame.mouse.get_pos()

        if not self.rect.collidepoint(mouse_pos):
            return

        padding = self.s(10)

        max_width = self.s(500)

        if not self.one_time:
            lines = wrap_text(self.description + f" Owned: {int(game_data[self.save_key2]):,}", font, max_width)
        else:
            lines = wrap_text(self.description, font, max_width)

        line_surfaces = [font.render(line, True, (255,255,255)) for line in lines]

        line_height = font.get_height()

        box_width = max(s.get_width() for s in line_surfaces) + padding * 2
        box_height = line_height * len(line_surfaces) + padding * 2

        x = self.rect.left - box_width - padding
        y = self.rect.top

        pygame.draw.rect(screen, (30, 30, 30), (x, y, box_width, box_height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, box_width, box_height), self.s(2))

        for i, surface in enumerate(line_surfaces):
            screen.blit(surface, (x + padding, y + padding + i * line_height))


    def draw(self, screen, text_title, text_cost, game_data):
        can_afford = self.can_afford(game_data)

        background = (4, 207, 116) if can_afford else (60, 60, 60)
        white_color = (255, 255, 255)

        pygame.draw.rect(screen, background, self.rect)
        pygame.draw.rect(screen, white_color, self.rect, self.s(3))

        padding = self.s(10)

        if self.icon:
            icon_rect = self.icon.get_rect()
            icon_rect.topleft = (
                self.rect.left + padding,
                self.rect.top + padding
            )
            screen.blit(self.icon, icon_rect)
        
        title = text_title.render(self.title, False, white_color)
        screen.blit(title, (self.rect.left + self.s(70), self.rect.top + self.s(10)))

        cost = text_cost.render(f"{self.cost:,} Ducks", False, white_color)
        screen.blit(cost, (self.rect.left + self.s(70), self.rect.top + self.s(40)))


    def update_cost(self, game_data):
        growth = 1.10
        key = self.save_key2 if self.save_key2 is not None else self.save_key
        times_bought = game_data.get(key, 0)

        if not isinstance(times_bought, (int, float)):
            self.cost = self.base_cost
            return

        self.cost = int(self.base_cost * (growth ** times_bought))

    
    def apply_enhancements(self, game_data):
        for key, effect in enhancement_effects.items():
            if game_data["purchases"].get(key, False):
                if effect["target_upgrade_title"] == self.title:
                    if "bonus_dpc" in effect:
                        self.bonus = effect["bonus_dpc"]
                    if "bonus_dps" in effect:
                        self.bonus = effect["bonus_dps"]

                    self.description = effect["description"]

                    if effect.get("icon"):
                        self.icon = load_icon(effect["icon"], int(52 * self.scale))


class UpgradeManager:
    def __init__(self, screen_width, screen_height, game_data, scale):
        self.scale = scale
        self.s = lambda v: int(v * scale)

        self.buttons_upgrades = []
        self.buttons_enhancements = []

        button_width = self.s(430)
        button_height = self.s(75)
        spacing = self.s(85)
        start_y = self.s(100)
        start_y2 = self.s(740)
        right_margin = self.s(20)


        with open(upgrade_data_file_dir, "r") as f:
            data = json.load(f)

        upgrades = data["upgrades"]
        enhancements = data["enhancements"]


        for i, config in enumerate(upgrades):
            x = screen_width - button_width - right_margin
            y = start_y + i * spacing

            rect = pygame.Rect(x, y, button_width, button_height)
            
            button = UpgradeButton(rect, config, scale)
            button.update_cost(game_data)

            self.buttons_upgrades.append(button)


        for button in self.buttons_upgrades:
            button.apply_enhancements(game_data)


        for i, config in enumerate(enhancements):
            purchase_key = config.get("purchase_key")

            if config["one_time"] and purchase_key and game_data["purchases"].get(purchase_key, False):
                continue
            
            x = screen_width - button_width - right_margin
            y = start_y2 + i * spacing

            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons_enhancements.append(UpgradeButton(rect, config, scale))


    def clicked(self, mouse_pos, game_data):

        for button in self.buttons_upgrades:
            if button.click(mouse_pos):

                if button.can_afford(game_data):
                    button.purchase(game_data)
                    button.update_cost(game_data)
                    return True, button.cost
                else:
                    error_sound.play()
                    return False, button.cost


        for buttonE in self.buttons_enhancements[:4]:
            if buttonE.click(mouse_pos):

                if buttonE.can_afford(game_data):
                    buttonE.purchase(game_data)

                    for upg in self.buttons_upgrades:
                        upg.apply_enhancements(game_data)

                    if buttonE.one_time:
                        self.buttons_enhancements.remove(buttonE)

                    return True, buttonE.cost
                else:
                    error_sound.play()
                    return False, buttonE.cost

        return False, 0
    
    
    def draw(self, screen, text_title, text_cost, desc, game_data):
        index = self.s(0)
        start_y = self.s(750)
        spacing = self.s(85)

        for button in self.buttons_upgrades:
            button.draw(screen, text_title, text_cost, game_data)

        for button in self.buttons_upgrades:
            button.draw_tooltip(screen, desc, game_data)


        for buttonE in self.buttons_enhancements[:4]:
            buttonE.rect.y = start_y + index * spacing
            index += 1
            buttonE.draw(screen, text_title, text_cost, game_data)

        for buttonE in self.buttons_enhancements[:4]:
            buttonE.draw_tooltip(screen, desc, game_data)
    

    def get_upgrade_icon(self, save_key):
        for b in self.buttons_upgrades:
            if b.save_key2 == save_key or b.save_key == save_key:
                return b.icon
        return None


    def get_upgrade_description(self, save_key):
        for b in self.buttons_upgrades:
            if b.save_key2 == save_key or b.save_key == save_key:
                return b.description
        return ""