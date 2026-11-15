# Au chargement du datapack. #state : 1 localise, 2 attend la zone, 3 terminé,
# -1 monde existant ignoré, -2 échec.
scoreboard objectives add rlm_spawn dummy
scoreboard objectives add rlm_spawn.deaths deathCount
execute unless score #state rlm_spawn matches -2147483648..2147483647 run function rlm_spawn:init
