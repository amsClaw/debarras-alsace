# H12 — preuves de recette

## Comparaison aux références choisies par Ams

| Référence obligatoire | Capture livrée | Structure contrôlée |
|---|---|---|
| `docs/maquette-hero/C-ordinateur-1280.jpg` | `h12-1280.png` (1280 × 860) | Photo pleine largeur en décor, texte clair à gauche, carte blanche entière à droite |
| `docs/maquette-hero/C-grand-ecran-1440.jpg` | `h12-1440.png` (1440 × 900) | Même disposition C, grille 1200 px alignée avec l’en-tête |
| `docs/maquette-hero/D-telephone-haut.jpg` | `h12-375.png` (375 × 812) | Photo de 340 px immédiatement sous l’en-tête, badge et titre dessus, suite sur fond clair |
| `docs/maquette-hero/D-telephone-devis.jpg` | Parcours téléphone dans `h12-parcours.zip` | Garanties puis devis ; aucune carte à cheval sur la photo |

Les deux références D sont des images 750 × 1624 (échelle ×2). Le script lit les quatre
images de référence et vérifie la structure correspondante sur le site démarré.
Le bouton principal finit à y=695 px, avant la barre mobile qui commence à y=736 px.
Sur les captures ordinateur, le devis va de y=181,09 à y=771,25 px et reste dans la bande.
Le dégradé est renforcé dans la zone du texte pour assurer le contraste demandé.

Limite explicite : l’outil d’analyse visuelle a refusé les images (crédit fournisseur épuisé).
Les contrôles de géométrie et de pixels sont exécutés, mais ne remplacent pas l’appréciation
esthétique : le juge doit regarder les captures à côté des quatre références avant la recette d’Ams.

## Vérifications exécutées

- `npm test` : 98 tests verts, aucun ignoré ; les anciens contrôles de chevauchement sont adaptés à H12, pas supprimés.
- `node tools/verifier-hero.mjs` : 17 largeurs de 320 à 1920 px, trois étapes du devis et repli sans JavaScript conformes.
- `node tools/mesurer-site.mjs --paliers` : 18 largeurs, étapes 1→2→3→2→1, estimateur, pages annexes, marges et barre mobile conformes.
- Parcours filmé : 28 étapes vertes, zéro échec ; 10 captures téléphone et 9 ordinateur.
- Cahier HTML essayé à 320, 375, 414, 768 et 1280 px : pas de débordement, 12 cases utilisables ; retours depuis mentions légales et 404 essayés.

## Contraste raster (WCAG 2.1)

Le script prend les rectangles de chaque ligne de texte, puis capture le même rendu avec
l’encre transparente, sans enlever photo, dégradé ou badge. Il teste chaque pixel sous ces
rectangles, et retient le pire rapport blanc/fond, pas une moyenne ni une couleur CSS théorique.
Résultats complets : `h12-verification.json`. Minimum : 6,571:1 à 375 px, 7,224:1 à 1280 px,
7,262:1 à 1440 px (seuil demandé : 4,5:1). Les captures finales conservent le texte.

Le rapport filmé se trouve dans `h12-parcours.json` ; l’archive ZIP contient les vidéos WEBM,
les captures intermédiaires et le rapport original. Les minuscules vidéos supplémentaires
correspondent aux fenêtres WhatsApp fermées aussitôt : aucun message n’a été envoyé.
