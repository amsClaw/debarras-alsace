# Débarras Alsace — Site web (Strasbourg & Alsace)

**Projet** : site vitrine + générateur de leads pour une société de débarras basée à
Strasbourg, intervenant dans toute l'Alsace.

**Promesse** : « Vous nous montrez ce qui doit partir. On s'occupe du reste. »

**Statut** : 🏭 **V3 en ligne** — page unique, mobile d'abord, construite par l'usine
logicielle (8 histoires, `docs/HISTOIRES.md`). Bascule validée par Ams (recette H8) : la
V3 est le site, les anciennes versions (V1 multi-pages, V2) ont été retirées.

**Site en ligne** : **https://amsclaw.github.io/debarras-alsace/** (GitHub Pages, dépôt
public `amsClaw/debarras-alsace`).

**Suivi** : board `factory` de Hermes (mode supervisé de l'usine logicielle).

## Ce qu'est le site

Une seule page HTML/CSS/JS statique, sans étape de build ni dépendance :

- `index.html` — la page d'accueil : en-tête, héros avec devis express, zone
  d'intervention, prestations et déroulé, prix indicatif avec estimateur de volume,
  réalisations, avis, FAQ, contact, pied de page, plus une barre d'actions fixe en
  mobile (appeler / WhatsApp / devis).
- `mentions-legales.html`, `confidentialite.html` — pages légales, même charte que
  l'accueil.
- `404.html` — page d'erreur avec retour à l'accueil.
- `assets/` — styles (`style.css`), scripts (`config.js`, `site.js`, `zone.js`,
  `volume.js`, `etapes.js`, `message.js`) et photos.

## Où est la maquette

La maquette source (Claude Design) est dans `docs/design/` (fichiers `.dc.html` au
format canevas). Canevas original : voir `docs/CADRAGE_V3.md` pour le lien (privé,
compte d'Ams).

## Comment modifier les coordonnées

Tout ce qui identifie l'entreprise (téléphone, WhatsApp, e-mail) est centralisé dans
**`assets/config.js`**, dans `window.DEBARRAS`. C'est le seul fichier à modifier pour
mettre à jour ces informations — elles sont reprises automatiquement partout sur la
page (en-tête, héros, barre mobile, pied de page, données structurées JSON-LD).

Les emplacements encore à compléter avant mise en ligne définitive (raison sociale,
SIRET, adresse, domaine réel) sont repérables entre crochets, ex. `[Raison sociale]`,
`[06 XX XX XX XX]`, `[domaine-du-site]` — voir `docs/QUESTIONS_OUVERTES.md` pour la
liste complète.

## Comment lancer les tests

```
npm test
```

Lance `node --test tests/*.test.mjs` (aucune dépendance à installer). Les tests
vérifient la structure de la page, l'absence de fausse preuve sociale, le SEO
(titre, description, Open Graph, JSON-LD LocalBusiness), les images, le poids des
photos et l'absence de lien interne cassé.

## Ce qui attend l'entreprise

La liste complète des décisions en attente (raison sociale, numéros réels, avis
Google réels, photos réelles des chantiers, zone d'intervention exacte, mentions
légales) est dans **`docs/QUESTIONS_OUVERTES.md`**.

## Décisions

| Date | Décision |
|---|---|
| 2026-09-13 | Création du projet + dossier git |
| 2026-09-14 | V2 épurée (une page + pages légales) publiée dans `/v2/`, en comparaison avec la V1 |
| 2026-09-26 | Reprise par l'usine : V3 une page (maquette Claude Design `docs/design/`), construite dans `v3/` par 8 cartes |
| 2026-09-26 | **Bascule (H8, recette d'Ams)** : la V3 devient le site à la racine. V1 (pages générées, `src/`) et V2 (`v2/`, `v2_src/`) sont retirées. `v3/` n'existe plus : son contenu est à la racine |
