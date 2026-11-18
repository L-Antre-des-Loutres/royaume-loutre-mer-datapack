# Généré par tools/convert_spawn_base.py : ne pas éditer.
data modify storage rlm_spawn:data lot.rotation set value "none"
place template rlm_spawn:base/p_0_0_0 ~0 ~1 ~0 none
place template rlm_spawn:base/p_1_0_0 ~45 ~1 ~0 none
place template rlm_spawn:base/p_2_0_0 ~90 ~1 ~0 none
place template rlm_spawn:base/p_3_0_0 ~135 ~1 ~0 none
place template rlm_spawn:base/p_4_0_0 ~180 ~1 ~0 none
place template rlm_spawn:base/p_0_0_1 ~0 ~1 ~38 none
place template rlm_spawn:base/p_1_0_1 ~45 ~1 ~38 none
place template rlm_spawn:base/p_2_0_1 ~90 ~1 ~38 none
place template rlm_spawn:base/p_3_0_1 ~135 ~1 ~38 none
place template rlm_spawn:base/p_4_0_1 ~180 ~1 ~38 none
place template rlm_spawn:base/p_0_0_2 ~0 ~1 ~76 none
place template rlm_spawn:base/p_1_0_2 ~45 ~1 ~76 none
place template rlm_spawn:base/p_2_0_2 ~90 ~1 ~76 none
place template rlm_spawn:base/p_3_0_2 ~135 ~1 ~76 none
place template rlm_spawn:base/p_4_0_2 ~180 ~1 ~76 none
place template rlm_spawn:base/p_0_1_0 ~0 ~44 ~0 none
place template rlm_spawn:base/p_1_1_0 ~45 ~44 ~0 none
place template rlm_spawn:base/p_2_1_0 ~90 ~44 ~0 none
place template rlm_spawn:base/p_3_1_0 ~135 ~44 ~0 none
place template rlm_spawn:base/p_4_1_0 ~180 ~44 ~0 none
place template rlm_spawn:base/p_0_1_1 ~0 ~44 ~38 none
place template rlm_spawn:base/p_1_1_1 ~45 ~44 ~38 none
place template rlm_spawn:base/p_2_1_1 ~90 ~44 ~38 none
place template rlm_spawn:base/p_3_1_1 ~135 ~44 ~38 none
place template rlm_spawn:base/p_4_1_1 ~180 ~44 ~38 none
place template rlm_spawn:base/p_0_1_2 ~0 ~44 ~76 none
place template rlm_spawn:base/p_1_1_2 ~45 ~44 ~76 none
place template rlm_spawn:base/p_2_1_2 ~90 ~44 ~76 none
place template rlm_spawn:base/p_3_1_2 ~135 ~44 ~76 none
place template rlm_spawn:base/p_4_1_2 ~180 ~44 ~76 none
place template rlm_spawn:base/p_0_2_0 ~0 ~86 ~0 none
place template rlm_spawn:base/p_1_2_0 ~45 ~86 ~0 none
place template rlm_spawn:base/p_2_2_0 ~90 ~86 ~0 none
place template rlm_spawn:base/p_3_2_0 ~135 ~86 ~0 none
place template rlm_spawn:base/p_4_2_0 ~180 ~86 ~0 none
place template rlm_spawn:base/p_0_2_1 ~0 ~86 ~38 none
place template rlm_spawn:base/p_1_2_1 ~45 ~86 ~38 none
place template rlm_spawn:base/p_2_2_1 ~90 ~86 ~38 none
place template rlm_spawn:base/p_3_2_1 ~135 ~86 ~38 none
place template rlm_spawn:base/p_4_2_1 ~180 ~86 ~38 none
place template rlm_spawn:base/p_0_2_2 ~0 ~86 ~76 none
place template rlm_spawn:base/p_1_2_2 ~45 ~86 ~76 none
place template rlm_spawn:base/p_2_2_2 ~90 ~86 ~76 none
place template rlm_spawn:base/p_3_2_2 ~135 ~86 ~76 none
place template rlm_spawn:base/p_4_2_2 ~180 ~86 ~76 none
data modify storage rlm_spawn:data spawn.yaw set value 180
execute positioned ~108 ~30 ~97 run function rlm_spawn:step/set_spawn with storage rlm_spawn:data spawn
execute store result score #verified rlm_spawn run function rlm_spawn:generated/verify_none
