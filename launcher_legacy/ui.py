import math
import system

black = color.rgb(0, 0, 0)
background = color.rgb(60, 15, 10)
phosphor = color.rgb(246, 135, 4)

def draw_background():
    screen.pen = color.rgb(0, 0, 0)
    screen.clear()

    if system.background_image:
        screen.alpha = 128
        screen.blit(system.background_image, vec2(0, 0))
        screen.alpha = 255

def draw_header():
    battery_level = badge.battery_level()

    if badge.is_charging():
        battery_display = (badge.ticks / 25) % 100
    else:
        battery_display = battery_level
    
    screen.pen = phosphor
    screen.text("Paperbark's Badge", 5, 2)

    pos = (137, 4)
    size = (16, 8)

    battery_percent_text = f"{battery_level}%"
    battery_percent_x, _ = screen.measure_text(battery_percent_text)
    screen.text(battery_percent_text, pos[0] - battery_percent_x - 2, pos[1] - 2)

    screen.pen = phosphor
    screen.shape(shape.rectangle(*pos, *size))
    screen.shape(shape.rectangle(pos[0] + size[0], pos[1] + 2, 1, 4))
    screen.pen = background
    screen.shape(shape.rectangle(pos[0] + 1, pos[1] + 1, size[0] - 2, size[1] - 2))

    width = math.ceil(((size[0] - 4) / 100) * battery_display)
    screen.pen = phosphor
    screen.shape(shape.rectangle(pos[0] + 2, pos[1] + 2, width, size[1] - 4))