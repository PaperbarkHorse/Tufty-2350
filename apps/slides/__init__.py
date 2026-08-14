from badgeware import State
import os
import random
import system
import menu
import toast
import draw

from slide import Slide, ImageSlide, DynamicSlide
import renderers
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

slides = {}

slide_index = -1
current_slide = None
next_slide = None
slide_start_time = 0
next_slide_time = 0

edit_mode = False

transitioning = False
transition_id = None
transition_style = None
transition_start_time = 0
transition_end_time = 0

edit_slide_index = 0
edit_slide_preview_image = None

def init():
    global slides

    State.load(STATE_ID, state)
    badge.mode(HIRES)

    slides = [
        DynamicSlide("Clock", renderers.ClockRenderer()),
    ]

    image_root_paths = ["/system/apps/slides/slides", "/system/apps/gallery/images"]
    image_paths = []

    for image_root_path in image_root_paths:
        image_paths.extend(list(map(lambda path: f"{image_root_path}/{path}", filter(lambda path: path.lower().endswith(".png"), os.listdir(image_root_path)))))
    
    image_paths.sort()

    for image_path in image_paths:
        slides.append(ImageSlide(image_path))

    all_slide_ids = list(map(lambda slide: slide.id, slides))
    state["display_slides"] = list(filter(lambda id: id in all_slide_ids, state["display_slides"]))
    save_state()

    init_settings_menu()

def init_settings_menu():
    settings = menu.Menu()
    transition_style_dropdown = menu.Dropdown("Style", get_transition_id, set_transition_id)
    
    settings.add_item(menu.Header("Settings"))
    settings.add_item(menu.Button("Back", settings.close))
    settings.add_item(menu.Spacer(5))
    settings.add_item(menu.Header("Playback"))
    settings.add_item(menu.Button("Edit Slides", lambda: set_edit_mode(True)).set_close_on_interact("all"))
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
    
    for transition in transitions.all_transitions:
        transition_style_dropdown.add_option(transition.id, transition.name)

    settings.add_item(menu.Spacer(5))
    settings.add_item(menu.Header("Slides"))
    
    for slide in slides:
        slide_settings = slide.init_settings_menu()

        if slide_settings:
            settings.add_item(menu.Subpanel(slide.name, slide_settings))

    system.set_settings_menu(settings)

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
    
    if badge.pressed(BUTTON_UP) and len(state["display_slides"]) > 1:
        if is_auto_cycle():
            set_auto_cycle(False)

        slide_index -= 1

        if slide_index < 0:
            slide_index = len(state["display_slides"]) - 1

        load_next_slide(state["display_slides"][slide_index])
        transition_to_next_slide(state["slide_duration"], None, 0)

        toast.show(f"Slide {slide_index + 1} of {len(state["display_slides"])}", toast.SHORT, toast.BOTTOM)
    
    if badge.pressed(BUTTON_DOWN) and len(state["display_slides"]) > 1:
        if is_auto_cycle():
            set_auto_cycle(False)

        slide_index += 1

        if slide_index >= len(state["display_slides"]):
            slide_index = 0

        load_next_slide(state["display_slides"][slide_index])
        transition_to_next_slide(state["slide_duration"], None, 0)

        toast.show(f"Slide {slide_index + 1} of {len(state["display_slides"])}", toast.SHORT, toast.BOTTOM)

