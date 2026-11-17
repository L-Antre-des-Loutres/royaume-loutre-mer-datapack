execute if score #rot rlm_spawn matches 0 run function rlm_spawn:generated/forceload_none
execute if score #rot rlm_spawn matches 1 run function rlm_spawn:generated/forceload_clockwise_90
execute if score #rot rlm_spawn matches 2 run function rlm_spawn:generated/forceload_clockwise_180
execute if score #rot rlm_spawn matches 3 run function rlm_spawn:generated/forceload_counterclockwise_90
scoreboard players set #footprint rlm_spawn 2
