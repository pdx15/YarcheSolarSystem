import json
import spiceypy as spice

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
    except:
        pass

with open("unity_positions.json", "w") as f:
    json.dump(data, f)