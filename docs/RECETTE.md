# RECETTE V1 — Débarras Alsace

Date : 2026-09-13 · Réalisée par l'agent (validation déléguée par Ams) · Site : V1 statique 49 pages.

## 1. Contrôles automatiques (build)

| Contrôle | Résultat |
|---|---|
| Pages générées | **49** (+ `404.html`, `sitemap.xml`, `robots.txt`, 4 fichiers d'assets) |
| Titres `<title>` uniques | ✅ (2 doublons détectés au 1er passage → corrigés) |
| Meta descriptions présentes et uniques | ✅ |
| Un seul `<h1>` par page | ✅ |
| Liens internes | ✅ aucun lien mort (1 lien mort détecté → corrigé) |
| Promesses interdites (« débarras gratuit », « rachat garanti ») | ✅ aucune occurrence |
| Sitemap | 49 URLs, `robots.txt` avec référence sitemap |

## 2. Smoke test HTTP (serveur local, 127.0.0.1:8100)

- **55 requêtes** : 49 pages + `style.css`, `app.js`, `favicon.svg`, `og.svg`, `robots.txt`, `404.html`.
- **Toutes en HTTP 200**, aucun titre en doublon, un seul H1 par page.

## 3. Tests fonctionnels dans un vrai navigateur (Chrome, CDP)

| Test | Résultat |
|---|---|
| Erreurs JavaScript sur 15 pages (accueil, service, ville, tarifs, contact, blog, situation, FAQ, réalisations, avis, à propos, 3 hubs) | **0 erreur**, 0 `console.error` |
| Vérification de zone — code desservi (67000) | ✅ « nous intervenons à Strasbourg » |
| Vérification de zone — code hors zone (75001) | ✅ message neutre + invitation à envoyer la demande |
| Simulateur de volume (5 boutons) | ✅ sélection visuelle + estimation en m³ + mention « estimation indicative » |
| Formulaire complet 7 étapes | ✅ validation bloquante à l'étape 1 sans saisie, 7 étapes franchies, récapitulatif complet (11 champs), lien e-mail pré-rempli généré |
| Menu mobile (390 px) | ✅ panneau plein écran, 11 liens, ouverture/fermeture, verrouillage du défilement |
| Barre mobile Appeler / WhatsApp / Devis | ✅ affichée sous 1180 px, 3 zones égales |

## 4. Défauts trouvés et corrigés pendant la recette

| # | Défaut observé | Correction |
|---|---|---|
| 1 | **Bandeau desktop débordant à 1280 px** : 11 entrées de menu + téléphone + CTA → numéro cassé sur 5 lignes, bouton coupé au bord droit | menu d'en-tête réduit à 8 entrées (Avis / À propos / FAQ restent en pied de page, menu mobile et liens croisés), point de rupture du menu complet porté à **1180 px**, `white-space: nowrap` sur le téléphone |
| 2 | **Chevauchement possible entre 900 et 1180 px** (menu visible mais non mis en forme) | les règles du menu desktop ont été regroupées dans un seul palier à 1180 px |
| 3 | `title` en double entre la page service « après décès » et la situation « décès » ; `h1` en double entre Tarifs et l'article de blog sur le prix | titres/h1 rendus uniques |
| 4 | Lien mort vers une commune voisine (« Hœnheim ») depuis les pages villes | lien construit depuis le slug réel de la ville |
| 5 | Champ de photos au style natif du navigateur | zone de dépôt stylée avec compteur (« 3 photos sélectionnées ») |

**Vérification par mesure (pas à l'œil)** après correction, à 1024 / 1120 / 1180 / 1240 / 1280 / 1366 / 1512 / 1920 px :
aucun débordement de page (0 px), menu complet sans chevauchement dès 1180 px (marge de 567 px avant les actions),
menu burger en dessous. Captures desktop et mobile conservées dans `docs/captures/`.

## 5. Illustrations (visuels de démonstration) — ajoutées puis vérifiées à l'œil

24 illustrations vectorielles générées par `src/illustrations.py`, branchées sur les réalisations (paires
avant/après), les pages services, situations, blog, à propos, la section valorisation et le simulateur de
volume (5 niveaux de camion).

| Contrôle | Résultat |
|---|---|
| Génération | 24 SVG écrits dans `assets/illus/` à chaque build |
| Chargement réel des images | vérifié dans le navigateur (`naturalWidth > 0`) sur réalisations 12/12, accueil 13/13, tarifs 6/6, blog 4/4, pages services 1/1 |
| Références | contrôle automatique du build étendu aux attributs `src` : aucun fichier référencé manquant |
| Relecture visuelle (vision) | 2 défauts corrigés : plante posée sur la ligne mur/sol (donc « flottante ») et décors incohérents (une cave ou un garage ne peuvent pas avoir une fenêtre de séjour) → décors dédiés (briques + ampoule, porte sectionnelle, poutres + lucarne) et plante posée au sol, plus grande, avec ombre portée |

⚠️ **Piège rencontré** : avec `loading="lazy"`, les images restaient vides dans certains contextes
d'aperçu/capture (défilement programmatique). Le chargement différé a été retiré pour ces SVG de quelques
kilo-octets — il n'apporte rien ici et il masquait le rendu réel. À réintroduire uniquement pour de vraies
photos, plus lourdes.

## 6. Ce qui reste à valider par un humain (non automatisable)

- Rendu sur **iPhone réel** (Safari), en particulier la barre fixe du bas et le sélecteur de photos.
- Validation par Ams du contenu éditorial et de la direction visuelle.
- **Données client** : téléphone, WhatsApp, e-mail, raison sociale, fiche Google, lot photo, fourchettes tarifaires
  (voir `docs/QUESTIONS_OUVERTES.md`). Les valeurs actuelles proviennent de la maquette et sont signalées comme
  provisoires (page Contact, page Mentions légales, page À propos).
- Envoi réel du formulaire : en V1 le récapitulatif part depuis la messagerie du visiteur (un site statique ne peut
  ni envoyer d'e-mail ni recevoir de photos). Branchement serveur documenté dans `docs/ARCHITECTURE.md` §5.

## 6. Verdict

**V1 conforme au PRD** : les 14 sections de la page d'accueil, les 13 prestations, les 7 situations, les 12 communes,
la page Tarifs avec simulateur, le blog (4 articles), la FAQ, le formulaire 7 étapes et le SEO technique sont en place
et vérifiés par exécution réelle. Aucune promesse interdite, aucune preuve inventée.
