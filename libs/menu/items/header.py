from badgeware import DEFAULT_FONT
from menu.base import MenuItem

class Header(MenuItem):

    def __init__(self, text = "Header"):
        super().__init__()
        self.text = text

    def get_size(self):
        screen.font = rom_font.teatime
        width, height = screen.measure_text(self.text)

        return height + 4

    def render(self, x, y, width, height, selected):
        screen.pen = color.rgb(255, 255, 255)
        screen.font = rom_font.teatime
        screen.text(self.text, x + 2, y + 1)
        screen.rectangle(x, y + height - 1, width, 1)