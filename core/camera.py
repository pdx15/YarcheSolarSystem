from ursina import *

class SimpleCamera(Entity):
    def __init__(self):
        super().__init__()

        camera.position = (0, 0, -50)
        camera.rotation = (0, 0, 0)

        self.speed = 80

    def update(self):
        if held_keys['w']:
            camera.position += camera.forward * self.speed * time.dt
        if held_keys['s']:
            camera.position -= camera.forward * self.speed * time.dt
        if held_keys['a']:
            camera.position -= camera.right * self.speed * time.dt
        if held_keys['d']:
            camera.position += camera.right * self.speed * time.dt

        if mouse.right:
            camera.rotation_y += mouse.velocity[0] * 200
            camera.rotation_x -= mouse.velocity[1] * 200
            camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    def input(self, key):
        if key == 'scroll up':
            camera.position += camera.forward * 5
        if key == 'scroll down':
            camera.position -= camera.forward * 5