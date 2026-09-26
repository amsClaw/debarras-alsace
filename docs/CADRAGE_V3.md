# Cadrage V3 — reprise par l'usine (2026-09-26)

## Le sujet, compris

Une entreprise de débarras **qui se lance** à Strasbourg (Eurométropole, puis Bas-Rhin et Haut-Rhin).
Elle vide un lieu de A à Z — tri, manutention, évacuation, valorisation (revente, don, recyclage),
balayage — et annonce un **prix ferme avant l'intervention**. Ses clients sont presque toujours sous
contrainte de date : succession, vente immobilière, entrée en EHPAD, fin de bail, logement très encombré.

Le site n'est **pas** la source principale de clients (Google Maps et les prescripteurs le sont, voir le
plan terrain). Son rôle : **transformer** un visiteur pressé en demande de devis, en moins d'une minute,
avec des photos. D'où une V3 en **une seule page**, mobile d'abord, dont chaque section pousse au devis.

## Historique

| Version | Date | Ce que c'était | Sort |
|---|---|---|---|
| V1 | 2026-09-14 | 49 pages générées (services, villes, blog) | jugée trop lourde pour une entreprise qui démarre (décision client) — supprimée à la bascule V3 |
| V2 | 2026-09-14 | une page épurée dans `/v2/`, formulaire express WhatsApp | bonne direction, trop austère — remplacée par V3 |
| **V3** | 2026-09-26 | une page, maquette Claude Design, plus stylée et plus pratique | construite par l'usine dans `/v3/`, bascule à la racine après recette d'Ams |

## La maquette (Claude Design)

- Canevas : https://claude.ai/artifact/K7AAund19S5PhwGvKqthMk (privé, compte d'Ams)
- Copie de référence dans le dépôt (les ouvriers n'ont pas le réseau) : `docs/design/`
  - `Main.dc.html` — accueil desktop 1440 px, toutes les sections, styles exacts en ligne
  - `Mobile.dc.html` — premier écran mobile 390 px + barre fixe Appeler / WhatsApp / Devis
  - `Devis.dc.html` — parcours de devis mobile en 3 étapes
  Ces fichiers sont au format du canevas (balises `<x-dc>`, `<sc-for>`, `{{…}}`) : ils servent de
  **référence visuelle et de valeurs** (couleurs, tailles, textes), pas de code à copier tel quel.
- Photos : `v3/assets/photos/` (visuels d'illustration générés en local, à remplacer par les vrais
  chantiers — le site le dit sous les réalisations).

### Système visuel « atelier alsacien »

| Jeton | Valeur | Usage |
|---|---|---|
| vert forêt | `#1E3A2B` | titres, bandeaux sombres, pied de page |
| vert 2 | `#2F5A40` / `#2A4A37` | icônes, cartes sur fond sombre |
| papier | `#F5F0E6` | fond de page |
| papier 2 | `#EDE5D5` | cartes des étapes |
| encre | `#1F221E` / texte secondaire `#3D413A` / discret `#5B5F57` | texte |
| brique | `#B5461B` | **une seule couleur d'action** : boutons devis, accents (blanc dessus : contraste ≥ 4,5) |
| trait | `#D6CCB6` / `#E2D9C6` | bordures de champs, séparateurs |
| titres | Fraunces 500/600 (italique pour l'accroche) | Google Fonts |
| texte | Public Sans 400–700 | Google Fonts |
| rayons | 12 px (champs, boutons), 20–22 px (cartes), 32 px (bloc prix) | |

## Décisions (techniques tranchées par Claude, fonctionnelles à valider par Ams)

| Date | Décision | Qui |
|---|---|---|
| 2026-09-26 | Le projet rentre dans l'usine en **mode supervisé** (site public sur GitHub Pages, client réel) ; checkpoint unique = la bascule V3 (recette d'Ams). | Ams (demande) / Claude (mécanisme) |
| 2026-09-26 | V3 = HTML/CSS/JS statiques écrits à la main, **sans étape de build** ni framework ; tests `node --test`. Les générateurs Python V1/V2 disparaissent à la bascule. | Claude |
| 2026-09-26 | Coordonnées (téléphone, WhatsApp, e-mail) en **un seul endroit** : `v3/assets/config.js` (`window.DEBARRAS`) + les liens `tel:` / `wa.me` du HTML vérifiés par un test de cohérence. | Claude |
| 2026-09-26 | Formulaire **sans serveur** : il compose le message et ouvre WhatsApp ou l'e-mail (repris de V2). Pas de stockage de photos côté site (RGPD simple). | Claude |
| 2026-09-26 | Rien d'inventé : note Google, avis, fourchettes de prix, SIRET restent des emplacements `[…]` tant que l'entreprise ne les a pas fournis. | brief client, section 10 |

## Ce qui attend l'entreprise (bloquant avant la bascule)

Voir `docs/QUESTIONS_OUVERTES.md` : raison sociale et SIRET, **vrai numéro** (appel + WhatsApp),
e-mail, fiche Google (note et avis réels), fourchettes de prix validées, photos réelles, nom de domaine.

## Plan terrain

Document « Débarras Alsace — plan de terrain pour gagner les premiers clients » (Claude Docs) :
https://claude.ai/code/artifact/303c95fb-84ad-40b0-86fb-5761b6dd8a3b
