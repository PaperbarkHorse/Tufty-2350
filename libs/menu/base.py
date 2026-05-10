from badgeware import DEFAULT_FONT
import math
import system

class MenuManager:

    def __init__(self):
        self.active_panels = []
        self.panel_active = False
        self.was_hires_mode = None

    def input(self):
        panel = self.get_active_panel()

        if panel == None:
            return

        self.get_active_panel().input()

    def render(self):
        panel = self.get_active_panel()

        if panel == None:
            return

        panel.render()

        screen.font = DEFAULT_FONT

    def on_first_panel_open(self):
        self.panel_active = True

        self.was_hires_mode = screen.width == 320

        if self.was_hires_mode:
            badge.mode(LORES)

    def on_last_panel_close(self):
        self.panel_active = False

        if self.was_hires_mode:
            badge.mode(HIRES)

        self.was_hires_mode = None

    def open(self, panel):
        if len(self.active_panels) == 0:
            self.on_first_panel_open()

        self.active_panels.append(panel)
        panel.on_open()

    def close(self):
        if len(self.active_panels) <= 0:
            return
        
        panel = self.active_panels.pop()
        panel.on_close()

        if len(self.active_panels) == 0:
            self.on_last_panel_close()

    def close_all(self):
        while len(self.active_panels) > 0:
            self.close()

    def get_active_panel(self):
        if len(self.active_panels) > 0:
            return self.active_panels[len(self.active_panels) - 1]
        else:
            return None
        

manager = MenuManager()

class Panel():
    def __init__(self):
        pass

    def on_open(self):
        pass

    def on_close(self):
        pass

    def input(self):
        pass

    def render(self):
        pass

    def open(self):
        manager.open(self)

    def close(self):
        if manager.get_active_panel() == self:
            manager.close()


class Menu(Panel):
    
    def __init__(self):
        self.items = []
        self.selected_index = None

    def on_open(self):
        self.selected_index = None
        self.select_next_item()

    def on_close(self):
        pass

    def input(self):
        if badge.pressed(BUTTON_A):
            self.close()
            return

        if badge.pressed(BUTTON_B):
            selected_item = self.get_selected_item()

            if selected_item != None and selected_item.is_interactive():
                selected_item.interact()
                return
        
        if badge.pressed(BUTTON_UP):
            self.select_prev_item()

        if badge.pressed(BUTTON_DOWN):
            self.select_next_item()


    def render(self):
        screen.pen = color.rgb(0, 0, 0)
        screen.clear()

        if system.background_image:
            screen.alpha = 70
            screen.blit(system.background_image, vec2(0, 0))
            screen.alpha = 255

        selected_item = self.get_selected_item()
        y = 0

        for index, item in enumerate(self.items):
            selected = index == self.selected_index

            height = item.get_size()
            item.layout(0, y, screen.width, height)

            y += height

        scroll_offset = 0

        if selected_item != None:
            scroll_offset = math.floor((screen.height / 2 - selected_item.y) - (selected_item.height / 2))

        scroll_offset = math.floor(min(max(scroll_offset, screen.height - y - 5), 0))

        for index, item in enumerate(self.items):
            selected = index == self.selected_index

            if item.y + item.height + scroll_offset < 0 or item.y + scroll_offset > screen.height:
                continue
            
            item.render(item.x, item.y + scroll_offset, item.width, item.height, selected)

    def add_item(self, item, index=None):
        if index:
            self.items.insert(index, item)
        else:
            self.items.append(item)

    def get_selected_item(self):
        if len(self.items) <= 0:
            return None
        
        if self.selected_index == None:
            return None

        return self.items[self.selected_index]
    
    def select_next_item(self):
        if len(self.items) == 0:
            self.selected_index = None
        
        check_index = 0 if self.selected_index == None else self.selected_index + 1

        for _ in range(0, len(self.items) + 1):
            if check_index >= len(self.items):
                check_index = 0

            item = self.items[check_index]

            if item.is_interactive():
                self.selected_index = check_index
                return
            
            check_index += 1
        
        self.selected_index = None
    
    def select_prev_item(self):
        if len(self.items) == 0:
            self.selected_index = None
        
        check_index = 0 if self.selected_index == None else self.selected_index - 1

        for _ in range(0, len(self.items) + 1):
            if check_index < 0:
                check_index = len(self.items) - 1

            item = self.items[check_index]

            if item.is_interactive():
                self.selected_index = check_index
                return
            
            check_index -= 1
        
        self.selected_index = None


class MenuItem:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.selected = False

    def get_size(self):
        return 0
    
    def is_interactive(self):
        return False

    def layout(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, x, y, width, height, selected):
        pass

    def interact(self):
        pass