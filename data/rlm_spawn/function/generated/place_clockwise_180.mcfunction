# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "clockwise_180"
fill ~-81 ~-1 ~-80 ~0 ~-1 ~0 minecraft:grass_block replace #minecraft:replaceable
fill ~-82 ~-2 ~-81 ~1 ~-2 ~1 minecraft:grass_block replace #minecraft:replaceable
fill ~-83 ~-3 ~-82 ~2 ~-3 ~2 minecraft:grass_block replace #minecraft:replaceable
fill ~-84 ~-4 ~-83 ~3 ~-4 ~3 minecraft:grass_block replace #minecraft:replaceable
fill ~-85 ~-5 ~-84 ~4 ~-5 ~4 minecraft:grass_block replace #minecraft:replaceable
fill ~-86 ~-6 ~-85 ~5 ~-6 ~5 minecraft:grass_block replace #minecraft:replaceable
fill ~-87 ~-7 ~-86 ~6 ~-7 ~6 minecraft:grass_block replace #minecraft:replaceable
fill ~-88 ~-8 ~-87 ~7 ~-8 ~7 minecraft:grass_block replace #minecraft:replaceable
fill ~-89 ~-9 ~-88 ~8 ~-9 ~8 minecraft:grass_block replace #minecraft:replaceable
fill ~-90 ~-10 ~-89 ~9 ~-10 ~9 minecraft:grass_block replace #minecraft:replaceable
fill ~-91 ~-11 ~-90 ~10 ~-11 ~10 minecraft:grass_block replace #minecraft:replaceable
fill ~-92 ~-12 ~-91 ~11 ~-12 ~11 minecraft:grass_block replace #minecraft:replaceable
fill ~-93 ~-13 ~-92 ~12 ~-13 ~12 minecraft:grass_block replace #minecraft:replaceable
fill ~-94 ~-14 ~-93 ~13 ~-14 ~13 minecraft:grass_block replace #minecraft:replaceable
fill ~-95 ~-15 ~-94 ~14 ~-15 ~14 minecraft:grass_block replace #minecraft:replaceable
fill ~-96 ~-16 ~-95 ~15 ~-16 ~15 minecraft:grass_block replace #minecraft:replaceable
fill ~-97 ~-17 ~-96 ~16 ~-17 ~16 minecraft:grass_block replace #minecraft:replaceable
fill ~-98 ~-18 ~-97 ~17 ~-18 ~17 minecraft:grass_block replace #minecraft:replaceable
fill ~-99 ~-19 ~-98 ~18 ~-19 ~18 minecraft:grass_block replace #minecraft:replaceable
fill ~-100 ~-20 ~-99 ~19 ~-20 ~19 minecraft:grass_block replace #minecraft:replaceable
fill ~-101 ~-21 ~-100 ~20 ~-21 ~20 minecraft:grass_block replace #minecraft:replaceable
fill ~-102 ~-22 ~-101 ~21 ~-22 ~21 minecraft:grass_block replace #minecraft:replaceable
fill ~-103 ~-23 ~-102 ~22 ~-23 ~22 minecraft:grass_block replace #minecraft:replaceable
fill ~-104 ~-24 ~-103 ~23 ~-24 ~23 minecraft:grass_block replace #minecraft:replaceable
place template rlm_spawn:base/p_0_0_0 ~0 ~0 ~0 180
place template rlm_spawn:base/p_1_0_0 ~-41 ~0 ~0 180
place template rlm_spawn:base/p_0_0_1 ~0 ~0 ~-41 180
place template rlm_spawn:base/p_1_0_1 ~-41 ~0 ~-41 180
place template rlm_spawn:base/p_0_1_0 ~0 ~30 ~0 180
place template rlm_spawn:base/p_1_1_0 ~-41 ~30 ~0 180
place template rlm_spawn:base/p_0_1_1 ~0 ~30 ~-41 180
place template rlm_spawn:base/p_1_1_1 ~-41 ~30 ~-41 180
data modify storage rlm_spawn:data spawn.yaw set value 180
execute positioned ~-41 ~1 ~-40 run function rlm_spawn:step/set_spawn with storage rlm_spawn:data spawn
execute store result score #verified rlm_spawn run function rlm_spawn:generated/verify_clockwise_180
