# Le site (emprise + marge) doit être entièrement dans le bon biome, avec la bonne surface.
execute unless function rlm_spawn:step/site_loaded run return 0
execute store result score #site_ok rlm_spawn run function rlm_spawn:step/site_ok
function rlm_spawn:step/site_unforceload
execute if score #site_ok rlm_spawn matches 0 run return run function rlm_spawn:step/reject_site
function rlm_spawn:step/load_footprint
