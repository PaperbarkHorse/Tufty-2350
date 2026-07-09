import transitions.wipe_up as wipe_up
import transitions.wipe_down as wipe_down
import transitions.wipe_left as wipe_left
import transitions.wipe_right as wipe_right

id = "wipe_random"
name = "Wipe (Random)"

random_group = [
    wipe_up,
    wipe_down,
    wipe_left,
    wipe_right,
]