"""Build deterministic 26.3 structure templates from vanilla wood profiles.

Requires nbtlib (`python -m pip install nbtlib`). No game or server is needed.
The profiles are an original approximation of the GiantTrees 1.1 silhouettes;
this script does not incorporate the GPL Arbaro renderer.
"""

import math
import random
import json
from pathlib import Path

import nbtlib
from nbtlib import tag


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src/main/resources/data/giant_trees/structure"
PROFILES = {
    "oak": (46, 16, "round"),
    "birch": (49, 13, "round"),
    "spruce": (54, 13, "cone"),
    "jungle": (61, 18, "round"),
    "dark_oak": (43, 20, "broad"),
    "acacia": (38, 21, "umbrella"),
    "mangrove": (48, 19, "broad"),
    "cherry": (46, 18, "round"),
    "pale_oak": (45, 18, "broad"),
    "bamboo": (50, 13, "cone"),
    "crimson": (48, 18, "umbrella"),
    "warped": (50, 16, "round"),
}
SHAPES = ("round", "cone", "broad", "umbrella")
FOLIAGE = {"bamboo": "minecraft:azalea_leaves", "crimson": "minecraft:nether_wart_block", "warped": "minecraft:warped_wart_block"}
BIOMES = {
    "mangrove": ["mangrove_swamp"],
    "cherry": ["cherry_grove"],
    "pale_oak": ["pale_garden"],
    "bamboo": ["bamboo_jungle"],
    "crimson": ["crimson_forest"],
    "warped": ["warped_forest"],
}
DATA = ROOT / "src/main/resources/data/giant_trees"


