from badgeware import DEFAULT_FONT
from menu.base import MenuItem

class Property(MenuItem):

    def __init__(self, text, get_value):
        super().__init__()
        self.text = text
        self.get_value = get_value

    def get_size(self):
        screen.font = DEFAULT_FONT
        width, height = screen.measure_text(self.text)

        return height + 2

    def is_interactive(self):
        return True

    def render(self, x, y, width, height, selected):
        if selected:
            screen.pen = color.rgb(20, 40, 80, 200)
        else:
            screen.pen = color.rgb(20, 20, 20, 100)
        
        screen.rectangle(x, y, width, height)

        screen.font = DEFAULT_FONT
        screen.pen = color.rgb(255, 255, 255)
        screen.text(self.text, x + 1, y + 1)

        value = self.get_value()

        if value != None:
            value_text = ""
            screen.pen = color.rgb(128, 128, 128)

            if value == True:
                value_text = "YES"
                screen.pen = color.rgb(100, 255, 100)
            elif value == False:
                value_text = "NO"
                screen.pen = color.rgb(255, 100, 100)
            else:
                value_text = str(value)

            choice_text_width, _ = screen.measure_text(value_text)

            screen.text(value_text, width - choice_text_width - 1, y + 1)