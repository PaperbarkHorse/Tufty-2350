from badgeware import State
import os
import random
import system
import menu

STATE_ID = "horse.paperbark.slides"
state = {
    "display_slides": [],
    "slide_duration": 5000,
    "shuffle_mode": "off",
    "transition_duration": 1000,
    "transition_style": "fade",
}

edit_mode = False

all_slide_paths = []

current_slide_image = None
next_slide_image = None

slide_index = 0
next_slide_time = 0

transitioning = False
transition_style = None
transition_start_time = 0
transition_end_time = 0

def init():
    global all_slide_paths

    State.load(STATE_ID, state)
    badge.mode(HIRES)

    settings = menu.Menu()
    
    settings.add_item(menu.Header("Settings"))
    settings.add_item(menu.Button("Back", settings.close))
    settings.add_item(menu.Spacer(5))
    settings.add_item(menu.Header("Slides"))
    settings.add_item(menu.Checkbox("Edit mode", is_edit_mode, set_edit_mode))
    settings.add_item(
        menu.Dropdown("Duration", get_slide_duration, set_slide_duration)
            .add_option(2000, "2s")
            .add_option(5000, "5s")
            .add_option(10000, "10s")
            .add_option(15000, "15s")
            .add_option(20000, "20s")
            .add_option(30000, "30s")
            .add_option(45000, "45s")
            .add_option(60000, "1 min")
    )
    settings.add_item(
        menu.Dropdown("Shuffle", get_shuffle_mode, set_shuffle_mode)
            .add_option("off", "Off")
            .add_option("random", "Random")
    )
    settings.add_item(menu.Spacer(5))
    settings.add_item(menu.Header("Transition"))
    settings.add_item(
        menu.Dropdown("Style", get_transition_style, set_transition_style)
            .add_option("fade", "Fade")
            .add_option("slide_up", "Slide (Up)")
            .add_option("slide_down", "Slide (Down)")
            .add_option("slide_left", "Slide (Left)")
            .add_option("slide_right", "Slide (Right)")
            .add_option("slide_random", "Slide (Random)")
            .add_option("wipe_up", "Wipe (Up)")
            .add_option("wipe_down", "Wipe (Down)")
            .add_option("wipe_left", "Wipe (Left)")
            .add_option("wipe_right", "Wipe (Right)")
            .add_option("wipe_random", "Wipe (Random)")
            .add_option("random", "Random")
    )
    settings.add_item(
        menu.Dropdown("Speed", get_transition_duration, set_transition_duration)
            .add_option(0, "Instant")
            .add_option(200, "Ludicrous")
            .add_option(400, "Quick")
            .add_option(600, "Fast")
            .add_option(800, "Normal")
            .add_option(1000, "Slow")
            .add_option(1500, "Crawl")
            .add_option(2000, "Snail")
            .add_option(5000, "Rock")
    )

    system.set_settings_menu(settings)

    slides_root_path = "/system/apps/slides/slides"
    all_slide_paths = list(map(lambda path: f"{slides_root_path}/{path}", filter(lambda path: path.lower().endswith(".png"), os.listdir(slides_root_path))))
    all_slide_paths.sort()

    state["display_slides"] = all_slide_paths # TODO: Debug only

def input():
    pass

