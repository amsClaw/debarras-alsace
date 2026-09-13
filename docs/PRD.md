# PRD V1 — Site Débarras Alsace (Strasbourg & Alsace)

Version : V1.0 · Date : 2026-09-13 · Base : brief client `source-client/BRIEF_CODEX_SITE_DEBARRAS.md`
+ `docs/BENCHMARK.md` · **Validation : déléguée à l'agent par Ams le 2026-09-13 (« je te laisse faire le
benchmark et le PRD et le valider en toute autonomie »)** — les décisions prises sont tracées au §12.

## 1. Objectif produit

Transformer une visite en **demande de devis qualifiée** (avec photos) en moins d'une minute, sans
obliger le visiteur à téléphoner, tout en construisant une présence SEO locale durable sur Strasbourg,
l'Eurométropole, le Bas-Rhin et l'Alsace.

Promesse affichée : **« Vous nous montrez ce qui doit partir. On s'occupe du reste. »**
Sous-promesse : Tri • Manutention • Évacuation • Valorisation • Nettoyage.

## 2. Cibles

| Persona | Situation | Attente principale | Levier sur le site |
|---|---|---|---|
| Héritier pressé (45-65 ans) | succession / après décès, logement à vider avant vente | être guidé, ne pas juger, délai court | page Succession / Après décès, ton humain, process en 4 étapes |
| Propriétaire qui déménage | déménagement, cave/grenier/garage | débarras rapide, prix clair | simulateur de volume, page Tarifs, formulaire photo |
| Famille d'une personne Diogène | logement très encombré | discrétion, accompagnement | page Diogène, confidentialité, coordination famille/tuteur |
| Professionnel (syndic, agence, hôtel, commerce) | local, bureau, entrepôt, archives | facture, délais, curage | page Professionnels, CTA devis pro |
| Prospect mobile (majorité) | cherche « débarras + ville » sur téléphone | appeler ou envoyer des photos tout de suite | barre sticky Appeler / WhatsApp / Devis, formulaire court |

## 3. Périmètre

**Dans la V1 (publiée sur GitHub Pages)** : accueil, 13 services, 7 situations, 12 villes, tarifs,
réalisations (structure + gabarit, contenus exemples), avis clients (structure, sans note inventée),
à propos, FAQ, blog (liste + 4 articles piliers), contact-devis (formulaire 7 étapes + photos +
simulateur de volume), mentions légales, politique de confidentialité, sitemap, robots, Schema.org.

