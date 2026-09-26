# HISTOIRES — Débarras Alsace V3 (une page, maquette Claude Design)

On construit la **V3** du site dans le dossier `v3/`, sans toucher au site en ligne (V1 à la racine,
V2 dans `v2/`) jusqu'à l'histoire 8, qui fait la bascule après la recette d'Ams. Cadrage complet :
`docs/CADRAGE_V3.md`. Référence visuelle : `docs/design/Main.dc.html` (desktop), `Mobile.dc.html`,
`Devis.dc.html` — **reprendre leurs couleurs, tailles, rayons, espacements et textes** ; leurs balises
`<x-dc>`, `<sc-for>`, `<sc-if>` et `{{…}}` sont du format de maquette, pas du HTML à copier.

Règles communes à toutes les histoires :
- HTML/CSS/JS **statiques écrits à la main**, sans framework, sans dépendance npm d'exécution, sans étape
  de build. Le site doit fonctionner en ouvrant `v3/index.html` servi par un simple serveur statique.
- Chemins **relatifs** (le site est servi sous `/debarras-alsace/` sur GitHub Pages).
- Tests avec le runner natif : `npm test` = `node --test tests/`. Les tests lisent les fichiers HTML/CSS/JS
  comme du texte (pas de navigateur, pas de dépendance) ; utilitaires partagés dans `tests/outils.mjs`.
- Rien d'inventé : aucune note, aucun nombre d'avis, aucun témoignage, aucun prix, aucun SIRET. Les
  données manquantes restent des emplacements entre crochets, ex. `[note réelle]`.
- Accessibilité : vrais `<button>`, `<a href>`, `<label>` ; cibles tactiles ≥ 44 px ; contraste ≥ 4,5:1.
- Plafonds de l'usine : ≤ 500 lignes par fichier, ≤ 1500 lignes ajoutées au total, ≤ 20 fichiers.

---

## Histoire 1 — Socle V3 : tests, jetons de design, squelette de page

**Titre :** Poser le socle de la V3 dans `v3/` (page vide mais valide, jetons de design, coordonnées centralisées) et une suite de tests qui tourne.

**Complexité :** simple

