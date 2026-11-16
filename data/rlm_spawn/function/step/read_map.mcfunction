# Exécutée par l'objet carte : lit la croix rouge (chunk de départ du repère).
execute unless data entity @s Item.components."minecraft:map_decorations"."+" run return 0
execute store result storage rlm_spawn:data lot.x int 1 run data get entity @s Item.components."minecraft:map_decorations"."+".x
execute store result storage rlm_spawn:data lot.z int 1 run data get entity @s Item.components."minecraft:map_decorations"."+".z
scoreboard players set #found rlm_spawn 1
