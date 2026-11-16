# Exécutée par l'ancre, positionnée sur son bloc.
execute if score #footprint rlm_spawn matches 0 run return run function rlm_spawn:step/load_footprint
execute if function rlm_spawn:step/footprint_loaded run function rlm_spawn:step/place
