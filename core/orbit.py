from ursina import *
import math

def create_orbit(radius):
    points = []
    for i in range(360):
        angle = math.radians(i)
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        points.append(Vec3(x, 0, z))

    return Entity(model=Mesh(vertices=points, mode='line'), color=color.white)