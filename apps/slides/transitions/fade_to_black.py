id = "fade_to_black"
name = "Fade to Black"

def render(t, prev, next):
    if t < 0.5:
        subdelta = t * 2
        if prev != None:
            screen.alpha = round((1 - subdelta) * 255)
            screen.blit(prev, vec2(0, 0))
            screen.alpha = 255
    else:
        subdelta = (t - 0.5) * 2

        screen.alpha = round(subdelta * 255)
        screen.blit(next, vec2(0, 0))
        screen.alpha = 255