import os
import json
import math
import system
from badgeware.filesystem import is_dir, file_exists

apps = []
selected_index = 0
launch_app = None

scroll_animation_offset = 0

battery_level = 0
next_battery_check = 0

def init():
    load_apps()

def input():
    global selected_index, launch_app

    if badge.pressed(BUTTON_UP):
        selected_index -= 1
        
        if selected_index < 0:
            selected_index = len(apps) - 1

    if badge.pressed(BUTTON_DOWN):
        selected_index += 1

        if selected_index >= len(apps):
            selected_index = 0

    if badge.pressed(BUTTON_B):
        launch_app = apps[selected_index]["path"]

def update():
    global launch_app

    if launch_app != None:
        return launch_app

    screen.pen = color.rgb(0, 0, 0)
    screen.clear()

    if system.background_image:
        screen.blit(system.background_image, vec2(0, 0))

    render_apps()
    render_header()

def render_apps():
    global apps, selected_index, scroll_animation_offset

    line_height = 28

    scroll_animation_target = (line_height * selected_index)
    scroll_animation_offset += (scroll_animation_target - scroll_animation_offset) * 10 * (badge.ticks_delta / 1000)

    scroll_offset = round((screen.height - line_height) / 2 - scroll_animation_offset)

    for i, app in enumerate(apps):
        line_y = (i * line_height) + scroll_offset

        if line_y < -line_height or line_y > screen.height:
            continue
    
        if i == selected_index:
            screen.alpha = 255
            screen.pen = color.rgb(20, 40, 80, 200)
        else:
            screen.alpha = 128
            screen.pen = color.rgb(20, 20, 20, 200)

        screen.rectangle(0, line_y, screen.width, line_height)

        if app["icon"] != None:
            screen.blit(app["icon"], vec2(2, line_y + 2))
        else:
            screen.pen = color.rgb(128, 128, 128)
            screen.rectangle(2, line_y + 2, 24, 24)

        screen.pen = color.rgb(255, 255, 255)
        screen.text(app["metadata"]["name"], 30, line_y + 3)
        screen.pen = color.rgb(160, 160, 160)
        screen.text(f"v{app["metadata"]["version"]}", 30, line_y + 12)

        screen.alpha = 255

def render_header():
    global battery_level, next_battery_check

    if badge.ticks >= next_battery_check:
        battery_level = badge.battery_level()
        next_battery_check = badge.ticks + (1000 * 30)

    if badge.is_charging():
        battery_display = (badge.ticks / 25) % 100
    else:
        battery_display = battery_level

    if system.background_image:
        screen.blit(system.background_image, rect(0, 0, screen.width, 13), rect(0, 0, screen.width, 13))

    screen.pen = color.rgb(20, 20, 20, 180)
    screen.rectangle(0, 0, screen.width, 13)

    screen.pen = color.rgb(255, 255, 255)
    screen.text("Paperbark's Badge", 2, 0)

    pos = (screen.width - 20, 2)
    size = (16, 8)

    battery_percent_text = f"{battery_level}%"
    battery_percent_x, _ = screen.measure_text(battery_percent_text)
    screen.text(battery_percent_text, pos[0] - battery_percent_x - 2, pos[1] - 2)

    screen.pen = color.rgb(255, 255, 255)
    screen.shape(shape.rectangle(*pos, *size))
    screen.shape(shape.rectangle(pos[0] + size[0], pos[1] + 2, 1, 4))
    screen.pen = color.rgb(0, 0, 0)
    screen.shape(shape.rectangle(pos[0] + 1, pos[1] + 1, size[0] - 2, size[1] - 2))

    width = math.ceil(((size[0] - 4) / 100) * battery_display)
    screen.pen = color.rgb(255, 255, 255)
    screen.shape(shape.rectangle(pos[0] + 2, pos[1] + 2, width, size[1] - 4))

    screen.rectangle(0, 13, screen.width, 1)

def load_apps():
    global apps
    apps.clear()

    apps_root = "/system/apps"

    for app_path in sorted(os.listdir(apps_root)):
        app_path = f"{apps_root}/{app_path}"

        if not is_dir(app_path):
            continue

        if not file_exists(f"{app_path}/app.json"):
            continue

        app_metadata = None
        app_icon = None

        with open(f"{app_path}/app.json", "r") as metadata_file:
            app_metadata = json.load(metadata_file)

        if file_exists(f"{app_path}/icon.png"):
            app_icon = image.load(f"{app_path}/icon.png")

        apps.append({
            "path": app_path,
            "metadata": app_metadata,
            "icon": app_icon,
        })