import random
import pygame
import math

class Duck:
    def __init__(self, rect, image, shiny = False):
        self.rect = rect
        self.image = image
        self.shiny = shiny
        self.t = random.uniform(0, math.pi * 2)

    def update(self):
        self.t += 0.04

    def draw(self, screen):
        angle = math.sin(self.t) * 10

        rotatedDuck = pygame.transform.rotate(self.image, angle)
        rotatedRect = rotatedDuck.get_rect(center=self.rect.center)

        screen.blit(rotatedDuck, rotatedRect)