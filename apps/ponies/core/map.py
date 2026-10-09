class MapType:
    def load(self) -> Map:
        pass

class Map:

    def __init__(self):
        self.ponies = []
        self.objects = []
        self.graph = None
        self.background_image = None

    def set_background(self, background_image):
        self.background_image = background_image