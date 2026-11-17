# Site refusé : on libère le repère et on cherche le suivant (la carte ne rend jamais deux fois le même).
function rlm_spawn:step/unforceload_anchor with storage rlm_spawn:data lot
scoreboard players add #attempts rlm_spawn 1
scoreboard players set #footprint rlm_spawn 0
execute if score #attempts rlm_spawn matches 16.. run return run function rlm_spawn:fail
scoreboard players set #timer rlm_spawn 0
scoreboard players set #state rlm_spawn 1
execute in minecraft:overworld run forceload add 0 0
