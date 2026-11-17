# Exécutée par l'ancre, positionnée sur son bloc (niveau de la surface).
# #footprint : 0 charger les points du site, 1 vérifier le site, 2 attendre l'emprise puis poser.
execute if score #footprint rlm_spawn matches 0 run return run function rlm_spawn:step/load_site
execute if score #footprint rlm_spawn matches 1 run return run function rlm_spawn:step/check_site
execute if function rlm_spawn:step/footprint_loaded run function rlm_spawn:step/place
