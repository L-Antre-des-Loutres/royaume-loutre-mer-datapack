# Cherche le terrain préparé le plus proche de 0,0 avec une carte d'exploration.
scoreboard players add #timer rlm_spawn 1
execute if score #timer rlm_spawn matches 1200.. run return run function rlm_spawn:fail
execute unless loaded 0 0 0 run return 0
scoreboard players set #found rlm_spawn 0
execute positioned 0.0 0 0.0 run loot spawn 0 300 0 loot rlm_spawn:locate_lot
execute as @e[type=minecraft:item,x=0,y=300,z=0,distance=..4,limit=1] run function rlm_spawn:step/read_map
kill @e[type=minecraft:item,x=0,y=300,z=0,distance=..4]
forceload remove 0 0
execute if score #found rlm_spawn matches 0 run return run function rlm_spawn:fail
function rlm_spawn:step/forceload_anchor with storage rlm_spawn:data lot
scoreboard players set #timer rlm_spawn 0
scoreboard players set #state rlm_spawn 2
