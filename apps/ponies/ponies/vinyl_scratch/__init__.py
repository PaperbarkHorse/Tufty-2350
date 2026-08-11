import goal
from utils import LEFT, RIGHT

id = "vinyl_scratch"
name = "Vinyl Scratch"

sprite_bounds = {
    "x": 18,
    "y": 41,
    "width": 44,
    "height": 50,
}

def animations():
    return {
        "idle": {
            "framerate": 1,
            LEFT: image.load("ponies/vinyl_scratch/idle_left.png").spritesheet(1, 1),
            RIGHT: image.load("ponies/vinyl_scratch/idle_right.png").spritesheet(1, 1),
        },
        "blink": None,
        "walk": {
            "framerate": 24,
            LEFT: image.load("ponies/vinyl_scratch/walk_left.png").spritesheet(16, 1),
            RIGHT: image.load("ponies/vinyl_scratch/walk_right.png").spritesheet(16, 1),
        },
    }

def available_goals(pony):
    goals = {
        "idle": {
            "weight": 10,
            "build": lambda pony: [goal.IdleGoal(pony)],
        },
        "wander": {
            "weight": 10,
            "build": lambda pony: [goal.WanderGoal(pony)],
        }
    }

    return goals