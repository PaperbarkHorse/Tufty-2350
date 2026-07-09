import transitions.barn_door_open as barn_door_open
import transitions.barn_door_close as barn_door_close

id = "barn_door_random"
name = "Barn Door (Random)"

random_group = [
    barn_door_open,
    barn_door_close,
]