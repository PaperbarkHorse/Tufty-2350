import draw
import system
from renderer import Renderer

class PaperbarkClock1(Renderer):

    def __init__(self):
        super().__init__()

    def on_load(self):
        self.background = image.load("/system/apps/slides/renderers/paperbark_clock_1/background.png")

    def on_unload(self):
        self.background = None

    def render_to(self, target):
        if self.background:
            target.blit(self.background, rect(0, 0, target.width, target.height))
        else:
            draw.clear(0, 0, 40, target)

        now = system.local_time()

        time_line = f"{now["hour"]:02}:{now["minute"]:02}:{now["second"]:02}"
        date_line = f"{now["day_of_week_short"]} {system.ordinal(now["day"])} {now["month_long"]} {now["year"]}"

        target.font = font.ignore

        target.pen = color.rgb(0, 0, 0, 100)
        draw.center_text_sized(time_line, target.width / 2 + 3, -2, 3, target)
        draw.center_text(date_line, target.width / 2 + 3, 75, target)

        target.pen = color.rgb(255, 255, 255)
        draw.center_text_sized(time_line, target.width / 2, -5, 3, target)
        draw.center_text(date_line, target.width / 2, 72, target)