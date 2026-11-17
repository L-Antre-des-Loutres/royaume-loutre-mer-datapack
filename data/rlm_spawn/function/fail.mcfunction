scoreboard players set #state rlm_spawn -2
execute in minecraft:overworld run forceload remove 0 0
execute if score #footprint rlm_spawn matches 1 in minecraft:overworld run function rlm_spawn:step/release_site with storage rlm_spawn:data lot
execute if score #footprint rlm_spawn matches 2 in minecraft:overworld run function rlm_spawn:step/release_footprint with storage rlm_spawn:data lot
execute if data storage rlm_spawn:data lot.x in minecraft:overworld run function rlm_spawn:step/unforceload_anchor with storage rlm_spawn:data lot
