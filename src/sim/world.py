from pygame import Surface
from pygame.draw import rect, line
from pygame.math import Vector2
from sim.objects.particle import Particle
from sim.objects.stick import connect
from random import randint


class World:
    def __init__(self):
        self.toggles = {
                "gravity": False,
                "cloth": False,
                }
        self.forces = []
        self.no_of_particles = 500
        self.size = (545, 350)
        self.surface = Surface(self.size)
        self.particles = [Particle(randint(0, self.size[0]), randint(0, self.size[1])) for _ in range(self.no_of_particles)]
        self.constrains = []
        self.anchor_point = Vector2(self.size[0]/2, self.size[1]/2)

    def make_cloth(self, c_width, c_height):
        # ----------- cloth -------------------
        for i in range(c_width):
            for j in range(c_height):
                self.constrains.append([10, self.particles[i+(c_width+1)*j], self.particles[i+1+(c_width+1)*j]])
                self.constrains.append([10, self.particles[i+(c_width+1)*j], self.particles[i+(c_width+1)+1+(c_width+1)*j]])

    def update(self):
        for p in self.particles:
            self.forces.clear()
            if self.toggles["gravity"]:
                self.forces.append(Vector2(0, 0.1))

            if self.toggles["cloth"] and self.constrains == []:
                self.make_cloth(10, 10)
            elif not self.toggles["cloth"]:
                self.constrains.clear()

            if self.constrains != [] and self.particles[0] == p:
                self.forces.append(self.anchor_point - (50, 0) - p.position)
            elif self.constrains !=[] and self.particles[10] == p:
                self.forces.append(self.anchor_point - (-50, 0) - p.position)
                
            p.update(air_friction=0, forces=self.forces)
        for c in self.constrains:
            connect(c[0], c[1], c[2])
        for p in self.particles:
            if p.position.x < 3 or p.position.x > self.size[0] - 3:
                p.previous_position.x = 2 * p.position.x - p.previous_position.x
            if p.position.y < 3 or p.position.y > self.size[1] - 3:
                p.previous_position.y = 2 * p.position.y - p.previous_position.y

    def render(self, surface):
        self.surface.fill((15, 15, 15))
        rect(self.surface, (200, 200, 0), (0, 0, self.size[0], self.size[1]), 1)
        for c in self.constrains:
            line(self.surface, (255, 0, 0), c[1].position, c[2].position, 1)
        for p in self.particles:
            p.render(self.surface)
        surface.blit(self.surface, (55, 0))

