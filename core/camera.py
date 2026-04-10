from ursina import *

class SimpleCamera(Entity):
    def __init__(self):
        super().__init__()
        camera.position = (0, 20, -50)
        self.zoom_speed = 20

    def update(self):
        if mouse.right:
            camera.rotation_y += mouse.velocity[0] * 100 * time.dt
            camera.rotation_x -= mouse.velocity[1] * 100 * time.dt
            camera.rotation_x = clamp(camera.rotation_x, -90, 90)

        if held_keys['+'] or held_keys['=']:
            camera.position += camera.forward * self.zoom_speed * time.dt
        if held_keys['-']:
            camera.position -= camera.forward * self.zoom_speed * time.dt

        if held_keys['q']:
            camera.position += camera.forward * self.zoom_speed * time.dt
        if held_keys['e']:
            camera.position -= camera.forward * self.zoom_speed * time.dt