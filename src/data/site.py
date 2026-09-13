# -*- coding: utf-8 -*-
"""Configuration du site — valeurs de démonstration à remplacer par les données réelles du client.

Tout ce qui est marqué `A_COMPLETER` doit être fourni par le client avant la mise en production
(voir docs/QUESTIONS_OUVERTES.md). Rien ici n'invente une preuve : pas de note, pas d'avis, pas de chiffre.
"""

SITE = {
    "nom": "Débarras Alsace",
    "baseline": "Strasbourg & Alsace",
    "promesse": "Vous nous montrez ce qui doit partir. On s'occupe du reste.",
    "sous_promesse": "Tri • Manutention • Évacuation • Valorisation • Nettoyage",
    "h1_accueil": "Débarras à Strasbourg et en Alsace",
    "url_base": "https://amsclaw.github.io/debarras-alsace",
    "langue": "fr",
    # --- Identité : à compléter par le client ---
    "raison_sociale": "A_COMPLETER — raison sociale du client",
    "siret": "A_COMPLETER",
    "adresse": "Strasbourg (67000), Bas-Rhin",
    "telephone": "04 13 24 56 78",          # numéro de la maquette : à remplacer
    "telephone_lien": "+33413245678",
    "mobile": "06 12 34 56 78",             # numéro de la maquette : à remplacer
    "mobile_lien": "+33612345678",
    "whatsapp_lien": "https://wa.me/33612345678",
    "email": "contact@a-completer.fr",
    "horaires": "Lundi – Samedi, 8h – 19h",
    "zone_texte": "Strasbourg, l'Eurométropole, le Bas-Rhin et l'ensemble de l'Alsace.",
}

# Codes postaux utilisés par la vérification de zone :
# les 12 villes du plan SEO + les principales communes de l'Eurométropole et du Bas-Rhin.
CODES_POSTAUX = {
    "67000": "Strasbourg", "67100": "Strasbourg", "67200": "Strasbourg",
    "67400": "Illkirch-Graffenstaden", "67540": "Ostwald", "67380": "Lingolsheim",
    "67300": "Schiltigheim", "67800": "Bischheim", "67800": "Hœnheim",
    "67118": "Geispolsheim", "67500": "Haguenau", "67120": "Molsheim",
    "67210": "Obernai", "67600": "Sélestat",
    "67000-67999": "Bas-Rhin (zone à confirmer selon la commune)",
}

NAV = [
    ("Accueil", "/"),
    ("Nos services", "/services/"),
    ("Situations", "/situations/"),
    ("Zones d'intervention", "/villes/"),
    ("Tarifs", "/tarifs/"),
    ("Réalisations", "/realisations/"),
    ("Avis clients", "/avis-clients/"),
    ("À propos", "/a-propos/"),
    ("Blog", "/blog/"),
    ("FAQ", "/faq/"),
    ("Contact & devis", "/contact-devis/"),
]

CTA = {
    "devis": "Demander un devis gratuit",
    "estimation": "Recevoir mon estimation",
    "appeler": "Appeler maintenant",
    "whatsapp": "WhatsApp",
    "photos": "Envoyer mes photos",
    "zone": "Vérifier ma zone",
    "service": "En savoir plus",
}

REASSURANCE = [
    ("Devis gratuit", "Sans engagement, réponse sous 24 h ouvrées."),
    ("Réponse rapide", "Nous rappelons pour cadrer le volume et le créneau."),
    ("Intervention locale", "Strasbourg, l'Eurométropole, le Bas-Rhin et l'Alsace."),
    ("Tri et valorisation", "Ce qui peut être donné, réemployé ou recyclé l'est."),
    ("Équipe professionnelle", "Manutention, protection des accès, travail soigné."),
    ("Discret et propre", "Logement rendu vide et nettoyé selon la prestation choisie."),
]

HERO_ARGUMENTS = [
    "Devis gratuit et sans engagement",
    "Intervention rapide selon la disponibilité",
    "Tri, réemploi et recyclage",
    "Service clé en main : manutention, évacuation, nettoyage",
]

ETAPES = [
    ("Vous nous décrivez la situation",
     "Type de bien, volume approximatif, code postal et, si possible, quelques photos."),
    ("Nous évaluons le volume",
     "Échange téléphonique ou visite sur place selon la situation ; accès, étage, stationnement."),
    ("Vous recevez votre devis",
     "Un devis détaillé, gratuit et sans engagement, avec ce qui est inclus dans la prestation."),
    ("Nous vidons, évacuons et nettoyons",
     "Tri au fur et à mesure, sortie des encombrants, évacuation, nettoyage et remise du logement."),
]

VALORISATION = [
    ("Réemploi", "Les objets encore utilisables sont identifiés avant tout enlèvement."),
    ("Don", "Ce qui peut servir à d'autres est orienté vers des structures locales lorsque c'est possible."),
    ("Recyclage", "Métaux, bois, cartons, déchets verts et encombrants sont orientés en filière adaptée."),
    ("Valorisation", "Lorsque des objets ont une valeur, elle est discutée et déduite quand c'est possible."),
]

