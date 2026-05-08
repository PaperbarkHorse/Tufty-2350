from badgeware import DEFAULT_FONT
from menu.base import MenuItem

class Label(MenuItem):

    def __init__(self, text = "Label"):
        super().__init__()
        self.text = text

    def get_size(self):
        screen.font = DEFAULT_FONT
        width, height = screen.measure_text(self.text)

        return height + 2

    def render(self, x, y, width, height, selected):
        screen.pen = color.rgb(255, 255, 255)
        screen.font = DEFAULT_FONT
        screen.text(self.text, x + 1, y + 1)