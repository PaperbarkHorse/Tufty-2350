import math
import gc
from animations import animations
import toast

hires = False

current_animation = None
current_index = 0

animation_sprites = []
animation_start_time = 0
animation_total_frames = 0

playback_speed = 1

def init():
    load_animation(animations[0])

def input():
    if badge.pressed(BUTTON_UP):
        prev_animation()

    if badge.pressed(BUTTON_DOWN):
        next_animation()

    if badge.pressed(BUTTON_A):
        set_speed(playback_speed - 0.1)

    if badge.pressed(BUTTON_C):
        set_speed(playback_speed + 0.1)

def update():
    if current_animation == None:
        return
    
    ms_per_frame = (1000 / current_animation["framerate"]) / playback_speed
    frame = math.floor((badge.ticks - animation_start_time) / ms_per_frame) % animation_total_frames

    sprite = get_frame_sprite(frame)
    screen.blit(sprite, rect(0, 0, screen.width, screen.height))

def next_animation():
    global current_index

    current_index += 1
    if current_index >= len(animations):
        current_index = 0

    load_animation(animations[current_index])

    toast.show(
        f"{animations[current_index]["name"]}",
        duration=toast.SHORT,
        position=toast.BOTTOM
    )

def prev_animation():
    global current_index

    current_index -= 1
    if current_index < 0:
        current_index = len(animations) - 1

    load_animation(animations[current_index])

    toast.show(
        f"{animations[current_index]["name"]}",
        duration=toast.SHORT,
        position=toast.BOTTOM
    )

def set_speed(new_speed):
    global playback_speed, animation_start_time

    playback_speed = max(0.1, min(10, new_speed))
    animation_start_time = badge.ticks

    toast.show(
        f"{playback_speed:.1f}x Speed",
        duration=toast.SHORT,
        position=toast.BOTTOM
    )

def load_animation(animation):
    global current_animation, animation_sprites, animation_start_time, animation_total_frames, hires

    del animation_sprites

    current_animation = animation
    animation_sprites = []
    animation_total_frames = 0
    
    gc.collect()

    for sprite_data in animation["sprites"]:
        animation_sprites.append(SpriteSheet(sprite_data["path"], sprite_data["width"], sprite_data["height"]))
        animation_total_frames += sprite_data["frames"]

    if hires != animation["hires"]:
        hires = animation["hires"]

        screen.pen = color.rgb(0, 0, 0)
        screen.clear()
        display.update()

        if hires:
            badge.mode(HIRES)
        else:
            badge.mode(LORES)

    animation_start_time = badge.ticks

def get_frame_sprite(frame):
    frame_counter = 0

    for index, sprite_data in enumerate(current_animation["sprites"]):
        if frame < frame_counter + sprite_data["frames"]:
            spritesheet = animation_sprites[index]
            sub_frame = frame - frame_counter

            x = sub_frame % sprite_data["width"]
            y = math.floor(sub_frame / sprite_data["width"])
            
            return spritesheet.sprite(x, y)
        
        frame_counter += sprite_data["frames"]
        
    return None