scoreboard players set #state rlm_spawn 1
scoreboard players set #timer rlm_spawn 0
scoreboard players set #c360 rlm_spawn 360
function rlm_spawn:generated/constants
execute in minecraft:overworld run forceload add 0 0
