package com.teamaonn.gianttrees;

import com.mojang.serialization.MapCodec;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.CraftingInput;
import net.minecraft.world.item.crafting.CustomRecipe;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.level.Level;

public final class EnchantedSaplingRecipe extends CustomRecipe {
    public static final EnchantedSaplingRecipe INSTANCE = new EnchantedSaplingRecipe();
    public static final RecipeSerializer<EnchantedSaplingRecipe> SERIALIZER = new RecipeSerializer<>(
        MapCodec.unit(INSTANCE), StreamCodec.unit(INSTANCE));

    private Item result(CraftingInput input) {
        if (input.width() != 3 || input.height() != 3) return null;
        for (int slot : new int[] {0, 2, 6, 8}) {
            if (!input.getItem(slot).is(Items.EMERALD)) return null;
        }
        for (int slot : new int[] {1, 3, 5, 7}) {
            if (!GiantTrees.fortuneThree(input.getItem(slot))) return null;
        }
        return GiantTrees.ENCHANTED_BY_BASE.get(input.getItem(4).getItem());
    }

    @Override public boolean matches(CraftingInput input, Level level) { return result(input) != null; }
    @Override public ItemStack assemble(CraftingInput input) {
        Item item = result(input);
        return item == null ? ItemStack.EMPTY : new ItemStack(item);
    }
    @Override public RecipeSerializer<? extends CustomRecipe> getSerializer() { return SERIALIZER; }
}
