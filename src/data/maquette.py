# -*- coding: utf-8 -*-
"""Contenu exact de la maquette client (MAQUETTE_DESKTOP.png) pour la page d'accueil.

Chaque texte de ce fichier est repris MOT POUR MOT de la maquette fournie par le client.
Les visuels sont les photos découpées dans la maquette elle-même (source-client/photos/,
copiées dans src/assets/photos/ puis publiées dans assets/photos/).

⚠️ Les notes et témoignages (4,9/5, « 150+ avis Google », Sophie M., Thomas R., Caroline D.)
proviennent de la maquette : ce sont des données de démonstration, à remplacer par les vrais
avis du client avant toute mise en production (voir docs/QUESTIONS_OUVERTES.md).
"""

HERO = {
    "badge": "Débarras Strasbourg & Alsace",
    "titre_blanc": "Vous nous montrez<br>ce qui doit partir.",
    "titre_vert": "On s'occupe du reste.",
    "texte": ("Maison, appartement, succession, cave, garage, locaux professionnels... "
              "Nous vidons, trions, évacuons et nettoyons vos biens rapidement et proprement."),
    "arguments": [("feuille", "Devis gratuit", "et sans engagement"),
                  ("horloge", "Intervention", "rapide"),
                  ("recycle", "Tri, valorisation", "et recyclage")],
    "cta_principal": "Obtenir mon estimation",
    "cta_telephone": "06 12 34 56 78",
    "photo": "hero",
}

CARTE = {
    "badge": "Estimation rapide",
    "titre": "Quel type de débarras ?",
    "sous_titre": "Répondez en quelques clics et recevez une estimation gratuitement.",
    "champ_type": "Type de bien",
    "type_defaut": "Sélectionnez",
    "champ_cp": "Code postal",
    "cp_placeholder": "Ex : 67000",
    "champ_tel": "Téléphone",
    "tel_placeholder": "Votre numéro",
    "champ_photos": "Ajoutez quelques photos (max 5)",
    "zone_depot": "Cliquez pour ajouter des photos ou glissez-les ici",
    "bouton": "Recevoir mon estimation",
    "mention": "100% gratuit • Sans engagement",
}

ZONE = {
    "titre": "Où se trouve votre débarras ?",
    "aide": "Vérifiez si nous intervenons dans votre secteur",
    "placeholder": "Code postal (ex : 67000)",
    "bouton": "Vérifier ma zone",
    "reassurance": [
        ("carte", "Entreprise locale", "à Strasbourg"),
        ("etoile", "4,9/5", "sur Google (150+ avis)"),
        ("feuille", "Éco-responsable", "Tri, don, recyclage"),
        ("horloge", "Intervention", "sous 24h"),
    ],
}

SERVICES_MAQUETTE = {
    "surtitre": "Nos services",
    "titre": "Un service de débarras pour chaque besoin",
    "texte": ("Du particulier au professionnel, nous intervenons dans toute l'Alsace pour vider, "
              "trier et nettoyer vos espaces."),
    "cta": "Voir tous nos services",
    "cartes": [
        ("service-maison", "feuille", "Débarras maison", "Maison complète ou quelques pièces", "debarras-maison"),
        ("service-appartement", "feuille", "Débarras appartement", "Studio, logement, etc.", "debarras-appartement"),
        ("service-cave", "recycle", "Cave, grenier & garage", "Objets, cartons, encombrants", "debarras-cave"),
        ("service-succession", "main", "Succession", "Tri et valorisation des biens", "debarras-succession"),
        ("service-deces", "coeur", "Après décès", "Intervention discrète et respectueuse", "debarras-apres-deces"),
        ("service-diogene", "maison", "Diogène", "Logement très encombré", "debarras-diogene"),
        ("service-pro", "bureau", "Professionnels", "Bureaux, commerces, locaux", "debarras-professionnel"),
        ("service-nettoyage", "propre", "Nettoyage", "Après débarras", "nettoyage-apres-debarras"),
    ],
}

SITUATIONS_MAQUETTE = {
    "surtitre": "Dans quelles situations ?",
    "titre": "Nous vous accompagnons à chaque étape de votre projet",
    "texte": ("Déménagement, succession, vente immobilière, rénovation... Quelle que soit la situation, "
              "nous avons la solution."),
    "cta": "Découvrir toutes les situations",
    "photo": "situations",
    "cartes": [
        ("camion", "Déménagement", "Libérez votre ancien logement", "demenagement"),
        ("main", "Succession", "Accompagnement de confiance", "succession"),
        ("coeur", "Décès", "Avec discrétion et respect", "deces"),
        ("doc", "Vente immobilière", "Préparez votre bien pour la vente", "vente-immobiliere"),
        ("marteau", "Rénovation", "Dépose, curage, évacuation", "renovation"),
        ("horloge", "Urgence", "Intervention rapide", "urgence"),
        ("maison", "Logement encombré", "Nous intervenons sans jugement", "services/debarras-diogene"),
    ],
}

