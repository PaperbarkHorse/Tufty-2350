from badgeware import State, display
import machine
import powman

import menu
import toast

STATE_ID = "horse.paperbark.system"
state = {
    "backlight": 0.5,
    "boot_app_path": None,
    "fps_overlay": False,
    "input_locked": False,
    "super_dim": False
}

background_image = None

app_menu = None
system_menu = None

# ===== State ===== #
def save_state():
    State.save(STATE_ID, state)

def load_state():
    State.load(STATE_ID, state)

# ===== Backlight ===== #
def set_backlight(value = None):
    if value == None:
        value = get_backlight()

    value = min(max(value, 0), 1)

    display.backlight((value * (1 - 0.45)) + 0.45)

    state["backlight"] = value
    save_state()

def get_backlight():
    return state["backlight"]

# ===== Input Locking ===== #
def set_input_locked(enabled):
    state["input_locked"] = enabled
    save_state()

def is_input_locked():
    return state["input_locked"]

def lock_input():
    menu.manager.close_all()
    set_input_locked(True)
    toast.show("Input locked", toast.SHORT, toast.CENTER)

# ===== Debuggers ===== #
def set_fps_overlay(enabled):
    state["fps_overlay"] = enabled
    save_state()

def is_fps_overlay_enabled():
    return state["fps_overlay"]

def set_super_dim(enabled):
    state["super_dim"] = enabled
    save_state()

    if enabled == True:
        set_backlight(0)

def is_super_dim_enabled():
    return state["super_dim"]

# ===== Launching ===== #
def set_boot_to_app(app_path):
    state["boot_app_path"] = app_path
    save_state()

def set_boot_to_launcher():
    state["boot_app_path"] = None
    save_state()

def get_boot_app_path():
    return state["boot_app_path"]

def quit_to_launcher():
    set_boot_to_launcher()
    machine.reset()

def launch_app(app_path):
    set_boot_to_app(app_path)
    machine.reset()

def launch_usb_disk_mode():
    import _msc.py

# ===== App Menu ===== #
def init_app_menu():
    global app_menu
    global system_menu

    app_menu = menu.Menu()
    system_menu = menu.Menu()

    app_menu.add_item(menu.Header("Main Menu")) # TODO: Populate with app name from metadata
    app_menu.add_item(menu.Button("Back", app_menu.close))
    app_menu.add_item(menu.Button("Settings"))
    app_menu.add_item(menu.Subpanel("System", system_menu))
    app_menu.add_item(menu.Button("Quit", quit_to_launcher))

    system_menu.add_item(menu.Header("System"))
    system_menu.add_item(menu.Button("Back", system_menu.close))
    system_menu.add_item(menu.Button("Lock input", lock_input))
    system_menu.add_item(menu.Subpanel("Brightness", menu.BacklightConfigPanel()))
    system_menu.add_item(menu.Spacer(5))
    system_menu.add_item(menu.Header("Experimental"))
    system_menu.add_item(menu.Checkbox("FPS overlay", is_fps_overlay_enabled, set_fps_overlay))
    system_menu.add_item(menu.Checkbox("Super dim", is_super_dim_enabled, set_super_dim))
    system_menu.add_item(menu.Spacer(5))
    system_menu.add_item(menu.Header("Hardware"))
    system_menu.add_item(menu.Button("Sleep", badge.sleep))
    system_menu.add_item(menu.Button("USB disk mode", launch_usb_disk_mode))
    system_menu.add_item(menu.Button("Enter shipping mode", powman.shipping_mode))

# ===== Init ===== #
def init():
    global background_image

    load_state()
    set_backlight()
    init_app_menu()

    background_image = image.load("/system/assets/images/background.png")