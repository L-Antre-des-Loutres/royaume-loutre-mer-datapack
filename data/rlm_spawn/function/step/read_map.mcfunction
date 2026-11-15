# Exécutée par l'objet carte : lit la croix rouge (milieu du chunk de départ du repère).
execute unless data entity @s Item.components."minecraft:map_decorations"."+" run return 0
execute store result score #x rlm_spawn run data get entity @s Item.components."minecraft:map_decorations"."+".x
execute store result score #z rlm_spawn run data get entity @s Item.components."minecraft:map_decorations"."+".z
scoreboard players set #found rlm_spawn 1
scoreboard players operation #x1 rlm_spawn = #x rlm_spawn
scoreboard players operation #x1 rlm_spawn -= #reach rlm_spawn
scoreboard players operation #x2 rlm_spawn = #x rlm_spawn
scoreboard players operation #x2 rlm_spawn += #reach rlm_spawn
scoreboard players operation #z1 rlm_spawn = #z rlm_spawn
scoreboard players operation #z1 rlm_spawn -= #reach rlm_spawn
scoreboard players operation #z2 rlm_spawn = #z rlm_spawn
scoreboard players operation #z2 rlm_spawn += #reach rlm_spawn
execute store result storage rlm_spawn:data lot.x int 1 run scoreboard players get #x rlm_spawn
execute store result storage rlm_spawn:data lot.z int 1 run scoreboard players get #z rlm_spawn
execute store result storage rlm_spawn:data lot.x1 int 1 run scoreboard players get #x1 rlm_spawn
execute store result storage rlm_spawn:data lot.z1 int 1 run scoreboard players get #z1 rlm_spawn
execute store result storage rlm_spawn:data lot.x2 int 1 run scoreboard players get #x2 rlm_spawn
execute store result storage rlm_spawn:data lot.z2 int 1 run scoreboard players get #z2 rlm_spawn
