# Photos à générer (voie recommandée)

Les photos actuelles du site sont **découpées dans la maquette**, donc minuscules (59 × 68 px pour les
avant/après, 86 × 50 px pour les cartes services, 272 × 320 px pour le héro). Elles servent à valider la
direction, pas à publier.

Pour les remplacer par de vraies photos nettes : **génère-les dans ChatGPT** (ou récupère des photos
réelles), nomme chaque fichier exactement comme ci-dessous, et dépose-les dans le dossier
`source-client/photos-hd/`. Ensuite je relance la commande et le site est à jour :

```bash
bash tools/photos.sh && python3 tools/build.py
```

## Règles communes (à mettre dans chaque prompt)

> Photo réaliste, style reportage, lumière naturelle du jour, Alsace (France), ambiance propre et
> professionnelle, **aucun texte, aucun logo, aucun filigrane**, pas de visage identifiable (personnes de
> dos ou hors cadre). Format paysage 3:2. Deux déménageurs en tenue de travail vert foncé et pantalon
> sombre, gants de manutention.

## 1. Héro — `hero.png` (format paysage large)

> Deux déménageurs de dos portant un fauteuil et des cartons vers un camion utilitaire blanc portes
> ouvertes, devant une maison de ville alsacienne en brique, rue calme, matin lumineux.

## 2. Cartes de services — format paysage

| Fichier | Prompt |
|---|---|
| `service-maison.png` | Façade extérieure d'une maison alsacienne avec jardin et allée, volets, arbres, ciel dégagé |
| `service-appartement.png` | Salon d'appartement lumineux avec canapé, table basse et cartons de déménagement prêts à partir |
| `service-cave.png` | Cave ou remise encombrée d'étagères en bois, caisses, outils, bouteilles, ampoule au plafond |
| `service-succession.png` | Intérieur d'un logement de famille : deux personnes de dos triant des cartons et des objets posés sur une table |
| `service-deces.png` | Pièce calme et sobre : fauteuils anciens, lampe, cartons fermés, parquet, lumière douce — aucune personne |
| `service-diogene.png` | Logement très encombré, pile d'objets et de cartons du sol au plafond, couloir étroit — vue de face, sans personne |
| `service-pro.png` | Open space de bureaux moderne avec chaises noires, cloisons vitrées, quelques cartons de déménagement |
| `service-nettoyage.png` | Pièce vidée tout juste nettoyée, sol brillant, plante verte, seau et balai posés à côté — lumineuse |

## 3. Ambiances

| Fichier | Format | Prompt |
|---|---|---|
| `situations.png` | portrait 2:3 | Intervenant de dos en polo vert, sangle de sac sur l'épaule, devant une entrée d'immeuble à Strasbourg, regardant le camion |
| `process.png` | portrait 3:4 | Intérieur rangé et lumineux : plantes vertes en pot au sol et sur étagère, quelques cartons kraft empilés, sol dégagé |
| `valorisation.png` | carré | Gros plan de deux mains tenant une jeune pousse verte dans de la terre, arrière-plan flou |
| `strasbourg.png` | paysage large | Strasbourg : Ponts Couverts et barrage Vauban sur l'Ill, flèche de la cathédrale au loin, toits traditionnels, début de soirée |
| `carte-alsace.png` | paysage | Illustration cartographique sobre du Bas-Rhin / Alsace, vert et beige, un repère de localisation sur Strasbourg, style plat, sans texte lisible |

## 4. Réalisations — paires AVANT / APRÈS (même pièce, même cadrage)

Chaque paire représente **la même pièce** avant et après débarras, avec les mêmes fenêtres et les mêmes
murs (important pour que la comparaison soit crédible).

| Avant | Après | Pièce |
|---|---|---|
| `real-appart-avant.png` | `real-appart-apres.png` | Salon d'appartement encombré de meubles rustiques et de cartons → même salon vidé, murs clairs, parquet net |
| `real-maison-avant.png` | `real-maison-apres.png` | Salle à manger de maison avec mobilier ancien en bois et vaisselle sur la table → même pièce vidée, sol et murs propres |
| `real-cave-avant.png` | `real-cave-apres.png` | Cave sombre avec étagères métalliques, cartons et matériel hétéroclite → même cave vide, sol balayé, passage dégagé |

## Ce qui ne peut pas être récupéré

La conversation ChatGPT citée (`chatgpt.com/share/6aa6f9eb-…`) ne contient que **deux images** : les deux
maquettes composites. Les photos qu'on y voit ont été générées *dans* la maquette : il n'existe aucun
fichier source plus grand à récupérer. La seule voie vers des photos nettes est de les régénérer.
