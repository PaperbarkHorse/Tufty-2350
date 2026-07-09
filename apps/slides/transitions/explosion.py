import math

id = "explosion"
name = "Explosion"

explosion = SpriteSheet("/system/apps/slides/assets/explosion.png", 16, 1).animation()

def render(t, prev, next):
    if t < 0.2:
        if prev != None:
            screen.blit(prev, vec2(0, 0))
    else:
        screen.blit(next, vec2(0, 0))

    screen.blit(explosion.frame(math.floor(t * 16)), rect(0, -screen.height * 0.1, screen.width, screen.height * 1.3))