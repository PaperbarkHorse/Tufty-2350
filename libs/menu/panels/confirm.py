from badgeware import DEFAULT_FONT
from menu.base import Panel
import system

class ConfirmPanel(Panel):
    
    def __init__(self, title, text, action):
        self.items = []
        self.title = title
        self.text = text
        self.action = action

    def on_open(self):
        pass

    def on_close(self):
        pass

    def input(self):
        if badge.pressed(BUTTON_B):
            self.close()
            self.action()
            return

        if badge.pressed(BUTTON_A):
            self.close()
            return

    def render(self):
        screen.pen = color.rgb(0, 0, 0)
        screen.clear()

        if system.background_image:
            screen.alpha = 50
            screen.blit(system.background_image, vec2(0, 0))
            screen.alpha = 255

        screen.pen = color.rgb(255, 255, 255)
        screen.font = rom_font.teatime

        title_width, title_height = screen.measure_text(self.title)
        screen.text(self.title, (screen.width - title_width) / 2, 5)

        screen.rectangle((screen.width - title_width) / 2, 5 + title_height + 2, title_width, 1)

        screen.font = DEFAULT_FONT

        if self.text:
            text.draw(screen, self.text, rect(10, 5 + title_height + 10, screen.width - 20, screen.height))