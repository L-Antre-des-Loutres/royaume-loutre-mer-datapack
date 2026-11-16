# Exécutée par l'ancre, positionnée sur son bloc, une fois l'emprise chargée.
execute if score #rot rlm_spawn matches 0 run function rlm_spawn:generated/place_none
execute if score #rot rlm_spawn matches 1 run function rlm_spawn:generated/place_clockwise_90
execute if score #rot rlm_spawn matches 2 run function rlm_spawn:generated/place_clockwise_180
execute if score #rot rlm_spawn matches 3 run function rlm_spawn:generated/place_counterclockwise_90
gamerule spawnRadius 0
function rlm_spawn:step/unforceload_footprint
function rlm_spawn:step/unforceload_anchor with storage rlm_spawn:data lot
scoreboard players set #state rlm_spawn 3
