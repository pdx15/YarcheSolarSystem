PLANETS = {
    "MERCURY": "MERCURY BARYCENTER",
    "VENUS": "VENUS BARYCENTER", 
    "EARTH": "EARTH BARYCENTER",
    "MARS": "MARS BARYCENTER",
    "JUPITER": "JUPITER BARYCENTER",
    "SATURN": "SATURN BARYCENTER",
    "URANUS": "URANUS BARYCENTER",
    "NEPTUNE": "NEPTUNE BARYCENTER"
}

JUPITER_MOONS = {
    "IO": "IO",
    "EUROPA": "EUROPA",
    "GANYMEDE": "GANYMEDE",
    "CALLISTO": "CALLISTO"
}

SATURN_MOONS = {
    "MIMAS": "MIMAS",
    "ENCELADUS": "ENCELADUS",
    "TETHYS": "TETHYS",
    "DIONE": "DIONE",
    "RHEA": "RHEA",
    "TITAN": "TITAN",
    "HYPERION": "HYPERION",
    "IAPETUS": "IAPETUS",
    "PHOEBE": "PHOEBE",
    "HELENE": "HELENE",
    "TELESTO": "TELESTO",
    "CALYPSO": "CALYPSO",
    "METHONE": "METHONE",
    "POLYDEUCES": "POLYDEUCES"
}

MARS_MOONS = {
    "PHOBOS": "PHOBOS",
    "DEIMOS": "DEIMOS"
}

MARS_MOON_SCALES = {
    "PHOBOS": 0.18,
    "DEIMOS": 0.14
}

JUPITER_MOON_SCALES = {
    "IO": 0.32,
    "EUROPA": 0.28,
    "GANYMEDE": 0.38,
    "CALLISTO": 0.34
}

SATURN_MOON_SCALES = {
    "MIMAS": 0.12,
    "ENCELADUS": 0.15,
    "TETHYS": 0.19,
    "DIONE": 0.18,
    "RHEA": 0.23,
    "TITAN": 0.42,
    "HYPERION": 0.12,
    "IAPETUS": 0.21,
    "PHOEBE": 0.10,
    "HELENE": 0.08,
    "TELESTO": 0.08,
    "CALYPSO": 0.08,
    "METHONE": 0.07,
    "POLYDEUCES": 0.07
}

PLANET_SCALES = {
    "MERCURY": 0.38,
    "VENUS": 0.95,
    "EARTH": 1,
    "MARS": 0.53,
    "JUPITER": 11.2,
    "SATURN": 9.45,
    "URANUS": 4,
    "NEPTUNE": 3.9,
    "PLUTO": 0.19
}

SUN_SCALE = 10

BODY_TEXTURES = {
    "SUN": "assets/textures/sun.jpg",
    "MERCURY": "assets/textures/mercury.jpg",
    "VENUS": "assets/textures/venus.jpg",
    "EARTH": "assets/textures/earth.jpg",
    "MARS": "assets/textures/mars.jpg",
    "JUPITER": "assets/textures/jupiter.jpg",
    "SATURN": "assets/textures/saturn.jpg",
    "URANUS": "assets/textures/uranus.jpg",
    "NEPTUNE": "assets/textures/neptune.jpg",
    "MOON": "assets/textures/moon.jpg",
    "PLUTO": "assets/textures/pluto.jpg",
    "CERES": "assets/textures/ceres.jpg",
    "PALLAS": "assets/textures/pallas.jpg",
    "VESTA": "assets/textures/vesta.jpg",
    "HYGIEA": "assets/textures/hygiea.jpg",
    "HAUMEA": "assets/textures/haumea.jpg",
    "MAKEMAKE": "assets/textures/makemake.jpg",
    "QUAOAR": "assets/textures/quaoar.jpg",
    "ORCUS": "assets/textures/orcus.jpg",
    "ERIS": "assets/textures/eris.jpg",
    "SEDNA": "assets/textures/sedna.jpg",
}

BODY_SCALES = {
    "SUN": SUN_SCALE,
    **PLANET_SCALES,
    "MOON": 0.27,
    "CERES": 0.11,
    "PALLAS": 0.08,
    "VESTA": 0.09,
    "HYGIEA": 0.07,
    "HAUMEA": 0.12,
    "MAKEMAKE": 0.11,
    "QUAOAR": 0.09,
    "ORCUS": 0.08,
    "ERIS": 0.12,
    "SEDNA": 0.06,
    "CHARON": 0.10,
    "NIX": 0.03,
    "HYDRA": 0.03,
    "KERBEROS": 0.02,
    "STYX": 0.02,
    "WEYWOT": 0.025,
    "VANTH": 0.035,
    "DYSNOMIA": 0.035,
    "MK2": 0.03,
    "HIIAKA": 0.045,
    "NAMAKA": 0.03,
}

