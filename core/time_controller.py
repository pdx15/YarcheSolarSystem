class TimeController:
    def __init__(self, initial_et, time_scale=500):
        self.et = initial_et
        self.time_scale = time_scale

    def update(self, dt):
        self.et += dt * self.time_scale
        return self.et

    def set_scale(self, scale):
        self.time_scale = scale

    def get_scale(self):
        return self.time_scale