from badgeware import State
import os
import random
import system
import menu
import toast
import transitions

STATE_ID = "horse.paperbark.slides"
state = {
    "display_slides": [],
    "slide_duration": 5000,
    "shuffle_mode": "off",
    "transition_duration": 1000,
    "transition_id": "fade",
    "auto_cycle": True,
    "timer_display": False,
}

presets = [
    {
        "name": "Empty",
        "display_slides": []
    },
    {
        "name": "Pony Boops",
        "display_slides": [
            "/system/apps/gallery/images/Paperbark Boop.png",
            "/system/apps/gallery/images/Vinyl Boop.png",
        ]
    },
    {
        "name": "Volunteer",
        "display_slides": [
            "/system/apps/slides/slides/Volunteer Nameplate.png",
            "/system/apps/slides/slides/Volunteer Need a Hoof.png",
        ]
    },
    {
        "name": "Fursuit Handler",
        "display_slides": [
            "/system/apps/slides/slides/Fursuit Handler Nameplate.png",
        ]
    },
]

settings = None

edit_mode = False

all_slide_paths = []

current_slide_image = None
next_slide_image = None

slide_index = -1
next_slide_time = 0
slide_start_time = 0

transitioning = False
transition_id = None
transition_style = None
transition_start_time = 0
transition_end_time = 0

edit_slide_index = 0
edit_slide_preview_image = None

def init():
    global settings, presets_menu, all_slide_paths

    State.load(STATE_ID, state)
    badge.mode(HIRES)

    settings = menu.Menu()
    presets_dropdown = menu.Dropdown("Preset", lambda: None, use_preset)
    transition_style_dropdown = menu.Dropdown("Style", get_transition_id, set_transition_id)
    
    settings.add_item(menu.Header("Settings"))
    settings.add_item(menu.Button("Back", settings.close))
    settings.add_item(menu.Spacer(5))
    settings.add_item(menu.Header("Slides"))
    settings.add_item(menu.Button("Edit", lambda: set_edit_mode(True)).set_close_on_interact("all"))
    settings.add_item(presets_dropdown)
    settings.add_item(menu.Spacer(5))
    settings.add_item(menu.Header("Playback"))
    settings.add_item(
        menu.Dropdown("Duration", get_slide_duration, set_slide_duration)
            .add_option(0, "Instant")
            .add_option(2000, "2s")
            .add_option(5000, "5s")
            .add_option(7000, "7s")
            .add_option(10000, "10s")
            .add_option(15000, "15s")
            .add_option(20000, "20s")
            .add_option(30000, "30s")
            .add_option(45000, "45s")
            .add_option(60000, "1 min")
            .add_option(120000, "2 mins")
            .add_option(300000, "5 mins")
    )
    settings.add_item(
        menu.Dropdown("Shuffle", get_shuffle_mode, set_shuffle_mode)
            .add_option("off", "Off")
            .add_option("random", "Random")
    )
    settings.add_item(menu.Checkbox("Auto Cycle", is_auto_cycle, set_auto_cycle))
    settings.add_item(menu.Checkbox("Timer", is_timer_display, set_timer_display))
    settings.add_item(menu.Spacer(5))
    settings.add_item(menu.Header("Transition"))
    settings.add_item(transition_style_dropdown)
    settings.add_item(
        menu.Dropdown("Speed", get_transition_duration, set_transition_duration)
            .add_option(0, "Instant")
            .add_option(200, "Ludicrous (200ms)")
            .add_option(400, "Quick (400ms)")
            .add_option(600, "Fast (600ms)")
            .add_option(800, "Normal (800ms)")
            .add_option(1000, "Slow (1.0s)")
            .add_option(1500, "Crawl (1.5s)")
            .add_option(2000, "Snail (2.0s)")
            .add_option(5000, "Rock (5.0s)")
    )

    for preset in presets:
        presets_dropdown.add_option(preset["display_slides"], preset["name"])
    
    for transition in transitions.all_transitions:
        transition_style_dropdown.add_option(transition.id, transition.name)

    system.set_settings_menu(settings)

    slides_root_paths = ["/system/apps/slides/slides", "/system/apps/gallery/images"]
    all_slide_paths = []

    for slides_root_path in slides_root_paths:
        all_slide_paths.extend(list(map(lambda path: f"{slides_root_path}/{path}", filter(lambda path: path.lower().endswith(".png"), os.listdir(slides_root_path)))))
    
    all_slide_paths.sort()

    state["display_slides"] = list(filter(lambda display_slide: display_slide in all_slide_paths, state["display_slides"]))
    save_state()


def input():
    if edit_mode:
        input_edit_mode()
    else:
        input_slide()

