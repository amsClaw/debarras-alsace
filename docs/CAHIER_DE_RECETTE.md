# Cahier de recette — Débarras Alsace

Bascule : le nouveau site (V3, une page) remplace l'ancien site en ligne.

## 1. Comment ouvrir le site

**Après fusion de cette carte**, le site est visible directement à cette adresse,
sans rien installer :

https://amsclaw.github.io/debarras-alsace/

Ça marche sur téléphone comme sur ordinateur, dans n'importe quel navigateur
(Safari, Chrome…). Il n'y a pas de compte à créer ni d'identifiant à saisir : c'est
un site public.

**Avant la fusion**, pour regarder le site en avance sur ton ordinateur, il faut un
petit serveur local (le site charge un script en module, ce qui ne fonctionne pas si
on ouvre juste le fichier en double-cliquant) :

1. Installe Node.js si ce n'est pas déjà fait (une seule fois).
2. Ouvre un terminal dans le dossier du projet.
3. Tape la commande : `npx serve .`
4. Ouvre dans ton navigateur l'adresse indiquée par la commande, en général
   `http://localhost:3000`.

## 2. Ce qu'il y a à tester (12 cas)

1. **Ouvrir la page d'accueil**
   Va sur `https://amsclaw.github.io/debarras-alsace/` (ou l'adresse locale du
   serveur).
   Résultat attendu : la page se charge, tu vois en haut « Débarras Alsace »,
   un gros bouton de devis avec un champ pour le code postal, et une photo.
   ☐ vu et conforme

2. **Demander un devis express (accueil)**
   Dans le bloc d'en-tête, saisis un code postal alsacien (ex. `67000`), choisis
   un type de bien, puis clique sur le bouton d'envoi du devis express.
   Résultat attendu : WhatsApp s'ouvre (ou une page de contact WhatsApp) avec un
   message pré-rempli reprenant tes informations. Rien n'est envoyé
   automatiquement : c'est toi qui dois appuyer sur « Envoyer » dans WhatsApp.
   ☐ vu et conforme

3. **Tester une zone hors secteur**
   Saisis un code postal qui n'est ni du Bas-Rhin (67), ni du Haut-Rhin (68), ni
   de Paris (75) — par exemple `13000` (Marseille).
   Résultat attendu : un message indique que la zone n'est pas couverte, sans
   bloquer le reste de la page.
   ☐ vu et conforme

4. **Utiliser l'estimateur de volume (prestation « Maison »)**
   Descends jusqu'à la section des prestations, ouvre l'estimateur de volume pour
   un débarras de type maison (nombre de pièces, niveau d'encombrement).
   Résultat attendu : une estimation de volume (en m³ ou équivalent) s'affiche
   selon tes réponses, sans prix ferme inventé.
   ☐ vu et conforme

5. **Lire la section « Syndrome de Diogène »**
   Cherche, sous les prestations, la carte « Diogène & logement très encombré »,
   puis clique sur son lien « Notre approche, ci-dessous ».
   Résultat attendu : tu arrives sur une section dédiée qui explique
   l'intervention (discrétion, absence de jugement, accompagnement au rythme du
   client).
   ☐ vu et conforme

6. **Parcourir la FAQ (7 questions)**
   Descends jusqu'à la section Questions fréquentes.
   Résultat attendu : 7 questions/réponses sont affichées, dont une sur le
   syndrome de Diogène.
   ☐ vu et conforme

7. **Vérifier la barre du bas sur téléphone**
   Ouvre le site sur un téléphone (ou réduis la largeur de la fenêtre du
   navigateur sur ordinateur).
   Résultat attendu : une barre reste collée en bas de l'écran avec des boutons
   Appeler / WhatsApp / Devis, toujours visible en faisant défiler la page.
   ☐ vu et conforme

8. **Faire un devis complet en 3 étapes (mobile)**
   Toujours en affichage mobile, clique sur « Devis » dans la barre du bas et
   remplis les 3 étapes proposées (type de bien, situation, coordonnées).
   Résultat attendu : les 3 étapes s'enchaînent sans bug, et à la fin un message
   pré-rempli s'ouvre vers WhatsApp ou l'e-mail, comme au cas n°2.
   ☐ vu et conforme

9. **Ouvrir les pages légales**
   En bas de page (pied de page), clique sur « Mentions légales » puis reviens en
   arrière et clique sur « Politique de confidentialité ».
   Résultat attendu : les deux pages s'ouvrent, avec le même habillage que
   l'accueil ; certains champs (raison sociale, adresse, e-mail) apparaissent
   entre crochets `[...]` — c'est normal, voir section 3 ci-dessous.
   ☐ vu et conforme

10. **Chercher un avis client ou un prix affiché**
    Relis l'ensemble de la page d'accueil à la recherche d'une note (ex.
    « 4,5/5 »), d'un nombre d'avis, ou d'un tarif chiffré.
    Résultat attendu : tu n'en trouves aucun — le site n'invente ni avis ni prix
    tant que l'entreprise ne les a pas fournis.
    ☐ vu et conforme

11. **Repérer les emplacements à remplacer**
    Cherche un numéro de téléphone ou une adresse e-mail affichés sur le site
    (en-tête, bouton d'appel, pied de page).
    Résultat attendu : ils apparaissent sous forme d'emplacement entre crochets,
    par exemple `[06 XX XX XX XX]` ou `[contact@domaine.fr]` — ce sont des
    réservations de place, pas de vrais contacts, tant que l'entreprise n'a pas
    donné les siens.
    ☐ vu et conforme

12. **Vérifier qu'une page introuvable est bien gérée**
    Va sur une adresse qui n'existe pas, par exemple
    `https://amsclaw.github.io/debarras-alsace/n-importe-quoi`.
    Résultat attendu : une page « Cette page n'existe pas. » s'affiche, avec un
    bouton pour revenir à l'accueil.
    ☐ vu et conforme

## 3. Ce qui est volontairement absent (ce n'est pas un défaut)

- **Pas de vrai numéro de téléphone ni e-mail** : l'entreprise n'a pas encore
  fourni ses coordonnées réelles. Le site affiche des emplacements `[...]` à la
  place, jamais un numéro inventé.
- **Pas d'avis client ni de note affichée** : sans avis réels fournis par
  l'entreprise, mieux vaut ne rien afficher que d'inventer une note ou un nombre
  d'avis.
- **Pas de prix chiffré** : seul un estimateur de volume indicatif est proposé,
  sans tarif ferme (voir `docs/QUESTIONS_OUVERTES.md` pour la tarification à
  trancher).
- **Pas de pages « villes » ni de blog** : la V3 est volontairement une seule
  page, plus légère et plus simple à maintenir que l'ancien site à 49 pages.
  C'est un choix assumé, pas un oubli.
- **Raison sociale et adresse des mentions légales entre crochets** : en attente
  de l'identité juridique exacte de l'entreprise.

## 4. Comment répondre

Si tous les cas ci-dessus sont conformes, réponds avec la phrase exacte :

`je valide H8 du projet debarras-alsace`

Si un cas pose problème, indique simplement son numéro et ce que tu as constaté,
par exemple : « le cas 2 ne marche pas, WhatsApp ne s'ouvre pas ».

---
Cahier de recette généré pour la carte H8 (bascule V3).
