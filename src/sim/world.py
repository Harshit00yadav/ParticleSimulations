from pygame import Surface
from pygame.draw import rect, line, circle
from pygame.math import Vector2
from pygame import mouse
from sim.objects.particle import Particle
from sim.objects.stick import connect
from random import randint
from math import dist, sqrt


class World:
    def __init__(self):
        self.toggles = {
                "mouse_interactions": False,
                "gravity": False,
                "cloth": False,
                "crystall": False,
                }
        self.forces = []
        self.no_of_particles = 620
        self.air_friction = 0.01
        self.interaction_radius = 9

        self.total_crystalls = 38
        self.crystal_size = 10
        self.crystall_no = 1
        self.crystall_wait_counter = 0
        self.crystall_wait_frames = 35
        
        self.cloth_width = 30
        self.cloth_height = 20
        self.x_fiber_length = 5
        self.y_fiber_length = 5
        self.cloth_offset_x = (self.cloth_width * self.x_fiber_length) / 2
        self.cloth_offset_y = 0

        self.size = (545, 350)
        self.surface = Surface(self.size)
        self.particles = [Particle(randint(5, self.size[0] - 5), randint(5, self.size[1] - 5)) for _ in range(self.no_of_particles)]
        self.constrains = []
        self.anchor_point = Vector2(self.size[0]/2, self.size[1]/6)
        self.anchor_indexies = [0, self.cloth_width//4, self.cloth_width*2//4, self.cloth_width*3//4, self.cloth_width]
        self.anchors = []
        self.inflate = True
        self.formation_complete = False

    def make_cloth(self, c_width, c_height, x_len=5, y_len=5):
        self.anchor_indexies.append(c_width)
        for i in range(c_width):
            for j in range(c_height):
                self.constrains.append([x_len, self.particles[i+(c_width+1)*j], self.particles[i+1+(c_width+1)*j], False])
        for i in range(c_width+1):
            for j in range(c_height-1):
                self.constrains.append([y_len, self.particles[i+(c_width+1)*j], self.particles[i+(c_width+1)*(j+1)], False])

    def make_crystall(self, no=0):
        size = self.crystal_size
        for a in range(no, no+1):
            for i in range(a*4, a*4+4):
                self.constrains.append([size, self.particles[i*4], self.particles[i*4+1], False])
                self.constrains.append([size, self.particles[i*4], self.particles[i*4+2], False])
                self.constrains.append([size, self.particles[i*4+1], self.particles[i*4+3], False])
                self.constrains.append([size, self.particles[i*4+2], self.particles[i*4+3], False])
                self.constrains.append([size*sqrt(2), self.particles[i*4], self.particles[i*4+3], False])
                self.constrains.append([size*sqrt(2), self.particles[i*4+1], self.particles[i*4+2], False])
                self.anchors.append(i*4+3)
            for j in range(a*4+0, a*4+4, 2):
                self.constrains.append([size, self.particles[j*4], self.particles[(j+1)*4], False])
                self.constrains.append([size, self.particles[j*4+1], self.particles[(j+1)*4+1], False])
                self.constrains.append([size*sqrt(2), self.particles[j*4+1], self.particles[(j+1)*4], False])
                self.constrains.append([size*sqrt(2), self.particles[j*4], self.particles[(j+1)*4+1], False])
                self.constrains.append([size*3, self.particles[j*4+3], self.particles[(j+1)*4+3], False])
                self.constrains.append([size*3, self.particles[j*4+2], self.particles[(j+1)*4+2], False])
            for k in range(a*4+0, a*4+2):
                self.constrains.append([size, self.particles[k*4], self.particles[(k+2)*4], False])
                self.constrains.append([size, self.particles[k*4+2], self.particles[(k+2)*4+2], False])
                self.constrains.append([size*sqrt(2), self.particles[k*4], self.particles[(k+2)*4+2], False])
                self.constrains.append([size*sqrt(2), self.particles[k*4+2], self.particles[(k+2)*4], False])
                self.constrains.append([size*3, self.particles[k*4+3], self.particles[(k+2)*4+3], False])
                self.constrains.append([size*3, self.particles[k*4+1], self.particles[(k+2)*4+1], False])

    def toggle_gravity(self):
        if self.forces != []:
            self.forces.clear()
        if self.toggles["gravity"]:
            self.forces.append(Vector2(0, 0.0598))

    def toggle_cloth(self):
        if self.toggles["cloth"] and self.constrains == []:
            self.make_cloth(self.cloth_width, self.cloth_height, x_len=self.x_fiber_length, y_len=self.y_fiber_length)
            self.anchors = self.anchor_indexies.copy()

    def toggle_crystall(self):
        if self.toggles["crystall"] and self.constrains == []:
            self.make_crystall()

    def toggle_mouse_interaction(self, p):
        if self.toggles["mouse_interactions"] and (self.mouse_position - p.position).magnitude() < self.interaction_radius:
            self.forces.append((p.position - self.mouse_position).normalize() * self.interaction_radius)

    def update(self):
        self.mouse_position = mouse.get_pos() - Vector2(55,0)
        for p in self.particles:
            self.toggle_gravity()
            self.toggle_cloth()
            self.toggle_crystall()
            self.toggle_mouse_interaction(p)
            p.update(air_friction=self.air_friction, forces=self.forces)
            if self.anchors != []:
                if self.toggles['cloth']:
                    for a in self.anchors:
                        if p == self.particles[a]:
                            p.position = self.anchor_point - (-self.cloth_offset_x + self.x_fiber_length * a, self.cloth_offset_y)
                            p.previous_position = self.anchor_point - (-self.cloth_offset_x + self.x_fiber_length * a, self.cloth_offset_y)
                elif self.toggles['crystall']:
                    if p == self.particles[self.anchors[0]]:
                        p.position = self.mouse_position - Vector2(self.crystal_size*0.5*3, self.crystal_size*0.5*3)
                        p.previous_position = self.mouse_position - Vector2(self.crystal_size*1.5*3, self.crystal_size*1.5*3)
                    elif p == self.particles[self.anchors[1]]:
                        p.position = self.mouse_position - Vector2(-self.crystal_size*0.5*3, self.crystal_size*0.5*3)
                        p.previous_position = self.mouse_position - Vector2(-self.crystal_size*1.5*3, self.crystal_size*1.5*3)
                    elif p == self.particles[self.anchors[2]]:
                        p.position = self.mouse_position - Vector2(self.crystal_size*0.5*3, -self.crystal_size*0.5*3)
                        p.previous_position = self.mouse_position - Vector2(self.crystal_size*1.5*3, -self.crystal_size*1.5*3)
                    elif p == self.particles[self.anchors[3]]:
                        p.position = self.mouse_position - Vector2(-self.crystal_size*0.5*3, -self.crystal_size*0.5*3)
                        p.previous_position = self.mouse_position - Vector2(-self.crystal_size*1.5*3, -self.crystal_size*1.5*3)

        # --------- UPDATE CONSTRAINS ----------
        if len(self.constrains) > 0 and not self.formation_complete:
            for c in self.constrains:
                if not c[3]:
                    break
            else:
                if self.toggles['crystall'] and self.crystall_wait_counter >= self.crystall_wait_frames:
                    if self.crystall_no < self.total_crystalls:
                        self.anchors.clear()
                        self.make_crystall(self.crystall_no)
                        self.crystall_no += 1
                    else:
                        self.formation_complete = True
                        self.crystall_no = 1
                        self.anchors.clear()
                        print('completed')
                    self.crystall_wait_counter = 0
                elif self.toggles['crystall']:
                    self.crystall_wait_counter += 1

        for _ in range(5):
            for c in self.constrains:
                c[3] = connect(c[0], c[1], c[2])
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

    def render(self, surface, font):
        self.surface.fill((15, 15, 15))
        if self.toggles["mouse_interactions"]:
            circle(self.surface, (255, 0, 0), self.mouse_position, self.interaction_radius, 1)
        rect(self.surface, (200, 200, 0), (0, 0, self.size[0], self.size[1]), 1)
        if self.constrains != []:
            for c in self.constrains:
                if c[3]:
                    line(self.surface, (255, 0, 0), c[1].position, c[2].position, 1)
                else:
                    c[1].render(self.surface)
                    c[2].render(self.surface)
                # text = font.render(f'{self.particles.index(c[1])}', True, (200, 0, 0))
                # self.surface.blit(text, c[1].position)
        if True:
            for p in self.particles:
                p.render(self.surface)
        surface.blit(self.surface, (55, 0))