def update():
    global current_slide_image, next_slide_image, state, slide_index, next_slide_time, transition_start_time, transition_end_time, transitioning, transition_style

    screen.pen = color.rgb(0, 0, 0)
    screen.clear()

    if badge.ticks >= next_slide_time:
        slide_index += 1

        if slide_index >= len(state["display_slides"]):
            slide_index = 0

        next_image = image.load(state["display_slides"][slide_index])
        next_image_hires = image(320, 240)
        next_image_lores = image(160, 120)
        next_image_hires.blit(next_image, rect(0, 0, next_image_hires.width, next_image_hires.height))
        next_image_lores.blit(next_image, rect(0, 0, next_image_lores.width, next_image_lores.height))
        
        next_slide_image = {
            "hires": next_image_hires,
            "lores": next_image_lores,
        }

        badge.mode(LORES)
        badge.poll()

        next_slide_time = badge.ticks + state["slide_duration"] + state["transition_duration"]
        transition_start_time = badge.ticks
        transition_end_time = transition_start_time + state["transition_duration"]

        if state["transition_style"] == "random":
            random_style = random.randint(0, 2)

            if random_style == 0:
                transition_style = "fade"
            elif random_style == 1:
                transition_style = "slide_random"
            elif random_style == 2:
                transition_style = "wipe_random"
        else:
            transition_style = state["transition_style"]

        if transition_style == "slide_random":
            random_direction = random.randint(0, 3)
            if random_direction == 0:
                transition_style = "slide_up"
            elif random_direction == 1:
                transition_style = "slide_down"
            elif random_direction == 2:
                transition_style = "slide_left"
            elif random_direction == 3:
                transition_style = "slide_right"
        
        if transition_style == "wipe_random":
            random_direction = random.randint(0, 3)
            if random_direction == 0:
                transition_style = "wipe_up"
            elif random_direction == 1:
                transition_style = "wipe_down"
            elif random_direction == 2:
                transition_style = "wipe_left"
            elif random_direction == 3:
                transition_style = "wipe_right"

        transitioning = True

    if transitioning and (badge.ticks >= transition_end_time or next_slide_image == None):
        transitioning = False
        current_slide_image = next_slide_image
        next_slide_image = None
        badge.mode(HIRES)

    if transitioning:
        transition_delta = (badge.ticks - transition_start_time) / (transition_end_time - transition_start_time)
        transition_delta = min(transition_delta, 1.0)

        if transition_style == "fade":
            if current_slide_image != None:
                screen.blit(current_slide_image["lores"], vec2(0, 0))

            screen.alpha = round(transition_delta * 255)
            screen.blit(next_slide_image["lores"], vec2(0, 0))
            screen.alpha = 255

        if transition_style == "slide_up":
            if current_slide_image != None:
                screen.blit(current_slide_image["lores"], vec2(0, transition_delta * -screen.height))
            
            screen.blit(next_slide_image["lores"], vec2(0, (1 - transition_delta) * screen.height))

        if transition_style == "slide_down":
            if current_slide_image != None:
                screen.blit(current_slide_image["lores"], vec2(0, transition_delta * screen.height))
            
            screen.blit(next_slide_image["lores"], vec2(0, (1 - transition_delta) * -screen.height))

        if transition_style == "slide_left":
            if current_slide_image != None:
                screen.blit(current_slide_image["lores"], vec2(transition_delta * -screen.width, 0))
            
            screen.blit(next_slide_image["lores"], vec2((1 - transition_delta) * screen.width, 0))

        if transition_style == "slide_right":
            if current_slide_image != None:
                screen.blit(current_slide_image["lores"], vec2(transition_delta * screen.width, 0))
            
            screen.blit(next_slide_image["lores"], vec2((1 - transition_delta) * -screen.width, 0))

        if transition_style == "wipe_down":
            if current_slide_image != None:
                screen.blit(current_slide_image["lores"], vec2(0, 0))
            
            wipe_area = rect(0, 0, screen.width, transition_delta * screen.height)
            screen.blit(next_slide_image["lores"], wipe_area, wipe_area)

        if transition_style == "wipe_up":
            if current_slide_image != None:
                screen.blit(current_slide_image["lores"], vec2(0, 0))
            
            wipe_area = rect(0, (1 - transition_delta) * screen.height, screen.width, transition_delta * screen.height)
            screen.blit(next_slide_image["lores"], wipe_area, wipe_area)

        if transition_style == "wipe_right":
            if current_slide_image != None:
                screen.blit(current_slide_image["lores"], vec2(0, 0))
            
            wipe_area = rect(0, 0, transition_delta * screen.width, screen.height)
            screen.blit(next_slide_image["lores"], wipe_area, wipe_area)

        if transition_style == "wipe_left":
            if current_slide_image != None:
                screen.blit(current_slide_image["lores"], vec2(0, 0))
            
            wipe_area = rect((1 - transition_delta) * screen.width, 0, transition_delta * screen.width, screen.height)
            screen.blit(next_slide_image["lores"], wipe_area, wipe_area)
    else:
        if current_slide_image != None:
            screen.blit(current_slide_image["hires"], vec2(0, 0))


def save_state():
    State.save(STATE_ID, state)

def is_edit_mode():
    global edit_mode
    return edit_mode

def set_edit_mode(new_edit_mode):
    global edit_mode
    edit_mode = new_edit_mode

def get_slide_duration():
    return state["slide_duration"]

def set_slide_duration(slide_duration):
    state["slide_duration"] = slide_duration
    save_state()

def get_shuffle_mode():
    return state["shuffle_mode"]

def set_shuffle_mode(shuffle_mode):
    state["shuffle_mode"] = shuffle_mode
    save_state()

def get_shuffle_mode():
    return state["shuffle_mode"]

def set_shuffle_mode(shuffle_mode):
    state["shuffle_mode"] = shuffle_mode
    save_state()

def get_transition_style():
    return state["transition_style"]

def set_transition_style(transition_style):
    state["transition_style"] = transition_style
    save_state()

def get_transition_duration():
    return state["transition_duration"]

def set_transition_duration(transition_duration):
    state["transition_duration"] = transition_duration
    save_state()