def update():
    screen.pen = color.rgb(0, 0, 0)
    screen.clear()

    if edit_mode:
        update_edit_mode()
    else:
        update_slide()

def input_slide():
    global slide_index

    if badge.pressed(BUTTON_B):
        set_auto_cycle(not is_auto_cycle())

        if is_auto_cycle():
            toast.show("Auto cycle ON", toast.SHORT, toast.BOTTOM)
        else:
            toast.show("Auto cycle OFF", toast.SHORT, toast.BOTTOM)
    
    if badge.pressed(BUTTON_UP) and len(state["display_slides"]) > 0:
        if is_auto_cycle():
            set_auto_cycle(False)

        slide_index -= 1

        if slide_index < 0:
            slide_index = len(state["display_slides"]) - 1

        load_slide(state["display_slides"][slide_index])
        transition_to_next_slide(state["slide_duration"], None, 0)

        toast.show(f"Slide {slide_index + 1} of {len(state["display_slides"])}", toast.SHORT, toast.BOTTOM)
    
    if badge.pressed(BUTTON_DOWN) and len(state["display_slides"]) > 0:
        if is_auto_cycle():
            set_auto_cycle(False)

        slide_index += 1

        if slide_index >= len(state["display_slides"]):
            slide_index = 0

        load_slide(state["display_slides"][slide_index])
        transition_to_next_slide(state["slide_duration"], None, 0)

        toast.show(f"Slide {slide_index + 1} of {len(state["display_slides"])}", toast.SHORT, toast.BOTTOM)

def update_slide():
    global current_slide_image, next_slide_image, state, slide_index, next_slide_time, transition_start_time, transition_end_time, transitioning, transition_id, slide_start_time
    
    if len(state["display_slides"]) <= 0:
        if not (badge.mode() & LORES):
            badge.mode(LORES)

        screen.pen = color.rgb(0, 0, 0)
        screen.clear()

        screen.pen = color.rgb(255, 255, 255)
        screen.text("No slides selected", 2, 2)
        screen.text("Use edit mode to add some", 2, 15)

        return

    if slide_index < 0:
        slide_index = 0
        
        load_slide(state["display_slides"][slide_index])
        current_slide_image = next_slide_image

        transitioning = False
        next_slide_time = badge.ticks + state["slide_duration"]
        slide_start_time = badge.ticks

    if badge.ticks >= next_slide_time and is_auto_cycle() and not transitioning and len(state["display_slides"]) > 1:
        prev_slide_index = slide_index

        if state["shuffle_mode"] == "random":
            if len(state["display_slides"]) > 1:
                while slide_index == prev_slide_index:
                    slide_index = random.randint(0, len(state["display_slides"]) - 1)
        else:
            slide_index += 1

            if slide_index >= len(state["display_slides"]):
                slide_index = 0

        load_slide(state["display_slides"][slide_index])
        badge.poll()

        transition_to_next_slide(state["slide_duration"], state["transition_id"], state["transition_duration"])

    if transitioning and (badge.ticks >= transition_end_time or next_slide_image == None):
        transitioning = False
        current_slide_image = next_slide_image
        slide_start_time = badge.ticks
        next_slide_image = None

    if transitioning:
        if not (badge.mode() & LORES):
            badge.mode(LORES)

        t = (badge.ticks - transition_start_time) / (transition_end_time - transition_start_time)
        t = min(t, 1.0)

        if transition_style != None:
            if current_slide_image == None:
                transition_style.render(t, None, next_slide_image["lores"])
            else:
                transition_style.render(t, current_slide_image["lores"], next_slide_image["lores"])

    else:
        if not (badge.mode() & HIRES):
            badge.mode(HIRES)
        
        if current_slide_image != None:
            screen.blit(current_slide_image["hires"], vec2(0, 0))

            if is_timer_display() and is_auto_cycle():
                screen.pen = color.rgb(0, 0, 0)
                screen.rectangle(0, screen.height - 2, screen.width, 2)

                screen.pen = color.rgb(200, 200, 200)
                screen.rectangle(0, screen.height - 2, screen.width * (1 - ((next_slide_time - badge.ticks) / (next_slide_time - slide_start_time))), 2)