def build(species, variant, shape=None):
    target_height, target_reach, native_shape = PROFILES[species]
    shape = shape or native_shape
    # Retain the original identifiers and random seeds for native silhouettes.
    template_name = f"{species}_{variant}" if shape == native_shape else f"{species}_{shape}_{variant}"
    rng = random.Random(f"giant_trees:{template_name}")
    height = target_height + rng.randint(-5, 5)
    reach = target_reach + rng.randint(-2, 2)
    wood = f"minecraft:{species}_{'stem' if species in ('crimson', 'warped') else 'block' if species == 'bamboo' else 'log'}"
    leaves = FOLIAGE.get(species, f"minecraft:{species}_leaves")
    placed = {}

    def put(x, y, z, name, axis=None):
        if y < 0:
            return
        state = (name, axis)
        key = (round(x), round(y), round(z))
        if name == leaves and key in placed and placed[key][0] == wood:
            return
        placed[key] = state

    def log_line(a, b, thickness=1):
        length = max(1, int(math.dist(a, b) * 2))
        delta = [b[i] - a[i] for i in range(3)]
        axis = "xyz"[max(range(3), key=lambda i: abs(delta[i]))]
        for i in range(length + 1):
            t = i / length
            x, y, z = [a[k] + delta[k] * t for k in range(3)]
            for dx in range(-thickness + 1, thickness):
                for dz in range(-thickness + 1, thickness):
                    if dx * dx + dz * dz < thickness * thickness + 0.5:
                        put(x + dx, y, z + dz, wood, axis)

    def canopy(cx, cy, cz, rx, ry, rz):
        for dx in range(-math.ceil(rx), math.ceil(rx) + 1):
            for dy in range(-math.ceil(ry), math.ceil(ry) + 1):
                for dz in range(-math.ceil(rz), math.ceil(rz) + 1):
                    d = (dx / rx) ** 2 + (dy / ry) ** 2 + (dz / rz) ** 2
                    if d <= 1 and (d < 0.78 or rng.random() > 0.18):
                        put(cx + dx, cy + dy, cz + dz, leaves)

    # Thick tapering trunk and buttress roots. All structure coordinates start
    # at ground level, allowing a heightmap-projected jigsaw to place it.
    base = 3 if species in ("jungle", "dark_oak") else 2
    for y in range(height + 1):
        thickness = base if y < height * 0.22 else (2 if y < height * 0.65 else 1)
        for dx in range(-thickness + 1, thickness):
            for dz in range(-thickness + 1, thickness):
                if dx * dx + dz * dz < thickness * thickness + 0.5:
                    put(dx, y, dz, wood, "y")
    for angle in range(0, 360, 60):
        rad = math.radians(angle + rng.randrange(-12, 13))
        end = (math.cos(rad) * (base + 4), 0, math.sin(rad) * (base + 4))
        log_line((0, 4, 0), end)

    if shape == "cone":
        for y in range(12, height, 3):
            ring = reach * (1 - y / (height + 6))
            for j in range(9):
                a = 2 * math.pi * j / 9 + rng.uniform(-0.14, 0.14)
                span = ring * rng.uniform(0.75, 1.1)
                tip = (math.cos(a) * span, y - 2, math.sin(a) * span)
                log_line((0, y + 1, 0), tip)
                canopy(*tip, 2.6, 2.0, 2.6)
        canopy(0, height, 0, 3, 4, 3)
    else:
        count = 24 if shape == "broad" else (18 if shape == "umbrella" else 17)
        for i in range(count):
            a = (2 * math.pi * i / count) + rng.uniform(-0.2, 0.2)
            if shape == "umbrella":
                start_y = rng.randint(int(height * 0.55), int(height * 0.83))
                end_y = rng.randint(height - 4, height + 3)
                span = rng.uniform(reach * 0.5, reach)
            elif shape == "broad":
                start_y = rng.randint(int(height * 0.38), int(height * 0.8))
                end_y = start_y + rng.randint(3, 12)
                span = rng.uniform(reach * 0.5, reach)
            else:
                start_y = rng.randint(int(height * 0.45), int(height * 0.89))
                end_y = start_y + rng.randint(2, 10)
                span = rng.uniform(reach * 0.42, reach)
            tip = (math.cos(a) * span, end_y, math.sin(a) * span)
            mid = (tip[0] * 0.55, start_y + (end_y - start_y) * 0.68 + 2, tip[2] * 0.55)
            log_line((0, start_y, 0), mid, 2 if shape == "broad" and i % 3 == 0 else 1)
            log_line(mid, tip)
            if shape == "umbrella":
                canopy(*tip, 5.5, 2.0, 5.5)
            else:
                canopy(*tip, 4.0 if species == "jungle" else 5.0, 3.1, 4.0 if species == "jungle" else 5.0)
        canopy(0, height, 0, 7 if shape == "broad" else 5, 4, 7 if shape == "broad" else 5)

    xs = [p[0] for p in placed]
    ys = [p[1] for p in placed]
    zs = [p[2] for p in placed]
    xmin, zmin = min(xs), min(zs)
    states = sorted(set(placed.values()))
    palette_index = {state: i for i, state in enumerate(states)}
    palette = tag.List[tag.Compound]()
    for name, axis in states:
        # DataVersion 5023 uses the 26.3 block-state encoding. The older
        # Name/Properties keys silently resolve to air at this version.
        state = tag.Compound({"id": tag.String(name)})
        if axis:
            state["properties"] = tag.Compound({"axis": tag.String(axis)})
        elif name.endswith("_leaves"):
            state["properties"] = tag.Compound({"persistent": tag.String("true"), "distance": tag.String("7")})
        palette.append(state)
    blocks = tag.List[tag.Compound]()
    for (x, y, z), state in sorted(placed.items(), key=lambda p: (p[0][1], p[0][0], p[0][2])):
        blocks.append(tag.Compound({
            "pos": tag.List[tag.Int]([x - xmin, y, z - zmin]),
            "state": tag.Int(palette_index[state]),
        }))
    root = nbtlib.File({
        "DataVersion": tag.Int(5023),
        "size": tag.List[tag.Int]([max(xs) - xmin + 1, max(ys) + 1, max(zs) - zmin + 1]),
        "palette": palette,
        "blocks": blocks,
        "entities": tag.List[tag.Compound](),
    }, gzipped=True)
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{template_name}.nbt"
    root.save(dest)
    print(dest.name, tuple(root["size"]), len(blocks))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def make_worldgen(species):
    native = PROFILES[species][2]
    names = [f"{species}_{variant}" if shape == native else f"{species}_{shape}_{variant}"
             for shape in SHAPES for variant in range(1, 4)]
    for name in names:
        write_json(DATA / "worldgen/template_pool" / f"{name}.json", {
            "name": f"giant_trees:{name}", "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {"element_type": "minecraft:single_pool_element",
                "projection": "rigid", "location": f"giant_trees:{name}", "processors": "minecraft:empty"}}],
        })
        write_json(DATA / "worldgen/structure" / f"{name}.json", {
            "type": "minecraft:jigsaw", "biomes": f"#giant_trees:has_structure/{species}",
            "max_distance_from_center": 128, "size": 1, "spawn_overrides": {},
            "start_height": {"absolute": 0}, "project_start_to_heightmap": "WORLD_SURFACE_WG",
            "start_pool": f"giant_trees:{name}", "step": "surface_structures",
            "terrain_adaptation": "none", "use_expansion_hack": False,
        })
    old_set = DATA / "worldgen/structure_set" / f"{species}.json"
    placement = json.loads(old_set.read_text())["placement"] if old_set.exists() else {
        "type": "minecraft:random_spread", "salt": 19860930 + sum(map(ord, species)),
        "spacing": 18, "separation": 9,
    }
    write_json(old_set, {"structures": [{"structure": f"giant_trees:{name}", "weight": 1} for name in names],
                         "placement": placement})
    if species in BIOMES:
        write_json(DATA / "tags/worldgen/biome/has_structure" / f"{species}.json",
                   {"replace": False, "values": [f"minecraft:{biome}" for biome in BIOMES[species]]})


def update_config():
    for filename in ("giant_trees_placement.json", "giant_trees_enable_disable.json"):
        path = ROOT / "src/main/resources/data/cristellib/structure_config" / filename
        config = json.loads(path.read_text())
        config["structure_sets"][0]["structure_set"] = [f"giant_trees:{species}" for species in PROFILES]
        write_json(path, config)


if __name__ == "__main__":
    for species in PROFILES:
        for shape in SHAPES:
            for variant in range(1, 4):
                build(species, variant, shape)
        make_worldgen(species)
    update_config()
