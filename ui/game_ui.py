from ursina import *
import threading
from data.api import get_body_info

BG = color.rgba(8, 12, 20, 170)
BORDER = color.rgba(80, 160, 255, 140)
GLOW = color.rgba(120, 200, 255, 220)
TEXT = color.rgb(200, 230, 255)

class GlassPanel(Entity):
    def __init__(self, scale=(1,1), position=(0,0)):
        super().__init__(
            parent=camera.ui,
            model='quad',
            scale=scale,
            position=position,
            color=BG
        )

        self.border = Entity(
            parent=self,
            model='quad',
            scale=1.03,
            color=BORDER,
            z=-0.01
        )

        self.glow = Entity(
            parent=self,
            model='quad',
            scale=0.98,
            color=color.rgba(40, 90, 160, 40),
            z=0.01
        )

class SciButton(Button):
    def __init__(self, text="", **kwargs):
        super().__init__(
            text=text,
            model='quad',
            color=color.rgba(25, 35, 55, 220),
            highlight_color=color.rgba(60, 120, 200, 220),
            pressed_color=color.rgba(120, 200, 255, 255),
            scale=(0.2, 0.05),
            **kwargs
        )

        self.text_entity.color = TEXT
        self.text_entity.scale = 0.8

class GameUI(Entity):
    def __init__(self, time_ctrl, scene):
        super().__init__(parent=camera.ui)

        self.time_ctrl = time_ctrl
        self.scene = scene

        self.left_panel = GlassPanel(scale=(0.28, 0.9), position=(-0.75, 0))

        Text(
            parent=self.left_panel,
            text="SOLAR SYSTEM",
            y=0.42,
            scale=1.6,
            color=GLOW
        )

        self.speed_text = Text(
            parent=self.left_panel,
            text=f"{self.time_ctrl.get_scale()}x",
            y=0.3,
            scale=1.2,
            color=TEXT
        )

        def set_speed(v):
            self.time_ctrl.set_scale(v)
            self.speed_text.text = f"{v}x"

        SciButton(parent=self.left_panel, text="PAUSE", y=0.2, on_click=lambda: set_speed(0))
        SciButton(parent=self.left_panel, text="NORMAL", y=0.1, on_click=lambda: set_speed(500))
        SciButton(parent=self.left_panel, text="FAST", y=0.0, on_click=lambda: set_speed(2000))

        Text(parent=self.left_panel, text="ZOOM", y=-0.15, color=GLOW)

        self.zoom = Slider(
            parent=self.left_panel,
            min=20,
            max=120,
            default=40,
            y=-0.25,
            scale=(0.8, 0.03),
        )

        self.right_panel = GlassPanel(scale=(0.35, 0.5), position=(0.65, -0.15))

        Text(parent=self.right_panel, text="OBJECT INFO", y=0.2, color=GLOW)

        self.info = Text(
            parent=self.right_panel,
            text="Click object",
            position=(-0.45, 0.05),
            scale=1,
            wordwrap=25,
            color=TEXT
        )

        self.crosshair = Entity(
            parent=camera.ui,
            model='quad',
            scale=(0.008, 0.008),
            color=GLOW
        )

        self.date = Text(
            parent=camera.ui,
            text="",
            position=(0, 0.45),
            origin=(0, 0),
            scale=1.2,
            color=TEXT
        )

    def update(self):
        import spiceypy as spice

        try:
            self.date.text = spice.et2utc(self.time_ctrl.et, "C", 0)
        except:
            pass

        camera.fov = lerp(90, 40, self.zoom.value / 120)

    def input(self, key):
        if key == "left mouse down":
            hit = mouse.hovered_entity

            if not hit or hit.has_ancestor(camera.ui):
                return

            data = self.scene.get_body_info(hit)
            if not data:
                return

            name = data["name"]
            self.info.text = f"{name}\nLoading..."

            def load():
                result = get_body_info(name)
                self.info.text = result

            threading.Thread(target=load, daemon=True).start()