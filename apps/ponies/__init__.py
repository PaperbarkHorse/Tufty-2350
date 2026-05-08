from world import World
from pony import Pony
import ponies.paperbark as paperbark
import ponies.vinyl_scratch as vinyl_scratch
import ponies.cocoa_butter as cocoa_butter

debug = False
debug_target_pony = 0

world = World()

def init():
    world.spawn_pony(paperbark)
    world.spawn_pony(vinyl_scratch)
    world.spawn_pony(cocoa_butter)

def input():
    global debug, debug_target_pony, world

    if badge.pressed(BUTTON_B):
        debug = not debug   

    if badge.pressed(BUTTON_A) and debug:
        debug_target_pony -= 1
        if debug_target_pony < 0:
            debug_target_pony = len(world.ponies) - 1   
    
    if badge.pressed(BUTTON_C) and debug:
        debug_target_pony += 1
        if debug_target_pony >= len(world.ponies):
            debug_target_pony = 0

def update():
    world.update()
    world.render()

    if debug:
        render_debug()

def render_debug():
    global debug_target_pony
    world.ponies[debug_target_pony].render_debug()