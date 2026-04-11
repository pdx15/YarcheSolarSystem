from ursina import *
from core.celestial import CelestialBody
from core.camera import SimpleCamera
from data.spice_loader import load_kernels, get_et
from data.bodies import PLANETS, JUPITER_MOONS, SATURN_MOONS, MARS_MOONS
from config import SIZE_SCALE, DISTANCE_SCALE
import spiceypy as spice
from data.bodies import PLANET_SCALES
from core.orbit import create_orbit

app = Ursina()
cam = SimpleCamera()
Sky(texture="assets/textures/8k_stars_milky_way.jpg")

load_kernels()
et = get_et()

sun = CelestialBody("SUN", "assets/textures/2k_sun.jpg", 5, "SUN")

sun_light = PointLight(parent=sun, intensity=5)
AmbientLight(color=color.rgba(80, 80, 80, 0.2))

bodies = []

for name, spice_name in PLANETS.items():
    body = CelestialBody(
        name,
        f"assets/textures/2k_{name.lower()}.jpg",
        PLANET_SCALES[name] * SIZE_SCALE,
        spice_name=spice_name,
        parent_body="SUN"
    )
    bodies.append(body)

for name, spice_name in MARS_MOONS.items():
    bodies.append(CelestialBody(name, "assets/textures/2k_moon.jpg", 0.2, spice_name, "MARS BARYCENTER"))

for name, spice_name in JUPITER_MOONS.items():
    bodies.append(CelestialBody(name, "assets/textures/2k_moon.jpg", 0.3, spice_name, "JUPITER BARYCENTER"))

for name, spice_name in SATURN_MOONS.items():
    bodies.append(CelestialBody(name, "assets/textures/2k_moon.jpg", 0.3, spice_name, "SATURN BARYCENTER"))

time_scale = 5000

orbits = []

for name, spice_name in PLANETS.items():
    try:
        pos, _ = spice.spkpos(spice_name, et, "J2000", "NONE", "SUN")
        radius = Vec3(pos[0], pos[2], pos[1]).length() * DISTANCE_SCALE
        
        orbit = create_orbit(radius)
        orbits.append(orbit)
    except:
        pass

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