"""Build deterministic 26.3 structure templates from six giant-tree profiles.

Requires nbtlib (`python -m pip install nbtlib`). No game or server is needed.
The profiles are an original approximation of the GiantTrees 1.1 silhouettes;
this script does not incorporate the GPL Arbaro renderer.
"""

import math
import random
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
}


def build(species, variant):
    target_height, target_reach, shape = PROFILES[species]
    rng = random.Random(f"giant_trees:{species}:{variant}")
    height = target_height + rng.randint(-5, 5)
    reach = target_reach + rng.randint(-2, 2)
    wood = f"minecraft:{species}_log"
    leaves = f"minecraft:{species}_leaves"
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
        elif name == leaves:
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
    dest = OUT / f"{species}_{variant}.nbt"
    root.save(dest)
    print(dest.name, tuple(root["size"]), len(blocks))


if __name__ == "__main__":
    for species in PROFILES:
        for variant in range(1, 4):
            build(species, variant)
