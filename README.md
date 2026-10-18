# Giant Trees for Fabric 26.3

An independent, data-driven reimagining inspired by Ryan Michela's GiantTrees
1.1 Bukkit plugin. It generates giant versions of all twelve vanilla wood
families: oak, birch, spruce, jungle, dark oak, acacia, mangrove, cherry,
pale oak, bamboo, crimson, and warped. Each has round, conical, broad, and
umbrella silhouettes, with three variations per silhouette (144 templates).
They generate in matching biomes, including crimson and warped forests.
The bamboo giants use bamboo blocks and azalea leaves; the Nether giants
use their matching stems and wart blocks.

Version 0.3.0 adds enchanted saplings for manual planting. Version 0.2.0
expanded the species and shapes. Version 0.1.1 corrected the
structure palette for Minecraft 26.3; version 0.1.0 could report a successful
`/place` without placing blocks.

This release does **not** contain the original GPLv3 Arbaro/Bukkit code or its
XML presets. The structures are newly generated approximations of those
species' scale and silhouettes. It does not yet include the original custom
sapling planting pattern, commands, editable species XML, or root system.

## Requirements

- Minecraft Java 26.3
- Fabric Loader 0.19.5 or newer
- Cristel Lib 3.1.12 or newer

Install the JAR in `mods/` alongside Cristel Lib. Explore new terrain; old
chunks will not gain trees. Each species has twelve variants and an independent
structure set with 18-chunk spacing and 9-chunk separation. Eligible biomes
are in `data/giant_trees/tags/worldgen/biome/has_structure/`. Cristel Lib
provides placement and enable/disable settings under `config/giant_trees/`.

The Overworld trees contain ordinary logs or bamboo blocks and persistent
leaves; Nether trees contain stems and wart blocks. They use native
heightmap-projected structures, so `/locate structure giant_trees:oak_1` can
find a generated variant. For a manual visual test, stand on open ground and
use `/place template giant_trees:oak_1 ~ ~ ~`. The trunk will be about 16
blocks east and south of the command position. `/place structure` projects
to terrain height and offsets the template, so its reported position is not
the trunk position.

## Enchanted saplings

Craft on a 3×3 table with four emeralds in the corners, four enchanted books
containing **Fortune III** on the cardinal sides, and the matching sapling in
the center. Fortune II and ordinary enchanted books do not match. For mangrove
use a propagule, for bamboo use bamboo, and for crimson or warped use the
matching fungus. The result is a shimmering sapling of that species.

Plant it on sturdy ground. It grows into one of that species' twelve giant
templates with time, or immediately when bone meal is applied. The full tree
must fit within loaded chunks and the world height limit; otherwise the
sapling remains in place until the area is loaded. Breaking a planted sapling
returns it. Allow ample open space around the sapling before growing it.

## Rebuild structures

`python -m pip install nbtlib` then `python tools/generate_trees.py` regenerates
the deterministic NBT templates. The generated templates are committed, so
Python is not required to build or play the mod.

The original project: https://github.com/rmichela/GiantTrees (GPLv3). This
repository's independently written code and generated structures are MIT.
