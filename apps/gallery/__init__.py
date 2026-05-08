import os
import sys
import math
from badgeware import State

import toast

sys.path.insert(0, "/system/apps/gallery")
os.chdir("/system/apps/gallery")

APP_ID = "quasar.gallery"

badge.mode(HIRES)

state = {
    "recent_image_path": None,
}

image_paths = []

current_index = 0
current_image = None

should_render = True

def init():
    global image_paths, state, current_index

    State.load(APP_ID, state)

    image_paths = list(filter(lambda path: path.lower().endswith(".png"), os.listdir("images")))
    image_paths.sort()

    if len(image_paths) > 0:
        try:
            index = image_paths.index(state["recent_image_path"])
            current_index = index
            change_image(image_paths[index])
        except ValueError:
            change_image(image_paths[0])

def input():
    if badge.pressed(BUTTON_A) or badge.pressed(BUTTON_UP):
        prev_image()

    if badge.pressed(BUTTON_C) or badge.pressed(BUTTON_DOWN):
        next_image()

def update():
    screen.font = rom_font.ignore

    screen.pen = color.rgb(0, 0, 0)
    screen.clear()

    if current_image == None:
        screen.pen = color.rgb(0, 0, 0)
        screen.clear()

        screen.pen = color.rgb(255, 255, 255)
        screen.text("No images available", 10, 10)

        return
    
    x = math.floor((screen.width - current_image.width) / 2)
    y = math.floor((screen.height - current_image.height) / 2)

    screen.blit(current_image, vec2(x, y))

def on_exit():
    pass

def change_image(image_path):
    global current_image, state, should_render
    current_image = image.load(f"images/{image_path}")

    state["recent_image_path"] = image_path
    State.save(APP_ID, state)

    should_render = True

def next_image():
    global current_index, image_paths

    if len(image_paths) == 0:
        return

    current_index += 1

    if current_index >= len(image_paths):
        current_index = 0

    change_image(image_paths[current_index])
    toast_current_image()

def prev_image():
    global current_index, image_paths

    if len(image_paths) == 0:
        return

    current_index -= 1

    if current_index < 0:
        current_index = len(image_paths) - 1

    change_image(image_paths[current_index])
    toast_current_image()


def toast_current_image():
    toast.show(
        f"{image_paths[current_index][:-4]}",
        duration=toast.SHORT,
        position=toast.BOTTOM
    )
