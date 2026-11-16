# L'orientation de l'ancre donne la rotation du repère : #rot 0 none, 1 cw90, 2 180, 3 ccw90.
execute store result score #yaw rlm_spawn run data get entity @s Rotation[0]
scoreboard players operation #yaw rlm_spawn += #c360 rlm_spawn
scoreboard players operation #yaw rlm_spawn %= #c360 rlm_spawn
scoreboard players set #rot rlm_spawn 0
execute if score #yaw rlm_spawn matches 46..135 run scoreboard players set #rot rlm_spawn 1
execute if score #yaw rlm_spawn matches 136..225 run scoreboard players set #rot rlm_spawn 2
execute if score #yaw rlm_spawn matches 226..314 run scoreboard players set #rot rlm_spawn 3
execute if score #rot rlm_spawn matches 0 run function rlm_spawn:generated/forceload_none
execute if score #rot rlm_spawn matches 1 run function rlm_spawn:generated/forceload_clockwise_90
execute if score #rot rlm_spawn matches 2 run function rlm_spawn:generated/forceload_clockwise_180
execute if score #rot rlm_spawn matches 3 run function rlm_spawn:generated/forceload_counterclockwise_90
scoreboard players set #footprint rlm_spawn 1
