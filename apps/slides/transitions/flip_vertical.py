id = "flip_vertical"
name = "Flip (Vertical)"

def render(t, prev, next):
    if t < 0.5:
        subdelta = t * 2

        if prev != None:
            screen.blit(prev, rect(0, subdelta * screen.height / 2, screen.width, screen.height * (1 - subdelta)))
    else:
        subdelta = (t - 0.5) * 2

        screen.blit(next, rect(0, (1 - subdelta) * screen.height / 2, screen.width, screen.height * subdelta))