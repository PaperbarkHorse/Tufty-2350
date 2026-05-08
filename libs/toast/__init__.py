import math

TOP = 1
BOTTOM = 2
CENTER = 3

SHORT = 1250
LONG = 4000

toast_text = ""
toast_lifetime = 0
toast_position = TOP

def show(text, duration=SHORT, position=TOP):
    global toast_text, toast_lifetime, toast_position
    toast_text = text
    toast_lifetime = duration
    toast_position = position

def clear():
    global toast_lifetime
    toast_lifetime = 0

def update():
    global toast_lifetime

    if toast_lifetime > 0:
        toast_lifetime -= badge.ticks_delta
        render()

def render():
    if screen.width == 320:
        screen.font = rom_font.ignore
    else:
        screen.font = rom_font.sins

    width, height = screen.measure_text(toast_text)
    height += 1
    x = math.floor((screen.width - width) / 2)

    if toast_position == TOP:
        y = 5
    elif toast_position == BOTTOM:
        y = screen.height - height - 5
    elif toast_position == CENTER:
        y = math.floor((screen.height - height) / 2)

    alpha = max(0, min(1, toast_lifetime / 333))

    screen.pen = color.rgb(0, 0, 0, math.floor(alpha * 192))

    screen.rectangle(x - 5, y - 1, 1, height + 2)
    screen.rectangle(x - 4, y - 2, width + 8, height + 4)
    screen.rectangle(x + width + 4, y - 1, 1, height + 2)

    screen.pen = color.rgb(255, 255, 255, math.floor(alpha * 255))
    screen.text(toast_text, x, y)