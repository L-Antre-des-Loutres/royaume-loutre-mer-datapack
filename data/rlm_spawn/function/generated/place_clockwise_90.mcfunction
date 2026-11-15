# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "clockwise_90"
fill ~-80 ~-1 ~0 ~0 ~-1 ~81 minecraft:grass_block replace #minecraft:replaceable
fill ~-81 ~-2 ~-1 ~1 ~-2 ~82 minecraft:grass_block replace #minecraft:replaceable
fill ~-82 ~-3 ~-2 ~2 ~-3 ~83 minecraft:grass_block replace #minecraft:replaceable
fill ~-83 ~-4 ~-3 ~3 ~-4 ~84 minecraft:grass_block replace #minecraft:replaceable
fill ~-84 ~-5 ~-4 ~4 ~-5 ~85 minecraft:grass_block replace #minecraft:replaceable
fill ~-85 ~-6 ~-5 ~5 ~-6 ~86 minecraft:grass_block replace #minecraft:replaceable
fill ~-86 ~-7 ~-6 ~6 ~-7 ~87 minecraft:grass_block replace #minecraft:replaceable
fill ~-87 ~-8 ~-7 ~7 ~-8 ~88 minecraft:grass_block replace #minecraft:replaceable
fill ~-88 ~-9 ~-8 ~8 ~-9 ~89 minecraft:grass_block replace #minecraft:replaceable
fill ~-89 ~-10 ~-9 ~9 ~-10 ~90 minecraft:grass_block replace #minecraft:replaceable
fill ~-90 ~-11 ~-10 ~10 ~-11 ~91 minecraft:grass_block replace #minecraft:replaceable
fill ~-91 ~-12 ~-11 ~11 ~-12 ~92 minecraft:grass_block replace #minecraft:replaceable
fill ~-92 ~-13 ~-12 ~12 ~-13 ~93 minecraft:grass_block replace #minecraft:replaceable
fill ~-93 ~-14 ~-13 ~13 ~-14 ~94 minecraft:grass_block replace #minecraft:replaceable
fill ~-94 ~-15 ~-14 ~14 ~-15 ~95 minecraft:grass_block replace #minecraft:replaceable
fill ~-95 ~-16 ~-15 ~15 ~-16 ~96 minecraft:grass_block replace #minecraft:replaceable
fill ~-96 ~-17 ~-16 ~16 ~-17 ~97 minecraft:grass_block replace #minecraft:replaceable
fill ~-97 ~-18 ~-17 ~17 ~-18 ~98 minecraft:grass_block replace #minecraft:replaceable
fill ~-98 ~-19 ~-18 ~18 ~-19 ~99 minecraft:grass_block replace #minecraft:replaceable
fill ~-99 ~-20 ~-19 ~19 ~-20 ~100 minecraft:grass_block replace #minecraft:replaceable
fill ~-100 ~-21 ~-20 ~20 ~-21 ~101 minecraft:grass_block replace #minecraft:replaceable
fill ~-101 ~-22 ~-21 ~21 ~-22 ~102 minecraft:grass_block replace #minecraft:replaceable
fill ~-102 ~-23 ~-22 ~22 ~-23 ~103 minecraft:grass_block replace #minecraft:replaceable
fill ~-103 ~-24 ~-23 ~23 ~-24 ~104 minecraft:grass_block replace #minecraft:replaceable
place template rlm_spawn:base/p_0_0_0 ~0 ~0 ~0 clockwise_90
place template rlm_spawn:base/p_1_0_0 ~0 ~0 ~41 clockwise_90
place template rlm_spawn:base/p_0_0_1 ~-41 ~0 ~0 clockwise_90
place template rlm_spawn:base/p_1_0_1 ~-41 ~0 ~41 clockwise_90
place template rlm_spawn:base/p_0_1_0 ~0 ~30 ~0 clockwise_90
place template rlm_spawn:base/p_1_1_0 ~0 ~30 ~41 clockwise_90
place template rlm_spawn:base/p_0_1_1 ~-41 ~30 ~0 clockwise_90
place template rlm_spawn:base/p_1_1_1 ~-41 ~30 ~41 clockwise_90
data modify storage rlm_spawn:data spawn.yaw set value 90
execute positioned ~-40 ~1 ~41 run function rlm_spawn:step/set_spawn with storage rlm_spawn:data spawn
execute store result score #verified rlm_spawn run function rlm_spawn:generated/verify_clockwise_90
