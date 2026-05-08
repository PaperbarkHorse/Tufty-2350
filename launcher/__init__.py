import os
import sys

import ui
from app import Apps

screen.font = rom_font.ark


# find installed apps and create apps
apps = Apps("/system/apps")
app_to_launch = None

active = 0

badge.poll()

def input():
    global active, apps, app_to_launch
    
    # process button inputs to switch between apps
    if badge.pressed(BUTTON_C):
        if (active % 3) < 2 and active < len(apps) - 1:
            active += 1
    if badge.pressed(BUTTON_A):
        if (active % 3) > 0 and active > 0:
            active -= 1
    if badge.pressed(BUTTON_UP) and active >= 3:
        active -= 3
    if badge.pressed(BUTTON_DOWN):
        active += 3
        if active >= len(apps):
            active = len(apps) - 1

    if badge.pressed(BUTTON_B):
        app_to_launch = f"/system/apps/{apps.active.path}"

def update():
    global active, apps

    apps.activate(active)

    if app_to_launch:
        return app_to_launch

    ui.draw_background()
    ui.draw_header()

    # draw menu apps
    apps.draw_icons()

    # draw label for active menu icon
    apps.draw_label()

    # draw hints for the active page
    apps.draw_pagination()

    return None