VALORISATION_MESSAGE = ("Avant d'évacuer, nous identifions ce qui peut être conservé, donné, réemployé ou "
                        "valorisé. Nous ne promettons pas systématiquement un débarras gratuit : selon le "
                        "volume et les objets, la valorisation peut réduire la facture, jamais l'annuler "
                        "d'office.")

POURQUOI_NOUS = [
    ("Vous n'avez rien à porter", "Notre équipe monte, descend et sort l'ensemble des encombrants."),
    ("Vous n'avez rien à transporter", "Camion et déchèterie : nous gérons l'évacuation complète."),
    ("Vous n'avez pas à tout trier seul", "Nous trions avec vous, pièce par pièce, ce qui doit rester."),
    ("Un devis clair", "Ce qui est inclus, ce qui ne l'est pas, et ce qui fait varier le prix."),
    ("Destination transparente", "Nous vous expliquons où vont les objets : don, filière, recyclage."),
    ("Un logement laissé propre", "Nettoyage du logement selon la prestation choisie."),
]

ZONES_PRESENTATION = (
    "Nous intervenons à Strasbourg et dans toute l'Alsace. Chaque commune ci-dessous dispose d'une page "
    "dédiée : accès, type d'habitat, contraintes courantes et exemples de chantiers."
)

FAQ_GENERALE = [
    ("Combien coûte un débarras ?",
     "Le prix dépend du volume à évacuer, de l'étage, de l'ascenseur, de la distance entre le camion et "
     "l'entrée, du type de biens et du niveau de tri souhaité. Un devis gratuit est établi après échange "
     "et, si besoin, après visite."),
    ("Le devis est-il gratuit ?",
     "Oui. Le devis est gratuit et sans engagement. Il détaille ce qui est inclus dans la prestation et ce "
     "qui expliquerait une variation de prix."),
    ("Peut-on envoyer des photos ?",
     "Oui, et c'est même la façon la plus rapide d'obtenir une estimation. Quelques photos des pièces et "
     "des encombrants permettent de cadrer le volume avant l'échange téléphonique."),
    ("Intervenez-vous sans ascenseur ?",
     "Oui. L'absence d'ascenseur, l'étage et la largeur des escaliers sont pris en compte dans le devis : "
     "c'est un facteur de temps d'intervention, pas un refus."),
    ("Que deviennent les meubles et les objets ?",
     "Ils sont triés. Ce qui peut être donné ou réemployé est orienté vers les filières adaptées, le reste "
     "est évacué en déchèterie ou en centre de traitement. Les objets de valeur sont identifiés avec vous."),
    ("Faites-vous le nettoyage après le débarras ?",
     "Oui, le nettoyage est une prestation complémentaire au débarras. Elle peut être incluse dans le devis "
     "si vous la demandez dès le départ."),
    ("Rachetez-vous certains objets ?",
     "Certains objets peuvent être valorisés : antiquités, mobilier, outillage, objets de collection. La "
     "valorisation éventuelle est discutée avant intervention et déduite du devis quand elle est confirmée."),
    ("Intervenez-vous en urgence ?",
     "Nous traitons les demandes urgentes en priorité selon nos disponibilités. Précisez-le dans votre "
     "demande : cela permet de vous répondre au plus vite."),
    ("Combien de temps dure un débarras ?",
     "Du quart de journée pour une cave ou un garage, à plusieurs jours pour une maison complète très "
     "encombrée. La durée est indiquée dans le devis."),
    ("Intervenez-vous le week-end ?",
     "Les interventions du samedi sont possibles selon le planning. Le dimanche est traité au cas par cas "
     "pour les situations urgentes."),
]

FAQ_ACCUEIL = FAQ_GENERALE[:6]

REALISATIONS_EXEMPLES = [
    ("Strasbourg — Neudorf", "Appartement 3 pièces", "10 à 20 m³", "1 jour"),
    ("Strasbourg — Cronenbourg", "Cave et grenier", "5 à 10 m³", "Demi-journée"),
    ("Illkirch-Graffenstaden", "Maison complète", "Plus de 40 m³", "3 jours"),
    ("Schiltigheim", "Garage et dépendance", "10 à 20 m³", "1 jour"),
    ("Haguenau", "Succession, appartement", "20 à 40 m³", "2 jours"),
    ("Obernai", "Local professionnel", "Plus de 40 m³", "2 jours"),
]

# Aucun avis n'est affiché tant qu'ils ne sont pas réels : le bloc l'indique clairement.
AVIS_MESSAGE = (
    "Les avis clients de la fiche Google de l'entreprise seront affichés ici dès qu'elle sera connectée. "
    "Nous préférons un emplacement vide à des témoignages inventés : cette page se remplira avec de vrais "
    "avis, à leur date et avec leur note réelle."
)

CONTACT_INTRO = (
    "Décrivez votre débarras en quelques étapes : type de bien, localisation, volume, accès et délai. "
    "Ajoutez des photos si vous en avez, c'est ce qui permet de vous répondre le plus précisément."
)
