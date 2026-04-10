from ursina import *
from core.celestial import CelestialBody
from core.camera import SimpleCamera
from data.spice_loader import load_kernels, get_et
from data.bodies import PLANETS, JUPITER_MOONS, SATURN_MOONS, MARS_MOONS
from config import SIZE_SCALE
import spiceypy as spice

app = Ursina()

cam = SimpleCamera()

Sky(texture="assets/textures/2k_stars.jpg")

load_kernels()
et = get_et()

sun = CelestialBody("SUN", "assets/textures/2k_sun.jpg", 5, "SUN")

sun_light = PointLight(parent=sun, intensity=5)
AmbientLight(color=color.rgba(80, 80, 80, 0.2))

bodies = []

for name in PLANETS:
    body = CelestialBody(
        name,
        f"assets/textures/2k_{name.lower()}.jpg",
        SIZE_SCALE,
        spice_name=name
    )
    bodies.append(body)

for moon in MARS_MOONS:
    bodies.append(CelestialBody(moon, "assets/textures/2k_moon.jpg", 0.2, moon))

for moon in JUPITER_MOONS:
    bodies.append(CelestialBody(moon, "assets/textures/2k_moon.jpg", 0.3, moon))

for moon in SATURN_MOONS:
    bodies.append(CelestialBody(moon, "assets/textures/2k_moon.jpg", 0.3, moon))

time_scale = 5000

def update():
    global et
    et += time.dt * time_scale

    for body in bodies:
        body.update_position(et)

app.run()