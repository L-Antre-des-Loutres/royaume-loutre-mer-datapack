# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "clockwise_90"
place template rlm_spawn:base/p_0_0_0 ~0 ~1 ~0 clockwise_90
place template rlm_spawn:base/p_1_0_0 ~0 ~1 ~45 clockwise_90
place template rlm_spawn:base/p_2_0_0 ~0 ~1 ~90 clockwise_90
place template rlm_spawn:base/p_3_0_0 ~0 ~1 ~135 clockwise_90
place template rlm_spawn:base/p_4_0_0 ~0 ~1 ~180 clockwise_90
place template rlm_spawn:base/p_0_0_1 ~-38 ~1 ~0 clockwise_90
place template rlm_spawn:base/p_1_0_1 ~-38 ~1 ~45 clockwise_90
place template rlm_spawn:base/p_2_0_1 ~-38 ~1 ~90 clockwise_90
place template rlm_spawn:base/p_3_0_1 ~-38 ~1 ~135 clockwise_90
place template rlm_spawn:base/p_4_0_1 ~-38 ~1 ~180 clockwise_90
place template rlm_spawn:base/p_0_0_2 ~-76 ~1 ~0 clockwise_90
place template rlm_spawn:base/p_1_0_2 ~-76 ~1 ~45 clockwise_90
place template rlm_spawn:base/p_2_0_2 ~-76 ~1 ~90 clockwise_90
place template rlm_spawn:base/p_3_0_2 ~-76 ~1 ~135 clockwise_90
place template rlm_spawn:base/p_4_0_2 ~-76 ~1 ~180 clockwise_90
place template rlm_spawn:base/p_0_1_0 ~0 ~44 ~0 clockwise_90
place template rlm_spawn:base/p_1_1_0 ~0 ~44 ~45 clockwise_90
place template rlm_spawn:base/p_2_1_0 ~0 ~44 ~90 clockwise_90
place template rlm_spawn:base/p_3_1_0 ~0 ~44 ~135 clockwise_90
place template rlm_spawn:base/p_4_1_0 ~0 ~44 ~180 clockwise_90
place template rlm_spawn:base/p_0_1_1 ~-38 ~44 ~0 clockwise_90
place template rlm_spawn:base/p_1_1_1 ~-38 ~44 ~45 clockwise_90
place template rlm_spawn:base/p_2_1_1 ~-38 ~44 ~90 clockwise_90
place template rlm_spawn:base/p_3_1_1 ~-38 ~44 ~135 clockwise_90
place template rlm_spawn:base/p_4_1_1 ~-38 ~44 ~180 clockwise_90
place template rlm_spawn:base/p_0_1_2 ~-76 ~44 ~0 clockwise_90
place template rlm_spawn:base/p_1_1_2 ~-76 ~44 ~45 clockwise_90
place template rlm_spawn:base/p_2_1_2 ~-76 ~44 ~90 clockwise_90
place template rlm_spawn:base/p_3_1_2 ~-76 ~44 ~135 clockwise_90
place template rlm_spawn:base/p_4_1_2 ~-76 ~44 ~180 clockwise_90
place template rlm_spawn:base/p_0_2_0 ~0 ~86 ~0 clockwise_90
place template rlm_spawn:base/p_1_2_0 ~0 ~86 ~45 clockwise_90
place template rlm_spawn:base/p_2_2_0 ~0 ~86 ~90 clockwise_90
place template rlm_spawn:base/p_3_2_0 ~0 ~86 ~135 clockwise_90
place template rlm_spawn:base/p_4_2_0 ~0 ~86 ~180 clockwise_90
place template rlm_spawn:base/p_0_2_1 ~-38 ~86 ~0 clockwise_90
place template rlm_spawn:base/p_1_2_1 ~-38 ~86 ~45 clockwise_90
place template rlm_spawn:base/p_2_2_1 ~-38 ~86 ~90 clockwise_90
place template rlm_spawn:base/p_3_2_1 ~-38 ~86 ~135 clockwise_90
place template rlm_spawn:base/p_4_2_1 ~-38 ~86 ~180 clockwise_90
place template rlm_spawn:base/p_0_2_2 ~-76 ~86 ~0 clockwise_90
place template rlm_spawn:base/p_1_2_2 ~-76 ~86 ~45 clockwise_90
place template rlm_spawn:base/p_2_2_2 ~-76 ~86 ~90 clockwise_90
place template rlm_spawn:base/p_3_2_2 ~-76 ~86 ~135 clockwise_90
place template rlm_spawn:base/p_4_2_2 ~-76 ~86 ~180 clockwise_90
data modify storage rlm_spawn:data spawn.yaw set value -90
execute positioned ~-97 ~30 ~108 run function rlm_spawn:step/set_spawn with storage rlm_spawn:data spawn
execute store result score #verified rlm_spawn run function rlm_spawn:generated/verify_clockwise_90
