id = "slide_left"
name = "Slide (Left)"

def render(t, prev, next):
    if prev != None:
        screen.blit(prev, vec2(t * -screen.width, 0))
    
    screen.blit(next, vec2((1 - t) * screen.width, 0))