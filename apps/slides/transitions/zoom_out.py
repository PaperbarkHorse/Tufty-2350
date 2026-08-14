id = "zoom_out"
name = "Zoom (Out)"

smooth = tween(0, 1, easing=tween.QUAD_IN)

def render(t, prev, next):
    t = smooth.at(t)

    screen.blit(next, vec2(0, 0))
    
    if prev != None:
        screen.blit(prev, rect(t * screen.width / 2, t * screen.height / 2, screen.width * (1 - t), screen.height * (1 - t)))