from skyfield.api import load

ts = load.timescale()
planets = load('de421.bsp')

def get_time():
    return ts.now()

def advance_time(t, dt, scale):
    return ts.tt_jd(t.tt + dt * scale)