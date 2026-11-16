# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "counterclockwise_90"
place template rlm_spawn:base/p_0_0_0 ~0 ~1 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_0_0 ~0 ~1 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_0_0 ~0 ~1 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_0_0 ~0 ~1 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_0_0 ~0 ~1 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_0_1 ~35 ~1 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_0_1 ~35 ~1 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_0_1 ~35 ~1 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_0_1 ~35 ~1 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_0_1 ~35 ~1 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_0_2 ~70 ~1 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_0_2 ~70 ~1 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_0_2 ~70 ~1 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_0_2 ~70 ~1 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_0_2 ~70 ~1 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_1_0 ~0 ~40 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_1_0 ~0 ~40 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_1_0 ~0 ~40 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_1_0 ~0 ~40 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_1_0 ~0 ~40 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_1_1 ~35 ~40 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_1_1 ~35 ~40 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_1_1 ~35 ~40 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_1_1 ~35 ~40 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_1_1 ~35 ~40 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_1_2 ~70 ~40 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_1_2 ~70 ~40 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_1_2 ~70 ~40 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_1_2 ~70 ~40 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_1_2 ~70 ~40 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_2_0 ~0 ~79 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_2_0 ~0 ~79 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_2_0 ~0 ~79 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_2_0 ~0 ~79 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_2_0 ~0 ~79 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_2_1 ~35 ~79 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_2_1 ~35 ~79 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_2_1 ~35 ~79 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_2_1 ~35 ~79 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_2_1 ~35 ~79 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_2_2 ~70 ~79 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_2_2 ~70 ~79 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_2_2 ~70 ~79 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_2_2 ~70 ~79 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_2_2 ~70 ~79 ~-173 counterclockwise_90
data modify storage rlm_spawn:data spawn.yaw set value 90
execute positioned ~86 ~30 ~-108 run function rlm_spawn:step/set_spawn with storage rlm_spawn:data spawn
execute store result score #verified rlm_spawn run function rlm_spawn:generated/verify_counterclockwise_90
