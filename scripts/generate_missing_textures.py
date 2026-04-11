import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


SIZE = (1024, 512)
OUTPUT_DIR = Path("assets/textures")


TEXTURE_SPECS = {
    "pluto.jpg": {
        "seed": 1,
        "base": (170, 145, 120),
        "bands": [(84, (110, 80, 70)), (220, (215, 195, 175)), (360, (95, 70, 66))],
        "spots": [((0.28, 0.42), 0.22, (235, 220, 200)), ((0.72, 0.55), 0.18, (110, 85, 78))],
    },
    "pallas.jpg": {
        "seed": 2,
        "base": (124, 122, 110),
        "bands": [(120, (98, 102, 90)), (290, (150, 146, 132))],
        "spots": [((0.34, 0.36), 0.12, (165, 160, 146)), ((0.66, 0.66), 0.15, (90, 90, 82))],
    },
    "vesta.jpg": {
        "seed": 3,
        "base": (132, 128, 124),
        "bands": [(90, (88, 88, 92)), (250, (178, 170, 162)), (410, (110, 106, 112))],
        "spots": [((0.47, 0.55), 0.18, (210, 202, 196)), ((0.2, 0.28), 0.10, (72, 74, 78))],
    },
    "hygiea.jpg": {
        "seed": 4,
        "base": (78, 82, 74),
        "bands": [(150, (54, 58, 52)), (340, (112, 116, 104))],
        "spots": [((0.58, 0.46), 0.16, (96, 106, 94)), ((0.3, 0.7), 0.11, (48, 54, 48))],
    },
    "quaoar.jpg": {
        "seed": 5,
        "base": (150, 106, 88),
        "bands": [(110, (178, 118, 94)), (300, (116, 84, 74)), (415, (188, 166, 144))],
        "spots": [((0.68, 0.34), 0.13, (220, 210, 198)), ((0.22, 0.62), 0.12, (116, 76, 68))],
    },
    "orcus.jpg": {
        "seed": 6,
        "base": (122, 132, 144),
        "bands": [(126, (98, 108, 126)), (278, (164, 172, 182)), (402, (124, 92, 92))],
        "spots": [((0.52, 0.48), 0.16, (196, 204, 214)), ((0.74, 0.63), 0.11, (108, 78, 78))],
    },
    "sedna.jpg": {
        "seed": 7,
        "base": (132, 68, 52),
        "bands": [(96, (166, 78, 56)), (246, (102, 42, 34)), (390, (188, 116, 82))],
        "spots": [((0.36, 0.44), 0.14, (214, 150, 110)), ((0.7, 0.3), 0.10, (86, 34, 30))],
    },
}


def clamp(value):
    return max(0, min(255, int(value)))


def blend(a, b, t):
    return tuple(clamp((1 - t) * av + t * bv) for av, bv in zip(a, b))


def add_noise(color, amount):
    return tuple(clamp(channel + amount) for channel in color)


def make_texture(filename, spec):
    rng = random.Random(spec["seed"])
    image = Image.new("RGB", SIZE, spec["base"])
    pixels = image.load()
    width, height = SIZE

    for y in range(height):
        v = y / max(1, height - 1)
        lat_wave = math.sin(v * math.pi)

        for x in range(width):
            u = x / max(1, width - 1)
            color = spec["base"]

            for center_x, band_color in spec["bands"]:
                distance = abs(x - center_x)
                if distance > width / 2:
                    distance = width - distance
                strength = max(0.0, 1.0 - distance / 180)
                color = blend(color, band_color, strength * 0.55 * lat_wave)

            noise = (
                math.sin((u * 11.0 + v * 3.7 + spec["seed"]) * math.tau)
                + math.cos((u * 4.3 - v * 8.1 + spec["seed"] * 0.3) * math.tau)
                + rng.uniform(-0.35, 0.35)
            )
            color = add_noise(color, noise * 18)
            pixels[x, y] = color

    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for (cx, cy), radius, color in spec["spots"]:
        x0 = int((cx - radius) * width)
        y0 = int((cy - radius) * height)
        x1 = int((cx + radius) * width)
        y1 = int((cy + radius) * height)
        alpha = 95 if sum(color) > 380 else 75
        draw.ellipse((x0, y0, x1, y1), fill=(*color, alpha))

    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=28))
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    image = image.filter(ImageFilter.GaussianBlur(radius=0.6))

    output_path = OUTPUT_DIR / filename
    image.save(output_path, quality=94)
    print(f"Generated {output_path}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, spec in TEXTURE_SPECS.items():
        make_texture(filename, spec)


if __name__ == "__main__":
    main()
