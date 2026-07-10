import math

id = "unshatter"
name = "Unshatter"

duration_multiplier = 1.5

def render(t, prev, next):
    t = 1 - t

    x_parts = 8
    y_parts = 6
    part_width = screen.width / x_parts
    part_height = screen.height / y_parts

    if prev != None:
        screen.blit(prev, vec2(0, 0))

    for i in range(0, x_parts):
        for j in range(0, y_parts):
            n = i + j * x_parts
            x = i * part_width
            y = j * part_height

            random_offset_x = math.cos(n) * (screen.width + part_width) * t * t
            random_offset_y = math.sin(n) * (screen.height + part_height) * t * t

            screen.blit(next, rect(x, y, part_width, part_height), rect(x + random_offset_x, y + random_offset_y, part_width, part_height))

        