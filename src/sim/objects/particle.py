from pygame.math import Vector2
from pygame.draw import circle
from random import randint


class Particle:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        temp_vector = Vector2(1,1)
        temp_vector.rotate_ip(randint(1, 360))
        self.previous_position = Vector2(x, y) + temp_vector
        self.color = (255, 0, 0)
        self.radius = 1
        self.terminal_velocity = 10

    def update(self, air_friction=0.0, forces=[]):
        v = (self.position - self.previous_position) * (1 - air_friction)
        if v.magnitude() > self.terminal_velocity:
            v.scale_to_length(self.terminal_velocity)
        self.previous_position.x, self.previous_position.y = self.position
        self.position += v
        for f in forces:
            self.position += f

    def render(self, surface):
        circle(surface, self.color, self.position, self.radius)
