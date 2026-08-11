import random
import goal
from utils import LEFT, RIGHT

id = "cocoa_butter"
name = "Cocoa Butter"

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
            LEFT: image.load("ponies/cocoa_butter/idle_left.png").spritesheet(1, 1),
            RIGHT: image.load("ponies/cocoa_butter/idle_right.png").spritesheet(1, 1),
        },
        "blink": None,
        "walk": {
            "framerate": 24,
            LEFT: image.load("ponies/cocoa_butter/walk_left.png",).spritesheet(6, 1),
            RIGHT: image.load("ponies/cocoa_butter/walk_right.png",).spritesheet(6, 1),
        },
        "huh": {
            "framerate": 1,
            LEFT: image.load("ponies/cocoa_butter/huh_left.png").spritesheet(1, 1),
            RIGHT: image.load("ponies/cocoa_butter/huh_right.png").spritesheet(1, 1),
        },
        "huh_behind": {
            "framerate": 1,
            LEFT: image.load("ponies/cocoa_butter/huh_behind_left.png").spritesheet(1, 1),
            RIGHT: image.load("ponies/cocoa_butter/huh_behind_right.png").spritesheet(1, 1),
        },
    }

def available_goals(pony):
    goals = {
        "idle": {
            "weight": 50,
            "build": lambda pony: [goal.IdleGoal(pony)],
        },
        "wander": {
            "weight": 10,
            "build": lambda pony: [goal.WanderGoal(pony)],
        },
        "huh": {
            "weight": 10,
            "build": lambda pony: [goal.AnimationLoopGoal(pony, "huh", random.randint(2000, 5000))],
        },
        "lost": {
            "weight": 5,
            "build": build_lost_goal,
        },
        "portal": {
            "weight": 1,
            "build": build_portal_goal,
        }
    }

    return goals

def build_lost_goal(pony):
    goals = []

    for i in range(0, random.randint(1, 3)):
        goals.append(goal.AnimationLoopGoal(pony, "huh", random.randint(1000, 2000)))
        goals.append(goal.AnimationLoopGoal(pony, "huh_behind", random.randint(1000, 2000)))

    goals.append(goal.AnimationLoopGoal(pony, "huh", 1000))

    return goals

def build_portal_goal(pony):
    if random.random() > 0.5:
        # Right portal
        return [
            goal.WalkToPointGoal(pony, screen.width + 20, pony.y),
            goal.TeleportGoal(pony, -20 - pony.width, pony.y),
            goal.WalkToPointGoal(pony, 10, pony.y),
            goal.WaitGoal(pony, 500),
            goal.AnimationLoopGoal(pony, "huh", 500),
            goal.AnimationLoopGoal(pony, "huh_behind", 3000),
            goal.AnimationLoopGoal(pony, "huh", 2000),
            goal.WaitGoal(pony, 1000),
        ]
    else:
        # Left portal
        return [
            goal.WalkToPointGoal(pony, -20 - pony.width, pony.y),
            goal.TeleportGoal(pony, screen.width + 20, pony.y),
            goal.WalkToPointGoal(pony, screen.width - pony.width - 10, pony.y),
            goal.WaitGoal(pony, 500),
            goal.AnimationLoopGoal(pony, "huh", 500),
            goal.AnimationLoopGoal(pony, "huh_behind", 3000),
            goal.AnimationLoopGoal(pony, "huh", 2000),
            goal.WaitGoal(pony, 1000),
        ]
