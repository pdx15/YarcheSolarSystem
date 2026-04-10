import spiceypy as spice
import os

def load_kernels():
    base = "data/kernels/"

    spice.furnsh(os.path.join(base, "naif0012.tls"))
    spice.furnsh(os.path.join(base, "de440.bsp"))
    spice.furnsh(os.path.join(base, "mar097.bsp"))
    spice.furnsh(os.path.join(base, "jup365.bsp"))
    spice.furnsh(os.path.join(base, "sat441.bsp"))
    
def get_et():
    return spice.str2et("2025-01-01T00:00:00")

def advance_et(et, dt, scale):
    return et + dt * scale