**Critères d'acceptation :**
1. `package.json` à la racine : `"private": true`, `"type": "module"`, script `"test": "node --test tests/"`, **aucune** dépendance.
2. `tests/outils.mjs` exporte `lire(chemin)` (texte d'un fichier depuis la racine du dépôt) et `compter(texte, motif)`.
3. `v3/index.html` : `<html lang="fr">`, `<meta charset>`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, `<title>` et `<meta name="description">` non vides, le lien Google Fonts de Fraunces + Public Sans (mêmes graisses que la maquette), `v3/assets/style.css`, puis `v3/assets/config.js` (classique, `defer`) et `v3/assets/site.js` (`type="module"`, pour pouvoir importer des fonctions pures testables).
4. `v3/assets/style.css` définit sur `:root` les jetons du tableau « Système visuel » de `docs/CADRAGE_V3.md` en variables CSS (`--vert`, `--vert-2`, `--papier`, `--papier-2`, `--encre`, `--texte-2`, `--discret`, `--brique`, `--trait`, `--titres`, `--texte`), une remise à zéro minimale, `body` en Public Sans sur fond papier, et un conteneur `.conteneur` (largeur max 1200 px, marges latérales 16 px sous 768 px, 120 px au-delà de 1440 px).
5. `v3/assets/config.js` définit `window.DEBARRAS = { tel: "[06 XX XX XX XX]", telInternational: "33000000000", whatsapp: "33000000000", mail: "[contact@domaine.fr]" }` avec un commentaire : c'est le seul endroit à modifier quand l'entreprise donne ses vraies coordonnées.
6. `v3/index.html` contient un `<header>` (logo maison + « Débarras Alsace » + « Strasbourg & toute l'Alsace »), un `<main>` avec **un seul** `<h1>` provisoire, et un `<footer>` (reprendre le pied de page de la maquette, emplacements `[Raison sociale]`, `[SIRET]` compris).
7. Tests (`tests/socle.test.mjs`) : les points 1 à 6 vérifiés ; aucune occurrence de `4,0/5`, `4,9/5`, `150+ avis` ni `étoiles` dans `v3/`.
8. `npm test` passe, au moins 1 test collecté, 0 échec.

**Ne touche pas :** la racine du site (V1), `v2/`, `v2_src/`, `tools/`, `src/`.

**Résultat visible :** `v3/index.html` s'ouvre avec l'en-tête, un titre et le pied de page aux couleurs de la maquette.

---

## Histoire 2 — En-tête et héros avec devis express

**Titre :** Construire l'en-tête et le héros de la maquette, avec le formulaire « Devis express » qui prépare un message WhatsApp ou e-mail.

**Complexité :** standard

**Critères d'acceptation :**
1. En-tête (desktop) : logo, navigation par ancres (`#prestations`, `#deroule`, `#prix`, `#realisations`, `#zone`, `#faq`), lien `tel:` avec le numéro, bouton « Devis gratuit » (couleur brique) vers `#devis`. Sous 900 px, la navigation est masquée et seul le bouton « Devis » reste (pas de menu burger).
2. Héros en deux colonnes (une seule sous 900 px) : pastille « Entreprise locale · … », `<h1>` « Vous montrez ce qui doit partir. *On s'occupe du reste.* » (seconde phrase en italique brique), paragraphe, deux boutons (« Obtenir mon devis gratuit » → `#devis`, « Photos par WhatsApp » → lien `https://wa.me/<whatsapp>`), trois réassurances avec icônes SVG en ligne (devis sous 24 h, prix ferme, tri & réemploi).
3. Colonne de droite : photo `assets/photos/hero.jpg` (texte alternatif descriptif, `width`/`height` renseignés) et la carte `<form id="devis">` qui la chevauche comme dans la maquette.
4. Le formulaire contient : un groupe « Que faut-il débarrasser ? » de 6 choix exclusifs (boutons radio stylés en pastilles : Maison, Appartement, Cave · grenier, Local pro, Très encombré, Autre), « Code postal », « Téléphone » (chacun avec son `<label>`), une mention « Ajoutez 2–3 photos dans WhatsApp après l'envoi », le bouton « Envoyer sur WhatsApp » et un lien « Préférer l'e-mail ».
5. `v3/assets/site.js` : à l'envoi, compose le message « Bonjour, je souhaite un devis de débarras. Type : … Code postal : … Téléphone : … » puis ouvre `https://wa.me/<whatsapp>?text=<message encodé>` ; le lien e-mail ouvre `mailto:<mail>?subject=…&body=<même message>`. Les coordonnées viennent de `window.DEBARRAS`. Sans JavaScript, le bouton reste un lien `wa.me` fonctionnel.
6. La logique de composition du message est une fonction pure `composerMessage(champs)` exportée pour les tests (ex. `v3/assets/message.js` en module ES, importé par `site.js`), testée : tous les champs présents, champs vides omis, caractères spéciaux encodés dans l'URL.
7. Tests : un seul `<h1>`, 6 choix de type, chaque champ a un `<label>`, les liens `tel:` et `wa.me` utilisent les valeurs de `config.js`.
8. `npm test` vert.

**Ne touche pas :** V1, `v2/`, sections sous le héros.

**Résultat visible :** le haut de page ressemble à la maquette ; remplir le formulaire ouvre WhatsApp avec le message prêt.

---

## Histoire 3 — « On vient chez vous ? », prestations et déroulé

**Titre :** Ajouter le bandeau de vérification de zone par code postal, les 4 prestations en cartes photo et le déroulé en 3 étapes.

**Complexité :** standard

**Critères d'acceptation :**
1. Bandeau vert « On vient chez vous ? » avec un champ code postal (`aria-label`) et une zone de réponse `aria-live="polite"`. Règle, dans une fonction pure testée `verifierZone(cp)` : 5 chiffres commençant par `67` ou `68` → « Oui, nous intervenons chez vous. Devis gratuit sous 24 h. » ; 5 chiffres ailleurs → « Hors de notre zone habituelle : appelez-nous, on vous dit tout de suite. » ; sinon → message d'attente. Le champ n'accepte que des chiffres (5 max).
2. Section `#prestations` : sur-titre, `<h2>`, paragraphe, 4 cartes `<article>` (Maison & appartement, Cave grenier & garage, Bureaux & locaux, Logement très encombré) avec leur photo de `assets/photos/` (`loading="lazy"`, `alt` descriptif), titre, texte et mention comme dans la maquette ; puis la ligne « Aussi : » et ses 5 pastilles. Grille 4 colonnes → 2 sous 1100 px → 1 sous 600 px.
3. Section `#deroule` : 3 étapes en liste ordonnée `<ol>` (numéros 01–03 en Fraunces italique brique), puis la pastille « Aucune avance à verser… ».
4. Tests : `verifierZone` (67xxx, 68xxx, 75xxx, saisie incomplète) ; 4 articles de prestations ; 3 `<li>` dans le déroulé ; toutes les images de `v3/index.html` ont un `alt` non vide et existent sur le disque.
5. `npm test` vert.

**Ne touche pas :** V1, `v2/`, en-tête et héros (sauf corrections nécessaires).

**Résultat visible :** on tape son code postal et la réponse s'affiche immédiatement ; les prestations et les étapes apparaissent comme sur la maquette.

---

## Histoire 4 — Le prix en clair et l'estimateur de volume

**Titre :** Ajouter le bloc vert « Le prix, en clair » avec les 3 cas (indemnisé, gratuit, payant) et l'estimateur de volume interactif.

**Complexité :** standard

**Critères d'acceptation :**
1. Section `#prix` en deux colonnes (une seule sous 900 px) sur fond vert forêt, rayon 32 px : sur-titre, `<h2>` « Un débarras n'est pas toujours payant. », paragraphe, les 3 cas.
2. Carte « Estimez votre volume » : 6 choix exclusifs (Cave / garage, Studio, T2 – T3, T4 et +, Maison, Local pro) sous forme de boutons radio stylés ; T2 – T3 sélectionné par défaut.
3. Les 3 tuiles Volume / Camion 20 m³ / Durée se mettent à jour au choix, valeurs de la maquette : cave 3–8 m³ · 1 · 2–3 h ; studio 8–15 m³ · 1 · ½ journée ; T2–T3 15–30 m³ · 1–2 · 1 journée ; T4+ 30–45 m³ · 2–3 · 1–2 jours ; maison 40–80 m³ · 2–4 · 2–3 jours ; local pro « sur visite » · — · selon accès. Les valeurs vivent dans un seul tableau de données, fonction pure `estimer(choix)` testée. Mention « ordre de grandeur ».
4. Ligne « Fourchette de prix pour ce volume : [fourchette validée par l'entreprise] » (emplacement, aucun prix inventé), bouton « Recevoir mon prix ferme » → `#devis`.
5. Sans JavaScript : les tuiles affichent les valeurs T2 – T3.
6. Tests : `estimer` pour les 6 choix ; aucun motif `\d+ ?€` dans `v3/index.html`.
7. `npm test` vert.

**Ne touche pas :** V1, `v2/`, autres sections.

**Résultat visible :** cliquer « Maison » affiche 40–80 m³, 2–4 camions, 2–3 jours.

---

## Histoire 5 — Réalisations, avis, zone, FAQ et appel final

**Titre :** Terminer la page desktop : avant/après, bloc avis honnête, communes desservies, FAQ en accordéon, bandeau d'appel final et pied de page définitif.

**Complexité :** standard

**Critères d'acceptation :**
1. `#realisations` : 3 cartes avant/après (maison, appartement, cave) avec les photos `real-*-avant.jpg` / `real-*-apres.jpg`, étiquettes « Avant » / « Après », titre et `[commune] · [volume]` ; mention visible « Visuels d'illustration — remplacés par vos chantiers réels. »
2. Bloc avis : « Ils nous ont fait confiance », « Note Google : [note réelle] · [nombre réel] avis », lien « Voir tous les avis sur Google » (`href="#"` + commentaire à remplacer), 3 emplacements en pointillés `[Avis Google réel n°1]`… — **aucun** texte de témoignage.
3. `#zone` : `<h2>`, phrase « Votre commune n'est pas listée ? … », 12 communes (Strasbourg, Schiltigheim, Illkirch, Ostwald, Lingolsheim, Bischheim, Hœnheim, Geispolsheim, Haguenau, Molsheim, Obernai, Sélestat) en liste `<ul>`.
4. `#faq` : les 6 questions/réponses de la maquette en `<details>`/`<summary>` (fonctionne sans JavaScript), la première ouverte ; signe + / − en CSS.
5. Bandeau final brique « Besoin de vider un logement ? » avec « Obtenir mon devis » (→ `#devis`) et « Appeler » (`tel:`), puis le pied de page (contact, horaires, liens vers `mentions-legales.html` et `confidentialite.html`).
6. Tests : 6 `<details>` ; 12 communes ; mention « Visuels d'illustration » présente ; aucune balise `<blockquote>` contenant autre chose qu'un emplacement entre crochets.
7. `npm test` vert.

**Ne touche pas :** V1, `v2/`, sections déjà livrées (sauf corrections nécessaires).

**Résultat visible :** la page desktop complète correspond à `docs/design/Main.dc.html`.

---

## Histoire 6 — Mobile : barre fixe et devis en 3 étapes

**Titre :** Rendre la V3 impeccable sur téléphone : barre fixe Appeler / WhatsApp / Devis et formulaire de devis découpé en 3 étapes.

**Complexité :** standard

**Critères d'acceptation :**
1. Sous 768 px : barre `<nav aria-label="Actions rapides">` fixée en bas (fond vert forêt, 3 boutons : Appeler `tel:`, WhatsApp `wa.me`, « Devis photo » brique → `#devis`), comme `docs/design/Mobile.dc.html` ; le `body` reçoit un `padding-bottom` pour que rien ne soit masqué. Au-delà de 768 px la barre n'existe pas visuellement.
2. Sous 768 px, le formulaire `#devis` devient un parcours en 3 étapes (Type + code postal → Accès : Plain-pied / Ascenseur / Étage sans ascenseur → Téléphone + « Quand idéalement ? » + récapitulatif du message), avec barre de progression, « Étape n / 3 », boutons « Continuer » / retour, comme `docs/design/Devis.dc.html`. Le champ Accès est ajouté au message composé (desktop compris).
3. Amélioration progressive : sans JavaScript, toutes les étapes sont visibles d'un bloc et l'envoi fonctionne.
4. Aucune largeur fixe qui provoque un défilement horizontal à 360 px : test qui refuse, dans `style.css`, toute largeur ou `min-width` en px supérieure à 360 hors `@media (min-width: …)`.
5. Toutes les cibles cliquables font au moins 44 px de haut (boutons, pastilles, liens de la barre) : vérifié par un test sur les règles CSS des classes concernées.
6. Tests : barre présente avec 3 liens ; `composerMessage` inclut l'accès ; la logique d'étapes (fonction pure `etapeSuivante(etat)`) testée.
7. `npm test` vert.

**Ne touche pas :** V1, `v2/`, contenu des sections.

**Résultat visible :** sur téléphone, le devis se remplit en 3 écrans et la barre d'actions reste sous le pouce.

---

## Histoire 7 — Référencement, performance et pages légales

**Titre :** Préparer la V3 à la mise en ligne : balises SEO, données structurées honnêtes, images légères, pages légales et 404.

**Complexité :** standard

**Critères d'acceptation :**
1. `v3/index.html` : `<title>` ≤ 60 caractères contenant « Débarras » et « Strasbourg », meta description 120–160 caractères, Open Graph (`og:title`, `og:description`, `og:image` → `assets/photos/hero.jpg`, `og:locale` `fr_FR`), `<link rel="canonical">` avec emplacement de domaine commenté.
2. JSON-LD `LocalBusiness` (nom, zone desservie Bas-Rhin et Haut-Rhin, téléphone depuis la même valeur que `config.js`, horaires lundi–samedi 8 h–19 h) — **sans** `aggregateRating` ni `review`. Test qui le vérifie.
3. Toutes les images hors héros en `loading="lazy"` avec `width`/`height` ; le héros en `fetchpriority="high"`. Poids total de `v3/assets/photos/` ≤ 1,5 Mo (test).
4. `v3/mentions-legales.html` et `v3/confidentialite.html` repris de `v2/` et adaptés au style V3 (même en-tête et pied de page), emplacements `[…]` conservés ; `v3/404.html` simple avec retour à l'accueil.
5. Polices : `preconnect` vers `fonts.googleapis.com` et `fonts.gstatic.com`, `display=swap`.
6. Tests : points 1 à 4 ; chaque lien interne de `v3/*.html` (ancre ou fichier) pointe vers une cible existante.
7. `npm test` vert.

**Ne touche pas :** V1, `v2/`.

**Résultat visible :** la V3 est complète et prête à remplacer le site en ligne.

---

## Histoire 8 — Bascule : la V3 devient le site (recette d'Ams)

**Titre :** Remplacer le site en ligne par la V3 : `v3/` passe à la racine, V1 et V2 sont retirées, le README est mis à jour.

**Complexité :** standard

**Critères d'acceptation :**
1. Le contenu de `v3/` est déplacé à la racine (`index.html`, `mentions-legales.html`, `confidentialite.html`, `404.html`, `assets/`) ; le dossier `v3/` n'existe plus ; les tests pointent vers les nouveaux chemins.
2. Supprimés : toutes les pages générées de la V1 (`a-propos/`, `avis-clients/`, `blog/`, `contact-devis/`, `faq/`, `mentions-legales/`, `politique-confidentialite/`, `realisations/`, `services/`, `situations/`, `tarifs/`, `villes/`, l'ancien `assets/`), `src/`, `v2/`, `v2_src/`, `tools/build.py`, `tools/build_v2.py`, `tools/smoke.py`. **Conservés** : `docs/`, `source-client/`, `tools/generer_photos.py`, `tools/photos.sh`.
3. `sitemap.xml` ne liste que l'accueil et les deux pages légales ; `robots.txt` le référence ; plus aucune balise `noindex` sur l'accueil.
4. `README.md` réécrit : ce qu'est le site, où est la maquette (`docs/design/`, lien du canevas), comment modifier les coordonnées (`assets/config.js`), comment lancer les tests, la liste de ce qui attend l'entreprise (`docs/QUESTIONS_OUVERTES.md`).
5. Tests : aucun fichier HTML hors `index.html`, `mentions-legales.html`, `confidentialite.html`, `404.html` et `docs/design/` ; aucun lien interne cassé.
6. `npm test` vert.

**Ne touche pas :** `docs/`, `source-client/`, `.factory.json`.

**Résultat visible :** https://amsclaw.github.io/debarras-alsace/ affiche la V3. **Checkpoint : cette fusion attend l'accord d'Ams (recette).**
