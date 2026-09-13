# Débarras Alsace — Site web (Strasbourg & Alsace)

**Projet** : site vitrine + générateur de leads, très orienté conversion et SEO local,
pour une société de débarras basée à Strasbourg intervenant dans toute l'Alsace.

**Promesse** : « Vous nous montrez ce qui doit partir. On s'occupe du reste. »

**Statut** : 🟡 Phase 0 — cadrage (brief client reçu, maquette desktop reçue)
**Dossier local** : `/Users/amsfox/projets/debarras-alsace` (repo git)
**Process** : Process AAS V0.3 — mode **complet** (projet commercial, SEO, lead-gen, multi-pages)
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
| `docs/BENCHMARK.md` | (à venir) benchmark FR/US + stratégie SEO local |
| `docs/PRD.md` | (à venir) spec fonctionnelle consolidée |
| `docs/FRONT_SPEC.md` | (à venir) design system + gabarits de pages |
| `docs/ARCHITECTURE.md` | (à venir) stack, arborescence, SEO technique |
| `docs/BACKLOG.md` | (à venir) epics + stories + critères d'acceptation |
| `docs/CAHIER_RECETTE.md` | (à venir) recette mobile iPhone + Core Web Vitals |

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
3. **Photos** : tout le site repose sur des photos réelles (avant/après, équipe, camion) —
   le client doit fournir un lot photo, sinon V1 en placeholder assumé.
4. **Volume de contenu** : ~13 services + 7 situations + 12 villes + 12 articles = ~45 pages de
   contenu unique. C'est le vrai coût du projet (rédaction + SEO), pas le code.
5. **Simulateur de volume** : intégré au socle dès la conception, mais sans prix ferme.

## Décisions

| Date | Décision |
|---|---|
| 2026-09-13 | Création du projet + dossier git + projet Paperclip (issues par phase en backlog) |
