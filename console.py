import pygame
import json

class Console:
    def __init__(self, screen_width, screen_height, scale, quit_callback, save_callback, reset_callback):
        self.active = False
        self.input_text = ""
        self.history = []
        self.scale = scale
        self.quit_callback = quit_callback
        self.save_callback = save_callback
        self.reset_callback = reset_callback
        self.font = pygame.font.Font(None, 20)
        self.first_time = True

        self.rect = pygame.Rect(
            0,
            0,
            screen_width,
            int(screen_height * 0.35)
        )

        self.max_history = 200

        with open("data/console_commands.json", "r") as f:
            self.commands = json.load(f)

    def toggle(self):
        self.active = not self.active
        self.input_text = ""

        if self.active == True and self.first_time == True:
            self.add_line("F9 to close, help for basic commands.", self.font)
            self.first_time = False

    def wrap_text(self, text, font, max_width):
        lines = []
        current_line = ""

        for char in text:
            test_line = current_line + char
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char

        if current_line:
            lines.append(current_line)

        return lines

    def handle_event(self, event, game_data, get_current_dps):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                self.execute_command(game_data, get_current_dps)
                self.input_text = ""

            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]

            else:
                if event.unicode.isprintable():
                    self.input_text += event.unicode

    def execute_command(self, game_data, get_current_dps):

        parts = self.input_text.split()

        if not parts:
            return

        command = parts[0].lower()
        value = None

        if len(parts) > 1:
            try:
                value = float(parts[1])
            except ValueError:
                self.add_line("Invalid number.", self.font)
                return

        if command not in self.commands:
            self.add_line("Unknown command.", self.font)
            return

        cmd = self.commands[command]

        if cmd["type"] in ["add", "set"]:
            target = cmd["target"]

            if target not in game_data:
                self.add_line("Invalid target.", self.font)
                return

            if value is None:
                self.add_line("Missing value.", self.font)
                return

            if cmd["type"] == "add":
                game_data[target] += value
                self.add_line(f"Added {value} to {target}.", self.font)
            else:
                game_data[target] = value
                self.add_line(f"Set {target} to {value}.", self.font)

        elif cmd["type"] == "simulate":

            if value is None:
                self.add_line("Missing value.", self.font)
                self.add_line("Usage: simulate <seconds>; Assumes dpc every 5 seconds.", self.font)
                return

            seconds = int(value)

            if seconds <= 0:
                self.add_line("Seconds must be positive.", self.font)
                return

            dps = get_current_dps()
            global_speed = game_data.get("globalGameSpeed", 1)

            base_dpc = game_data["ducksPerClick"] * game_data["multiplierDPC"]

            crit_chance = game_data.get("criticalChance", 0)
            crit_power = game_data.get("criticalPower", 1)

            total_added = 0

            for sec in range(1, seconds + 1):

                dps_gain = dps * global_speed
                game_data["ducks"] += dps_gain
                total_added += dps_gain

                if sec % 5 == 0:

                    dpc = base_dpc

                    if crit_chance > 0:
                        import random
                        if random.random() < crit_chance:
                            dpc *= crit_power

                    dpc *= global_speed

                    game_data["ducks"] += dpc
                    total_added += dpc

            game_data["playtime"] += seconds

            self.add_line(
                f"Simulated {seconds}s and gained {int(total_added):,} ducks.",
                self.font
            )


        elif cmd["type"] == "speed":
            if value is not None:
                game_data["globalGameSpeed"] = value
                self.add_line(f"Game speed set to {value}.", self.font)

        elif cmd["type"] == "quit":
            self.quit_callback()
            self.add_line("Game quitting...", self.font)

        elif cmd["type"] == "save":
            self.save_callback(game_data)
            self.add_line("Game saved.", self.font)

        elif cmd["type"] == "reset":
            self.reset_callback()
            self.add_line("Game values reset to default.", self.font)

        elif cmd["type"] == "stats":
            formatted = json.dumps(game_data)
            for line in formatted.split("\n"):
                self.add_line(line, self.font)

        elif cmd["type"] == "help":
            self.add_line("close - close console", self.font)
            self.add_line("quit - quit game", self.font)
            self.add_line("save - save game", self.font)
            self.add_line("reset - reset all game values", self.font)
            self.add_line("stats - display current stats", self.font)
            self.add_line("*More commands in commands.txt*", self.font)

        elif cmd["type"] == "close":
            self.toggle()

        elif cmd["type"] == "timeto":

            if value is None:
                self.add_line("Missing value.", self.font)
                self.add_line("Usage: timeto <duck amount>; Assumes dpc every 5 seconds.", self.font)
                return

            target = int(value)
            current = game_data["ducks"]

            if target <= current:
                self.add_line("You already have that many ducks.", self.font)
                return

            dps = get_current_dps()

            base_dpc = game_data["ducksPerClick"] * game_data["multiplierDPC"]
            if game_data.get("criticalChance", 0) > 0:
                crit_chance = game_data["criticalChance"]
                crit_power = game_data["criticalPower"]
                avg_multiplier = (1 - crit_chance) + (crit_chance * crit_power)
                base_dpc *= avg_multiplier

            base_dpc = int(base_dpc)

            simulated_ducks = current
            seconds = 0

            if dps <= 0 and base_dpc <= 0:
                self.add_line("No duck production detected.", self.font)
                return

            while simulated_ducks < target:
                seconds += 1
                simulated_ducks += dps

                if seconds % 5 == 0:
                    simulated_ducks += base_dpc

                if seconds > 10_000_000:
                    break

            minutes = seconds // 60
            remaining_seconds = seconds % 60

            if minutes > 0:
                self.add_line(
                    f"Time to {target:,} ducks: {minutes}m {remaining_seconds}s",
                    self.font
                )
            else:
                self.add_line(
                    f"Time to {target:,} ducks: {seconds}s",
                    self.font
                )


    def add_line(self, text, font):
        max_width = self.rect.width - 20
        wrapped = self.wrap_text(text, font, max_width)

        for line in wrapped:
            self.history.append(line)

        self.history = self.history[-self.max_history:]


    def draw(self, screen, font):
        if not self.active:
            return

        overlay = pygame.Surface(self.rect.size)
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))

        screen.blit(overlay, self.rect.topleft)

        y = 10

        visible_lines = self.history[-14:]

        for line in visible_lines:
            text = font.render(line, True, (0, 255, 0))
            screen.blit(text, (10, y))
            y += font.get_height()

        input_surface = font.render("> " + self.input_text, True, (255, 255, 255))
        screen.blit(input_surface, (10, self.rect.height - 40))
