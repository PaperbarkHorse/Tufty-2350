from badgeware import DEFAULT_FONT
from menu.base import MenuItem

class Checkbox(MenuItem):

    def __init__(self, text, get_state, callback = None):
        super().__init__()
        self.text = text
        self.get_state = get_state
        self.state = get_state()
        self.callback = callback

    def get_size(self):
        screen.font = DEFAULT_FONT
        width, height = screen.measure_text(self.text)

        return height + 2

    def is_interactive(self):
        return True

    def render(self, x, y, width, height, selected):
        self.state = self.get_state()
        
        if selected:
            screen.pen = color.rgb(20, 40, 80, 200)
        else:
            screen.pen = color.rgb(20, 20, 20, 100)

        screen.rectangle(x, y, width, height)
        
        screen.pen = color.rgb(255, 255, 255)
        screen.font = DEFAULT_FONT
        screen.text(self.text, x + height, y + 1)

        screen.pen = color.rgb(255, 255, 255)
        screen.rectangle(x + 2, y + 2, height - 4, height - 4)

        screen.pen = color.rgb(0, 0, 0)
        screen.rectangle(x + 3, y + 3, height - 6, height - 6)

        if self.state == True:
            screen.pen = color.rgb(255, 255, 255)
            screen.rectangle(x + 4, y + 4, height - 8, height - 8)

    def interact(self):
        self.state = not self.state
        
        if self.callback:
            self.callback(self.state)