PLANETARY_BODY_DEFINITIONS = [
    {"name": "MERCURY", "targets": ["199", "1"]},
    {"name": "VENUS", "targets": ["299", "2"]},
    {"name": "EARTH", "targets": ["399", "3"]},
    {"name": "MARS", "targets": ["499", "4"]},
    {"name": "JUPITER", "targets": ["599", "5"]},
    {"name": "SATURN", "targets": ["699", "6"]},
    {"name": "URANUS", "targets": ["799", "7"]},
    {"name": "NEPTUNE", "targets": ["899", "8"]},
    {"name": "PLUTO", "targets": ["999", "9"]},
]

PLANETARY_SATELLITE_FAMILIES = {
    "EARTH": {"planet_targets": ["399", "3"], "observer": "399", "ranges": ((301, 399),)},
    "MARS": {"planet_targets": ["499", "4"], "observer": "499", "ranges": ((401, 499),)},
    "JUPITER": {"planet_targets": ["599", "5"], "observer": "599", "ranges": ((501, 599), (55501, 55600))},
    "SATURN": {"planet_targets": ["699", "6"], "observer": "699", "ranges": ((601, 699), (65286, 65350))},
    "URANUS": {"planet_targets": ["799", "7"], "observer": "799", "ranges": ((701, 799), (75051, 75100))},
    "NEPTUNE": {"planet_targets": ["899", "8"], "observer": "899", "ranges": ((801, 899),)},
    "PLUTO": {"planet_targets": ["999", "9"], "observer": "999", "ranges": ((901, 999),)},
}

SMALL_BODY_DEFINITIONS = [
    {"name": "CERES", "targets": ["2000001"]},
    {"name": "PALLAS", "targets": ["2000002"]},
    {"name": "VESTA", "targets": ["2000004"]},
    {"name": "HYGIEA", "targets": ["2000010"]},
    {"name": "HAUMEA", "targets": ["20136108"]},
    {"name": "MAKEMAKE", "targets": ["20136472"]},
    {"name": "QUAOAR", "targets": ["20050000"]},
    {"name": "ORCUS", "targets": ["20090482"]},
    {"name": "ERIS", "targets": ["20136199"]},
    {"name": "SEDNA", "targets": ["20090377"]},
]

TNO_SYSTEM_DEFINITIONS = [
    {
        "name": "MAKEMAKE",
        "planet_targets": ["20136472"],
        "observer": "20136472",
        "satellites": [
            {"name": "MK2", "targets": ["120136472"]},
        ],
    },
    {
        "name": "HAUMEA",
        "planet_targets": ["20136108"],
        "observer": "20136108",
        "satellites": [
            {"name": "HIIAKA", "targets": ["120136108"]},
            {"name": "NAMAKA", "targets": ["220136108"]},
        ],
    },
    {
        "name": "QUAOAR",
        "planet_targets": ["20050000"],
        "observer": "20050000",
        "satellites": [
            {"name": "WEYWOT", "targets": ["120050000"]},
        ],
    },
    {
        "name": "ORCUS",
        "planet_targets": ["20090482"],
        "observer": "20090482",
        "satellites": [
            {"name": "VANTH", "targets": ["120090482"]},
        ],
    },
    {
        "name": "ERIS",
        "planet_targets": ["20136199"],
        "observer": "20136199",
        "satellites": [
            {"name": "DYSNOMIA", "targets": ["120136199"]},
        ],
    },
]

SATELLITE_SCALE_HINTS = {
    301: BODY_SCALES["MOON"],
    401: MARS_MOON_SCALES["PHOBOS"],
    402: MARS_MOON_SCALES["DEIMOS"],
    501: JUPITER_MOON_SCALES["IO"],
    502: JUPITER_MOON_SCALES["EUROPA"],
    503: JUPITER_MOON_SCALES["GANYMEDE"],
    504: JUPITER_MOON_SCALES["CALLISTO"],
    601: SATURN_MOON_SCALES["MIMAS"],
    602: SATURN_MOON_SCALES["ENCELADUS"],
    603: SATURN_MOON_SCALES["TETHYS"],
    604: SATURN_MOON_SCALES["DIONE"],
    605: SATURN_MOON_SCALES["RHEA"],
    606: SATURN_MOON_SCALES["TITAN"],
    607: SATURN_MOON_SCALES["HYPERION"],
    608: SATURN_MOON_SCALES["IAPETUS"],
    609: SATURN_MOON_SCALES["PHOEBE"],
    612: SATURN_MOON_SCALES["HELENE"],
    613: SATURN_MOON_SCALES["TELESTO"],
    614: SATURN_MOON_SCALES["CALYPSO"],
    632: SATURN_MOON_SCALES["METHONE"],
    634: SATURN_MOON_SCALES["POLYDEUCES"],
    901: BODY_SCALES["CHARON"],
    902: BODY_SCALES["NIX"],
    903: BODY_SCALES["HYDRA"],
    904: BODY_SCALES["KERBEROS"],
    905: BODY_SCALES["STYX"],
}
