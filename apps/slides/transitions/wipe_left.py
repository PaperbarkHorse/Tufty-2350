id = "wipe_left"
name = "Wipe (Left)"

def render(t, prev, next):
    if prev != None:
        screen.blit(prev, vec2(0, 0))
    
    wipe_area = rect((1 - t) * screen.width, 0, t * screen.width, screen.height)
    screen.blit(next, wipe_area, wipe_area)