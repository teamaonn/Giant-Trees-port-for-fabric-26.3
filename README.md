# Giant Trees for Fabric 26.3

An independent, data-driven reimagining inspired by Ryan Michela's GiantTrees
1.1 Bukkit plugin. It generates giant oak, birch, spruce, jungle, dark oak,
and acacia trees in matching Overworld biomes. The archive's natural-generation
setting was enabled; this port starts with that feature.

This release does **not** contain the original GPLv3 Arbaro/Bukkit code or its
XML presets. The 18 structures are newly generated approximations of those
species' scale and silhouettes. It does not yet include the original custom
sapling planting pattern, commands, editable species XML, or root system.

## Requirements

- Minecraft Java 26.3
- Fabric Loader 0.19.5 or newer
- Cristel Lib 3.1.12 or newer

Install the JAR in `mods/` alongside Cristel Lib. Explore new terrain; old
chunks will not gain trees. Each species has three variants and an independent
structure set with 18-chunk spacing and 9-chunk separation. Eligible biomes
are in `data/giant_trees/tags/worldgen/biome/has_structure/`. Cristel Lib
provides placement and enable/disable settings under `config/giant_trees/`.

The trees contain ordinary logs and persistent leaves. They use native
heightmap-projected structures, so `/locate structure giant_trees:oak_1` can
find a generated variant. For a manual test, use `/place structure
 giant_trees:oak_1` on open ground in a disposable world.

## Rebuild structures

`python -m pip install nbtlib` then `python tools/generate_trees.py` regenerates
the deterministic NBT templates. The generated templates are committed, so
Python is not required to build or play the mod.

The original project: https://github.com/rmichela/GiantTrees (GPLv3). This
repository's independently written code and generated structures are MIT.
