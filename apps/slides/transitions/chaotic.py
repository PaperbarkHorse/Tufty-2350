import transitions.flip_random as flip_random
import transitions.zoom_random as zoom_random
import transitions.barn_door_random as barn_door_random
import transitions.explosion as explosion
import transitions.shatter as shatter
import transitions.unshatter as unshatter

id = "chaotic"
name = "Chaotic"

random_group = [
    flip_random,
    zoom_random,
    barn_door_random,
    explosion,
    shatter,
    unshatter,
]