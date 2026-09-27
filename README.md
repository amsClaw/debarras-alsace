# Débarras Alsace — Site web (Strasbourg & Alsace)

**Projet** : site vitrine + générateur de leads pour une société de débarras basée à
Strasbourg, intervenant dans toute l'Alsace (Bas-Rhin / Haut-Rhin).

**Promesse** : « Vous nous montrez ce qui doit partir. On s'occupe du reste. »

**Statut** : 🏭 Site V3 — une seule page, statique, sans dépendance ni étape de build.
Après fusion et validation de la recette (Ams), le site est en ligne à cette adresse :
**https://amsclaw.github.io/debarras-alsace/** (GitHub Pages, dépôt public
`amsClaw/debarras-alsace`)

## Ce qu'est le site

Une page d'accueil (`index.html`) : héros avec devis express (code postal + estimation
de volume), zone d'intervention 67/68/75, présentation des prestations (maison,
appartement, cave/grenier, professionnel, syndrome de Diogène), 3 étapes du processus,
FAQ, barre d'appel/WhatsApp collante en mobile. Deux pages légales (`mentions-legales.html`,
`confidentialite.html`) et une page d'erreur (`404.html`).

Le formulaire de devis ne passe par aucun serveur : les réponses composent un message
et ouvrent WhatsApp (`wa.me/…`) ou l'e-mail du visiteur, qui reste libre de l'envoyer.

## Où est la maquette

La maquette source (Claude Design) est conservée dans `docs/design/` :
`Main.dc.html`, `Mobile.dc.html`, `Devis.dc.html`. Canevas d'origine (privé, compte
d'Ams) : https://claude.ai/artifact/K7AAund19S5PhwGvKqthMk. Le cadrage complet est
dans `docs/CADRAGE_V3.md`, la spec fonctionnelle dans `docs/FRONT_SPEC.md` et
l'historique des histoires livrées dans `docs/HISTOIRES.md`.

## Comment modifier les coordonnées

Un seul fichier à toucher : `assets/config.js`. Il centralise le téléphone, le numéro
WhatsApp et l'e-mail de contact ; le reste du site les lit via `window.DEBARRAS`. Les
valeurs entre crochets (`[06 XX XX XX XX]`, `[contact@domaine.fr]`) sont des emplacements
à remplacer par les vraies coordonnées de l'entreprise — jamais des données inventées.

Le domaine officiel (balise `<link rel="canonical">` de `index.html`) et les raisons
sociale/adresse des pages légales (`mentions-legales.html`, `confidentialite.html`, entre
crochets eux aussi) sont à compléter de la même façon une fois l'entreprise identifiée.

## Comment lancer les tests

```
npm test
```

Lance `node --test tests/*.test.mjs` : aucune dépendance à installer, seule la
bibliothèque standard de Node est utilisée. Les tests vérifient le contenu des pages,
le CSS, le JS du devis (composition du message, estimation de volume, zone
d'intervention), le SEO (meta, Open Graph, JSON-LD, sitemap) et l'absence de liens
internes cassés ou d'avis/notes inventés.

## Ce qui attend l'entreprise

La liste complète des décisions encore ouvertes (raison sociale, numéros réels, avis
Google, photos, zone d'intervention exacte, mentions légales…) est dans
`docs/QUESTIONS_OUVERTES.md`. Tant que ces réponses ne sont pas fournies, le site reste
en ligne avec des emplacements `[...]` explicites à la place des données réelles — aucune
donnée n'est inventée (nom, téléphone, avis, prix).

## Historique

| Date | Décision |
|---|---|
| 2026-09-13 | Création du projet |
| 2026-09-26 | **Reprise par l'usine** : conception d'une V3 une page (maquette Claude Design), construite dans `v3/` par 8 histoires, puis bascule à la racine (H8) après recette d'Ams — V1 (multi-pages) et V2 (page intermédiaire) retirées. Stack : statique sans build, tests `node --test` |
