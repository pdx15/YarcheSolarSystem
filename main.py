from ursina import *
from core.camera import SimpleCamera
from core.solar_system_scene import SolarSystemScene
from core.time_controller import TimeController
from data.api import get_body_info
from config import TIME_SCALE
import spiceypy as spice
import os
import threading
from ui.game_ui import GameUI
from ursina import *

def main():
    app = Ursina()

    window.title = "Solar System"
    window.borderless = False
    window.size = (1280, 720)
    window.fullscreen = False
    window.color = color.black
    window.vsync = True
    window.color = color.black
    camera.clip_plane_far = 100000

    scene = SolarSystemScene()
    time_ctrl = TimeController(scene.et, TIME_SCALE)

    cam = SimpleCamera()
    camera.position = (0, 10, -30)

    sky_path = "assets/textures/stars_milky_way.jpg"
    if os.path.exists(sky_path):
        Sky(texture=sky_path)
    else:
        print(f"Предупреждение: текстура неба не найдена: {sky_path}")

    ui = GameUI(time_ctrl, scene)

    def update():
        dt = time.dt
        scene.et = time_ctrl.update(dt)
        scene.update()
        ui.update()

    app.run()

if __name__ == "__main__":
    main()