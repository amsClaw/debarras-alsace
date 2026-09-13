# -*- coding: utf-8 -*-
"""7 pages situations — on part du vécu du visiteur, pas de la prestation."""

SITUATIONS = [
    {
        "slug": "demenagement", "nom": "Déménagement",
        "h1": "Débarras avant ou après un déménagement",
        "title": "Débarras avant déménagement en Alsace — devis gratuit",
        "meta": "Débarras avant ou après un déménagement en Alsace : ce que le camion de déménagement n'emporte pas est évacué. Tri, don et recyclage inclus.",
        "intro": (
            "Le jour du déménagement, il reste toujours ce que personne ne veut transporter : mobilier "
            "abîmé, électroménager hors service, cartons oubliés, objets de jardin. Nous intervenons avant "
            "le départ pour alléger, ou juste après pour vider ce qui reste."),
        "situation": [
            "Vous déménagez dans un logement plus petit et tout n'entre pas.",
            "Le camion de déménagement refuse certains objets (matelas, mobilier très abîmé).",
            "Vous devez libérer le logement avant l'état des lieux de sortie.",
        ],
        "reponses": [
            "Débarras ciblé sur ce qui ne part pas, sans toucher aux cartons que vous gardez.",
            "Intervention calée avant ou après le passage des déménageurs, sur le même créneau si besoin.",
            "Évacuation, tri et orientation des objets en don ou en recyclerie.",
            "Nettoyage du logement en option, pour l'état des lieux de sortie.",
        ],
        "services_lies": ["debarras-appartement", "debarras-maison", "debarras-encombrants"],
        "faq": [
            ("Pouvez-vous passer juste après les déménageurs ?",
             "Oui, c'est fréquent : nous réservons le créneau en fonction de leur heure de départ estimée."),
            ("Faut-il tout préparer avant votre arrivée ?",
             "Non. Indiquez-nous seulement ce qui doit rester : nous nous occupons du reste."),
        ],
    },
    {
        "slug": "succession", "nom": "Succession",
        "h1": "Vider un logement dans le cadre d'une succession",
        "title": "Débarras succession Alsace — accompagnement pas à pas",
        "meta": "Débarras de succession en Alsace : tri par catégories, objets familiaux mis de côté, documents conservés, logement libéré pour la vente. Devis gratuit.",
        "intro": (
            "Une succession, c'est un volume à traiter et des décisions à prendre à plusieurs. Notre "
            "méthode consiste à séparer clairement les catégories : ce que la famille garde, ce qui est "
            "donné, ce qui est évacué, et ce qui mérite un regard avant décision."),
        "situation": [
            "Le logement d'un parent doit être vidé avant la vente ou la location.",
            "Les héritiers habitent loin et ne peuvent pas trier sur place.",
            "Personne n'a le temps de s'occuper de chaque objet individuellement.",
        ],
        "reponses": [
            "Tri par catégories avec mise de côté systématique de ce que la famille veut garder.",
            "Documents et papiers jamais évacués : rassemblés et remis pour tri.",
            "Pilotage à distance possible (photos et échanges réguliers).",
            "Intervention en plusieurs passages si vous avez besoin de temps.",
            "Devis nominatif transmissible au notaire.",
        ],
        "services_lies": ["debarras-succession", "debarras-maison", "debarras-apres-deces"],
        "faq": [
            ("Pouvez-vous gérer plusieurs héritiers avec des avis différents ?",
             "Oui : nous fonctionnons avec un mandataire désigné, et nous documentons ce qui est mis de côté. "
             "Nous repartons sur un second passage si une décision doit être prise plus tard."),
            ("Récupérez-vous les bijoux et objets de valeur ?",
             "Nous ne faisons pas de récupération : ces objets sont identifiés, photographiés et mis de côté "
             "pour vous."),
        ],
    },
    {
        "slug": "deces", "nom": "Après un décès",
        "h1": "Vider un logement après un décès",
        "title": "Vider un logement après un décès en Alsace — guide et devis",
        "meta": "Débarras après un décès en Alsace : intervention discrète, respectueuse et organisée, de la mise de côté des objets personnels à la remise du logement.",
        "intro": (
            "C'est une démarche difficile, et souvent contrainte par un délai : restitution de bail, mise "
            "en vente, rendez-vous chez le notaire. Nous intervenons de manière discrète, en vous laissant "
            "le temps de décider ce qui compte."),
        "situation": [
            "Vous devez vider le logement d'un proche dans un délai court.",
            "Vous vivez loin et ne pouvez pas vous déplacer souvent.",
            "Vous ne souhaitez pas que les objets personnels soient évacués sans contrôle.",
        ],
        "reponses": [
            "Intervention discrète, véhicule neutre sur demande.",
            "Objets personnels et documents systématiquement mis de côté.",
            "Pilotage à distance possible, avec photos avant évacuation.",
            "Coordination avec notaire, syndic ou bailleur si nécessaire.",
            "Nettoyage du logement en option avant restitution ou vente.",
        ],
        "services_lies": ["debarras-apres-deces", "debarras-succession", "nettoyage-apres-debarras"],
        "faq": [
            ("Pouvez-vous intervenir si je ne peux pas être présent ?",
             "Oui, après un échange détaillé et un repérage. Nous documentons ce qui est mis de côté et nous "
             "ne validons aucune évacuation d'objet personnel sans votre accord."),
            ("Intervenez-vous rapidement en cas de bail à restituer ?",
             "Oui, ces situations passent en priorité selon nos disponibilités : indiquez la date limite."),
        ],
    },
    {
        "slug": "vente-immobiliere", "nom": "Vente immobilière",
        "h1": "Débarras avant une vente immobilière",
        "title": "Débarras avant vente immobilière en Alsace — bien libéré",
        "meta": "Débarras avant vente immobilière en Alsace : logement vidé, nettoyé et présentable pour les visites. Intervention planifiée et devis gratuit.",
        "intro": (
            "Un bien encombré se vend moins bien : les visites sont difficiles, les volumes paraissent plus "
            "petits, et les photos sont moins vendeuses. Un débarras avant mise en vente rend le logement "
            "lisible, visiteable, prêt à être montré."),
        "situation": [
            "Le logement est encombré et les visites sont compliquées à organiser.",
            "L'agence demande un bien vide ou présentable avant les photos.",
            "La vente est signée et vous devez libérer le bien avant la remise des clés.",
        ],
        "reponses": [
            "Débarras complet, avec démontage du mobilier volumineux.",
            "Nettoyage du logement pour les photos et les visites.",
            "Planification alignée sur les rendez-vous de l'agence ou du notaire.",
            "Évacuation documentée en cas de besoin (débarras après succession).",
        ],
        "services_lies": ["debarras-maison", "debarras-appartement", "nettoyage-apres-debarras"],
        "faq": [
            ("Peut-on débarrasser en plusieurs fois selon les visites ?",
             "Oui : un premier passage peut dégager les pièces principales et un second traiter cave, grenier "
             "et extérieurs."),
            ("Travaillez-vous avec les agences immobilières ?",
             "Oui, nous intervenons régulièrement pour elles, avec devis nominatif et facture."),
        ],
    },
    {
        "slug": "renovation", "nom": "Rénovation",
        "h1": "Débarras et curage avant des travaux de rénovation",
        "title": "Débarras avant travaux Alsace — curage et évacuation",
        "meta": "Débarras et curage avant travaux en Alsace : logement vidé, cloisons et revêtements déposés, gravats évacués. Préparation de chantier, devis gratuit.",
        "intro": (
            "Avant une rénovation, il faut libérer puis casser. Ces deux étapes conditionnent le planning "
            "des artisans : si elles traînent, tout le chantier décale. Nous les traitons comme un seul "
            "chantier, avec évacuation complète des gravats."),
        "situation": [
            "Un artisan doit intervenir mais le logement est encore encombré.",
            "Les cloisons, carrelages ou anciennes cuisines doivent être déposés avant travaux.",
            "Les gravats s'accumulent et personne ne peut les évacuer.",
        ],
        "reponses": [
            "Débarras du logement en amont des travaux, y compris cave et dépendances.",
            "Démolition de cloisons et dépose de revêtements non porteurs.",
            "Évacuation complète des gravats et matériaux, en filière adaptée.",
            "Possibilité d'enchaîner débarras puis dépose sur le même chantier.",
        ],
        "services_lies": ["demolition-interieure", "curage", "debarras-professionnel"],
        "faq": [
            ("Pouvez-vous intervenir avant le passage des artisans ?",
             "Oui, et c'est préférable : un logement libéré permet aux corps d'état de commencer sans délai "
             "supplémentaire."),
            ("Les gravats sont-ils compris dans le devis ?",
             "Oui, l'évacuation est intégrée. C'est souvent le premier poste de coût, car tout doit être "
             "descendu et transporté."),
        ],
    },
    {
        "slug": "expulsion", "nom": "Expulsion / fin de bail",
        "h1": "Débarras après expulsion ou fin de bail",
        "title": "Débarras après expulsion ou fin de bail en Alsace",
        "meta": "Débarras après expulsion ou fin de bail en Alsace : logement vidé et nettoyé, évacuation des encombrants, coordination avec bailleur, syndic ou commissaire de justice.",
        "intro": (
            "Ces situations sont tendues et souvent urgentes : le logement doit être vidé dans un délai "
            "précis, avec parfois une intervention ordonnée par un commissaire de justice. Nous "
            "intervenons proprement, sans commentaire sur la situation, et nous orientons en priorité les "
            "objets utilisables vers le don ou le stockage quand c'est possible."),
        "situation": [
            "Le logement doit être vidé après un départ contraint ou une expulsion.",
            "Le bailleur, le syndic ou le commissaire de justice attend une remise en état.",
            "Des affaires personnelles doivent être mises de côté plutôt que détruites.",
        ],
        "reponses": [
            "Intervention planifiée avec le mandataire (bailleur, syndic, commissaire de justice).",
            "Mise de côté des affaires personnelles identifiables, sur consigne écrite.",
            "Évacuation des encombrants et nettoyage complet du logement.",
            "Devis nominatif et facture à l'entité mandante ; compte rendu d'intervention si demandé.",
        ],
        "services_lies": ["debarras-appartement", "nettoyage-apres-debarras", "debarras-professionnel"],
        "faq": [
            ("Pouvez-vous documenter l'intervention ?",
             "Oui : photos datées et liste des éléments mis de côté, sur demande du mandataire."),
            ("Quel délai pour intervenir ?",
             "Ces demandes sont traitées en priorité selon nos disponibilités. Indiquez la date imposée dès la "
             "demande de devis."),
        ],
    },
    {
        "slug": "urgence", "nom": "Urgence",
        "h1": "Débarras urgent à Strasbourg et en Alsace",
        "title": "Débarras urgent Alsace — intervention prioritaire",
        "meta": "Débarras urgent en Alsace : délai court, intervention prioritaire selon disponibilité. Décrivez la situation, envoyez des photos, recevez une réponse rapide.",
        "intro": (
            "Il y a des situations où attendre une semaine n'est pas possible : dégât des eaux, logement à "
            "libérer immédiatement, sinistre, restitution de clés le lendemain. Nous ne promettons pas "
            "d'intervenir en une heure partout : nous regardons nos créneaux réels et nous vous répondons "
            "honnêtement sur ce qui est faisable."),
        "situation": [
            "Le logement doit être vidé dans les 24 à 72 heures.",
            "Un sinistre (dégât des eaux, incendie) impose d'évacuer rapidement.",
            "Un rendez-vous immanquable (état des lieux, remise des clés) impose une date.",
        ],
        "reponses": [
            "Traitement prioritaire de la demande dès réception.",
            "Estimation rapide par téléphone et photos, sans attendre une visite.",
            "Mobilisation d'une équipe dédiée si un créneau est disponible.",
            "En cas d'impossibilité, nous vous le disons tout de suite pour que vous puissiez chercher une alternative.",
        ],
        "services_lies": ["debarras-appartement", "debarras-encombrants", "nettoyage-apres-debarras"],
        "faq": [
            ("Garantissez-vous une intervention en 24 h ?",
             "Non, personne ne peut le garantir sérieusement. En revanche, les demandes urgentes sont "
             "examinées immédiatement et nous vous répondons sur ce qui est réellement possible."),
            ("Que dois-je préparer pour gagner du temps ?",
             "Quelques photos, l'adresse exacte, l'étage et l'accès, et ce qui doit impérativement être "
             "conservé. C'est suffisant pour chiffrer rapidement."),
        ],
    },
]

SITUATIONS_BY_SLUG = {s["slug"]: s for s in SITUATIONS}
