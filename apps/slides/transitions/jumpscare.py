import math

id = "jumpscare"
name = "Jumpscare"

duration_multiplier = 1.6

jumpscare = image.load("/system/apps/slides/assets/jumpscare.png").spritesheet(3, 3)

def render(t, prev, next):
    t1 = min(t / 0.6, 1)

    if prev != None:
        screen.blit(prev, vec2(0, 0))

    screen.alpha = round(min(t1 * 2, 1) * 255)
    screen.blit(jumpscare.sprite(math.ceil(t1 * 9)), rect(screen.width * -0.1, screen.height * -0.1, screen.width * 1.2, screen.height * 1.2))
    screen.alpha = 255

    if t >= 0.6:
        subdelta = (t - 0.6) / 0.4
        
        screen.alpha = round(subdelta * 255)
        screen.blit(next, vec2(0, 0))
        screen.alpha = 255