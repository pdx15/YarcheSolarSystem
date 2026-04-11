from ursina import *

from core.camera import SimpleCamera
from core.solar_system_scene import SolarSystemScene

if __name__ == "__main__":
    app = Ursina()
    cam = SimpleCamera()
    Sky(texture="assets/textures/stars_milky_way.jpg")
    scene = SolarSystemScene()
    app.run()
    raise SystemExit
"""

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

SATELLITE_SYSTEMS = {
    "MARS BARYCENTER": {
        "moons": MARS_MOONS,
        "scales": MARS_MOON_SCALES,
        "default_scale": 0.15,
    },
    "JUPITER BARYCENTER": {
        "moons": JUPITER_MOONS,
        "scales": JUPITER_MOON_SCALES,
        "default_scale": 0.3,
    },
    "SATURN BARYCENTER": {
        "moons": SATURN_MOONS,
        "scales": SATURN_MOON_SCALES,
        "default_scale": 0.14,
    },
}

SATURN_RING_BANDS = (
    {"scale_multiplier": 1.45, "tint": color.rgba(189, 170, 134, 90)},
    {"scale_multiplier": 1.75, "tint": color.rgba(214, 196, 156, 140)},
    {"scale_multiplier": 2.05, "tint": color.rgba(235, 220, 186, 105)},
)


def to_scaled_vec(position):
    return Vec3(
        position[0] * DISTANCE_SCALE,
        position[2] * DISTANCE_SCALE,
        position[1] * DISTANCE_SCALE
    )


def get_scaled_position(target, et, observer):
    position, _ = spice.spkpos(target, et, "J2000", "NONE", observer)
    return to_scaled_vec(position)


def create_saturn_rings(saturn_body):
    rings = []

    for index, band in enumerate(SATURN_RING_BANDS, start=1):
        rings.append(Entity(
            parent=saturn_body,
            model="quad",
            texture="assets/textures/saturn_ring_alpha.png",
            double_sided=True,
            unlit=True,
            rotation_x=90,
            y=index * 0.01,
            scale=saturn_body.scale_x * band["scale_multiplier"],
            color=band["tint"],
        ))

    return rings


planet_bodies = []
satellite_bodies = {parent: [] for parent in SATELLITE_SYSTEMS}
saturn = None

for name, spice_name in PLANETS.items():
    body = CelestialBody(
        name,
        f"assets/textures/{name.lower()}.jpg",
        PLANET_SCALES[name] * SIZE_SCALE,
        spice_name=spice_name,
        parent_body="SUN"
    )
    planet_bodies.append(body)

    if name == "SATURN":
        saturn = body

for parent_body, system in SATELLITE_SYSTEMS.items():
    for name, spice_name in system["moons"].items():
        satellite_bodies[parent_body].append(
            CelestialBody(
                name,
                "assets/textures/moon.jpg",
                system["scales"].get(name, system["default_scale"]),
                spice_name,
                parent_body
            )
        )

saturn_rings = create_saturn_rings(saturn) if saturn else []
bodies = planet_bodies + [
    moon
    for moons in satellite_bodies.values()
    for moon in moons
]

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

for name, spice_name in SATURN_MOONS.items():
    orbit = create_real_orbit(
        spice_name,
        "SATURN BARYCENTER",
        et,
        duration_days=180,
        steps=180
    )
    if orbit:
        orbit.y = -0.03
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
"""
