id = "slide_down"
name = "Slide (Down)"

smooth = tween(0, 1, easing=tween.QUAD_INOUT)

def render(t, prev, next):
    t = smooth.at(t)
    
    if prev != None:
        screen.blit(prev, vec2(0, t * screen.height))
    
    screen.blit(next, vec2(0, (1 - t) * -screen.height))