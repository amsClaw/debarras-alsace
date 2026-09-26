# Débarras Alsace — Site web (Strasbourg & Alsace)

**Projet** : site vitrine + générateur de leads, très orienté conversion et SEO local,
pour une société de débarras basée à Strasbourg intervenant dans toute l'Alsace.

**Promesse** : « Vous nous montrez ce qui doit partir. On s'occupe du reste. »

**Statut** : 🏭 **Repris par l'usine le 2026-09-26** (mode supervisé) — V3 une page en préparation dans `v3/`,
maquette Claude Design, 8 histoires prêtes (`docs/HISTOIRES.md`), en attente de la validation du cadrage par Ams.
Cadrage : `docs/CADRAGE_V3.md` · Plan terrain (Claude Docs) : https://claude.ai/code/artifact/303c95fb-84ad-40b0-86fb-5761b6dd8a3b
**Site en ligne** : **https://amsclaw.github.io/debarras-alsace/** (GitHub Pages, dépôt public `amsClaw/debarras-alsace`)
**Dossier local** : `/Users/amsfox/projets/debarras-alsace` (repo git)
**Process** : Process AAS V0.3 — mode **complet** (projet commercial, SEO, lead-gen, multi-pages)
**Génération du site** : `python3 tools/build.py` (site statique, stdlib uniquement) puis
`python3 tools/smoke.py <base>` pour le test de toutes les URLs. Le contenu se modifie dans `src/data/*.py`
(site, services, villes, situations, articles) — jamais dans les pages HTML générées.
**Suivi** : projet Paperclip « Débarras Alsace — Site web » + une issue par phase/livrable

| Élément | Valeur |
|---|---|
| Paperclip — projet | `Débarras Alsace — Site web` (id `60575f2c-3117-4465-a926-6aa85abd49a9`, statut backlog) |
| Paperclip — issues | 14 issues `DEB — …` (une par phase/livrable), toutes en **backlog** (parked, non assignées) |
| Paperclip — workspace | `debarras-alsace local` (id `4cf7dce6-a01e-47e4-a225-d6c74e89b80e`), `effectiveLocalFolder` = ce dossier |
| UI | http://127.0.0.1:3100 (mode local_trusted, pas de login) |

⚠️ Les issues sont volontairement **non assignées** : le dev se fait en conversation (Ams valide ici).
Assigner une issue à un agent passe son statut en `todo` et réveille un run autonome Paperclip — à ne
faire que pour déléguer réellement un livrable.

## Documents

| Fichier | Contenu |
|---|---|
| `source-client/BRIEF_CODEX_SITE_DEBARRAS.md` | Brief client complet (21 sections) — source de vérité du besoin |
| `source-client/MAQUETTE_DESKTOP.png` | Maquette desktop fournie par le client (770 × 2042) |
| `docs/QUESTIONS_OUVERTES.md` | Points à trancher avec le client / Ams |
| `docs/BENCHMARK.md` | Benchmark FR/US + stratégie SEO local |
| `docs/PRD.md` | Spec fonctionnelle consolidée |
| `docs/FRONT_SPEC.md` | Design system + gabarits de pages |
| `docs/ARCHITECTURE.md` | Stack, arborescence, SEO technique |
| `docs/BACKLOG.md` | Epics + stories + critères d'acceptation |
| `docs/RECETTE.md` | Recette mobile iPhone + Core Web Vitals |

## Ce que dit le brief (résumé)

- **Positionnement** : débarras clé en main — tri, manutention, évacuation, valorisation, nettoyage.
- **Zones** : Strasbourg, Eurométropole, Bas-Rhin, Alsace (Strasbourg, Illkirch, Ostwald,
  Lingolsheim, Schiltigheim, Bischheim, Hœnheim, Geispolsheim, Haguenau, Molsheim, Obernai, Sélestat).
- **Arborescence** : accueil, 13 pages services, 7 pages situations, ~12 pages villes,
  tarifs, réalisations, avis, à propos, FAQ, blog, contact-devis.
