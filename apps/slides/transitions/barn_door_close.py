id = "barn_door_close"
name = "Barn Door (Close)"

def render(t, prev, next):
    if prev != None:
        screen.blit(prev, vec2(0, 0))

    screen.blit(
        next,
        rect(0, 0, screen.width / 2 + 1, screen.height),
        rect(-(1 - t) * screen.width / 2, 0, screen.width / 2, screen.height),
    )
    screen.blit(
        next,
        rect(screen.width / 2, 0, screen.width / 2 + 1, screen.height),
        rect(((1 - t) * screen.width / 2) + screen.width / 2, 0, screen.width / 2, screen.height),
    )