PROCESS_MAQUETTE = {
    "surtitre": "Comment ça marche ?",
    "titre_avant": "Votre débarras en ",
    "titre_chiffre": "4",
    "titre_apres": " étapes",
    "sous_titre": "Simple, rapide et sans stress.",
    "cta": "Je demande mon devis",
    "photo": "process",
    "etapes": [
        ("telephone", "Vous nous contactez", "Par téléphone ou formulaire en ligne."),
        ("appareil", "Nous évaluons le débarras", "Photos ou visite sur place selon le projet."),
        ("doc", "Vous recevez votre devis", "Un prix clair et détaillé avant intervention."),
        ("camion", "Nous vidons et nettoyons", "Tri, évacuation, valorisation et nettoyage."),
    ],
}

VALORISATION_MAQUETTE = {
    "surtitre": "Valorisation",
    "titre": "Et si certains objets avaient encore de la valeur ?",
    "texte": ("Avant d'évacuer vos meubles et objets, nous identifions ceux qui peuvent être "
              "réemployés, donnés ou valorisés."),
    "photo": "valorisation",
    "items": [("recycle", "Recyclage"), ("coeur", "Don"), ("euro", "Valorisation"), ("camion", "Évacuation")],
    "encart": ("Certains biens peuvent être estimés et rachetés par notre partenaire "
               "antiquaire / brocanteur."),
}

REALISATIONS_MAQUETTE = {
    "titre": "Nos réalisations",
    "sous_titre": "Des débarras concrets à Strasbourg et en Alsace.",
    "cta": "Voir toutes nos réalisations",
    "cartes": [
        ("Appartement – Strasbourg", "real-appart-avant", "real-appart-apres"),
        ("Maison – Illkirch", "real-maison-avant", "real-maison-apres"),
        ("Cave – Ostwald", "real-cave-avant", "real-cave-apres"),
    ],
}

AVIS_MAQUETTE = {
    "titre": "Ils nous ont fait confiance",
    "note": "4,9/5",
    "nb_avis": "(150+ avis Google)",
    "cta": "Voir tous nos avis Google",
    "temoignages": [
        ("Équipe très professionnelle, discrète et efficace. Le débarras de notre maison s'est fait "
         "en 2 jours. Nous recommandons sans hésiter !", "Sophie M.", "Strasbourg"),
        ("Service impeccable, du devis au nettoyage. Tout a été géré avec sérieux et bienveillance. "
         "Merci encore !", "Thomas R.", "Illkirch"),
        ("Une équipe humaine et respectueuse. Ils ont vidé l'appartement de ma mère après son décès. "
         "Un grand merci.", "Caroline D.", "Obernai"),
    ],
}

ZONES_MAQUETTE = {
    "badge": "Notre zone d'intervention",
    "titre": "Débarras à Strasbourg et dans toute l'Eurométropole",
    "sous_titre": "Nous intervenons dans toutes les communes du Bas-Rhin et en Alsace.",
    "photo": "strasbourg",
    "carte": "carte-alsace",
    "colonnes": [
        ("Strasbourg", ["Centre-ville, Neudorf, Krutenau, Esplanade", "Robertsau, Cronenbourg...",
                        "Hoenheim, Bischheim, etc."]),
        ("Eurométropole", ["Illkirch, Ostwald, Lingolsheim", "Schiltigheim...", "Sélestat, Saverne, etc."]),
        ("Autres villes", ["Haguenau, Molsheim, Obernai,", "Sélestat, Saverne, etc.", ""]),
    ],
    "encart": "Et bien d'autres villes en Alsace !",
    "cta": "Voir toutes les communes",
}

CTA_FINAL_MAQUETTE = {
    "titre": "Un débarras, sans le stress, de A à Z.",
    "texte": "Nous vidons. Nous trions. Nous valorisons. Nous évacuons. Nous nettoyons.",
    "bouton": "Demander mon devis gratuit",
    "telephone": "06 12 34 56 78",
}

PIED_MAQUETTE = {
    "accroche": "Une équipe locale, engagée pour un cadre de vie plus propre.",
    "reseaux": ["Facebook", "Instagram", "YouTube"],
    "contact": {"telephone": "06 12 34 56 78", "email": "contact@debarras-alsace.fr",
                "lieu": "Strasbourg / Alsace"},
    "copyright": "© 2025 Débarras Alsace. Tous droits réservés.",
    "liens_legaux": ["Mentions légales", "Politique de confidentialité", "Cookies", "CGV"],
    "badges": ["100% sécurisé", "Google 4.9/5"],
}
