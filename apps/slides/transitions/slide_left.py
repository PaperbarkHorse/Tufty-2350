id = "slide_left"
name = "Slide (Left)"

smooth = tween(0, 1, easing=tween.QUAD_INOUT)

def render(t, prev, next):
    t = smooth.at(t)

    if prev != None:
        screen.blit(prev, vec2(t * -screen.width, 0))
    
    screen.blit(next, vec2((1 - t) * screen.width, 0))