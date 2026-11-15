# Exécutée par l'ancre, positionnée sur son bloc. Son orientation donne la rotation du repère.
execute store result score #yaw rlm_spawn run data get entity @s Rotation[0]
scoreboard players operation #yaw rlm_spawn += #c360 rlm_spawn
scoreboard players operation #yaw rlm_spawn %= #c360 rlm_spawn
execute if score #yaw rlm_spawn matches 315.. run function rlm_spawn:generated/place_none
execute if score #yaw rlm_spawn matches ..45 run function rlm_spawn:generated/place_none
execute if score #yaw rlm_spawn matches 46..135 run function rlm_spawn:generated/place_clockwise_90
execute if score #yaw rlm_spawn matches 136..225 run function rlm_spawn:generated/place_clockwise_180
execute if score #yaw rlm_spawn matches 226..314 run function rlm_spawn:generated/place_counterclockwise_90
gamerule spawnRadius 0
function rlm_spawn:step/unforceload_area with storage rlm_spawn:data lot
scoreboard players set #state rlm_spawn 3
