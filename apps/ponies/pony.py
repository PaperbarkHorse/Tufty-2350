import math
import random

import utils

shadow_image = image.load("assets/shadow.png")

class Pony:

    def __init__(self, data, world):
        self.data = data
        self.world = world
        
        self.width = self.data.sprite_bounds["width"]
        self.height = self.data.sprite_bounds["height"]
        self.x = random.randint(0, screen.width - self.width)
        self.y = random.randint(0, screen.height - self.height)
        self.facing = utils.LEFT
        self.alive = True

        self.animations = self.data.animations()
        self.animation_id = "idle"
        self.animation_sprites = self.animations["idle"][self.facing]
        self.animation_loop = True
        self.animation_start = badge.ticks
        self.animation_ms_per_frame = 1000 / self.animations["idle"]["framerate"]

        self.last_goal = None
        self.goal = None
        self.goal_queue = []

    def update(self):
        if self.goal:
            finished = self.goal.update()

            if finished:
                self.goal.finish(False)
                self.goal = None
        
        if not self.goal:
            if len(self.goal_queue) == 0:
                self.enqueue_random_goal()
            
            if len(self.goal_queue) > 0:
                self.start_goal(self.goal_queue.pop(0))


    def render_shadow(self):
        shadow_x = math.floor(self.x - self.data.sprite_bounds["x"] + 19)
        shadow_y = math.floor(self.y - self.data.sprite_bounds["y"] + 86)

        screen.alpha = 100
        screen.blit(shadow_image, vec2(shadow_x, shadow_y))
        screen.alpha = 255

    def render(self):
        sprite_x = math.floor(self.x - self.data.sprite_bounds["x"])
        sprite_y = math.floor(self.y - self.data.sprite_bounds["y"])

        frame = self.get_animation_frame()
        screen.blit(self.animation_sprites.sprite(frame), vec2(sprite_x, sprite_y))

    def render_debug(self):
        debug = [
            f"{self.data.id}",
            f"{self.last_goal} ({len(self.goal_queue) + 1})",
        ]

        screen.pen = color.rgb(128, 128, 255)
        screen.shape(shape.rectangle(self.x, self.y, self.width, self.height).stroke(1))

        if self.goal:
            debug.extend(self.goal.debug())
        else:
            debug.append("no goal")

        for index, line in enumerate(debug):
            screen.pen = color.rgb(255, 255, 255)
            screen.text(line, 2, index * 8)

    def animate(self, animation_id, loop=True):
        if self.animations[animation_id] == None and animation_id != "idle":
            return self.animate_oneshot("idle")

        self.animation_id = animation_id
        self.animation_sprites = self.animations[animation_id][self.facing]
        self.animation_loop = loop
        self.animation_start = badge.ticks
        self.animation_ms_per_frame = 1000 / self.animations[animation_id]["framerate"]

    def animate_oneshot(self, animation_id):
        self.animate(animation_id, loop=False)
        
    def animate_looping(self, animation_id):
       self.animate(animation_id, loop=True)

    def get_animation_frame(self):
        frame = math.floor((badge.ticks - self.animation_start) / self.animation_ms_per_frame)

        if not self.animation_loop:
            frame = min(frame, self.animation_sprites.sprites)

        return frame
    
    def is_animation_finished(self):
        if self.animation_loop:
            return False
        
        frame = math.floor((badge.ticks - self.animation_start) / self.animation_ms_per_frame)

        return frame >= self.animation_sprites.sprites
    
    def set_facing(self, facing):
        self.facing = facing
        self.animation_sprites = self.animations[self.animation_id][self.facing]

    def start_goal(self, goal):
        self.stop_goal(interrupt=True)
        self.goal = goal
        self.goal.start()

    def stop_goal(self, interrupt=True):
        if self.goal:
            self.goal.finish(interrupt)

    def queue_goal(self, goal):
        self.goal_queue.append(goal)

    def enqueue_random_goal(self):
        available_goals = self.data.available_goals(self)

        goals = []
        weights = []

        for id, available_goal in available_goals.items():
            if id == self.last_goal and len(available_goal) > 1:
                continue

            available_goal["id"] = id
            goals.append(available_goal)
            weights.append(available_goal["weight"])

        selected_goal = utils.weighted_random(goals, weights=weights)
        selected_goal_queue = selected_goal["build"](self)

        self.goal_queue.extend(selected_goal_queue)
        self.last_goal = selected_goal["id"]