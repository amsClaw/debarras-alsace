# FRONT_SPEC — Débarras Alsace

## 1. Palette (variables CSS)

| Rôle | Variable | Valeur | Usage |
|---|---|---|---|
| Vert profond | `--vert` | `#14532d` | header, titres, aplats de confiance |
| Vert moyen | `--vert-2` | `#1c6b3f` | survols, dégradés, icônes |
| Vert clair | `--vert-clair` | `#e8f2ea` | fonds de sections alternées, badges |
| Anthracite | `--anthracite` | `#1f2937` | texte courant, footer |
| Gris doux | `--gris` | `#5b6472` | textes secondaires |
| Beige | `--beige` | `#f7f5ef` | fond de page |
| Blanc | `--blanc` | `#ffffff` | cartes |
| Accent CTA | `--accent` | `#e8622a` | boutons d'action principaux |
| Accent foncé | `--accent-fonce` | `#c94f1c` | survol/pressed |
| Bordure | `--bord` | `#e3ded2` | séparateurs, cartes |
| Focus | `--focus` | `#0b63ce` | contour de focus clavier (AA) |

Contrastes : texte anthracite sur beige/blanc ≥ 12:1 ; blanc sur vert/anthracite ≥ 7:1 ; blanc sur orange
≈ 4,6:1 (AA pour texte ≥ 18,66 px gras ou 24 px) → **les boutons orange utilisent un texte ≥ 17 px semi-gras**.

## 2. Typographie

- Pile système : `-apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` (aucun téléchargement).
- H1 accueil 2,1 rem mobile / 3,1 rem desktop ; H1 pages internes 1,7 / 2,3 rem ; H2 1,5 / 1,9 rem ; H3 1,15 / 1,25 rem.
- Corps 1,02 rem, interligne 1,65. Texte secondaire 0,92 rem. Mention légale 0,8 rem.
- Titres : `letter-spacing: -0,01em`, `font-weight: 750`. Aucun texte en majuscules longues (sauf surtitres).

## 3. Grille et espacements

- Largeur max de contenu 1160 px, marges latérales 18 px (mobile) / 28 px (≥ 720 px).
- Échelle d'espacement : 4, 8, 12, 16, 24, 32, 48, 64, 96 px.
- Sections : 48 px de padding vertical en mobile, 80 px en desktop, alternance beige / blanc / vert clair.
- Grilles : services 1 → 2 → 4 colonnes (480 / 900 px) ; villes 2 → 3 → 4 ; blog 1 → 2 → 3.

## 4. Composants (obligatoires)

`Header` (logo + menu 8 entrées + CTA devis + téléphone) · `Nav mobile` (panneau plein écran, 1 geste) ·
`MobileStickyBar` (Appeler / WhatsApp / Devis, hauteur 56 px, toujours visible < 900 px) ·
`Hero` (+ variante interne) · `TrustBadges` · `QuoteForm` (express et multi-étapes) ·
`VolumeEstimator` · `ServiceCard` · `SituationCard` · `ProcessSteps` · `ValueRecoverySection` ·
`BeforeAfterGallery` · `Testimonials` (état « à connecter » assumé) · `LocalAreas` · `FAQAccordion` ·
`CTASection` · `Footer` (4 colonnes) · `Breadcrumb` · `BlogCard` · `CityPageTemplate` ·
`ServicePageTemplate` · `PageHero` · `Notice` (bandeau d'information honnête).

## 5. États et interactions

- **Boutons** : normal / survol (foncé -8 %) / actif (translate 1 px) / focus (contour 3 px bleu) /
  désactivé (opacité 0,55, curseur interdit). Cible tactile ≥ 48 px.
- **Cartes** : survol = élévation d'ombre légère + bordure verte ; jamais de déplacement de texte.
- **Accordéons FAQ** : `<details>/<summary>` natifs (accessibles et sans JS).
- **Menu mobile** : ouverture par bouton (aria-expanded), fermeture par Échap et par clic sur un lien ;
  verrouillage du défilement du fond.
- **Formulaires** : label toujours visible, erreur en rouge + texte sous le champ (jamais la couleur seule),
  état « en cours » sur le bouton d'envoi, succès = encadré vert avec récapitulatif copiable.
- **Récapitulatif** : liste des réponses + bouton « Copier » + lien `mailto:` prérempli.

## 6. Accessibilité

- Contraste AA minimum partout, focus visible, `aria-label` sur les boutons icônes.
- Un seul `<h1>` par page, hiérarchie Hn sans saut de niveau.
- `lang="fr"`, `alt` descriptif sur chaque image, formulaires avec `<label for>`.
- Aucun contenu porteur d'information uniquement visuel (l'estimation de volume est aussi écrite en m³).
- Pas de mouvement automatique (aucun carrousel automatique) — respect de `prefers-reduced-motion`.

## 7. Ce qu'on ne fait pas

Pas de banque d'images présentée comme des photos réelles · pas de note Google inventée ·
pas de pop-up d'entrée · pas de chatbot factice · pas de compte à rebours · pas de témoignage fictif.

## 8. Illustrations (visuels de démonstration)

En attendant le lot photo du client, le site utilise **24 illustrations vectorielles générées** par le projet
lui-même (`src/illustrations.py`, aucun fichier externe, aucune banque d'images, aucune dépendance) :

| Famille | Contenu | Où |
|---|---|---|
| Scènes avant/après | 6 locaux (appartement, maison, cave, grenier, garage, local pro) × 2 états | réalisations (accueil + page dédiée) |
| Décors dédiés | mur de cave + ampoule, poutres de grenier + lucarne, porte de garage sectionnelle, fenêtre de séjour | idem |
| Scènes métier | camion chargé, équipe en manutention, tri (don / recyclage / valorisation), nettoyage, succession, chantier | pages services, situations, blog, à propos, valorisation |
| Niveaux de camion | 5 remplissages (1/8 → complet) | simulateur de volume (Tarifs + formulaire) |

Règles respectées : aucune illustration ne prétend être une photo de chantier (légende explicite
« Illustration de démonstration — les photos réelles du chantier viendront ici »), et le décor change selon
le type de local (une cave a des murs de briques et une ampoule, un garage a une porte sectionnelle —
pas une fenêtre de séjour).

**Remplacer les illustrations par les vraies photos** (V1.1, sans toucher au code des pages) :
remplacer les fichiers `assets/illus/<nom>.svg` par des `.webp` de même nom, ou ajouter un champ `photo`
dans `src/data/*.py` et brancher `illus()`/`avant_apres()` sur ces fichiers. La légende « illustration de
démonstration » est alors retirée des gabarits.

