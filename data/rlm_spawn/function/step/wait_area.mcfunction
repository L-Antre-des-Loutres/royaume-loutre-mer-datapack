# La carte donne le milieu du chunk de départ ; l'ancre est à l'origine du gabarit,
# quelque part dans ce chunk : on la cherche dans tout le chunk.
scoreboard players add #timer rlm_spawn 1
execute if score #timer rlm_spawn matches 6000.. run return run function rlm_spawn:fail
$execute positioned $(x) -64 $(z) positioned ~-8 ~ ~-8 as @e[type=minecraft:marker,tag=rlm_spawn.anchor,dx=15,dy=448,dz=15,limit=1] at @s align xyz if function rlm_spawn:generated/area_loaded run function rlm_spawn:step/place
