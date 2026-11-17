# Datapack Royaume de Loutre Mer

Datapack du modpack « Cobblemon Royaume de Loutre Mer » (Fabric, Minecraft 1.21.1).
Il contient les starters Cobblemon (`data/cobblemon/starters/`) et le spawn dans
la structure de départ (`data/rlm_spawn/`).

## Installation

Construire le jar puis le poser dans le dossier `mods/` du pack :

```bash
python tools/build_jar.py
```

Le jar est écrit dans `build/`. Il active tout le datapack : le spawn **et** les
starters RLM.

## Le spawn dans la structure

Le build actuel est le **Paradis Æther** (`tools/source/paradis-aether.litematic`),
posé **sur l'océan**.

À la création d'un monde, le jeu marque des emplacements (repères invisibles) dans
les biomes choisis. Au premier chargement, le datapack prend celui qui est le plus
proche du centre du monde, charge la seule zone du build, l'y pose une seule fois,
y place le point d'apparition et y envoie chaque nouveau joueur. Après une mort
sans lit, on revient au point d'apparition.

- Seuls les mondes tout neufs sont concernés : un monde déjà existant n'est
  jamais modifié (son spawn ne bouge pas).
- Si aucun terrain n'est trouvé, le spawn reste normal et un message le signale.
- `/locate structure rlm_spawn:spawn_lot` retrouve l'emplacement.

### Changer le biome

Liste des biomes : `data/rlm_spawn/tags/worldgen/biome/has_structure/spawn_lot.json`.
Actuellement tous les océans sauf les océans gelés (icebergs, surface en glace).

Sur l'océan, le repère ne modifie pas le terrain (`"terrain_adaptation": "none"`
dans `data/rlm_spawn/worldgen/structure/spawn_lot.json`). Pour un biome terrestre,
remettre `"beard_box"` (terrain aplani autour du build) et prévoir des fondations
(`foundation_depth` ci-dessous).

### Changer le build

1. Mettre le nouveau fichier Litematica dans `tools/source/` (une seule région,
   au plus 256 chunks à charger, soit environ 224 x 224 blocs) et indiquer son
   chemin dans `tools/spawn_base.json`. `tools/source/base.litematic` sert aux tests :
   le garder.
2. Régler `tools/spawn_base.json` (coordonnées comptées depuis le coin du build
   une fois les couches vides retirées) :
   - `ground_layer` : couche du build posée au niveau du bloc de surface (sol ou
     eau) ; les couches du dessous sont enterrées. `-1` : le build est posé juste
     au-dessus de la surface sans la remplacer (cas de l'océan) ;
   - `spawn` : `[x, y, z]` du bloc où l'on apparaît (2 blocs d'air, un bloc
     solide dessous) ;
   - `spawn_yaw` : direction du regard en degrés (180 = vers le nord du build) ;
   - `foundation_depth` : profondeur max d'un talus en escalier comblé sous le
     build (vide et eau seulement), utile sur terrain en pente. `0` sur l'océan ;
   - `ground_blocks` : blocs du terrain d'origine copiés avec le build (eau, algues…),
     pas reposés au niveau du sol et en dessous : le terrain du monde reste ;
   - `exclude_entities` : entités à ne pas recopier, par exemple les Pokémon
     sauvages (`cobblemon:pokemon`) présents lors de la copie ;
   - `empty_containers` : `true` vide coffres et tonneaux (restes de chantier).

   Les blocs de bedrock aux deux coins du Paradis Æther sont des repères de
   sélection : ils sont gardés.
3. Régénérer puis reconstruire le jar :

```bash
python tools/convert_spawn_base.py
```

```bash
python tools/build_jar.py
```

Le convertisseur avertit si le build contient des blocs de mods ou vient d'une
version plus récente que 1.21.1. Un build d'une version plus ancienne (le Paradis
Æther est en 1.16.5) garde sa version : le jeu met à jour ses blocs et ses
panneaux au chargement. Les fichiers de `data/rlm_spawn/structure/` et
`data/rlm_spawn/function/generated/` sont régénérés : ne pas les éditer à la main.

### Limites connues

- Le biome n'est vérifié qu'au point de départ : un grand build peut déborder
  sur une plage ou une île voisine.
- Le build est orienté au hasard d'un monde à l'autre.
- Au retour de l'End sans lit, le jeu fait réapparaître sur le toit.

## Tests

```bash
python -m unittest discover -s tools/tests -v
```

Test sur un vrai serveur 1.21.1 (nécessite `tools/.server/server.jar` et
`tools/.server/eula.txt`, non committés) :

```bash
python tools/server_test.py --java <chemin vers java.exe> --seed rlm-1
```

Options : `--biome minecraft:the_void` (biome introuvable) et `--existing-world`
(monde déjà existant).
