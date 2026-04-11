import math
import os
import random

import spiceypy as spice
from ursina import *

from config import DISTANCE_SCALE, SIZE_SCALE, TIME_SCALE
from core.celestial import CelestialBody
from core.orbit import create_real_orbit
from data.bodies import (
    BODY_SCALES,
    BODY_TEXTURES,
    PLANETARY_BODY_DEFINITIONS,
    PLANETARY_SATELLITE_FAMILIES,
    SATELLITE_SCALE_HINTS,
    SMALL_BODY_DEFINITIONS,
    SUN_SCALE,
    TNO_SYSTEM_DEFINITIONS,
)
from data.spice_loader import get_et, get_loaded_spk_targets, load_kernels


SATURN_RING_BANDS = (
    {"inner": 1.35, "outer": 1.58, "color": color.rgba(198, 184, 148, 110)},
    {"inner": 1.62, "outer": 1.92, "color": color.rgba(221, 205, 167, 150)},
    {"inner": 1.96, "outer": 2.22, "color": color.rgba(238, 225, 194, 105)},
)

ASTEROID_BELT_INNER_RADIUS_KM = 329_000_000
ASTEROID_BELT_OUTER_RADIUS_KM = 478_000_000
ASTEROID_BELT_COUNT = 450
MAX_SATELLITE_ORBITS_PER_SYSTEM = 24


def select_target(targets, available_targets):
    for target in targets:
        try:
            if int(target) in available_targets:
                return target
        except ValueError:
            continue
    return None


def resolve_name(target_code, fallback_name):
    try:
        return spice.bodc2n(int(target_code))
    except Exception:
        return fallback_name


def get_texture_path(body_name, fallback_name="MOON"):
    candidate = BODY_TEXTURES.get(body_name, BODY_TEXTURES.get(fallback_name))
    fallback = BODY_TEXTURES.get(fallback_name, BODY_TEXTURES["MOON"])

    if candidate and os.path.exists(candidate):
        return candidate
    if fallback and os.path.exists(fallback):
        return fallback
    return BODY_TEXTURES["MOON"]


def scaled_size(body_name):
    if body_name == "SUN":
        return SUN_SCALE
    return BODY_SCALES.get(body_name, BODY_SCALES["MOON"]) * SIZE_SCALE


def to_scaled_vec(position):
    return Vec3(
        position[0] * DISTANCE_SCALE,
        position[2] * DISTANCE_SCALE,
        position[1] * DISTANCE_SCALE,
    )


def get_scaled_position(target, et, observer):
    position, _ = spice.spkpos(target, et, "J2000", "NONE", observer)
    return to_scaled_vec(position)


def create_ring_mesh(inner_radius, outer_radius, segments=128):
    vertices = []
    uvs = []
    triangles = []

    for step in range(segments + 1):
        angle = (step / segments) * math.tau
        x = math.cos(angle)
        z = math.sin(angle)

        vertices.append(Vec3(x * outer_radius, 0, z * outer_radius))
        vertices.append(Vec3(x * inner_radius, 0, z * inner_radius))
        uvs.append((step / segments, 1))
        uvs.append((step / segments, 0))

    for step in range(segments):
        outer_index = step * 2
        inner_index = outer_index + 1
        next_outer = outer_index + 2
        next_inner = outer_index + 3

        triangles.extend(
            [
                outer_index,
                inner_index,
                next_outer,
                next_outer,
                inner_index,
                next_inner,
            ]
        )

    return Mesh(vertices=vertices, triangles=triangles, uvs=uvs, mode="triangle")


