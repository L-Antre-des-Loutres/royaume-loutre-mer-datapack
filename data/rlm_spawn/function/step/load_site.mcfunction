# L'orientation de l'ancre donne la rotation du repère : #rot 0 none, 1 cw90, 2 180, 3 ccw90.
execute store result score #yaw rlm_spawn run data get entity @s Rotation[0]
scoreboard players operation #yaw rlm_spawn += #c360 rlm_spawn
scoreboard players operation #yaw rlm_spawn %= #c360 rlm_spawn
scoreboard players set #rot rlm_spawn 0
execute if score #yaw rlm_spawn matches 46..135 run scoreboard players set #rot rlm_spawn 1
execute if score #yaw rlm_spawn matches 136..225 run scoreboard players set #rot rlm_spawn 2
execute if score #yaw rlm_spawn matches 226..314 run scoreboard players set #rot rlm_spawn 3
function rlm_spawn:step/site_forceload
scoreboard players set #footprint rlm_spawn 1
