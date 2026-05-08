import os
import sys
import math
import random

import toast

from scenes import scenes
from characters import characters

sys.path.insert(0, "/system/apps/dance")
os.chdir("/system/apps/dance")

current_scene_index = 0
current_scene = None

current_character_index = 0
current_character = None

current_animation = None
current_animation_index = 0
current_animation_sprites = None
animation_start_time = badge.ticks

auto_cycle = False
auto_cycle_timer = 0

ms_per_frame = 1000 / 30

screen.antialias = image.X2

def init():
    load_scene(scenes[current_scene_index])
    load_character(characters[current_character_index])
    load_animation(current_character.animations[current_animation_index])

def input():
    if badge.pressed(BUTTON_A):
        set_auto_cycle(not auto_cycle)

        if auto_cycle:
            toast.show("Auto Cycle: ON", duration=toast.SHORT, position=toast.TOP)
        else:
            toast.show("Auto Cycle: OFF", duration=toast.SHORT, position=toast.TOP)

    if badge.pressed(BUTTON_B):
        cycle_character()
    
    if badge.pressed(BUTTON_C):
        cycle_scene()

    if badge.pressed(BUTTON_UP):
        prev_animation()

    if badge.pressed(BUTTON_DOWN):
        next_animation()

def update():
    update_auto_cycle()
    render()

def render():
    global message_timer
    
    current_scene.render_background()

    frame = math.floor((badge.ticks - animation_start_time) / ms_per_frame)

    image = current_animation_sprites.frame(frame)

    scale = 2
    x_offset = -8
    y_offset = 4

    x = math.floor((screen.width - (image.width * scale)) / 2 + x_offset)
    y = math.floor(screen.height - (image.height * scale) + y_offset)

    screen.blit(image, rect(x, y, image.width * scale, image.height * scale))
    
    current_scene.render_overlay()

def on_exit():
    pass

def cycle_scene():
    global current_scene_index

    current_scene_index += 1

    if current_scene_index >= len(scenes):
        current_scene_index = 0

    load_scene(scenes[current_scene_index])

    toast.show(current_scene.name, duration=toast.SHORT, position=toast.TOP)

def cycle_character():
    global current_character_index

    if auto_cycle:
        set_auto_cycle(False)

    current_character_index += 1

    if current_character_index >= len(characters):
        current_character_index = 0

    load_character(characters[current_character_index])

    toast.show(current_character.name, duration=toast.SHORT, position=toast.TOP)

def next_animation():
    global current_animation_index, animation_start_time

    if auto_cycle:
        toast.show("Auto cycle disabled", duration=toast.SHORT, position=toast.TOP)
        set_auto_cycle(False)
    
    current_animation_index += 1

    if current_animation_index >= len(current_character.animations):
        current_animation_index = 0

    load_animation(current_character.animations[current_animation_index])

def prev_animation():
    global current_animation_index, animation_start_time
    
    if auto_cycle:
        toast.show("Auto cycle disabled", duration=toast.SHORT, position=toast.TOP)
        set_auto_cycle(False)

    current_animation_index -= 1

    if current_animation_index < 0:
        current_animation_index = len(current_character.animations) - 1

    load_animation(current_character.animations[current_animation_index])

def set_auto_cycle(enabled):
    global auto_cycle, auto_cycle_timer

    auto_cycle = enabled
    auto_cycle_timer = 0

def update_auto_cycle():
    global auto_cycle, auto_cycle_timer

    if not auto_cycle:
        return
    
    auto_cycle_timer -= badge.ticks_delta

    if auto_cycle_timer <= 0:
        auto_cycle_timer = random.randint(4000, 8000)

        candidate_animations = list(filter(
            lambda animation: 
                animation["auto_cycle"] == True and animation["path"] != current_animation["path"],
            current_character.animations
        ))
        
        if len(candidate_animations) > 1:
            animation = random.choice(candidate_animations)
            load_animation(animation)

            time_per_loop = ms_per_frame * animation["frames"]
            auto_cycle_timer = math.ceil(auto_cycle_timer / time_per_loop) * time_per_loop

def load_scene(scene):
    global current_scene
    current_scene = scene

def load_character(character):
    global current_character, current_animation_index
    
    current_character = character

    current_animation_index = 0
    load_animation(current_character.animations[current_animation_index])

def load_animation(animation):
    global current_animation, current_animation_sprites, animation_start_time
    current_animation = animation
    current_animation_sprites = SpriteSheet(animation["path"], animation["frames"], 1).animation()
    animation_start_time = badge.ticks