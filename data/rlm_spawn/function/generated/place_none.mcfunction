# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "none"
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
