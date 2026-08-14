id = "wipe_left"
name = "Wipe (Left)"

smooth = tween(0, 1, easing=tween.QUAD_INOUT)

def render(t, prev, next):
    t = smooth.at(t)

    if prev != None:
        screen.blit(prev, vec2(0, 0))
    
    wipe_area = rect((1 - t) * screen.width, 0, t * screen.width, screen.height)
    screen.blit(next, wipe_area, wipe_area)