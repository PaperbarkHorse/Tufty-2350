id = "drop"
name = "Drop"

duration_multiplier = 1.5

smooth = tween(0, 1, easing=tween.BOUNCE_OUT)

def render(t, prev, next):
    t = smooth.at(t)
    
    if prev != None:
        screen.blit(prev, vec2(0, 0))
    
    screen.blit(next, vec2(0, (1 - t) * -screen.height))