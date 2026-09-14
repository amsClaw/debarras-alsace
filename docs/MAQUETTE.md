# Correspondance maquette → site

Objectif : pouvoir vérifier poste par poste que le site reprend la maquette `source-client/MAQUETTE_DESKTOP.png`.
Tous les textes viennent du fichier `src/data/maquette.py` (repris mot pour mot de la maquette) et toutes les
photos sont découpées dans la maquette elle-même (`source-client/photos/` → `src/assets/photos/` → `assets/photos/`).

## En-tête
| Maquette | État |
|---|---|
| Logo maison verte + feuille, « Débarras Alsace » / « Strasbourg & environs » | ✅ SVG recréé (maison + feuille bicolore) |
| Menu : Accueil, Nos services ▾, Situations ▾, Zones d'intervention ▾, Réalisations, Avis clients, A propos, Blog, FAQ, Contact | ✅ 10 entrées, 3 avec sous-menu |
| Pastille verte + icône téléphone « 06 12 34 56 78 » | ✅ pastille verte, visible ≥ 1180 px |
| Bouton orange « Demander un devis » | ✅ |

## Accueil — de haut en bas
| Bloc maquette | État | Détail |
|---|---|---|
| Hero photo (déménageurs + camion) | ✅ | photo découpée dans la maquette, en fond de hero, dégradé vert sur la gauche |
| Badge « Débarras Strasbourg & Alsace » | ✅ | |
| H1 « Vous nous montrez ce qui doit partir. » (blanc) + « On s'occupe du reste. » (vert) | ✅ | deux couleurs comme sur la maquette |
| Texte « Maison, appartement, succession, cave, garage, locaux professionnels... » | ✅ | mot pour mot |
| 3 arguments : Devis gratuit / Intervention rapide / Tri, valorisation et recyclage | ✅ | icônes feuille, horloge, recyclage |
| Boutons « Obtenir mon estimation → » + « 06 12 34 56 78 » | ✅ | |
| Carte « Estimation rapide » : badge, « Quel type de débarras ? », « Répondez en quelques clics… », Type de bien / Code postal / Téléphone, zone pointillée photos, « Recevoir mon estimation → », « 100% gratuit • Sans engagement » | ✅ | le formulaire envoie réellement (récapitulatif + e-mail) |
| Bande « Où se trouve votre débarras ? » + champ « Code postal (ex : 67000) » + « Vérifier ma zone → » | ✅ | la vérification fonctionne (codes postaux réels) |
| 4 réassurances : Entreprise locale / 4,9 sur Google / Éco-responsable / Intervention sous 24h | ✅ | ⚠️ la note et le nombre d'avis viennent de la maquette (démo) |
| « NOS SERVICES » + « Un service de débarras pour chaque besoin » + texte + bouton | ✅ | |
| 8 cartes services avec photos (maison, appartement, cave/grenier/garage, succession, après décès, Diogène, professionnels, nettoyage) | ✅ | photos découpées dans la maquette |
| « DANS QUELLES SITUATIONS ? » + titre + texte + bouton + 7 cartes + photo | ✅ | |
| « COMMENT ÇA MARCHE ? » + « Votre débarras en 4 étapes » + 4 cartes numérotées 01-04 | ✅ | le 4 est mis en couleur comme sur la maquette |
| « VALORISATION » + photo pousse + 4 items (Recyclage, Don, Valorisation, Évacuation) + encart partenaire antiquaire | ✅ | |
| « Nos réalisations » + 3 paires Avant/Après (Appartement – Strasbourg, Maison – Illkirch, Cave – Ostwald) | ✅ | thumbnails découpés dans la maquette |
| « Ils nous ont fait confiance » + note + 3 témoignages + bouton avis Google | ✅ | ⚠️ témoignages issus de la maquette (démo) |
| « NOTRE ZONE D'INTERVENTION » + panorama Strasbourg + carte Alsace + 3 colonnes de communes + encart | ✅ | |
| CTA final « Un débarras, sans le stress, de A à Z. » + bouton + téléphone | ✅ | |
| Pied de page 5 colonnes + réseaux sociaux + contact + liens légaux + badges | ✅ | |

## Limites à connaître
1. **Résolution des photos** : la maquette est une image de 770 × 2 042 px ; ses photos intégrées mesurent
   de 59 × 68 px (avant/après) à 272 × 320 px (héro). Elles sont agrandies (Lanczos ×2 à ×4) : utilisables
   pour valider la direction, **pas** pour la mise en ligne. Les originaux doivent être fournis.
2. **Données de démonstration** : la note « 4,9/5 », « 150+ avis Google » et les trois témoignages
   (Sophie M., Thomas R., Caroline D.) sont repris de la maquette. Ils doivent être remplacés par les avis
   réels avant toute publication côté client (voir docs/QUESTIONS_OUVERTES.md).
3. **Coordonnées** : téléphone, e-mail et adresse sont ceux de la maquette (démonstration).
