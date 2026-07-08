from badgeware import DEFAULT_FONT
from menu.base import MenuItem, Panel
import system

class Dropdown(MenuItem):

    def __init__(self, text, get_state, set_state = None):
        super().__init__()
        self.text = text
        self.options = []
        self.state = get_state()
        self.get_state = get_state
        self.set_state = set_state

    def add_option(self, value, text):
        self.options.append(DropdownOption(value, text))
        return self

    def get_choice(self):
        state = self.get_state()
        return next(filter(lambda option: option.value == state, self.options), None)

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

        choice = self.get_choice()

        if choice != None:
            choice_text_width, _ = screen.measure_text(choice.text)

            screen.pen = color.rgb(128, 128, 128)
            screen.text(choice.text, width - choice_text_width - 1, y + 1)

    def interact(self):
        if len(self.options) <= 0:
            return
        
        DropdownPanel(self).open()

class DropdownOption:
    def __init__(self, value, text):
        self.value = value
        self.text = text

class DropdownPanel(Panel):
    
    def __init__(self, dropdown: Dropdown):
        self.dropdown = dropdown
        self.scroll_animation_offset = None
        self.selected_index = 0
        self.initial_choice = None

    def on_open(self):
        state = self.dropdown.get_state()

        self.scroll_animation_offset = None
        self.initial_choice = self.dropdown.get_choice()

        self.selected_index = 0
        for i, option in enumerate(self.dropdown.options):
            if option.value == state:
                self.selected_index = i
                break 

    def on_close(self):
        pass

    def input(self):
        if badge.pressed(BUTTON_UP):
            self.selected_index -= 1

            if self.selected_index < 0:
                self.selected_index = len(self.dropdown.options) - 1

        if badge.pressed(BUTTON_DOWN):
            self.selected_index += 1

            if self.selected_index >= len(self.dropdown.options):
                self.selected_index = 0

        if badge.pressed(BUTTON_A):
            if self.initial_choice != None:
                self.dropdown.set_state(self.initial_choice.value)

            self.close()

        if badge.pressed(BUTTON_B):
            self.dropdown.set_state(self.dropdown.options[self.selected_index].value)
            self.close()

    def render(self):
        screen.pen = color.rgb(0, 0, 0)
        screen.clear()

        if system.background_image:
            screen.alpha = 70
            screen.blit(system.background_image, vec2(0, 0))
            screen.alpha = 255

        screen.font = DEFAULT_FONT
        _, line_height = screen.measure_text("#")
        line_height += 2

        scroll_animation_target = (line_height * self.selected_index)

        if self.scroll_animation_offset == None:
            self.scroll_animation_offset = scroll_animation_target

        self.scroll_animation_offset += (scroll_animation_target - self.scroll_animation_offset) * 10 * (badge.ticks_delta / 1000)

        scroll_offset = round((screen.height - line_height) / 2 - self.scroll_animation_offset)

        for i, choice in enumerate(self.dropdown.options):
            line_y = (i * line_height) + scroll_offset

            if line_y < -line_height or line_y > screen.height:
                continue

            if i == self.selected_index:
                screen.pen = color.rgb(20, 40, 80, 200)
            else:
                screen.pen = color.rgb(20, 20, 20, 100)

            screen.rectangle(0, line_y, screen.width, line_height)

            screen.pen = color.rgb(255, 255, 255)
            screen.text(choice.text, 1, line_y + 1)

        # screen.pen = color.rgb(255, 255, 255)
        # screen.font = rom_font.teatime

        # title_width, title_height = screen.measure_text(self.dropdown.text)

        # if system.background_image:
        #     screen.pen = color.rgb(0, 0, 0)
        #     screen.rectangle(0, 0, screen.width, title_height + 2)
        #     screen.alpha = 70
        #     screen.blit(system.background_image, rect(0, 0, screen.width, title_height + 2), rect(0, 0, screen.width, title_height + 2))
        #     screen.alpha = 255

        # screen.pen = color.rgb(255, 255, 255)
        # screen.text(self.dropdown.text, (screen.width - title_width) / 2, 1)
        # screen.rectangle(0, title_height + 1, screen.width, 1)