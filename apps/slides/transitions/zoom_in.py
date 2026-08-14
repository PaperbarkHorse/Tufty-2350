id = "zoom_in"
name = "Zoom (In)"

smooth = tween(0, 1, easing=tween.QUAD_OUT)

def render(t, prev, next):
    t = smooth.at(t)

    if prev != None:
        screen.blit(prev, vec2(0, 0))

    screen.blit(next, rect((1 - t) * screen.width / 2, (1 - t) * screen.height / 2, screen.width * t, screen.height * t))