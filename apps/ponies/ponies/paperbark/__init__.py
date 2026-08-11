import random
import goal
from utils import LEFT, RIGHT

id = "paperbark"
name = "Paperbark"

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
            LEFT: image.load("ponies/paperbark/idle_left.png").spritesheet(1, 1),
            RIGHT: image.load("ponies/paperbark/idle_right.png").spritesheet(1, 1),
        },
        "blink": {
            "framerate": 24,
            LEFT: image.load("ponies/paperbark/blink_left.png").spritesheet(5, 1),
            RIGHT: image.load("ponies/paperbark/blink_right.png").spritesheet(5, 1),
        },
        "walk": {
            "framerate": 24,
            LEFT: image.load("ponies/paperbark/walk_left.png",).spritesheet(6, 1),
            RIGHT: image.load("ponies/paperbark/walk_right.png",).spritesheet(6, 1),
        },
        "yawn": {
            "framerate": 24,
            LEFT: image.load("ponies/paperbark/yawn_left.png",).spritesheet(2, 1),
            RIGHT: image.load("ponies/paperbark/yawn_right.png",).spritesheet(2, 1),
        },
        "giggle": {
            "framerate": 9,
            LEFT: image.load("ponies/paperbark/giggle_left.png").spritesheet(8, 1),
            RIGHT: image.load("ponies/paperbark/giggle_right.png").spritesheet(8, 1),
        },
        "boop": {
            "framerate": 24,
            LEFT: image.load("ponies/paperbark/boop_left.png",).spritesheet(2, 1),
            RIGHT: image.load("ponies/paperbark/boop_right.png",).spritesheet(2, 1),
        },
    }

def available_goals(pony):
    goals = {
        "idle": {
            "weight": 50,
            "build": lambda pony: [goal.IdleGoal(pony, duration=random.randint(1000, 7000))],
        },
        "wander": {
            "weight": 6,
            "build": lambda pony: [goal.WanderGoal(pony, duration=random.randint(3000, 6000))],
        },
        "sneak": {
            "weight": 1,
            "build": build_sneak_goal,
        },
        # TODO: Yawn and animation is broken :'3
        # "yawn": {
        #     "weight": 1,
        #     "build": lambda pony: [goal.AnimationGoal(pony, "yawn")],
        # },
        "giggle": {
            "weight": 2,
            "build": lambda pony: [goal.AnimationGoal(pony, "giggle")],
        },
    }

    vinyl_scratch = pony.world.random_pony_of_type("vinyl_scratch")

    if vinyl_scratch:
        goals["follow_vinyl_scratch"] = {
            "weight": 1,
            "build": lambda pony: [goal.FollowPonyGoal(pony, vinyl_scratch, duration=random.randint(20000, 30000))],
        }

    return goals

def build_sneak_goal(pony):
    x_offset = pony.width / 2
    return [
        # Walk off screen
        goal.WalkToPointGoal(pony, -pony.width - 20, pony.y),

        # Left side peek
        goal.TeleportGoal(pony, screen.width / 4 * 1 - x_offset, screen.height + 10),
        goal.WaitGoal(pony, duration=2000),
        goal.WalkToPointGoal(pony, screen.width / 4 * 1 - x_offset, screen.height - 19),
        goal.IdleGoal(pony, duration=1000),
        goal.AnimationGoal(pony, "giggle"),
        goal.WalkToPointGoal(pony, screen.width / 4 * 1 - x_offset, screen.height + 10),
        
        # Right side peek
        goal.WalkToPointGoal(pony, screen.width / 4 * 3 - x_offset, screen.height + 10),
        goal.WalkToPointGoal(pony, screen.width / 4 * 3 - x_offset, screen.height - 19),
        goal.IdleGoal(pony, duration=1000),
        goal.AnimationGoal(pony, "giggle"),
        goal.WalkToPointGoal(pony, screen.width / 4 * 3 - x_offset, screen.height + 10),

        # Center peek
        goal.WalkToPointGoal(pony, screen.width / 4 * 2 - x_offset, screen.height + 10),
        goal.WalkToPointGoal(pony, screen.width / 4 * 2 - x_offset, screen.height - 19),
        goal.IdleGoal(pony, duration=1000),
        goal.AnimationGoal(pony, "giggle"),
        goal.IdleGoal(pony, duration=1000),

        # Reveal
        goal.WalkToPointGoal(pony, screen.width / 2 - pony.width / 2, screen.height / 2 - pony.height / 2),
    ]