def input_edit_mode():
    global edit_slide_index, edit_slide_preview_image

    if badge.pressed(BUTTON_UP):
        edit_slide_index -= 1

        if edit_slide_index < 0:
            edit_slide_index = len(all_slide_paths) - 1

        edit_slide_preview_image = image.load(all_slide_paths[edit_slide_index])

    if badge.pressed(BUTTON_DOWN):
        edit_slide_index += 1

        if edit_slide_index >= len(all_slide_paths):
            edit_slide_index = 0

        edit_slide_preview_image = image.load(all_slide_paths[edit_slide_index])

    if badge.pressed(BUTTON_B):
        display_index = None
        for i, display_slide in enumerate(state["display_slides"]):
            if display_slide == all_slide_paths[edit_slide_index]:
                display_index = i

        if display_index == None:
            state["display_slides"].append(all_slide_paths[edit_slide_index])
        else:
            state["display_slides"].remove(all_slide_paths[edit_slide_index])

        save_state()
    
    if badge.pressed(BUTTON_A):
        set_edit_mode(False)


def update_edit_mode():
    global edit_slide_index, edit_slide_preview_image

    edit_slide_path = all_slide_paths[edit_slide_index]

    if not (badge.mode() & LORES):
        badge.mode(LORES)

    screen.pen = color.rgb(0, 0, 0)
    screen.clear()

    if not edit_slide_preview_image:
        edit_slide_preview_image = image.load(edit_slide_path)
    
    screen.blit(edit_slide_preview_image, rect(30, 0, 100, 75))

    display_index = None
    for i, display_slide in enumerate(state["display_slides"]):
        if display_slide == edit_slide_path:
            display_index = i

    screen.pen = color.rgb(255, 255, 255)
    
    center_text(f"{edit_slide_path.split("/")[-1].split(".")[0]}", screen.width / 2, 75)
    # center_text(f"{edit_slide_index + 1} / {len(all_slide_paths)}", screen.width / 2, 86)

    if display_index != None:
        center_text(f"{display_index + 1} of {len(state["display_slides"])}", screen.width / 2, 86)
    else:
        center_text(f"- of {len(state["display_slides"])}", screen.width / 2, 86)
    

def load_slide(slide_path):
    global next_slide_image

    next_image = image.load(slide_path)
    next_image_hires = image(320, 240)
    next_image_lores = image(160, 120)
    next_image_hires.blit(next_image, rect(0, 0, next_image_hires.width, next_image_hires.height))
    next_image_lores.blit(next_image, rect(0, 0, next_image_lores.width, next_image_lores.height))
    
    next_slide_image = {
        "hires": next_image_hires,
        "lores": next_image_lores,
    }

def transition_to_next_slide(slide_duration, new_transition_id, transition_duration):
    global next_slide_time, transition_start_time, transition_end_time, transitioning, transition_id, transition_style

    transition_id = new_transition_id
    transition_style = transitions.by_id(transition_id)

    while hasattr(transition_style, "random_group"):
        random_group = transition_style.random_group
        transition_style = random_group[random.randint(0, len(random_group) - 1)]

    if hasattr(transition_style, "duration_multiplier"):
        transition_duration *= transition_style.duration_multiplier

    next_slide_time = badge.ticks + slide_duration + transition_duration
    transition_start_time = badge.ticks
    transition_end_time = transition_start_time + transition_duration

    transitioning = True

def save_state():
    State.save(STATE_ID, state)

def is_edit_mode():
    global edit_mode
    return edit_mode

def set_edit_mode(new_edit_mode):
    global edit_mode

    if new_edit_mode == False and edit_mode == True:
        reset_playback()
   
    edit_mode = new_edit_mode

def get_slide_duration():
    return state["slide_duration"]

def set_slide_duration(slide_duration):
    state["slide_duration"] = slide_duration
    save_state()
    reset_playback()

def get_shuffle_mode():
    return state["shuffle_mode"]

def set_shuffle_mode(shuffle_mode):
    state["shuffle_mode"] = shuffle_mode
    save_state()

def get_transition_id():
    return state["transition_id"]

def set_transition_id(transition_id):
    state["transition_id"] = transition_id
    save_state()

def get_transition_duration():
    return state["transition_duration"]

def set_transition_duration(transition_duration):
    state["transition_duration"] = transition_duration
    save_state()

def use_preset(display_slides):
    state["display_slides"] = list(filter(lambda display_slide: display_slide in all_slide_paths, display_slides))
    save_state()
    reset_playback()

def is_auto_cycle():
    return state["auto_cycle"]

def set_auto_cycle(auto_cycle):
    state["auto_cycle"] = auto_cycle
    save_state()

def is_timer_display():
    return state["timer_display"]

def set_timer_display(timer_display):
    state["timer_display"] = timer_display
    save_state()

def reset_playback():
    global current_slide_image, next_slide_image, transitioning, next_slide_time, slide_index

    slide_index = -1
    current_slide_image = None
    next_slide_image = None

    transitioning = False
    next_slide_time = badge.ticks + state["slide_duration"]

def center_text(text, x, y):
    width, height = screen.measure_text(text)
    screen.text(text, x - width / 2, y)