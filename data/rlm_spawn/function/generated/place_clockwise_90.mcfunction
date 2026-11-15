# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "clockwise_90"
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
