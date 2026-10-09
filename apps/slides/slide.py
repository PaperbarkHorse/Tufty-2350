from badgeware import State
from renderer import Renderer
import math

SLIDES_STATE_ID = "horse.paperbark.slides.settings"

slides_state = {}
State.load(SLIDES_STATE_ID, slides_state)

class Slide:
    def __init__(self, id):
        self.id = id
        self.name = id
        self.loaded = False
        self.state = {}
        self.load_state()

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

    def init_settings_menu(self):
        return None

    def save_state(self):
        slides_state[self.id] = self.state
        State.save(SLIDES_STATE_ID, slides_state)

    def load_state(self):
        State.load(SLIDES_STATE_ID, slides_state)

        if self.id in slides_state:
            self.state = slides_state[self.id]
        else:
            self.state = {}
            self.save_state()

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
        renderer.slide = self

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

    def init_settings_menu(self):
        return self.renderer.init_settings_menu()

class AnimationSlide(Slide):
    def __init__(self, animation):
        super().__init__(f"{animation["name"]} Animation")

        self.animation = animation
        self.animation_sprites = []
        self.animation_total_frames = 0
        self.animation_start_time = 0
        self.last_frame_time = 0

    def load(self):
        super().load()

        self.animation_sprites = []
        self.animation_total_frames = 0

        for sprite_data in self.animation["sprites"]:
            self.animation_sprites.append(image.load(sprite_data["path"]).spritesheet(sprite_data["width"], sprite_data["height"]))
            self.animation_total_frames += sprite_data["frames"]

        self.animation_start_time = badge.ticks
    
    def unload(self):
        super().unload()
        self.animation_sprites = None

    def render(self):
        if not self.loaded:
            return
        
        ms_per_frame = (1000 / self.animation["framerate"])
        frame = math.floor((badge.ticks - self.animation_start_time) / ms_per_frame) % self.animation_total_frames
        
        sprite = self.get_frame_sprite(frame)
        screen.blit(sprite, rect(0, 0, screen.width, screen.height))

        self.last_frame_time = badge.ticks

    def on_transition_start(self, out):
        frame = 0

        if not out:
            self.animation_start_time = badge.ticks
        else:
            frame = self.get_frame_at(self.last_frame_time)

        sprite = self.get_frame_sprite(frame)

        self.transition_image = image(screen.width, screen.height)
        self.transition_image.blit(sprite, rect(0, 0, screen.width, screen.height))

    def on_transition_end(self, out):
        self.transition_image = None

        if not out:
            self.animation_start_time = badge.ticks

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
        if not self.loaded:
            return None
        
        return self.get_frame_sprite(0)

    def get_frame_at(self, time):
        ms_per_frame = (1000 / self.animation["framerate"])
        return math.floor((time - self.animation_start_time) / ms_per_frame) % self.animation_total_frames

    def get_frame_sprite(self, frame):
        frame_counter = 0

        for index, sprite_data in enumerate(self.animation["sprites"]):
            if frame < frame_counter + sprite_data["frames"]:
                spritesheet = self.animation_sprites[index]
                sub_frame = frame - frame_counter

                x = sub_frame % sprite_data["width"]
                y = math.floor(sub_frame / sprite_data["width"])
                
                return spritesheet.sprite(x, y)
            
            frame_counter += sprite_data["frames"]
            
        return None