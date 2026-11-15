# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "counterclockwise_90"
fill ~0 ~-1 ~-81 ~80 ~-1 ~0 minecraft:grass_block replace #minecraft:replaceable
fill ~-1 ~-2 ~-82 ~81 ~-2 ~1 minecraft:grass_block replace #minecraft:replaceable
fill ~-2 ~-3 ~-83 ~82 ~-3 ~2 minecraft:grass_block replace #minecraft:replaceable
fill ~-3 ~-4 ~-84 ~83 ~-4 ~3 minecraft:grass_block replace #minecraft:replaceable
fill ~-4 ~-5 ~-85 ~84 ~-5 ~4 minecraft:grass_block replace #minecraft:replaceable
fill ~-5 ~-6 ~-86 ~85 ~-6 ~5 minecraft:grass_block replace #minecraft:replaceable
fill ~-6 ~-7 ~-87 ~86 ~-7 ~6 minecraft:grass_block replace #minecraft:replaceable
fill ~-7 ~-8 ~-88 ~87 ~-8 ~7 minecraft:grass_block replace #minecraft:replaceable
fill ~-8 ~-9 ~-89 ~88 ~-9 ~8 minecraft:grass_block replace #minecraft:replaceable
fill ~-9 ~-10 ~-90 ~89 ~-10 ~9 minecraft:grass_block replace #minecraft:replaceable
fill ~-10 ~-11 ~-91 ~90 ~-11 ~10 minecraft:grass_block replace #minecraft:replaceable
fill ~-11 ~-12 ~-92 ~91 ~-12 ~11 minecraft:grass_block replace #minecraft:replaceable
fill ~-12 ~-13 ~-93 ~92 ~-13 ~12 minecraft:grass_block replace #minecraft:replaceable
fill ~-13 ~-14 ~-94 ~93 ~-14 ~13 minecraft:grass_block replace #minecraft:replaceable
fill ~-14 ~-15 ~-95 ~94 ~-15 ~14 minecraft:grass_block replace #minecraft:replaceable
fill ~-15 ~-16 ~-96 ~95 ~-16 ~15 minecraft:grass_block replace #minecraft:replaceable
fill ~-16 ~-17 ~-97 ~96 ~-17 ~16 minecraft:grass_block replace #minecraft:replaceable
fill ~-17 ~-18 ~-98 ~97 ~-18 ~17 minecraft:grass_block replace #minecraft:replaceable
fill ~-18 ~-19 ~-99 ~98 ~-19 ~18 minecraft:grass_block replace #minecraft:replaceable
fill ~-19 ~-20 ~-100 ~99 ~-20 ~19 minecraft:grass_block replace #minecraft:replaceable
fill ~-20 ~-21 ~-101 ~100 ~-21 ~20 minecraft:grass_block replace #minecraft:replaceable
fill ~-21 ~-22 ~-102 ~101 ~-22 ~21 minecraft:grass_block replace #minecraft:replaceable
fill ~-22 ~-23 ~-103 ~102 ~-23 ~22 minecraft:grass_block replace #minecraft:replaceable
fill ~-23 ~-24 ~-104 ~103 ~-24 ~23 minecraft:grass_block replace #minecraft:replaceable
place template rlm_spawn:base/p_0_0_0 ~0 ~0 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_0_0 ~0 ~0 ~-41 counterclockwise_90
place template rlm_spawn:base/p_0_0_1 ~41 ~0 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_0_1 ~41 ~0 ~-41 counterclockwise_90
place template rlm_spawn:base/p_0_1_0 ~0 ~30 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_1_0 ~0 ~30 ~-41 counterclockwise_90
place template rlm_spawn:base/p_0_1_1 ~41 ~30 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_1_1 ~41 ~30 ~-41 counterclockwise_90
data modify storage rlm_spawn:data spawn.yaw set value -90
execute positioned ~40 ~1 ~-41 run function rlm_spawn:step/set_spawn with storage rlm_spawn:data spawn
execute store result score #verified rlm_spawn run function rlm_spawn:generated/verify_counterclockwise_90
