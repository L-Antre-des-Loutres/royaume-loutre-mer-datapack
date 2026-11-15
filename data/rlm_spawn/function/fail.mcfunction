scoreboard players set #state rlm_spawn -2
execute in minecraft:overworld run forceload remove 0 0
execute if data storage rlm_spawn:data lot.x1 in minecraft:overworld run function rlm_spawn:step/unforceload_area with storage rlm_spawn:data lot
