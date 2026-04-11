from ursina import *

from core.camera import SimpleCamera
from core.solar_system_scene import SolarSystemScene

if __name__ == "__main__":
    app = Ursina()
    cam = SimpleCamera()
    Sky(texture="assets/textures/stars_milky_way.jpg")
    scene = SolarSystemScene()
    app.run()
