from badgeware import DEFAULT_FONT
from menu.base import MenuItem

class Button(MenuItem):

    def __init__(self, text = "Button", action = None):
        super().__init__()
        self.text = text
        self.action = action
        self.enabled = True

    def set_action(self, action):
        self.action = action
        return self
    
    def set_enabled(self, enabled):
        self.enabled = enabled
        return self

    def get_size(self):
        screen.font = DEFAULT_FONT
        width, height = screen.measure_text(self.text)

        return height + 2

    def is_interactive(self):
        return self.enabled

    def render(self, x, y, width, height, selected):
        if selected:
            screen.pen = color.rgb(20, 40, 80, 200)
        else:
            screen.pen = color.rgb(20, 20, 20, 100)

        screen.rectangle(x, y, width, height)
        
        if self.enabled:
            screen.pen = color.rgb(255, 255, 255)
        else:
            screen.pen = color.rgb(128, 128, 128)

        screen.font = DEFAULT_FONT
        screen.text(self.text, x + 1, y + 1)

    def interact(self):
        if self.action != None:
            self.action()