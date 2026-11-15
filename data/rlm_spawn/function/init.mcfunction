# Premier chargement dans ce monde : on ne touche qu'aux mondes de moins de 30 s.
execute store result score #age rlm_spawn run time query gametime
scoreboard players set #state rlm_spawn -1
execute if score #age rlm_spawn matches ..599 run function rlm_spawn:start
