from renderer import Renderer

class Slide:
    def __init__(self, id):
        self.id = id
        self.name = id
        self.loaded = False

    def load(self):
        self.loaded = True

    def unload(self):
        self.loaded = False

    def render(self):
        pass

    def on_transition_start(self, out):
        pass

    def on_transition_end(self, out):
        pass

    def get_transition_image(self):
        return None

    def get_preview_image(self):
        return None

class ImageSlide(Slide):
    def __init__(self, image_path):
        super().__init__(image_path)
        self.image_path = image_path
        self.image = None
        self.name = image_path.split("/")[-1].split(".")[0]

    def load(self):
        super().load()
        self.image = image.load(self.image_path)

    def unload(self):
        super().unload()
        self.image = None

    def render(self):
        screen.font = font.ignore
        screen.pen = color.rgb(255, 255, 255)
        
        if not self.image:
            screen.text("No image", 10, 10)

            screen.font = font.sins
            screen.text(f"{self.image_path}", 10, 40)
            return

        screen.blit(self.image, rect(0, 0, screen.width, screen.height))

    def get_transition_image(self):
        return self.image

    def get_preview_image(self):
        if self.image:
            return self.image
        
        return image.load(self.image_path)

class DynamicSlide(Slide):
    def __init__(self, id, renderer: Renderer):
        super().__init__(id)
        self.renderer = renderer
        self.transition_image = None

    def load(self):
        super().load()
        self.transition_image = None
        self.renderer.on_load()
    
    def unload(self):
        super().unload()
        self.transition_image = None
        self.renderer.on_unload()

    def render(self):
        self.renderer.render_to(screen)

    def on_transition_start(self, out):
        self.transition_image = image(screen.width, screen.height)
        self.renderer.on_transition_start(out)
        self.renderer.render_to(self.transition_image)
    
    def on_transition_end(self, out):
        self.renderer.on_transition_end(out)
        self.transition_image = None

    def get_transition_image(self):
        return self.transition_image

    def get_preview_image(self):
        if self.loaded:
            return self.render_preview_image()
        else:
            self.load()
            preview = self.render_preview_image()
            self.unload()

            return preview

    def render_preview_image(self):
        preview = image(screen.width, screen.height)
        self.renderer.render_to(preview)
        return preview