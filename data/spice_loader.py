import spiceypy as spice
import os

KERNEL_PATH = "data/kernels/"

def load_kernels():
    for file in os.listdir(KERNEL_PATH):
        if file.endswith(".bsp") or file.endswith(".tls"):
            spice.furnsh(os.path.join(KERNEL_PATH, file))

def get_et():
    return spice.str2et("2025-01-01T00:00:00")

def advance_et(et, dt, scale):
    return et + dt * scale