import json
import spiceypy as spice

spice.furnsh("Assets/StreamingAssets/kernels/naif0012.tls")
spice.furnsh("Assets/StreamingAssets/kernels/de440.bsp")

et = spice.str2et("2025-01-01T00:00:00")

bodies = [
    "MERCURY BARYCENTER",
    "VENUS BARYCENTER",
    "EARTH BARYCENTER",
    "MARS BARYCENTER",
]

data = {}

for b in bodies:
    try:
        pos, _ = spice.spkpos(b, et, "J2000", "NONE", "SUN")
        data[b] = {
            "x": float(pos[0]),
            "y": float(pos[1]),
            "z": float(pos[2])
        }
    except Exception as e:
        print("Ошибка:", b, e)

with open("unity_positions.json", "w") as f:
    json.dump({"keys": list(data.keys()), "values": list(data.values())}, f, indent=2)

spice.kclear()