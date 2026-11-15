# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "none"
fill ~0 ~-1 ~0 ~81 ~-1 ~80 minecraft:grass_block replace #minecraft:replaceable
fill ~-1 ~-2 ~-1 ~82 ~-2 ~81 minecraft:grass_block replace #minecraft:replaceable
fill ~-2 ~-3 ~-2 ~83 ~-3 ~82 minecraft:grass_block replace #minecraft:replaceable
fill ~-3 ~-4 ~-3 ~84 ~-4 ~83 minecraft:grass_block replace #minecraft:replaceable
fill ~-4 ~-5 ~-4 ~85 ~-5 ~84 minecraft:grass_block replace #minecraft:replaceable
fill ~-5 ~-6 ~-5 ~86 ~-6 ~85 minecraft:grass_block replace #minecraft:replaceable
fill ~-6 ~-7 ~-6 ~87 ~-7 ~86 minecraft:grass_block replace #minecraft:replaceable
fill ~-7 ~-8 ~-7 ~88 ~-8 ~87 minecraft:grass_block replace #minecraft:replaceable
fill ~-8 ~-9 ~-8 ~89 ~-9 ~88 minecraft:grass_block replace #minecraft:replaceable
fill ~-9 ~-10 ~-9 ~90 ~-10 ~89 minecraft:grass_block replace #minecraft:replaceable
fill ~-10 ~-11 ~-10 ~91 ~-11 ~90 minecraft:grass_block replace #minecraft:replaceable
fill ~-11 ~-12 ~-11 ~92 ~-12 ~91 minecraft:grass_block replace #minecraft:replaceable
fill ~-12 ~-13 ~-12 ~93 ~-13 ~92 minecraft:grass_block replace #minecraft:replaceable
fill ~-13 ~-14 ~-13 ~94 ~-14 ~93 minecraft:grass_block replace #minecraft:replaceable
fill ~-14 ~-15 ~-14 ~95 ~-15 ~94 minecraft:grass_block replace #minecraft:replaceable
fill ~-15 ~-16 ~-15 ~96 ~-16 ~95 minecraft:grass_block replace #minecraft:replaceable
fill ~-16 ~-17 ~-16 ~97 ~-17 ~96 minecraft:grass_block replace #minecraft:replaceable
fill ~-17 ~-18 ~-17 ~98 ~-18 ~97 minecraft:grass_block replace #minecraft:replaceable
fill ~-18 ~-19 ~-18 ~99 ~-19 ~98 minecraft:grass_block replace #minecraft:replaceable
fill ~-19 ~-20 ~-19 ~100 ~-20 ~99 minecraft:grass_block replace #minecraft:replaceable
fill ~-20 ~-21 ~-20 ~101 ~-21 ~100 minecraft:grass_block replace #minecraft:replaceable
fill ~-21 ~-22 ~-21 ~102 ~-22 ~101 minecraft:grass_block replace #minecraft:replaceable
fill ~-22 ~-23 ~-22 ~103 ~-23 ~102 minecraft:grass_block replace #minecraft:replaceable
fill ~-23 ~-24 ~-23 ~104 ~-24 ~103 minecraft:grass_block replace #minecraft:replaceable
place template rlm_spawn:base/p_0_0_0 ~0 ~0 ~0 none
place template rlm_spawn:base/p_1_0_0 ~41 ~0 ~0 none
place template rlm_spawn:base/p_0_0_1 ~0 ~0 ~41 none
place template rlm_spawn:base/p_1_0_1 ~41 ~0 ~41 none
place template rlm_spawn:base/p_0_1_0 ~0 ~30 ~0 none
place template rlm_spawn:base/p_1_1_0 ~41 ~30 ~0 none
place template rlm_spawn:base/p_0_1_1 ~0 ~30 ~41 none
place template rlm_spawn:base/p_1_1_1 ~41 ~30 ~41 none
data modify storage rlm_spawn:data spawn.yaw set value 0
execute positioned ~41 ~1 ~40 run function rlm_spawn:step/set_spawn with storage rlm_spawn:data spawn
execute store result score #verified rlm_spawn run function rlm_spawn:generated/verify_none
