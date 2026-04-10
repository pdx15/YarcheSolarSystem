from ursina import *

class SimpleCamera(Entity):
    def __init__(self):
        super().__init__()
        camera.position = (0, 20, -50)

    def update(self):
        if mouse.right:
            camera.rotation_y += mouse.velocity[0] * 100
            camera.rotation_x -= mouse.velocity[1] * 100

        camera.position += camera.forward * mouse.wheel[1] * 20