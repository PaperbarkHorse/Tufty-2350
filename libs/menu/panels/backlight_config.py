from menu.base import Panel
import system

class BacklightConfigPanel(Panel):
    
    def __init__(self):
        self.items = []

    def on_open(self):
        pass

    def on_close(self):
        pass

    def input(self):
        if badge.pressed(BUTTON_A):
            system.set_backlight(system.get_backlight() - 0.1)

        if badge.pressed(BUTTON_C):
            system.set_backlight(system.get_backlight() + 0.1)

        if badge.pressed(BUTTON_B):
            self.close()

    def render(self):
        if system.background_image:
            screen.blit(system.background_image, rect(0, 0, screen.width, screen.height))

        screen.pen = color.rgb(0, 0, 0)
        screen.rectangle(1, 1, screen.width - 2, 16)

        screen.pen = color.rgb(255, 255, 255)
        screen.rectangle(3, 3, screen.width - 6, 12)

        screen.pen = color.rgb(0, 0, 0)
        screen.rectangle(4, 4, screen.width - 8, 10)

        screen.pen = color.rgb(255, 255, 255)
        screen.rectangle(5, 5, round((screen.width - 11) * system.get_backlight()) + 1, 8)