# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "counterclockwise_90"
place template rlm_spawn:base/p_0_0_0 ~0 ~-1 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_0_0 ~0 ~-1 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_0_0 ~0 ~-1 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_0_0 ~0 ~-1 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_0_0 ~0 ~-1 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_0_1 ~38 ~-1 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_0_1 ~38 ~-1 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_0_1 ~38 ~-1 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_0_1 ~38 ~-1 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_0_1 ~38 ~-1 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_0_2 ~76 ~-1 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_0_2 ~76 ~-1 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_0_2 ~76 ~-1 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_0_2 ~76 ~-1 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_0_2 ~76 ~-1 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_1_0 ~0 ~46 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_1_0 ~0 ~46 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_1_0 ~0 ~46 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_1_0 ~0 ~46 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_1_0 ~0 ~46 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_1_1 ~38 ~46 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_1_1 ~38 ~46 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_1_1 ~38 ~46 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_1_1 ~38 ~46 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_1_1 ~38 ~46 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_1_2 ~76 ~46 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_1_2 ~76 ~46 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_1_2 ~76 ~46 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_1_2 ~76 ~46 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_1_2 ~76 ~46 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_2_0 ~0 ~93 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_2_0 ~0 ~93 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_2_0 ~0 ~93 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_2_0 ~0 ~93 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_2_0 ~0 ~93 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_2_1 ~38 ~93 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_2_1 ~38 ~93 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_2_1 ~38 ~93 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_2_1 ~38 ~93 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_2_1 ~38 ~93 ~-173 counterclockwise_90
place template rlm_spawn:base/p_0_2_2 ~76 ~93 ~0 counterclockwise_90
place template rlm_spawn:base/p_1_2_2 ~76 ~93 ~-44 counterclockwise_90
place template rlm_spawn:base/p_2_2_2 ~76 ~93 ~-87 counterclockwise_90
place template rlm_spawn:base/p_3_2_2 ~76 ~93 ~-130 counterclockwise_90
place template rlm_spawn:base/p_4_2_2 ~76 ~93 ~-173 counterclockwise_90
data modify storage rlm_spawn:data spawn.yaw set value 90
execute positioned ~96 ~30 ~-108 run function rlm_spawn:step/set_spawn with storage rlm_spawn:data spawn
execute store result score #verified rlm_spawn run function rlm_spawn:generated/verify_counterclockwise_90
