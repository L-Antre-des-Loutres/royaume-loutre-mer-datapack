execute if score #state rlm_spawn matches 1 in minecraft:overworld run function rlm_spawn:step/locate
execute if score #state rlm_spawn matches 2 in minecraft:overworld run function rlm_spawn:step/wait_area with storage rlm_spawn:data lot
execute if score #state rlm_spawn matches 3 as @e[type=minecraft:player,tag=!rlm_spawn.arrived] run function rlm_spawn:arrive with storage rlm_spawn:data spawn
execute if score #state rlm_spawn matches 3 as @e[type=minecraft:player,scores={rlm_spawn.deaths=1..}] run function rlm_spawn:respawned
execute if score #state rlm_spawn matches -2 as @a[tag=!rlm_spawn.warned] run function rlm_spawn:warn
