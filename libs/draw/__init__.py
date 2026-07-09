def clear(r=0, g=0, b=0, target=None):
    if not target:
        target = screen

    screen.pen = color.rgb(r, g, b)
    screen.clear()

def center_text(text, x, y, target=None):
    if not target:
        target = screen

    width, _ = target.measure_text(text)
    target.text(text, x - width / 2, y)