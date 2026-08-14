id = "barn_door_open"
name = "Barn Door (Open)"

smooth = tween(0, 1, easing=tween.QUAD_IN)

def render(t, prev, next):
    t = smooth.at(t)

    screen.blit(next, vec2(0, 0))

    if prev != None:
        screen.blit(
            prev,
            rect(0, 0, screen.width / 2 + 1, screen.height),
            rect(-t * screen.width / 2, 0, screen.width / 2, screen.height),
        )
        screen.blit(
            prev,
            rect(screen.width / 2, 0, screen.width / 2 + 1, screen.height),
            rect((t * screen.width / 2) + screen.width / 2, 0, screen.width / 2, screen.height),
        )