- **Conversion** : hero avec devis express + code postal, formulaire multi-étapes (7 étapes) avec
  photos, simulateur de volume, barre sticky mobile (Appeler / WhatsApp / Devis), CTA permanents.
- **SEO** : pages villes réellement uniques (pas de duplication), Schema.org LocalBusiness,
  sitemap, robots, meta uniques, Open Graph, breadcrumbs, Core Web Vitals.
- **Design** : vert profond + anthracite + blanc + beige clair + accent chaud (CTA orange),
  photos réelles (équipe, camion, chantiers, avant/après), pas de banque d'images générique.
- **Éditorial** : simple, rassurant, direct, humain, phrases courtes. Jamais de promesse de
  « débarras gratuit », jamais de note Google inventée.
- **Stack** : à trancher — Next.js/TS/Tailwind (option moderne) ou WordPress (autonomie client).

## Écarts / points de vigilance identifiés dès la lecture du brief

1. **Note Google** : la maquette affiche « 4,0/5 sur Google (150+ avis) » — la section 10 du brief
   interdit d'inventer une note. À remplacer par la note réelle du client (ou masquer en attendant).
2. **Téléphone de la maquette** : 04 13 24 56 78 / 06 12 34 56 78 = numéros fictifs.
   Les vrais numéros (téléphone + WhatsApp) sont nécessaires avant mise en ligne.
3. **Photos** : **20 visuels générés en local** (SDXL photoréaliste, `tools/generer_photos.py`) —
   aucun banque d'images, aucun droit tiers. Ils sont explicitement présentés comme
   « visuels d'illustration » sous les réalisations ; les photos réelles des chantiers doivent
   les remplacer (dépôt dans `source-client/photos-hd/` + `bash tools/photos.sh`).
4. **Volume de contenu** : ~13 services + 7 situations + 12 villes + 12 articles = ~45 pages de
   contenu unique. C'est le vrai coût du projet (rédaction + SEO), pas le code.
5. **Simulateur de volume** : intégré au socle dès la conception, mais sans prix ferme.

## Décisions

| Date | Décision |
|---|---|
| 2026-09-13 | Création du projet + dossier git + projet Paperclip (issues par phase en backlog) |
| 2026-09-26 | **Reprise par l'usine** : V3 une page (maquette Claude Design `docs/design/`), construite dans `v3/` par 8 cartes, bascule à la racine en H8 après recette d'Ams (seul checkpoint). Stack : statique sans build, tests `node --test`. Paperclip n'est plus le suivi : c'est le board `factory` de Hermes |
| 2026-09-14 | **V2 épurée** : une page d'atterrissage + pages légales, publiée dans `/v2/` (la V1 reste à la racine pour comparaison). Décision client : un site de 49 pages est trop lourd pour une entreprise qui se lance |

## V2 épurée (en ligne : https://amsclaw.github.io/debarras-alsace/v2/)

Version courte, mobile d'abord, une seule page : héros + 4 prestations + 3 étapes + explication du prix
+ zone d'intervention + demande de devis. Pas de menu à rallonge, pas de blog, pas de pages villes.

- **Source** : `v2_src/style.css` (design), `v2_src/app.js` (apparition douce + formulaire express)
  et `tools/build_v2.py` (générateur).
- **Construire** : `python3 tools/build_v2.py` → écrit dans `v2/` (12 fichiers, ~390 Ko dont 6 photos).
- **Formulaire sans backend** : les 4 champs composent un message, puis ouvrent WhatsApp
  (`wa.me/…?text=…`) ou l'e-mail prérempli. Rien n'est envoyé depuis le site : le visiteur confirme.
  Sans JavaScript, le bouton reste un lien `wa.me` standard.
- **Bascule prévue** : quand la V2 est validée, `v2/` devient la racine et la V1 est supprimée
  (voir la case « décision » à confirmer).
- Les pages V2 sont en `noindex` tant que la comparaison est en cours.
