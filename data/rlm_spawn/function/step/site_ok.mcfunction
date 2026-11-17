execute if score #rot rlm_spawn matches 0 run return run function rlm_spawn:generated/site_ok_none
execute if score #rot rlm_spawn matches 1 run return run function rlm_spawn:generated/site_ok_clockwise_90
execute if score #rot rlm_spawn matches 2 run return run function rlm_spawn:generated/site_ok_clockwise_180
execute if score #rot rlm_spawn matches 3 run return run function rlm_spawn:generated/site_ok_counterclockwise_90
return fail
