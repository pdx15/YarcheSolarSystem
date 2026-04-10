from ursina import *
import spiceypy as spice
from config import DISTANCE_SCALE

class CelestialBody(Entity):
    def __init__(self, name, texture, scale, spice_name=None, parent=None):
        super().__init__(
            model='sphere',
            texture=texture,
            scale=scale,
            collider='sphere'
        )

        self.name = name
        self.spice_name = spice_name
        self.parent_body = parent

    def update_position(self, et, observer="SUN"):
        if self.spice_name:
            pos, _ = spice.spkpos(self.spice_name, et, "J2000", "NONE", observer)

            self.position = Vec3(
                pos[0] * DISTANCE_SCALE,
                pos[2] * DISTANCE_SCALE,
                pos[1] * DISTANCE_SCALE
            )