# Spawn dans une structure unique — résumé validé

Validé en conversation le 2026-11-15.

## But

À chaque nouveau monde créé avec le modpack « Cobblemon Royaume de Loutre Mer »
(Fabric, Minecraft 1.21.1), une structure (à terme le Paradis Æther) apparaît
en **un seul exemplaire**, dans **un biome précis**, avec le terrain raccordé
autour, et **tous les joueurs y apparaissent**.

## Objectifs

- La structure est posée automatiquement, sans action du joueur ni mod en plus.
- Elle n'existe qu'une fois par monde.
- Elle n'apparaît que dans le biome choisi (une ligne à changer ;
  `minecraft:plains` en provisoire).
- Le terrain se fond autour d'elle (pas de colline coupée net).
- Tout nouveau joueur apparaît dedans. Sans lit, on y revient après une mort.
- Changer de build = relancer un script de conversion sur un autre `.litematic`.

## Hors périmètre

- Le vrai Paradis Æther : on travaille avec la base de test
  (`Cobblemon base principal.litematic`, 82×87×81, blocs vanilla, sans entité).
- Les mondes déjà existants ne sont pas modifiés.
- Rien n'est poussé sur GitHub sans demande explicite.

## Ce qui ferait de ça un échec

- Un deuxième exemplaire du build dans le même monde.
- Un build posé hors du biome choisi.
- Un monde existant dont le spawn change après mise à jour du pack.

## Contraintes

- Livré dans le dépôt `L-Antre-des-Loutres/royaume-loutre-mer-datapack`, sous
  forme de jar à poser dans `mods/` (ajout d'un `fabric.mod.json`), comme le
  jar des dresseurs. Le pack n'a pas de mod chargeur de datapacks.
- Le build source est fait en 1.21.7 ; il ne doit utiliser que des blocs qui
  existent en 1.21.1 ou dans les mods du pack.
- Le jar embarque aussi `data/cobblemon/starters/default.json`, déjà présent
  dans le dépôt : l'installer active donc ces starters.

## Approches considérées

| Approche | Unique | Biome | Terrain fondu | Retenue |
|---|---|---|---|---|
| Pose à 0,0 par script | oui | non | non | non |
| Vraie structure de génération, très espacée | presque | oui | oui | non : pas strictement unique, spawn très loin du centre |
| **Terrains préparés + pose unique** | oui | oui | oui | **oui** |
| Talus taillés par script après la pose | oui | oui | grossier | non : pierre nue |
| Mod Java dédié | oui | oui | oui | non : démesuré, pas de JDK |
| Monde pré-construit livré avec le pack | oui | oui | oui | non : même seed pour tous |

### L'approche retenue

1. Un **repère invisible** : une vraie structure de génération, vide, de la
   taille du build, limitée au biome choisi. Là où elle tombe, elle aplanit et
   raccorde le terrain (comme sous un village). `/locate` la trouve.
2. Une **pose unique** : à la création du monde, un script demande au jeu le
   repère le plus proche du centre (mécanisme des cartes au trésor), y pose le
   build, puis ne recommence jamais.
3. Le **spawn** : le point d'apparition du monde est fixé dans le build, et
   chaque nouveau joueur y est téléporté.

Conséquence acceptée : d'autres terrains préparés existent ailleurs dans le
même biome, sous forme de clairières plates et vides, espacées pour rester
rares.

## Choix laissés au réalisateur (non discutés, à corriger si besoin)

- Seuls les mondes tout neufs sont concernés (monde âgé de moins de 30 s au
  premier chargement du datapack).
- Si aucun repère n'est trouvé à distance raisonnable, le spawn reste normal et
  un message le signale aux joueurs.
- Le jeu vanilla fait réapparaître sur le bloc le plus haut de la colonne, donc
  sur le toit d'un bâtiment : le retour après une mort sans lit passe par une
  téléportation au point de spawn intérieur.
- Limite connue : au retour de l'End sans lit, le jeu place le joueur sur le
  toit ; non traité.
- Test : serveur Minecraft 1.21.1 sans interface, avec le Java 21 livré par
  Modrinth. Demande le téléchargement du `server.jar` officiel et l'acceptation
  de la licence Minecraft par l'utilisateur. Test final : créer un nouveau monde
  dans le pack complet.
