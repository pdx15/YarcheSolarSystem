import spiceypy as spice
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kernels_path = os.path.join(project_root, "data", "kernels")

print(f"Поиск файлов в: {kernels_path}")

tls_file = os.path.join(kernels_path, "naif0012.tls")
bsp_file = os.path.join(kernels_path, "de440.bsp")

if not os.path.exists(tls_file):
    print(f"Файл не найден: {tls_file}")
    exit(1)
if not os.path.exists(bsp_file):
    print(f"Файл не найден: {bsp_file}")
    exit(1)

spice.furnsh(tls_file)
spice.furnsh(bsp_file)

print("Файлы успешно загружены!\n")

et = spice.str2et("2025-01-01T00:00:00")

planets = ["MERCURY BARYCENTER", "VENUS BARYCENTER", "EARTH BARYCENTER", 
           "MARS BARYCENTER", "JUPITER BARYCENTER", "SATURN BARYCENTER",
           "URANUS BARYCENTER", "NEPTUNE BARYCENTER"]

print("Доступные эфемериды планет:")
for planet in planets:
    try:
        pos, _ = spice.spkpos(planet, et, "J2000", "NONE", "SUN")
        print(f"✓ {planet}: {pos}")
    except Exception as e:
        print(f"✗ {planet}: {e}")

moons = ["PHOBOS", "DEIMOS", "IO", "EUROPA", "GANYMEDE", "CALLISTO", "TITAN"]
print("\nЛуны:")
for moon in moons:
    try:
        pos, _ = spice.spkpos(moon, et, "J2000", "NONE", "SUN")
        print(f"✓ {moon}: {pos}")
    except Exception as e:
        print(f"✗ {moon}: {e}")

print("\nОтносительные позиции:")
try:
    pos, _ = spice.spkpos("PHOBOS", et, "J2000", "NONE", "MARS BARYCENTER")
    print(f"✓ PHOBOS относительно MARS BARYCENTER: {pos}")
except Exception as e:
    print(f"✗ PHOBOS относительно MARS BARYCENTER: {e}")

spice.kclear()