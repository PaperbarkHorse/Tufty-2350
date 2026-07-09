import transitions.fade as fade
import transitions.fade_to_black as fade_to_black
import transitions.slide_up as slide_up
import transitions.slide_down as slide_down
import transitions.slide_left as slide_left
import transitions.slide_right as slide_right
import transitions.slide_random as slide_random
import transitions.wipe_up as wipe_up
import transitions.wipe_down as wipe_down
import transitions.wipe_left as wipe_left
import transitions.wipe_right as wipe_right
import transitions.wipe_random as wipe_random
import transitions.flip_horizontal as flip_horizontal
import transitions.flip_vertical as flip_vertical
import transitions.flip_random as flip_random
import transitions.zoom_in as zoom_in
import transitions.zoom_out as zoom_out
import transitions.zoom_random as zoom_random
import transitions.barn_door_open as barn_door_open
import transitions.barn_door_close as barn_door_close
import transitions.barn_door_random as barn_door_random
import transitions.explosion as explosion
import transitions.random as random

all_transitions = [
    fade,
    fade_to_black,
    slide_up,
    slide_down,
    slide_left,
    slide_right,
    slide_random,
    wipe_up,
    wipe_down,
    wipe_left,
    wipe_right,
    wipe_random,
    flip_horizontal,
    flip_vertical,
    flip_random,
    zoom_in,
    zoom_out,
    zoom_random,
    barn_door_open,
    barn_door_close,
    barn_door_random,
    explosion,
    random,
]

def by_id(id):
    for transition in all_transitions:
        if transition.id == id:
            return transition

    return None