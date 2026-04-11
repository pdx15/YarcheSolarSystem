from ursina import *
from core.camera import SimpleCamera
from core.solar_system_scene import SolarSystemScene
from core.time_controller import TimeController
from data.api import get_body_info
from config import TIME_SCALE
import spiceypy as spice
import os

class SimulationUI(Entity):
    def __init__(self, time_ctrl, scene):
        super().__init__(parent=camera.ui)
        self.time_ctrl = time_ctrl
        self.scene = scene

        self.date_text = Text(
            text="Загрузка даты...",
            position=(-0.85, 0.45),
            origin=(-0.5, 0.5),
            scale=2
        )

        self.speed_slider = Slider(
            min=0, max=2000, default=TIME_SCALE, step=10,
            position=(-0.85, -0.4), scale=(0.3, 0.02),
            dynamic=True,
            on_value_changed=self.on_speed_change
        )
        self.speed_label = Text(
            text=f"Скорость: {TIME_SCALE}x",
            position=(-0.85, -0.35),
            scale=1.5
        )

        self.zoom_slider = Slider(
            min=5, max=200, default=30, step=1,
            position=(-0.85, -0.45), scale=(0.3, 0.02),
            dynamic=True,
            on_value_changed=self.on_zoom_change
        )
        self.zoom_label = Text(
            text="Расстояние камеры: 30",
            position=(-0.85, -0.5),
            scale=1.5
        )

        self.info_panel = Text(
            text="Кликните по объекту",
            position=(0.7, 0.4),
            origin=(0, 0),
            scale=1.8,
            line_height=1.5
        )

        self.last_clicked = None

    def on_speed_change(self):
        val = self.speed_slider.value
        self.time_ctrl.set_scale(val)
        self.speed_label.text = f"Скорость: {val:.0f}x"

    def on_zoom_change(self):
        dist = self.zoom_slider.value
        forward = camera.forward
        if forward.length() > 0:
            camera.position = -forward.normalized() * dist
        self.zoom_label.text = f"Расстояние камеры: {dist:.0f}"

    def update(self):
        et = self.time_ctrl.et
        try:
            utc_str = spice.et2utc(et, "C", 0)
            self.date_text.text = f"Дата: {utc_str}"
        except Exception:
            self.date_text.text = f"ET: {et:.2f}"

    def input(self, key):
        if key == 'left mouse down':
            self.check_click()

    def check_click(self):
        hit = mouse.hovered_entity
        if hit is None:
            self.info_panel.text = "Кликните по объекту"
            return

        if hasattr(hit, 'parent') and hit.parent == camera.ui:
            return

        obj_name = getattr(hit, 'name', None) or "Неизвестный объект"
        info = self.scene.get_body_info(hit)
        if info:
            name = info['name']
            try:
                api_info = get_body_info(name)
                self.info_panel.text = f"Выбрано: {name}\n{api_info}"
            except Exception as e:
                self.info_panel.text = f"Выбрано: {name}\nОшибка API: {e}"
            self.last_clicked = hit
        else:
            self.info_panel.text = f"Объект: {obj_name}\nНет данных в сцене"


def main():
    app = Ursina()

    scene = SolarSystemScene()
    time_ctrl = TimeController(scene.et, TIME_SCALE)

    cam = SimpleCamera()
    camera.position = (0, 10, -30)

    sky_path = "assets/textures/stars_milky_way.jpg"
    if os.path.exists(sky_path):
        Sky(texture=sky_path)
    else:
        print(f"Предупреждение: текстура неба не найдена: {sky_path}")

    ui = SimulationUI(time_ctrl, scene)

    def update():
        dt = time.dt
        scene.et = time_ctrl.update(dt)
        scene.update()
        ui.update()

    app.update = update
    app.run()


if __name__ == "__main__":
    main()