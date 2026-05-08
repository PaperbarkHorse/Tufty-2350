from menu.items.button import Button

class Subpanel(Button):

    def __init__(self, text, panel):
        super().__init__()
        self.text = text
        self.panel = panel

    def interact(self):
        if self.panel:
            self.panel.open()