# L'ancre est à l'origine du gabarit, dans le chunk indiqué par la carte : on la cherche
# dans ce chunk. 1er passage : on charge l'emprise du build ; ensuite on attend qu'elle soit prête.
scoreboard players add #timer rlm_spawn 1
execute if score #timer rlm_spawn matches 6000.. run return run function rlm_spawn:fail
$execute positioned $(x) -64 $(z) positioned ~-8 ~ ~-8 as @e[type=minecraft:marker,tag=rlm_spawn.anchor,dx=15,dy=448,dz=15,limit=1] at @s align xyz run function rlm_spawn:step/at_anchor
