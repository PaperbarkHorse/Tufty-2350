from badgeware import fatal_error

try:
    import sys
    import os
    from badgeware import display, DEFAULT_FONT
    import machine
    import gc

    sys.path.append("/system/libs")
    import system
    import menu
    import toast

    system.init()

    badge.default_clear = None
    badge.mode(LORES)

    badge.poll()
    if badge.held(BUTTON_HOME):
        system.set_boot_to_launcher()
        system.set_input_locked(False)
        system.set_super_dim(False)

        screen.pen = color.rgb(255, 0, 0)
        screen.clear()
        display.update()
        
        while badge.held(BUTTON_HOME):
            badge.poll()

    screen.pen = color.rgb(0, 0, 0)
    screen.clear()
    display.update()

    def run(app):
        try:
            screen.font = DEFAULT_FONT
            screen.pen = color.rgb(0, 0, 0)
            screen.clear()
            screen.pen = color.rgb(255, 255, 255)

            init = getattr(app, "init", None)
            update = getattr(app, "update")
            input = getattr(app, "input", None)
            on_exit = getattr(app, "on_exit", None)

            home_hold_start = None

            if init:
                init()
            
            result = None

            while result == None:
                should_update = True

                badge.poll()

                if badge.pressed(BUTTON_HOME):
                    home_hold_start = badge.ticks

                    if system.app_menu:
                        if menu.manager.get_active_panel():
                            menu.manager.close_all()
                        elif not system.is_input_locked():
                            system.app_menu.open()

                if badge.held(BUTTON_HOME) and system.is_input_locked() and home_hold_start != None and badge.ticks > home_hold_start + 1000:
                    system.set_input_locked(False)
                    toast.show("Input unlocked", toast.SHORT, toast.CENTER)

                if menu.manager.panel_active:
                    should_update = False
                    menu.manager.input()
                else:
                    if system.is_input_locked():
                        if badge.pressed():
                            toast.show("Hold HOME to unlock", toast.SHORT, toast.CENTER)
                    else:
                        if input:
                            input()

                if should_update:
                    result = update()

                if menu.manager.panel_active:
                    menu.manager.render()
                
                toast.update()

                if system.is_fps_overlay_enabled():
                    screen.pen = color.rgb(0, 0, 0, 200)
                    screen.rectangle(0, 0, 40, 15)
                    screen.font = DEFAULT_FONT
                    screen.pen = color.rgb(255, 255, 255)
                    screen.text(f"{1000 / badge.ticks_delta:.1f}", 2, 0)

                if system.is_super_dim_enabled():
                    screen.pen = color.rgb(0, 0, 0, 160)
                    screen.rectangle(0, 0, screen.width, screen.height)

                display.update()

            if on_exit:
                on_exit()

            return result

        except Exception as e:
            if not badge.usb_connected():
                system.set_boot_to_launcher()

            fatal_error("App Error", e)

    def home_button_interrupt(pin):
        system.set_boot_to_launcher()
        
        while not pin.value():
            pass
        
        machine.reset()


    app = system.get_boot_app_path()

    if app == None:
        try:
            sys.path.insert(0, "/system/launcher")
            launcher = __import__("/system/launcher")
        except Exception as e:  # noqa: BLE001
            fatal_error("Launcher Error", e)
        
        app = run(launcher)

        if sys.path[0].startswith("/system/launcher"):
            sys.path.pop(0)
        
        del launcher

    gc.collect()

    if app is None:
        fatal_error("App Launching Error", "Launcher did not provide an app to run")

    system.set_boot_to_app(app)

    badge.poll()
    badge.poll()

    while badge.held():
        badge.poll()

    # machine.Pin.board.BUTTON_HOME.irq(
    #     trigger=machine.Pin.IRQ_FALLING, handler=home_button_interrupt
    # )

    sys.path.insert(0, app)

    try:
        os.chdir(app)
        running_app = __import__(app)
    except Exception as e:
        system.set_boot_to_launcher()        
        fatal_error("App Launching Error", e)

    run(running_app)

    machine.reset()

except Exception as e:
    screen.pen = color.rgb(0, 0, 0)
    screen.clear()
    fatal_error("System Error", e)