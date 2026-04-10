from config import TIME_SCALE

class TimeController:
    def __init__(self, et):
        self.et = et
        self.scale = TIME_SCALE

    def update(self, dt):
        self.et += dt * self.scale
        return self.et