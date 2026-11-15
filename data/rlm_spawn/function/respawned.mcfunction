# Sans lit, le jeu fait réapparaître sur le toit : on renvoie à l'intérieur.
scoreboard players set @s rlm_spawn.deaths 0
execute unless data entity @s SpawnX run function rlm_spawn:arrive with storage rlm_spawn:data spawn
