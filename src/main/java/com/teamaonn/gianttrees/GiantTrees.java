package com.teamaonn.gianttrees;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Function;
import net.fabricmc.api.ModInitializer;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.component.ItemEnchantments;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.item.enchantment.Enchantments;
import net.minecraft.world.item.crafting.RecipeSerializer;

public final class GiantTrees implements ModInitializer {
    public static final String ID = "giant_trees";
    public static final Map<Item, Item> ENCHANTED_BY_BASE = new LinkedHashMap<>();
    private static final String[] SPECIES = {"oak", "birch", "spruce", "jungle", "dark_oak", "acacia", "mangrove", "cherry", "pale_oak", "bamboo", "crimson", "warped"};
    private static final Item[] BASES = {Items.OAK_SAPLING, Items.BIRCH_SAPLING, Items.SPRUCE_SAPLING, Items.JUNGLE_SAPLING,
        Items.DARK_OAK_SAPLING, Items.ACACIA_SAPLING, Items.MANGROVE_PROPAGULE, Items.CHERRY_SAPLING,
        Items.PALE_OAK_SAPLING, Items.BAMBOO, Items.CRIMSON_FUNGUS, Items.WARPED_FUNGUS};

    public static ResourceLocation id(String path) { return ResourceLocation.fromNamespaceAndPath(ID, path); }

    @Override public void onInitialize() {
        for (int i = 0; i < SPECIES.length; i++) {
            String name = "enchanted_" + SPECIES[i] + "_sapling";
            ResourceLocation id = id(name);
            ResourceKey<Block> blockKey = ResourceKey.create(Registries.BLOCK, id);
            Block block = Registry.register(BuiltInRegistries.BLOCK, id,
                new EnchantedSaplingBlock(SPECIES[i], BlockBehaviour.Properties.of().setId(blockKey).noCollission().randomTicks().instabreak()));
            ResourceKey<Item> itemKey = ResourceKey.create(Registries.ITEM, id);
            Item item = Registry.register(BuiltInRegistries.ITEM, id,
                new BlockItem(block, new Item.Properties().setId(itemKey).useBlockDescriptionPrefix()
                    .component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true)));
            ENCHANTED_BY_BASE.put(BASES[i], item);
        }
        Registry.register(BuiltInRegistries.RECIPE_SERIALIZER, id("enchanted_sapling"), EnchantedSaplingRecipe.SERIALIZER);
    }

    public static boolean fortuneThree(net.minecraft.world.item.ItemStack stack) {
        if (!stack.is(Items.ENCHANTED_BOOK)) return false;
        ItemEnchantments enchants = stack.get(DataComponents.STORED_ENCHANTMENTS);
        return enchants != null && enchants.entrySet().stream()
            .anyMatch(entry -> entry.getKey().is(Enchantments.FORTUNE) && entry.getValue() == 3);
    }
}
