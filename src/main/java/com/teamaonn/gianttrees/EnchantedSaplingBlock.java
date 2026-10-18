package com.teamaonn.gianttrees;

import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.Vec3i;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.BonemealableBlock;
import net.minecraft.world.level.block.BonemealSource;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

public final class EnchantedSaplingBlock extends Block implements BonemealableBlock {
    private static final VoxelShape SHAPE = Block.box(2, 0, 2, 14, 14, 14);
    private static final String[] SHAPES = {"round", "cone", "broad", "umbrella"};
    private final String species;

    public EnchantedSaplingBlock(String species, Properties properties) {
        super(properties);
        this.species = species;
    }
    @Override protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) { return SHAPE; }
    @Override protected boolean canSurvive(BlockState state, LevelReader level, BlockPos pos) {
        BlockPos below = pos.below();
        return level.getBlockState(below).isFaceSturdy(level, below, Direction.UP);
    }
    @Override protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (random.nextInt(7) == 0) grow(level, pos, state, random);
    }
    @Override public boolean isValidBonemealTarget(LevelReader level, BlockPos pos, BlockState state, BonemealSource source) { return true; }
    @Override public boolean isBonemealSuccess(Level level, RandomSource random, BlockPos pos, BlockState state, BonemealSource source) { return true; }
    @Override public void performBonemeal(ServerLevel level, RandomSource random, BlockPos pos, BlockState state, BonemealSource source) {
        grow(level, pos, state, random);
    }
    private void grow(ServerLevel level, BlockPos pos, BlockState state, RandomSource random) {
        String shape = SHAPES[random.nextInt(SHAPES.length)];
        int variant = 1 + random.nextInt(3);
        boolean nativeShape = switch (species) {
            case "spruce", "bamboo" -> shape.equals("cone");
            case "dark_oak", "mangrove", "pale_oak" -> shape.equals("broad");
            case "acacia", "crimson" -> shape.equals("umbrella");
            default -> shape.equals("round");
        };
        String name = species + (nativeShape ? "" : "_" + shape) + "_" + variant;
        Optional<StructureTemplate> found = level.getServer().getStructureTemplateManager().get(GiantTrees.id(name));
        if (found.isEmpty()) return;
        StructureTemplate template = found.get();
        Vec3i size = template.getSize();
        BlockPos origin = pos.offset(-size.getX() / 2, 0, -size.getZ() / 2);
        if (origin.getY() + size.getY() >= level.getMaxY() || !level.hasChunksAt(origin, origin.offset(size))) return;
        level.removeBlock(pos, false);
        if (!template.placeInWorld(level, origin, origin, new StructurePlaceSettings(), random, 2)) {
            level.setBlock(pos, state, 3);
        }
    }
}
