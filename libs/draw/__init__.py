def clear(r=0, g=0, b=0, target=None):
    if not target:
        target = screen

    target.pen = color.rgb(r, g, b)
    target.clear()

def center_text(text, x, y, target=None):
    if not target:
        target = screen

    width, _ = target.measure_text(text)
    target.text(text, x - width / 2, y)

def center_text_sized(text, x, y, size, target=None):
    if not target:
        target = screen

    width, _ = target.measure_text(text, size)
    target.text(text, x - width / 2, y, size)