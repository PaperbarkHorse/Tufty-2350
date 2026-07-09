id = "slide_down"
name = "Slide (Down)"

def render(t, prev, next):
    if prev != None:
        screen.blit(prev, vec2(0, t * screen.height))
    
    screen.blit(next, vec2(0, (1 - t) * -screen.height))