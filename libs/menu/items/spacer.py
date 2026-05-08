from menu.base import MenuItem

class Spacer(MenuItem):

    def __init__(self, height = 0):
        super().__init__()
        self.height = height

    def get_size(self):
        return self.height