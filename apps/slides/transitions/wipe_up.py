id = "wipe_up"
name = "Wipe (Up)"

def render(t, prev, next):
    if prev != None:
        screen.blit(prev, vec2(0, 0))
    
    wipe_area = rect(0, (1 - t) * screen.height, screen.width, t * screen.height)
    screen.blit(next, wipe_area, wipe_area)