def update_slide():
    global current_slide, next_slide, state, slide_index, next_slide_time, transition_start_time, transition_end_time, transitioning, transition_id, slide_start_time
    
    if len(state["display_slides"]) <= 0:
        screen.pen = color.rgb(0, 0, 0)
        screen.clear()

        screen.pen = color.rgb(255, 255, 255)
        screen.text("No slides selected", 2, 2)
        screen.text("Use edit mode to add some", 2, 15)

        return

    if slide_index < 0:
        slide_index = 0

        if current_slide:
            current_slide.unload()
        
        load_next_slide(state["display_slides"][slide_index])

        current_slide = next_slide

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

        load_next_slide(state["display_slides"][slide_index])
        badge.poll()

        transition_to_next_slide(state["slide_duration"], state["transition_id"], state["transition_duration"])

    if transitioning and (badge.ticks >= transition_end_time or next_slide == None):
        if current_slide:
            current_slide.on_transition_end(True)
            current_slide.unload()

        next_slide.on_transition_end(False)

        transitioning = False
        current_slide = next_slide
        slide_start_time = badge.ticks
        next_slide = None

    if transitioning:
        t = (badge.ticks - transition_start_time) / (transition_end_time - transition_start_time)
        t = min(t, 1.0)

        if transition_style != None:
            if current_slide == None:
                transition_style.render(t, None, next_slide.get_transition_image())
            else:
                transition_style.render(t, current_slide.get_transition_image(), next_slide.get_transition_image())

        if is_timer_display() and is_auto_cycle():
            screen.pen = color.rgb(0, 0, 0)
            screen.rectangle(0, screen.height - 3, screen.width, 3)
            
            screen.pen = color.rgb(255, 255, 255, round((1 - t) * 255))
            screen.rectangle(0, screen.height - 2, screen.width, 2)

    else:    
        if current_slide != None:
            current_slide.render()

            if is_timer_display() and is_auto_cycle() and next_slide_time - slide_start_time > 0:
                screen.pen = color.rgb(0, 0, 0)
                screen.rectangle(0, screen.height - 3, screen.width, 3)

                screen.pen = color.rgb(255, 255, 255)
                screen.rectangle(0, screen.height - 2, screen.width * (1 - ((next_slide_time - badge.ticks) / (next_slide_time - slide_start_time))), 2)

def input_edit_mode():
    global edit_slide_index, edit_slide_preview_image

    if badge.pressed(BUTTON_UP):
        edit_slide_index -= 1

        if edit_slide_index < 0:
            edit_slide_index = len(slides) - 1

        edit_slide_preview_image = None

    if badge.pressed(BUTTON_DOWN):
        edit_slide_index += 1

        if edit_slide_index >= len(slides):
            edit_slide_index = 0

        edit_slide_preview_image = None

    if badge.pressed(BUTTON_B):
        display_index = None
        for i, display_slide_id in enumerate(state["display_slides"]):
            if display_slide_id == slides[edit_slide_index].id:
                display_index = i

        if display_index == None:
            state["display_slides"].append(slides[edit_slide_index].id)
        else:
            state["display_slides"].remove(slides[edit_slide_index].id)

        save_state()
    
    if badge.pressed(BUTTON_A):
        set_edit_mode(False)


def update_edit_mode():
    global edit_slide_index, edit_slide_preview_image

    edit_slide = slides[edit_slide_index]

    draw.clear(0, 0, 0)

    screen.pen = color.rgb(255, 255, 255)
    screen.font = font.ignore

    if not edit_slide_preview_image:
        edit_slide_preview_image = edit_slide.get_preview_image()

    if edit_slide_preview_image:
        screen.blit(edit_slide_preview_image, rect(60, 0, 200, 150))
    else:
        screen.text("No preview", 60, 0)

    display_index = None
    for i, display_slide in enumerate(state["display_slides"]):
        if display_slide == edit_slide.id:
            display_index = i
    
    draw.center_text(f"{edit_slide.name}", screen.width / 2, 150)

    if display_index != None:
        draw.center_text(f"{display_index + 1} of {len(state["display_slides"])}", screen.width / 2, 172)
    else:
        draw.center_text(f"- of {len(state["display_slides"])}", screen.width / 2, 172)
    

def load_next_slide(id):
    global next_slide

    next_slide = next(filter(lambda slide: slide.id == id, slides), None)

    if next_slide == None:
        raise ValueError(f"Attempt to load slide, not found: {id}")

    next_slide.load()

def transition_to_next_slide(slide_duration, new_transition_id, transition_duration):
    global next_slide_time, transition_start_time, transition_end_time, transitioning, transition_id, transition_style

    if current_slide:
        current_slide.on_transition_start(True)
    
    if next_slide:
        next_slide.on_transition_start(False)

    transition_id = new_transition_id
    transition_style = transitions.by_id(transition_id)

    while hasattr(transition_style, "random_group"):
        random_group = transition_style.random_group
        transition_style = random_group[random.randint(0, len(random_group) - 1)]

    if hasattr(transition_style, "duration_multiplier"):
        transition_duration *= transition_style.duration_multiplier

    badge.poll()

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
    global current_slide, next_slide, transitioning, next_slide_time, slide_index

    slide_index = -1
    current_slide = None
    next_slide = None

    transitioning = False
    next_slide_time = badge.ticks + state["slide_duration"]