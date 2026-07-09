id = "flip_horizontal"
name = "Flip (Horizontal)"

def render(t, prev, next):
    if t < 0.5:
        subdelta = t * 2

        if prev != None:
            screen.blit(prev, rect(subdelta * screen.width / 2, 0, screen.width * (1 - subdelta), screen.height))
    else:
        subdelta = (t - 0.5) * 2

        screen.blit(next, rect((1 - subdelta) * screen.width / 2, 0, screen.width * subdelta, screen.height))