class SolarSystemScene(Entity):
    def __init__(self):
        super().__init__()
        self.kernel_paths = load_kernels()
        self.available_targets = get_loaded_spk_targets(self.kernel_paths)
        self.et = get_et()
        self.body_records = []
        self.body_lookup = {}
        self.satellite_records = []
        self.orbits = []

        self.sun = CelestialBody("SUN", get_texture_path("SUN"), SUN_SCALE, "10")
        self.sun_light = PointLight(parent=self.sun, intensity=5)
        self.ambient_light = AmbientLight(color=color.rgba(80, 80, 80, 51))
        self.asteroid_belt = self._create_asteroid_belt()

        self._create_planets()
        self._create_small_bodies()
        self._create_planetary_satellites()
        self._create_tno_satellites()
        self._create_saturn_rings()
        self._create_orbits()

    def _add_body(self, name, target, texture_name=None):
        if name in self.body_lookup:
            return self.body_lookup[name]

        body = CelestialBody(
            name,
            get_texture_path(texture_name or name),
            scaled_size(name),
            spice_name=target,
            parent_body="SUN",
        )
        record = {
            "name": name,
            "entity": body,
            "target": target,
        }
        self.body_lookup[name] = record
        self.body_records.append(record)
        return record

    def _add_satellite(self, name, target, observer, parent_name):
        texture_name = "MOON"
        scale = SATELLITE_SCALE_HINTS.get(int(target), BODY_SCALES.get(name, 0.08)) * SIZE_SCALE
        satellite = CelestialBody(
            name,
            get_texture_path(texture_name),
            scale,
            spice_name=target,
            parent_body=observer,
        )
        record = {
            "name": name,
            "entity": satellite,
            "target": target,
            "observer": observer,
            "parent_name": parent_name,
        }
        self.satellite_records.append(record)
        return record

    def _create_planets(self):
        for definition in PLANETARY_BODY_DEFINITIONS:
            target = select_target(definition["targets"], self.available_targets)
            if target:
                self._add_body(definition["name"], target)

    def _create_small_bodies(self):
        for definition in SMALL_BODY_DEFINITIONS:
            target = select_target(definition["targets"], self.available_targets)
            if target:
                self._add_body(definition["name"], target)

    def _create_planetary_satellites(self):
        for parent_name, family in PLANETARY_SATELLITE_FAMILIES.items():
            if parent_name not in self.body_lookup:
                continue

            observer = family["observer"]
            excluded_targets = {int(target) for target in family["planet_targets"]}

            if int(observer) not in self.available_targets:
                continue

            target_ids = sorted(
                body_id
                for body_id in self.available_targets
                if any(str(body_id).startswith(prefix) for prefix in family["prefixes"])
                and body_id not in excluded_targets
            )

            for body_id in target_ids:
                name = resolve_name(body_id, f"{parent_name}_{body_id}")
                self._add_satellite(name, str(body_id), observer, parent_name)

    def _create_tno_satellites(self):
        for system in TNO_SYSTEM_DEFINITIONS:
            parent = self.body_lookup.get(system["name"])
            observer = system["observer"]

            if not parent or int(observer) not in self.available_targets:
                continue

            for satellite in system["satellites"]:
                target = select_target(satellite["targets"], self.available_targets)
                if target:
                    self._add_satellite(satellite["name"], target, observer, system["name"])

    def _create_saturn_rings(self):
        saturn = self.body_lookup.get("SATURN")
        if not saturn:
            self.saturn_rings = []
            return

        self.saturn_rings = []
        saturn_entity = saturn["entity"]

        for index, band in enumerate(SATURN_RING_BANDS, start=1):
            mesh = create_ring_mesh(
                saturn_entity.scale_x * band["inner"],
                saturn_entity.scale_x * band["outer"],
            )
            ring = Entity(
                parent=saturn_entity,
                model=mesh,
                double_sided=True,
                unlit=True,
                rotation_x=90,
                y=index * 0.01,
                color=band["color"],
            )
            self.saturn_rings.append(ring)

    def _create_asteroid_belt(self):
        belt_parent = Entity(parent=self.sun)
        rng = random.Random(42)
        inner = ASTEROID_BELT_INNER_RADIUS_KM * DISTANCE_SCALE
        outer = ASTEROID_BELT_OUTER_RADIUS_KM * DISTANCE_SCALE

        for _ in range(ASTEROID_BELT_COUNT):
            radius = rng.uniform(inner, outer)
            angle = rng.uniform(0, math.tau)
            y_offset = rng.uniform(-0.18, 0.18)
            rock_scale = rng.uniform(0.015, 0.045) * SIZE_SCALE

            Entity(
                parent=belt_parent,
                model="cube",
                color=color.rgba(140, 132, 116, rng.randint(90, 160)),
                position=Vec3(math.cos(angle) * radius, y_offset, math.sin(angle) * radius),
                rotation=Vec3(
                    rng.uniform(0, 360),
                    rng.uniform(0, 360),
                    rng.uniform(0, 360),
                ),
                scale=rock_scale,
            )

        return belt_parent

    def _add_orbit(self, target, center, duration_days, steps, y_offset=0):
        orbit = create_real_orbit(target, center, self.et, duration_days=duration_days, steps=steps)
        if orbit:
            orbit.y = y_offset
            self.orbits.append(orbit)

    def _create_orbits(self):
        for record in self.body_records:
            if record["name"] == "SUN":
                continue

            duration_days = 3650
            steps = 300

            if record["name"] in {"PLUTO", "HAUMEA", "MAKEMAKE", "QUAOAR", "ORCUS", "ERIS", "SEDNA"}:
                duration_days = 20000
                steps = 360
            elif record["name"] in {"CERES", "PALLAS", "VESTA", "HYGIEA"}:
                duration_days = 2500
                steps = 240

            self._add_orbit(record["target"], "SUN", duration_days, steps, y_offset=-0.05)

        satellite_groups = {}
        for record in self.satellite_records:
            satellite_groups.setdefault(record["parent_name"], []).append(record)

        for records in satellite_groups.values():
            for record in records[:MAX_SATELLITE_ORBITS_PER_SYSTEM]:
                self._add_orbit(record["target"], record["observer"], 180, 180, y_offset=-0.02)

    def update(self):
        self.et += time.dt * TIME_SCALE
        self.sun.position = Vec3(0, 0, 0)

        for record in self.body_records:
            if record["name"] == "SUN":
                continue
            try:
                record["entity"].position = get_scaled_position(record["target"], self.et, "SUN")
            except Exception:
                continue

        for record in self.satellite_records:
            parent = self.body_lookup.get(record["parent_name"])
            if not parent:
                continue
            try:
                parent_position = parent["entity"].position
                relative_position = get_scaled_position(record["target"], self.et, record["observer"])
                record["entity"].position = parent_position + relative_position
            except Exception:
                continue
