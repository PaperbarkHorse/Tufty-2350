id = "wipe_right"
name = "Wipe (Right)"

def render(t, prev, next):
    if prev != None:
        screen.blit(prev, vec2(0, 0))
    
    wipe_area = rect(0, 0, t * screen.width, screen.height)
    screen.blit(next, wipe_area, wipe_area)