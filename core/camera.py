from ursina import *

class SimpleCamera(Entity):
    def __init__(self):
        super().__init__()
        camera.position = (0, 10, -30)
        camera.rotation = (0, 0, 0)
        self.move_speed = 50
        self.rotate_speed = 200
        # Зум через колесо убран, т.к. используется слайдер

    def update(self):
        # Вращение левой кнопкой мыши
        if mouse.left:
            camera.rotation_y += mouse.velocity[0] * self.rotate_speed
            camera.rotation_x -= mouse.velocity[1] * self.rotate_speed
            camera.rotation_x = clamp(camera.rotation_x, -90, 90)

        # Вращение правой кнопкой мыши (альтернатива)
        if mouse.right:
            camera.rotation_y += mouse.velocity[0] * self.rotate_speed
            camera.rotation_x -= mouse.velocity[1] * self.rotate_speed
            camera.rotation_x = clamp(camera.rotation_x, -90, 90)

        # Перемещение клавишами
        movement = Vec3(0, 0, 0)
        if held_keys['w']:
            movement += camera.forward
        if held_keys['s']:
            movement -= camera.forward
        if held_keys['d']:
            movement += camera.right
        if held_keys['a']:
            movement -= camera.right
        if held_keys['e']:
            movement += camera.up
        if held_keys['q']:
            movement -= camera.up

        if movement.length() > 0:
            camera.position += movement.normalized() * self.move_speed * time.dt