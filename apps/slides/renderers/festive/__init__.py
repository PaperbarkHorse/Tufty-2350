import menu
from renderer import Renderer
import math
import random

class FestiveRenderer(Renderer):

    def __init__(self):
        super().__init__()

        self.background = None
        self.paperbark = None
        self.overlay = None
        self.particles = []

    def on_load(self):
        self.background = image.load("/system/apps/slides/renderers/festive/background.png")
        self.paperbark = image.load("/system/apps/slides/renderers/festive/paperbark.png")
        self.overlay = image.load("/system/apps/slides/renderers/festive/overlay.png")
        self.particles = []

        for i in range(0, 60):
            self.particles.append(Particle(i))

    def on_unload(self):
        self.background = None
        self.paperbark = None
        self.overlay = None

    def render_to(self, target):
        target.alpha = 1

        now = badge.ticks / 1000
        delta = badge.ticks_delta / 1000

        for particle in self.particles:
            vx = 0
            vy = 0

            vx += math.sin(particle.y / 400 + now / 2) * 30
            vx += math.sin(particle.i + now * 2.5) * 30

            vy += 60 * particle.size + 40
            vy += math.sin(particle.i + now) * 20

            particle.x += vx * delta
            particle.y += vy * delta

            if particle.y > 240 + particle.margin:
                particle.y -= 240 + particle.margin * 2

            if particle.x > 320 + particle.margin:
                particle.x -= 320 + particle.margin * 2

            if particle.x < -particle.margin:
                particle.x += 320 + particle.margin * 2

        target.alpha = 255
        target.blit(self.background, vec2(0, 0))

        for particle in self.particles:
            if not particle.front:
                particle.render(target) 

        target.alpha = 255
        target.blit(self.paperbark, vec2(0, 0))

        for particle in self.particles:
            if particle.front:
                particle.render(target) 

        target.alpha = 255
        target.blit(self.overlay, vec2(0, 240 - 81))

class Particle():

    def __init__(self, i):
        self.margin = 10
        self.i = i
        self.x = random.random() * (320 + self.margin * 2) - self.margin
        self.y = random.random() * (240 + self.margin * 2) - self.margin
        self.size = random.random()
        self.size = self.size * self.size
        self.front = self.size > 0.7

    def render(self, target):
        radius = self.size * 3 + 2
        alpha = math.floor(clamp((self.size * 0.6 + 0.4), 0, 1) * 255) if not self.front else 255

        target.alpha = alpha
        target.pen = color.rgb(255, 255, 255)
        target.circle(self.x, self.y, radius)

def clamp(value, lower, upper):
    return min(max(value, lower), upper)