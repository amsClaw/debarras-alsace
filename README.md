# Débarras Alsace — Site web (Strasbourg & Alsace)

**Projet** : site vitrine et générateur de demandes de devis pour une société de débarras basée
à Strasbourg, intervenant dans toute l'Alsace (Bas-Rhin, Haut-Rhin).

**Promesse** : « Vous nous montrez ce qui doit partir. On s'occupe du reste. »

**En ligne** : **https://amsclaw.github.io/debarras-alsace/** (GitHub Pages, dépôt public
`amsClaw/debarras-alsace`). Le lien n'est pas diffusé : il sert à la validation par Ams, le
nom de domaine définitif viendra ensuite.

## Ce qu'est le site

Une seule page, en HTML/CSS/JS statiques, sans étape de build ni dépendance :

| Fichier | Rôle |
|---|---|
| `index.html` | Accueil : héros avec devis express, zone d'intervention, prestations, syndrome de Diogène, déroulé, prix et estimateur de volume, réalisations, FAQ, appel final, barre fixe mobile (Appeler · WhatsApp · Devis) |
| `mentions-legales.html`, `confidentialite.html` | Pages légales |
| `404.html` | Page introuvable, correcte à n'importe quelle profondeur d'adresse |
| `assets/` | `style.css`, scripts (`site.js`, `message.js`, `etapes.js`, `volume.js`, `zone.js`), `config.js`, photos et polices hébergées sur le site (aucun appel à Google Fonts) |
| `sitemap.xml`, `robots.txt` | Plan du site (accueil et pages légales) et consignes aux moteurs |

Le devis ne passe par aucun serveur : les réponses du visiteur composent un message qui ouvre
WhatsApp (`wa.me/…`) ou sa messagerie, et il reste libre de l'envoyer.

## Où est la maquette

La maquette source (Claude Design) est dans `docs/design/` : `Main.dc.html`, `Mobile.dc.html`,
`Devis.dc.html`. Canevas d'origine (privé, compte d'Ams) :
https://claude.ai/artifact/K7AAund19S5PhwGvKqthMk

Le cadrage est dans `docs/CADRAGE_V3.md`, les histoires livrées dans `docs/HISTOIRES.md` et le
cahier de recette dans `docs/CAHIER_DE_RECETTE.md`.

## Comment modifier les coordonnées

Un seul fichier : **`assets/config.js`**. Il porte le téléphone affiché, le numéro
international (liens `tel:`), le numéro WhatsApp et l'e-mail ; toutes les pages les lisent via
`window.DEBARRAS`. Le même fichier réaffiche les blocs aujourd'hui masqués faute
d'information : avis clients et note Google, commune et volume sous les photos avant/après,
fourchettes de prix, raison sociale et SIRET du pied de page. Tant qu'un réglage est vide, le
bloc correspondant reste masqué — rien n'est inventé.

Les champs de l'entreprise encore entre crochets dans `mentions-legales.html` (raison sociale,
forme juridique, adresse, SIRET, représentant légal) se complètent directement dans la page.

## Comment lancer les tests

```
npm test
```

Lance `node --test tests/*.test.mjs` : rien à installer, seule la bibliothèque standard de Node
est utilisée. Les tests vérifient le contenu des pages, le CSS, le JS du devis (message,
estimation de volume, zone), le référencement (meta, Open Graph, JSON-LD, plan du site), les
coordonnées, la typographie, l'absence de liens internes cassés, de fichiers HTML hors du site
et d'avis inventés.

Mesures dans un vrai navigateur (hors `npm test`, nécessite Playwright et Chromium déjà
installés sur la machine) :

```
node tools/mesurer-site.mjs --paliers
```

Pour voir le site en local : `npx serve .` puis ouvrir l'adresse affichée.

## Ce qui attend l'entreprise

La liste des informations encore à fournir (raison sociale, forme juridique, adresse, SIRET,
directeur de la publication, vrais avis et note Google, photos des chantiers, fourchettes de
prix…) est dans **`docs/QUESTIONS_OUVERTES.md`**.

Photos : les visuels actuels sont des illustrations générées en local
(`tools/generer_photos.py`) ; les vraies photos des chantiers se déposent dans
`source-client/photos-hd/` puis `bash tools/photos.sh` les prépare dans `assets/photos/`.

## Historique

| Date | Décision |
|---|---|
| 2026-09-13 | Création du projet : brief client (`source-client/`), site multi-pages V1 généré par script |
| 2026-09-26 | Reprise par l'usine : V3 d'une seule page (maquette Claude Design), construite dans `v3/` |
| 2026-10-01 | Corrections de la recette d'Ams (H10 mise en page, H11 textes, coordonnées, référencement), puis bascule H8 : la V3 passe à la racine, V1 et V2 sont retirées |
