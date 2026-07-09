import transitions.slide_random as slide_random
import transitions.wipe_random as wipe_random
import transitions.flip_random as flip_random
import transitions.zoom_random as zoom_random
import transitions.barn_door_random as barn_door_random

id = "random"
name = "Random"

random_group = [
    slide_random,
    wipe_random,
    flip_random,
    zoom_random,
    barn_door_random,
]