# Exécutée à l'ancre.
execute if score #rot rlm_spawn matches 0 run function rlm_spawn:generated/unforceload_none
execute if score #rot rlm_spawn matches 1 run function rlm_spawn:generated/unforceload_clockwise_90
execute if score #rot rlm_spawn matches 2 run function rlm_spawn:generated/unforceload_clockwise_180
execute if score #rot rlm_spawn matches 3 run function rlm_spawn:generated/unforceload_counterclockwise_90
