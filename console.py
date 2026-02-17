import pygame
import json

class Console:
    def __init__(self, screen_width, screen_height, scale):
        self.active = False
        self.input_text = ""
        self.history = []
        self.scale = scale

        self.rect = pygame.Rect(
            0,
            0,
            screen_width,
            int(screen_height * 0.35)
        )

        with open("data/console_commands.json", "r") as f:
            self.commands = json.load(f)

    def toggle(self):
        self.active = not self.active
        self.input_text = ""

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
        if not self.input_text.startswith("/"):
            self.history.append("Commands must start with '/'.")
            return


        parts = self.input_text[1:].split()

        if not parts:
            return

        command = parts[0].lower()
        value = None
        if len(parts) > 1:
            try:
                value = float(parts[1])
            except ValueError:
                self.history.append("Invalid number.")
                return

        if command not in self.commands:
            self.history.append("Unknown command.")
            return

        cmd = self.commands[command]

        if cmd["type"] in ["add", "set"]:
            target = cmd["target"]

            if target not in game_data:
                self.history.append("Invalid target.")
                return

            if value is None:
                self.history.append("Missing value.")
                return

            if cmd["type"] == "add":
                game_data[target] += value
                self.history.append(f"Added {value} to {target}.")
            else:
                game_data[target] = value
                self.history.append(f"Set {target} to {value}.")


        elif cmd["type"] == "simulate":
            if value is not None:
                seconds = int(value)
                game_data["ducks"] += get_current_dps() * seconds
                game_data["playtime"] += seconds
                self.history.append(f"Simulated {seconds}s.")

        elif cmd["type"] == "speed":
            if value is not None:
                game_data["globalGameSpeed"] = value
                self.history.append(f"Game speed set to {value}.")

    def draw(self, screen, font):
        if not self.active:
            return

        overlay = pygame.Surface(self.rect.size)
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))

        screen.blit(overlay, self.rect.topleft)

        y = 10

        for line in self.history[-8:]:
            text = font.render(line, True, (0, 255, 0))
            screen.blit(text, (10, y))
            y += font.get_height()

        input_surface = font.render("> " + self.input_text, True, (255, 255, 255))
        screen.blit(input_surface, (10, self.rect.height - 40))
