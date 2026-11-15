# Positionnée sur le coin du bloc de spawn. Mémorise le centre du bloc.
$setworldspawn ~ ~ ~ $(yaw)
summon minecraft:marker ~0.5 ~ ~0.5 {Tags:["rlm_spawn.tmp"]}
data modify storage rlm_spawn:data spawn.x set from entity @e[type=minecraft:marker,tag=rlm_spawn.tmp,limit=1] Pos[0]
data modify storage rlm_spawn:data spawn.y set from entity @e[type=minecraft:marker,tag=rlm_spawn.tmp,limit=1] Pos[1]
data modify storage rlm_spawn:data spawn.z set from entity @e[type=minecraft:marker,tag=rlm_spawn.tmp,limit=1] Pos[2]
kill @e[type=minecraft:marker,tag=rlm_spawn.tmp]
