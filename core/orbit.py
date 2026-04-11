from ursina import *
import spiceypy as spice

def create_real_orbit(spice_name, center, et, duration_days=365, steps=200, distance_multiplier=1):
    points = []

    step = (duration_days * 86400) / steps

    for i in range(steps):
        t = et + i * step

        try:
            pos, _ = spice.spkpos(spice_name, t, "J2000", "NONE", center)

            points.append(Vec3(
                pos[0],
                pos[2],
                pos[1]
            ))
        except:
            continue

    if not points:
        return None

    from config import DISTANCE_SCALE
    points = [p * DISTANCE_SCALE * distance_multiplier for p in points]

    return Entity(
        model=Mesh(vertices=points, mode='line'),
        color=color.rgba(255,255,255,120)
    )
