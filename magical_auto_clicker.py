import pygame
import math
import random
from floating_text import FloatingText

class MagicalAutoClicker:
    def __init__(self, pos, image):
        self.pos = pygame.Vector2(pos)
        self.start_pos = pygame.Vector2(pos)
        self.original_image = image
        self.image = image
        self.target = None
        self.click_cooldown = 0
        self.angle = 0
        self.last_duck_sound_time = 0 

    def choose_target(self, ducks):
        if ducks:
            self.target = random.choice(ducks)
        else:
            self.target = None

    def update(self, ducks, duck_click_sound, speed, game_data, floating_texts):

        if self.target not in ducks:
            self.choose_target(ducks)

        if self.target:
            target_pos = pygame.Vector2(self.target.rect.center)
            direction = target_pos - self.pos
            distance = direction.length()

            if distance != 0:
                direction = direction.normalize()

                self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
                self.image = pygame.transform.rotate(self.original_image, self.angle)

            self.pos += direction * speed

            if distance < 10:
                game_data["ducks"] += game_data["ducksPerClick"]
                ducks.remove(self.target)
                current_time_now = pygame.time.get_ticks()
                if current_time_now - self.last_duck_sound_time > 1000:
                    duck_click_sound.play()
                    self.last_duck_sound_time = current_time_now
                floating_texts.append(
                    FloatingText(f"+{game_data['ducksPerClick']}", self.target.rect.center)
                )
                self.target = None

        else:
            direction = self.start_pos - self.pos
            distance = direction.length()

            if distance > speed:
                direction = direction.normalize()

                self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
                self.image = pygame.transform.rotate(self.original_image, self.angle)

                self.pos += direction * speed

            else:
                self.pos = self.start_pos.copy()
                self.angle = 0
                self.image = self.original_image

    def draw(self, screen):
        rect = self.image.get_rect(center=self.pos)
        screen.blit(self.image, rect)