**Hors V1 (V1.1)** : back-office d'administration du contenu, secondes langues (DE/EN), envoi serveur
des photos (backend), pages villes restantes (communauté d'agglomération élargie), blog complet (12 articles),
Google Business Profile + Search Console + GA4 (nécessitent les accès du client).

## 4. Architecture de l'information (URLs de la V1)

```
/                             accueil
/services/                    13 services
  debarras-maison, debarras-appartement, debarras-cave, debarras-grenier, debarras-garage,
  debarras-succession, debarras-apres-deces, debarras-diogene, debarras-encombrants,
  debarras-professionnel, nettoyage-apres-debarras, curage, demolition-interieure
/situations/                  7 situations
  demenagement, succession, deces, vente-immobiliere, renovation, expulsion, urgence
/villes/                      12 villes
  strasbourg, illkirch-graffenstaden, ostwald, lingolsheim, schiltigheim, bischheim,
  hoenheim, geispolsheim, haguenau, molsheim, obernai, selestat
/tarifs/  /realisations/  /avis-clients/  /a-propos/  /faq/  /blog/  /blog/<article>/
/contact-devis/  /mentions-legales/  /politique-confidentialite/  /404
```

Chaque page est **une page physique** (pas de SPA) : indexabilité maximale, vitesse, simplicité.

## 5. Homepage — 14 sections (ordre imposé par le brief §6)

| # | Section | Contenu | CTA |
|---|---|---|---|
| 1 | Hero | H1 « Débarras à Strasbourg et en Alsace » + promesse + sous-texte + 4 réassurances | Obtenir mon devis gratuit / Appeler maintenant |
| 2 | Formulaire express | type de débarras, code postal, téléphone, photos (max 5) | Recevoir mon estimation |
| 3 | Vérification de zone | code postal → « nous intervenons » / « à confirmer » | Vérifier ma zone |
| 4 | Bandeau réassurance | 6 arguments (devis gratuit, réponse rapide, local, tri, équipe pro, travail propre) | — |
| 5 | Services | 8 cartes (maison, appartement, cave/grenier/garage, succession, après décès, Diogène, encombrants, professionnels + nettoyage) | En savoir plus |
| 6 | Situations | 7 blocs de situation | Voir la situation |
| 7 | Fonctionnement | 4 étapes | Demander mon devis |
| 8 | Valorisation | réemploi / don / recyclage / valorisation + phrase de transparence | — |
| 9 | Réalisations | 6 gabarits de chantier (ville, type, volume, durée) — **photos à fournir** | Voir toutes nos réalisations |
| 10 | Pourquoi nous choisir | 6 arguments (rien à porter, rien à transporter, rien à trier, devis clair, destination transparente, logement propre) | — |
| 11 | Avis clients | emplacement prévu, **aucune note inventée** : bloc remplacé par un appel à laisser un avis tant que le client n'a pas fourni sa fiche Google | — |
| 12 | Zones d'intervention | 12 communes cliquables + note Eurométropole/Bas-Rhin | Voir ma ville |
| 13 | FAQ | 10 questions (accordéon, Schema.org FAQPage) | — |
| 14 | CTA final | bloc « Besoin de vider un logement ? » | Devis / Appeler / WhatsApp |

## 6. Parcours de conversion

**Devis express (hero)** : 4 champs → crée une demande courte.
**Formulaire complet 7 étapes** (brief §8) : ① type de besoin ② localisation (adresse, CP, ville)
③ volume (petite quantité, 5-10, 10-20, 20-40, +40 m³, « je ne sais pas ») ④ accès (RDC, étage,
ascenseur, escaliers, accès difficile, distance camion) ⑤ délai (urgent, cette semaine, ce mois, flexible)
⑥ photos (plusieurs, depuis smartphone) ⑦ coordonnées (prénom/nom, téléphone, e-mail, message) →
**récapitulatif** puis envoi.

**Règles** : progression visible, retour arrière, aucun champ obligatoire en étape 1, téléphone OU e-mail
suffit, message d'erreur explicite en français, récapitulatif copiable.

**Simulateur de volume** : sélection visuelle 1/8, 1/4, 1/2, 3/4, camion complet, avec repère
« ≈ X m³ » et mention « estimation indicative — le devis définitif est établi après échange ».

**Mobile** : barre fixe en bas **Appeler · WhatsApp · Devis**, téléphone cliquable partout.

## 7. Règles éditoriales (non négociables)

1. Jamais de « débarras gratuit » garantie, jamais de « rachat garanti ».
2. Jamais de note Google, nombre d'avis, statistique ou témoignage inventé.
3. Phrases courtes, bénéfices avant technique, tutoiement interdit (vouvoiement client), pas de jargon.
4. Ton respectueux sur succession, décès, Diogène (aucune photo choc, aucune stigmatisation).
5. Accents et typographie française corrects (œ, apostrophes typographiques, majuscules accentuées).
6. Aucune photo de banque d'images présentée comme une photo d'équipe : les emplacements photo sont
   identifiés comme tels tant que le client n'a pas fourni ses images.

## 8. SEO technique

Title unique par page (≤ 60 car.), meta description unique (≤ 155 car.), H1 unique, hiérarchie Hn propre,
URLs courtes en français, fil d'Ariane, maillage interne systématique (ville ↔ service ↔ situation),
`sitemap.xml`, `robots.txt`, canoniques, Open Graph, Schema.org `LocalBusiness` (+ `Service`, `FAQPage`,
`BreadcrumbList`), images avec `alt` descriptif, lazy loading, aucune dépendance externe bloquante
(aucune police/JS tiers — le site doit rester rapide et sans cookie tiers).

## 9. Design

Direction : moderne, sobre, chaleureux, local, très lisible. Mobile-first.
Palette : vert profond (confiance/recyclage) `#14532d` / `#1c6b3f`, anthracite `#1f2937`,
beige très clair `#f7f5ef`, blanc, accent chaud orange pour les CTA `#e8622a`, vert clair d'appui `#e8f2ea`.
Typographie système (aucune police téléchargée), contrastes AA, focus clavier visible,
boutons ≥ 48 px sur mobile. Détail : `docs/FRONT_SPEC.md`.

## 10. Données à fournir par le client (bloquant pour la mise en production réelle)

1. Raison sociale + SIRET + adresse + logo. 2. Téléphone + numéro WhatsApp. 3. Fiche Google Business
Profile réelle (note/avis/lien). 4. Lot photo (équipe, camion, chantiers avant/après, tri).
5. Zone d'intervention exacte. 6. Adresse de réception des demandes de devis. 7. Fourchettes tarifaires
validées. 8. Nom de domaine. 9. Mentions légales / hébergeur.
En attendant, la V1 tourne avec des **valeurs de démonstration explicitement listées**
(`docs/QUESTIONS_OUVERTES.md`) et remplaçables en un seul endroit du code.

## 11. Critères d'acceptation (recette)

- [ ] Toutes les URLs du §4 répondent 200 ; aucune page en erreur ; 404 personnalisée.
- [ ] 0 erreur JavaScript en console sur l'accueil, une page service, une page ville, le formulaire.
- [ ] Homepage conforme : les 14 sections présentes dans l'ordre.
- [ ] Formulaire : les 7 étapes avancent, reculent, valident, et produisent un récapitulatif complet.
- [ ] Simulateur de volume : sélection visuelle fonctionnelle + estimation textuelle cohérente.
- [ ] Barre mobile Appeler / WhatsApp / Devis visible et cliquable sur une page mobile.
- [ ] Chaque page a un title, une meta description et un H1 uniques (vérifié par script).
- [ ] Aucune promesse interdite (§7) : contrôle par recherche automatique sur le HTML publié.
- [ ] Site publié accessible en HTTPS, navigation réelle vérifiée, liens internes sans 404.
- [ ] Rendu vérifié à l'œil sur captures desktop (≥ 1280 px) et mobile (viewport mobile réel).

## 12. Décisions prises en autonomie (2026-09-13, délégation Ams)

| # | Décision | Justification |
|---|---|---|
| 1 | **Stack = site statique généré** (HTML/CSS/JS, générateur Python), publié sur GitHub Pages | exigence « v1 sur mon GitHub » ; Pages ne sert que du statique sans serveur ; zéro coût d'hébergement ; le plus rapide à vérifier et à héberger. Le CMS pourra venir en V1.1 sans tout casser (contenu externalisé en données). |
| 2 | **Contenu externalisé** dans des fichiers de données (`src/data/*.py`) + gabarits | permet de brancher plus tard un panneau d'admin ou un CMS sans réécrire les pages, et d'éviter la duplication entre les 32 pages services/villes/situations. |
| 3 | **Pas de prix affiché en dur** : fourchettes retirées par défaut, page Tarifs explicative | aucun tarif client validé à ce jour ; inventer des prix serait une faute commerciale. |
| 4 | **Aucun avis/note chiffrée** : emplacement « avis à connecter » | brief §10 interdit les avis inventés ; le bloc est prêt à recevoir la fiche Google réelle. |
| 5 | **Photos = visuels d'attente sobres** (motifs CSS/SVG, pas de banque d'images) | brief §12 : éviter les banques d'images génériques ; ne pas faire croire à des photos réelles. |
| 6 | **Formulaire : envoi mailto + récapitulatif copiable en V1**, backend documenté en V1.1 | un site statique ne peut pas envoyer d'e-mail ni stocker des photos : mieux vaut un parcours qui fonctionne vraiment (récapitulatif + e-mail prérempli) que l'apparence d'un envoi serveur. Branché sur l'adresse du client dès qu'elle est connue (FormSubmit ou backend Express réutilisé du projet CAPSAAA). |
| 7 | **FR uniquement en V1**, sélecteur DE/EN prévu en V1.1 | l'allemand est un levier réel (cf. benchmark) mais double le contenu : à faire une fois que la V1 est validée par le client. |
