import draw
import system
import menu
from renderer import Renderer

class ClockRenderer(Renderer):

    def __init__(self):
        super().__init__()

    def on_load(self):
        self.background = None
        style = self.get_style()

        if style == "paperbark_bottom":
            self.background = image.load("/system/apps/slides/renderers/clock/paperbark_bottom.png")
        elif style == "paperbark_sticky_note":
            self.background = image.load("/system/apps/slides/renderers/clock/paperbark_sticky_note.png")

    def on_unload(self):
        self.background = None

    def render_to(self, target):
        if self.background:
            target.blit(self.background, rect(0, 0, target.width, target.height))
        else:
            draw.clear(0, 0, 0, target)

        now = system.local_time()
        style = self.get_style()
        time_format = self.get_time_format()

        time_line = ""

        if time_format == "24":
            time_line = f"{now["hour"]:02}:{now["minute"]:02}:{now["second"]:02}"
        elif time_format == "12":
            time_line = f"{now["hour_12"]}:{now["minute"]:02}{now["am_pm"]}"

        date_line = f"{now["day_of_week_short"]} {system.ordinal(now["day"])} {now["month_long"]} {now["year"]}"

        if style == "paperbark_bottom":
            target.font = font.ignore

            target.pen = color.rgb(0, 0, 0, 100)
            draw.center_text_sized(time_line, target.width / 2 + 3, -2, 3, target)
            draw.center_text(date_line, target.width / 2 + 3, 75, target)

            target.pen = color.rgb(255, 255, 255)
            draw.center_text_sized(time_line, target.width / 2, -5, 3, target)
            draw.center_text(date_line, target.width / 2, 72, target)

        elif style == "paperbark_sticky_note":
            target.font = font.ignore

            target.pen = color.rgb(40, 40, 40)
            draw.center_text_sized(time_line, target.width / 2, 123, 3, target)
            draw.center_text(date_line, target.width / 2, 123 + 75, target)

        else:
            target.font = font.ignore

            target.pen = color.rgb(255, 255, 255)
            draw.center_text_sized(time_line, target.width / 2, 65, 3, target)
            draw.center_text(date_line, target.width / 2, 65 + 75, target)

    def init_settings_menu(self):
        settings = menu.Menu()

        style_dropdown = menu.Dropdown("Style", self.get_style, self.set_style)
        style_dropdown.add_option("basic", "Basic")
        style_dropdown.add_option("paperbark_bottom", "Paperbark (Bottom)")
        style_dropdown.add_option("paperbark_sticky_note", "Paperbark (Sticky Note)")

        time_format_dropdown = menu.Dropdown("Time Format", self.get_time_format, self.set_time_format)
        time_format_dropdown.add_option("12", "12hr h:mm")
        time_format_dropdown.add_option("24", "24hr hh:mm:ss")

        settings.add_item(menu.Header(self.slide.name))
        settings.add_item(menu.Button("Back", settings.close))
        settings.add_item(style_dropdown)
        settings.add_item(time_format_dropdown)

        return settings

    def set_style(self, style):
        self.slide.state["style"] = style
        self.slide.save_state()

    def get_style(self):
        if not "style" in self.slide.state:
            self.slide.state["style"] = "basic"
            self.slide.save_state()
        
        return self.slide.state["style"]

    def set_time_format(self, format):
        self.slide.state["time_format"] = format
        self.slide.save_state()

    def get_time_format(self):
        if not "time_format" in self.slide.state:
            self.slide.state["time_format"] = "24"
            self.slide.save_state()
        
        return self.slide.state["time_format"]