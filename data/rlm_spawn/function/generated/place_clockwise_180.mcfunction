# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "clockwise_180"
place template rlm_spawn:base/p_0_0_0 ~0 ~1 ~0 180
place template rlm_spawn:base/p_1_0_0 ~-44 ~1 ~0 180
place template rlm_spawn:base/p_2_0_0 ~-87 ~1 ~0 180
place template rlm_spawn:base/p_3_0_0 ~-130 ~1 ~0 180
place template rlm_spawn:base/p_4_0_0 ~-173 ~1 ~0 180
place template rlm_spawn:base/p_0_0_1 ~0 ~1 ~-35 180
place template rlm_spawn:base/p_1_0_1 ~-44 ~1 ~-35 180
place template rlm_spawn:base/p_2_0_1 ~-87 ~1 ~-35 180
place template rlm_spawn:base/p_3_0_1 ~-130 ~1 ~-35 180
place template rlm_spawn:base/p_4_0_1 ~-173 ~1 ~-35 180
place template rlm_spawn:base/p_0_0_2 ~0 ~1 ~-70 180
place template rlm_spawn:base/p_1_0_2 ~-44 ~1 ~-70 180
place template rlm_spawn:base/p_2_0_2 ~-87 ~1 ~-70 180
place template rlm_spawn:base/p_3_0_2 ~-130 ~1 ~-70 180
place template rlm_spawn:base/p_4_0_2 ~-173 ~1 ~-70 180
place template rlm_spawn:base/p_0_1_0 ~0 ~40 ~0 180
place template rlm_spawn:base/p_1_1_0 ~-44 ~40 ~0 180
place template rlm_spawn:base/p_2_1_0 ~-87 ~40 ~0 180
place template rlm_spawn:base/p_3_1_0 ~-130 ~40 ~0 180
place template rlm_spawn:base/p_4_1_0 ~-173 ~40 ~0 180
place template rlm_spawn:base/p_0_1_1 ~0 ~40 ~-35 180
place template rlm_spawn:base/p_1_1_1 ~-44 ~40 ~-35 180
place template rlm_spawn:base/p_2_1_1 ~-87 ~40 ~-35 180
place template rlm_spawn:base/p_3_1_1 ~-130 ~40 ~-35 180
place template rlm_spawn:base/p_4_1_1 ~-173 ~40 ~-35 180
place template rlm_spawn:base/p_0_1_2 ~0 ~40 ~-70 180
place template rlm_spawn:base/p_1_1_2 ~-44 ~40 ~-70 180
place template rlm_spawn:base/p_2_1_2 ~-87 ~40 ~-70 180
place template rlm_spawn:base/p_3_1_2 ~-130 ~40 ~-70 180
place template rlm_spawn:base/p_4_1_2 ~-173 ~40 ~-70 180
place template rlm_spawn:base/p_0_2_0 ~0 ~79 ~0 180
place template rlm_spawn:base/p_1_2_0 ~-44 ~79 ~0 180
place template rlm_spawn:base/p_2_2_0 ~-87 ~79 ~0 180
place template rlm_spawn:base/p_3_2_0 ~-130 ~79 ~0 180
place template rlm_spawn:base/p_4_2_0 ~-173 ~79 ~0 180
place template rlm_spawn:base/p_0_2_1 ~0 ~79 ~-35 180
place template rlm_spawn:base/p_1_2_1 ~-44 ~79 ~-35 180
place template rlm_spawn:base/p_2_2_1 ~-87 ~79 ~-35 180
place template rlm_spawn:base/p_3_2_1 ~-130 ~79 ~-35 180
place template rlm_spawn:base/p_4_2_1 ~-173 ~79 ~-35 180
place template rlm_spawn:base/p_0_2_2 ~0 ~79 ~-70 180
place template rlm_spawn:base/p_1_2_2 ~-44 ~79 ~-70 180
place template rlm_spawn:base/p_2_2_2 ~-87 ~79 ~-70 180
place template rlm_spawn:base/p_3_2_2 ~-130 ~79 ~-70 180
place template rlm_spawn:base/p_4_2_2 ~-173 ~79 ~-70 180
data modify storage rlm_spawn:data spawn.yaw set value 0
execute positioned ~-108 ~30 ~-86 run function rlm_spawn:step/set_spawn with storage rlm_spawn:data spawn
execute store result score #verified rlm_spawn run function rlm_spawn:generated/verify_clockwise_180
