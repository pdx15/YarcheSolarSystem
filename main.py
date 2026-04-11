from ursina import *
from core.celestial import CelestialBody
from core.camera import SimpleCamera
from data.spice_loader import load_kernels, get_et
from data.bodies import PLANETS, JUPITER_MOONS, SATURN_MOONS, MARS_MOONS
from config import SIZE_SCALE, DISTANCE_SCALE
import spiceypy as spice
from data.bodies import PLANET_SCALES, SUN_SCALE
from core.orbit import create_real_orbit

app = Ursina()
cam = SimpleCamera()
Sky(texture="assets/textures/stars_milky_way.jpg")

load_kernels()
et = get_et()

sun = CelestialBody(
    "SUN",
    "assets/textures/sun.jpg",
    SUN_SCALE,
    "SUN"
)

sun_light = PointLight(parent=sun, intensity=5)
AmbientLight(color=color.rgba(80, 80, 80, 0.2))

bodies = []

for name, spice_name in PLANETS.items():
    body = CelestialBody(
        name,
        f"assets/textures/{name.lower()}.jpg",
        PLANET_SCALES[name] * SIZE_SCALE,
        spice_name=spice_name,
        parent_body="SUN"
    )
    bodies.append(body)

for name, spice_name in MARS_MOONS.items():
    bodies.append(CelestialBody(name, "assets/textures/moon.jpg", 0.2, spice_name, "MARS BARYCENTER"))

for name, spice_name in JUPITER_MOONS.items():
    bodies.append(CelestialBody(name, "assets/textures/moon.jpg", 0.3, spice_name, "JUPITER BARYCENTER"))

for name, spice_name in SATURN_MOONS.items():
    bodies.append(CelestialBody(name, "assets/textures/moon.jpg", 0.3, spice_name, "SATURN BARYCENTER"))

time_scale = 5000

orbits = []

for name, spice_name in PLANETS.items():
    orbit = create_real_orbit(
        spice_name,
        "SUN",
        et,
        duration_days=3650,
        steps=300
    )

    if orbit:
        orbit.y = -0.1
        orbits.append(orbit)

for name, spice_name in JUPITER_MOONS.items():
    orbit = create_real_orbit(
        spice_name,
        "JUPITER BARYCENTER",
        et,
        duration_days=20,
        steps=150
    )
    if orbit:
        orbit.y = -0.05
        orbits.append(orbit)

def update():
    global et
    et += time.dt * time_scale
    
    sun.position = Vec3(0, 0, 0)
    
    for body in bodies:
        if body.parent_body == "SUN":
            body.update_position(et, "SUN")
        elif body.parent_body == "MARS BARYCENTER":
            try:
                mars_pos, _ = spice.spkpos("MARS BARYCENTER", et, "J2000", "NONE", "SUN")
                moon_pos, _ = spice.spkpos(body.spice_name, et, "J2000", "NONE", "MARS BARYCENTER")
                body.position = Vec3(
                    (mars_pos[0] + moon_pos[0]) * DISTANCE_SCALE,
                    (mars_pos[2] + moon_pos[2]) * DISTANCE_SCALE,
                    (mars_pos[1] + moon_pos[1]) * DISTANCE_SCALE
                )
            except Exception as e:
                print(f"Ошибка с {body.name}: {e}")
        elif body.parent_body == "JUPITER BARYCENTER":
            try:
                jupiter_pos, _ = spice.spkpos("JUPITER BARYCENTER", et, "J2000", "NONE", "SUN")
                moon_pos, _ = spice.spkpos(body.spice_name, et, "J2000", "NONE", "JUPITER BARYCENTER")
                body.position = Vec3(
                    (jupiter_pos[0] + moon_pos[0]) * DISTANCE_SCALE,
                    (jupiter_pos[2] + moon_pos[2]) * DISTANCE_SCALE,
                    (jupiter_pos[1] + moon_pos[1]) * DISTANCE_SCALE
                )
            except Exception as e:
                print(f"Ошибка с {body.name}: {e}")
        elif body.parent_body == "SATURN BARYCENTER":
            try:
                saturn_pos, _ = spice.spkpos("SATURN BARYCENTER", et, "J2000", "NONE", "SUN")
                moon_pos, _ = spice.spkpos(body.spice_name, et, "J2000", "NONE", "SATURN BARYCENTER")
                body.position = Vec3(
                    (saturn_pos[0] + moon_pos[0]) * DISTANCE_SCALE,
                    (saturn_pos[2] + moon_pos[2]) * DISTANCE_SCALE,
                    (saturn_pos[1] + moon_pos[1]) * DISTANCE_SCALE
                )
            except Exception as e:
                print(f"Ошибка с {body.name}: {e}")

app.run()