id = "fade"
name = "Fade"

def render(t, prev, next):
    if prev != None:
        screen.blit(prev, vec2(0, 0))

    screen.alpha = round(t * 255)
    screen.blit(next, vec2(0, 0))
    screen.alpha = 255