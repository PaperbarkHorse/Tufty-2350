import math

id = "shatter"
name = "Shatter"

duration_multiplier = 1.5

def render(t, prev, next):
    x_parts = 8
    y_parts = 6
    part_width = screen.width / x_parts
    part_height = screen.height / y_parts

    screen.blit(next, vec2(0, 0))

    if prev != None:
        gravity_offset_y = t * t * (screen.height + 40)

        for i in range(0, x_parts):
            for j in range(0, y_parts):
                n = i + j * x_parts
                x = i * part_width
                y = j * part_height

                random_offset_x = math.cos(n) * 40 * t
                random_offset_y = math.sin(n) * 40 * t

                screen.blit(prev, rect(x, y, part_width, part_height), rect(x + random_offset_x, y + random_offset_y + gravity_offset_y, part_width, part_height))

        