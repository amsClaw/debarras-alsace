# ARCHITECTURE — Débarras Alsace V1

## 1. Choix technique

**Site statique généré**, publié sur **GitHub Pages** (aucun serveur, aucun coût d'hébergement).

```
src/
  data/           contenu structuré (Python) : services, villes, situations, articles, FAQ, config du site
  templates/      gabarits HTML (fonctions Python pures, aucune dépendance externe)
  assets/         style.css, app.js, images/ (SVG d'attente), favicon
tools/build.py    génère le site dans la racine du dépôt (à côté de docs/)
```

- Générateur : **Python 3 stdlib uniquement** (aucune dépendance à installer, rejouable sur n'importe quelle machine).
- Sortie : `index.html`, `services/<slug>/index.html`, `villes/<slug>/index.html`,
  `situations/<slug>/index.html`, `blog/<slug>/index.html`, pages simples, `assets/`,
  `sitemap.xml`, `robots.txt`, `404.html`.
- `build.py` est **idempotent** : il efface et régénère ses sorties, il ne touche jamais `docs/`, `src/`, `README.md`.

## 2. Modèle de données (pourquoi c'est important)

Chaque ville est un enregistrement : `slug, nom, code_postal, h1, intro (rédigée), quartiers[],
communes_voisines[], chantiers[], faq[], note_locale`. Idem pour les services, situations et articles.
→ **Une seule source de vérité** pour le contenu ; les 32 pages sont générées à partir de données
réellement différentes (pas de duplication de contenu : chaque `intro` et chaque `note_locale` est écrite
pour la commune).

C'est aussi ce qui rend la V1.1 simple : brancher un back-office (pattern « Espace CAPSAAA ») ou un CMS
revient à écrire ces mêmes fichiers de données, sans toucher aux gabarits.

## 3. Déploiement GitHub Pages

1. `git init` (fait), commit, `gh repo create amsClaw/debarras-alsace --public --source . --push`
2. Pages : `gh api -X POST repos/amsClaw/debarras-alsace/pages -f build_type=legacy
   -f "source[branch]=main" -f "source[path]=/"`
3. URL publique : **https://amsclaw.github.io/debarras-alsace/**
4. Premier build Pages : 30-120 s → vérification réelle des URLs (pas seulement le 200 de la racine).

## 4. Formulaire et photos (V1 statique : ce qui fonctionne vraiment)

| Étape | V1 (statique) | V1.1 (backend) |
|---|---|---|
| Saisie multi-étapes | ✅ JavaScript local, progression + validation | inchangé |
| Photos | ✅ sélection + aperçu local (min 1, max 5, compression canvas) | upload réel |
| Envoi | ✅ **récapitulatif copiable + `mailto:` prérempli** (objet + corps structuré) | POST API → e-mail + stockage |
| Accusé | message explicite « voici votre demande, envoyez-la / appelez-nous » | e-mail + confirmation |

Choix assumé : un site statique ne peut pas envoyer d'e-mail ni recevoir de fichiers. On livre un parcours
**qui fonctionne réellement** (rien de factice) plutôt qu'un faux bouton « Envoyé ». Le branchement
serveur est documenté (§5) et déjà éprouvé sur un autre projet (backend Express + stockage + envoi).

## 5. V1.1 — branchement serveur (documenté, non fait)

- Réutiliser le pattern du projet « Espace CAPSAAA » : petit backend Express sur le VPS OVH existant
  (POST `/api/devis`), stockage des photos dans un dossier daté, e-mail au client, anti-spam (honeypot +
  limitation de débit), RGPD (durée de conservation, suppression sur demande).
- Alternative sans serveur : FormSubmit **avec vérification d'activation obligatoire** (piège connu :
  aucun message n'arrive tant que le lien d'activation n'a pas été cliqué).

## 6. SEO technique généré

`sitemap.xml` (toutes les URLs, `lastmod` du build) · `robots.txt` (+ référence sitemap) ·
`canonical` absolu par page (base configurable dans `src/data/site.py`) · Open Graph + Twitter Card ·
JSON-LD `LocalBusiness` (accueil/contact), `Service` (pages services), `FAQPage` (FAQ), `BreadcrumbList`
(pages internes) · `404.html` personnalisée.

## 7. Vérification (recette)

1. `python3 -m http.server` sur un port libre → **smoke test de toutes les URLs** (script) : statut 200 + title unique.
2. Contrôles automatiques : promesses interdites absentes (« débarras gratuit », « rachat garanti »),
   un seul H1 par page, meta description présente et unique, liens internes sans 404.
3. Captures **Chrome headless** desktop 1280×900 et mobile 430×932, lues à l'œil (vision) — attention au
   piège du viewport CSS minimum 500 px en headless sur les petites largeurs.
4. Après publication : re-vérifier le site **en ligne** (URLs, form, sticky bar), pas seulement en local.

## 8. Hors périmètre technique assumé

Pas de base de données, pas d'authentification, pas de paiement, pas de CMS en V1, pas d'analytics tiers
(GA4 à brancher dès que le client a un compte — emplacement + événements déjà prévus dans `app.js`).
