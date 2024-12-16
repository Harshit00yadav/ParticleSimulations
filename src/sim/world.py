from pygame import Surface
from pygame.draw import rect, line, circle
from pygame.math import Vector2
from pygame import mouse
from sim.objects.particle import Particle
from sim.objects.stick import connect
from random import randint


class World:
    def __init__(self):
        self.toggles = {
                "mouse_interactions": False,
                "gravity": False,
                "cloth": False,
                }
        self.forces = []
        self.no_of_particles = 620
        self.air_friction = 0.0
        self.interaction_radius = 9
        self.cloth_width = 30
        self.cloth_height = 20
        self.x_fiber_length = 5
        self.y_fiber_length = 5
        self.cloth_offset_x = (self.cloth_width * self.x_fiber_length) / 2
        self.cloth_offset_y = 0
        self.size = (545, 350)
        self.surface = Surface(self.size)
        self.particles = [Particle(randint(0, self.size[0]), randint(0, self.size[1])) for _ in range(self.no_of_particles)]
        self.constrains = []
        self.anchor_point = Vector2(self.size[0]/2, self.size[1]/6)
        self.anchor_indexies = [0, self.cloth_width//2, self.cloth_width]
        self.anchors = []

    def make_cloth(self, c_width, c_height, x_len=5, y_len=5):
        self.anchor_indexies.append(c_width)
        for i in range(c_width):
            for j in range(c_height):
                self.constrains.append([x_len, self.particles[i+(c_width+1)*j], self.particles[i+1+(c_width+1)*j]])
        for i in range(c_width+1):
            for j in range(c_height-1):
                self.constrains.append([y_len, self.particles[i+(c_width+1)*j], self.particles[i+(c_width+1)*(j+1)]])

    def toggle_gravity(self):
        if self.forces != []:
            self.forces.clear()
        if self.toggles["gravity"]:
            self.forces.append(Vector2(0, 0.1))

    def toggle_cloth(self, p):
        if self.toggles["cloth"] and self.constrains == []:
            self.make_cloth(self.cloth_width, self.cloth_height, x_len=self.x_fiber_length, y_len=self.y_fiber_length)
            self.anchors = self.anchor_indexies.copy()
        elif not self.toggles["cloth"] and self.constrains != []:
            self.constrains.clear()
            self.anchors.clear()
 
        if self.anchors != []:
            for a in self.anchors:
                if p == self.particles[a]:
                    self.forces.append(self.anchor_point - (-self.cloth_offset_x + self.x_fiber_length * a, self.cloth_offset_y) - p.position)
    
    def toggle_mouse_interaction(self, p):
        if self.toggles["mouse_interactions"] and (self.mouse_position - p.position).magnitude() < self.interaction_radius:
            self.forces.append((p.position - self.mouse_position).normalize() * self.interaction_radius)

    def update(self):
        self.mouse_position = mouse.get_pos() - Vector2(55,0)
        for p in self.particles:
            self.toggle_gravity()
            self.toggle_cloth(p)
            self.toggle_mouse_interaction(p)
            p.update(air_friction=self.air_friction, forces=self.forces)

        # --------- UPDATE CONSTRAINS ----------
        for c in self.constrains:
            connect(c[0], c[1], c[2])
        # ---------------------------------------
        self.keep_particles_inside_frame()

    def keep_particles_inside_frame(self):
        for p in self.particles:
            if p.position.x < 3 or p.position.x > self.size[0] - 3:
                tempx = p.position.x
                p.position.x = p.previous_position.x
                p.previous_position.x = tempx
            if p.position.y < 3 or p.position.y > self.size[1] - 3:
                tempy = p.position.y
                p.position.y = p.previous_position.y
                p.previous_position.y = tempy

    def render(self, surface):
        self.surface.fill((15, 15, 15))
        if self.toggles["mouse_interactions"]:
            circle(self.surface, (255, 0, 0), self.mouse_position, self.interaction_radius, 1)
        rect(self.surface, (200, 200, 0), (0, 0, self.size[0], self.size[1]), 1)
        for c in self.constrains:
            line(self.surface, (255, 0, 0), c[1].position, c[2].position, 1)
        for p in self.particles:
            p.render(self.surface)
        surface.blit(self.surface, (55, 0))

