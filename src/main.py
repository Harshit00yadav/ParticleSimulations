import pygame
from sim.world import World

class App:
    def __init__(self):
        self.exit = False
        self.resolution = (600, 350)
        self.display = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self._initialization_()

    def _initialization_(self):
        self.world = World()

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    quit()
                elif event.key == pygame.K_g:
                    self.world.toggles["gravity"] = not self.world.toggles["gravity"]
                elif event.key == pygame.K_c:
                    self.world.toggles["cloth"] = not self.world.toggles["cloth"]

    def update(self):
        self.world.update()

    def render(self):
        self.display.fill((0, 0, 0))
        self.world.render(self.display)

    def run(self):
        while not self.exit:
            self.update()
            self.eventHandler()
            self.render()
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    demo = App()
    demo.run()
