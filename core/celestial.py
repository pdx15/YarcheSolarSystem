from ursina import *
import spiceypy as spice
from config import DISTANCE_SCALE

class CelestialBody(Entity):
    def __init__(self, name, texture, scale, spice_name=None, parent_body="SUN"):
        super().__init__(
            model='sphere',
            texture=texture,
            scale=scale,
            collider='sphere'
        )

        self.name = name
        self.spice_name = spice_name
        self.parent_body = parent_body

    def update_position(self, et, observer="SUN"):
        if self.spice_name:
            try:

                pos, _ = spice.spkpos(self.spice_name, et, "J2000", "NONE", observer)
                
                self.position = Vec3(
                    pos[0] * DISTANCE_SCALE,
                    pos[2] * DISTANCE_SCALE,
                    pos[1] * DISTANCE_SCALE
                )
            except Exception as e:
                print(f"Ошибка при вычислении позиции {self.name}: {e}")