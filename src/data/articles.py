# -*- coding: utf-8 -*-
"""4 articles de blog piliers. Aucun chiffre inventé : on explique les mécanismes,
on ne donne pas de prix ferme tant que le client n'a pas validé ses fourchettes."""

ARTICLES = [
    {
        "slug": "combien-coute-un-debarras-a-strasbourg",
        "titre": "Combien coûte un débarras à Strasbourg ?",
        "title": "Combien coûte un débarras à Strasbourg ? — les facteurs de prix",
        "meta": "Volume, étage, ascenseur, accès, tri, nettoyage : découvrez ce qui fait réellement varier le prix d'un débarras à Strasbourg et comment lire un devis.",
        "date": "2026-09-13",
        "chapeau": (
            "Aucune entreprise sérieuse ne peut annoncer un prix de débarras sans connaître le volume et "
            "l'accès. Voici ce qui fait réellement varier la facture — et les questions à poser avant de "
            "valider un devis."),
        "sections": [
            ("1. Le volume, exprimé en mètres cubes",
             ["C'est le premier facteur. Un débarras se chiffre en m³, pas en nombre de pièces : une cave de "
              "20 m² peut contenir plus qu'un appartement de 50 m² s'il est rempli du sol au plafond.",
              "Pour estimer le volume, on raisonne souvent en fractions de camion : un huitième, un quart, "
              "une moitié, un camion complet. Un camion de débarras courant correspond à une vingtaine de "
              "mètres cubes utiles."]),
            ("2. L'accès : le facteur le plus sous-estimé",
             ["Le temps de manutention dépend de la distance entre le logement et le camion. Un pavillon avec "
              "accès direct ne coûte pas le même temps qu'un appartement au 4ᵉ étage sans ascenseur, dans une "
              "rue piétonne, avec 40 mètres à parcourir en brouette.",
              "Sont donc pris en compte : l'étage, la présence d'un ascenseur utilisable, la largeur des "
              "escaliers, les portes palières, le stationnement autorisé et le point de chargement."]),
            ("3. La nature des objets",
             ["Mobilier, électroménager, gravats, pneus, produits chimiques ne relèvent pas des mêmes "
              "filières. Les gravats et les déchets de chantier se pèsent et se traitent à part ; certains "
              "produits (peintures, solvants, batteries) nécessitent une collecte spécifique."]),
            ("4. Le niveau de tri demandé",
             ["Un débarras « tout évacué » n'est pas la même prestation qu'un tri fin, avec mise de côté des "
              "objets à conserver, orientation vers le don et la recyclerie. Le tri demande du temps sur "
              "place, et ce temps se retrouve dans le prix."]),
            ("5. Le nettoyage après débarras",
             ["Le nettoyage est une prestation distincte, souvent couplée au débarras. La réaliser dans la "
              "foulée coûte moins cher qu'un second déplacement, mais elle reste un poste à part dans le "
              "devis."]),
            ("Comment lire un devis de débarras",
             ["Un devis lisible indique : le volume estimé, la durée prévue, le nombre d'intervenants, ce qui "
              "est inclus (manutention, évacuation, tri, nettoyage), ce qui ne l'est pas, et ce qui "
              "entraînerait une variation (gravats découverts, volume plus important que prévu).",
              "Méfiez-vous d'un prix annoncé par téléphone en trente secondes, sans photos ni description : "
              "il est presque toujours révisé à la hausse le jour de l'intervention."]),
            ("Les questions à poser avant de valider",
             ["Le prix est-il ferme pour le volume décrit ? Que se passe-t-il si le volume réel est plus "
              "important ? Les gravats sont-ils inclus ? Le nettoyage est-il compris ? Les objets de valeur "
              "sont-ils mis de côté ? Existe-t-il un rachat ou une valorisation possible, et sur quels "
              "objets ?"]),
        ],
        "faq": [
            ("Peut-on avoir un prix sans visite ?",
             "Souvent oui, à partir de photos précises et d'une description de l'accès. Pour les volumes "
             "importants ou les situations complexes, une visite reste plus fiable pour tout le monde."),
            ("Le prix baisse-t-il si des objets ont de la valeur ?",
             "Parfois : certains objets (mobilier ancien, outillage, antiquités) peuvent être valorisés ou "
             "rachetés, ce qui réduit la facture. Cette déduction n'est jamais automatique ni garantie."),
        ],
    },
    {
        "slug": "vider-une-maison-apres-un-deces",
        "titre": "Comment vider une maison après un décès ?",
        "title": "Vider une maison après un décès — méthode pas à pas",
        "meta": "Vider une maison après un décès : ordre des démarches, documents à conserver, gestion des objets personnels, délais et aide possible. Guide pratique.",
        "date": "2026-09-13",
        "chapeau": (
            "Entre les démarches administratives et la charge émotionnelle, vider le logement d'un proche "
            "demande de la méthode. Voici un ordre de travail qui évite de regretter une décision."),
        "sections": [
            ("1. Commencez par ce qui est administratif",
             ["Avant de toucher aux meubles, repérez et rassemblez les documents : papiers d'identité, actes "
              "notariés, contrats, relevés bancaires, titres de propriété, factures importantes, courriers "
              "en cours. Ces documents ne doivent jamais partir avec les encombrants.",
              "Prévoyez une boîte dédiée, fermée, qui ne quittera pas le logement avant d'être triée par un "
              "proche ou par le notaire."]),
            ("2. Faites un premier passage « objets personnels »",
             ["Avant tout débarras, un passage dédié aux souvenirs : photos, courriers, bijoux, objets "
              "familiaux. C'est l'étape qu'on ne peut pas refaire après coup.",
              "Si vous êtes plusieurs héritiers, désignez une personne qui centralise, et notez ce qui est "
              "mis de côté pour qui. Un simple tableau partagé évite beaucoup de tensions."]),
            ("3. Demandez l'accord des personnes concernées",
             ["Pour un logement loué, prévenez le bailleur et convenez d'une date de restitution des clés. "
              "Pour une copropriété, informez le syndic. En cas d'indivision, l'intervention doit être "
              "mandatée par une personne autorisée."]),
            ("4. Décidez du sort du mobilier",
             ["Trois catégories suffisent : ce qui se garde, ce qui se donne (associations, recyclerie, "
              "proches), ce qui est évacué. Le tri fin se fait en avançant : plus vous attendez, plus la "
              "décision devient lourde.",
              "Pour les objets qui ont potentiellement de la valeur (mobilier ancien, tableaux, outillage), "
              "mettez-les de côté et faites-les regarder avant toute évacuation."]),
            ("5. Organisez le débarras lui-même",
             ["Une fois les objets à conserver isolés, le reste peut être évacué. C'est à ce moment qu'une "
              "entreprise de débarras fait gagner du temps : manutention, évacuation, orientation en "
              "filières, nettoyage.",
              "Prévoyez une pièce « à garder » clairement identifiée (avec une étiquette sur la porte) : "
              "c'est la meilleure protection contre les erreurs."]),
            ("6. Traitez la remise en état du logement",
             ["Si le logement est vendu ou loué, un nettoyage complet est presque toujours nécessaire après "
              "évacuation : poussière accumulée, sanitaires, cuisine, vitres. Prévoyez-le dans le même "
              "chantier pour éviter un second déplacement."]),
        ],
        "faq": [
            ("Combien de temps faut-il prévoir ?",
             "Pour un appartement, une à deux journées suffisent en général pour l'évacuation. Pour une "
             "maison avec cave, grenier et dépendances, comptez plutôt deux à quatre jours."),
            ("Faut-il être présent pendant l'intervention ?",
             "Utile au démarrage, pas indispensable ensuite. Beaucoup de familles pilotent à distance après "
             "avoir validé ce qui est mis de côté."),
        ],
    },
    {
        "slug": "qui-paie-le-debarras-dune-succession",
        "titre": "Qui paie le débarras d'une succession ?",
        "title": "Qui paie le débarras d'une succession ? — explications",
        "meta": "Qui paie le débarras d'un logement en succession ? Frais engagés par le mandataire, traitement dans le règlement successoral, cas de l'indivision et du bail.",
        "date": "2026-09-13",
        "chapeau": (
            "La question revient à chaque succession : qui avance les frais, et comment sont-ils traités "
            "entre héritiers ? Voici le fonctionnement habituel et les points à clarifier avec le notaire."),
        "sections": [
            ("En pratique, une personne engage la dépense",
             ["Le débarras est une dépense de conservation et de gestion du bien. Elle est généralement "
              "engagée par la personne qui gère concrètement le logement : un héritier mandaté, le notaire "
              "en charge de la succession, un mandataire ou un exécuteur testamentaire.",
              "L'entreprise de débarras facture la personne ou l'entité qui la mandate : établissez un devis "
              "nominatif, c'est la pièce qui permettra de traiter la dépense dans le règlement de la "
              "succession."]),
            ("Le traitement entre héritiers",
             ["La dépense est en principe supportée par la succession, puis répartie entre les héritiers au "
              "prorata de leurs droits, sauf accord différent. Les modalités précises relèvent du notaire : "
              "c'est lui qui arbitre et inscrit la dépense dans le compte de succession.",
              "En cas d'indivision conflictuelle, mieux vaut un accord écrit entre héritiers avant "
              "l'intervention, ou une décision du notaire : cela évite qu'un héritier conteste la dépense "
              "après coup."]),
            ("Si le logement est loué",
             ["La dépense de débarras reste à la charge de la succession. Le bailleur, lui, attend la "
              "restitution d'un logement vide et en état : pensez au délai du préavis et au calendrier de "
              "l'état des lieux.",
              "Un débarras réalisé rapidement évite de payer des loyers supplémentaires pendant que le "
              "logement reste encombré."]),
            ("Si le logement est vendu",
             ["Le débarras est alors une dépense de préparation de la vente. Un logement vide se visite mieux "
              "et se négocie plus facilement : la dépense est souvent rentabilisée par la vente elle-même.",
              "Là encore, devis et facture nominatifs : ils se rattachent aux frais de la succession."]),
            ("Les points à vérifier avant de signer",
             ["Qui mandate l'entreprise et à quel nom est établi le devis ? La dépense a-t-elle été validée "
              "par les autres héritiers ou par le notaire ? Que se passe-t-il si le volume réel est plus "
              "important que l'estimation ? Les objets de valeur sont-ils mis de côté et documentés ?"]),
        ],
        "faq": [
            ("Un héritier peut-il refuser de payer sa part ?",
             "Le traitement des dettes et dépenses successorales relève du droit des successions et de "
             "l'appréciation du notaire. Notre rôle s'arrête au devis et à la facture, nominatifs, que vous "
             "transmettez au dossier."),
            ("Faut-il l'accord de tous les héritiers pour débarrasser ?",
             "Dans la pratique, l'intervention est mandatée par une personne autorisée à agir. En cas de "
             "désaccord, mieux vaut passer par le notaire avant de lancer les travaux."),
        ],
    },
    {
        "slug": "debarras-gratuit-est-ce-possible",
        "titre": "Débarras gratuit : est-ce vraiment possible ?",
        "title": "Débarras gratuit : est-ce vraiment possible ? — ce qu'il faut savoir",
        "meta": "Débarras gratuit : comprendre la valorisation des objets, pourquoi la gratuité est rarement garantie et comment repérer les promesses commerciales trompeuses.",
        "date": "2026-09-13",
        "chapeau": (
            "Beaucoup d'entreprises annoncent un « débarras gratuit ». Derrière cette promesse, il y a "
            "toujours une condition. Voici comment ça fonctionne réellement — et comment ne pas se faire "
            "surprendre."),
        "sections": [
            ("D'où vient l'idée de gratuité",
             ["Un débarras coûte de l'argent : main-d'œuvre, camion, carburant, dépôt en filière. La "
              "gratuité ne peut venir que d'une seule source : la valeur des objets récupérés, revendus par "
              "l'entreprise.",
              "La promesse est donc conditionnelle. Elle suppose un logement contenant suffisamment d'objets "
              "revendables pour couvrir le coût de l'intervention."]),
            ("Ce qui se revend vraiment (et ce qui ne se revend pas)",
             ["Peuvent avoir une valeur : mobilier ancien ou de marque en bon état, outillage, antiquités, "
              "objets de collection, vaisselle recherchée, certains vinyles ou livres.",
              "N'ont généralement aucune valeur de revente : matelas, canapés usés, mobilier de grande "
              "surface en aggloméré abîmé, électroménager hors service, gravats, cartons, textiles "
              "ordinaires. Or c'est souvent la majorité du volume."]),
            ("Les trois formes de « gratuit » que vous rencontrerez",
             ["① « gratuit si récupération » : l'entreprise ne facture pas si la valeur récupérée couvre le "
              "chantier — sinon elle facture, parfois après avoir commencé. ② « gratuit » avec frais annexes "
              "(déplacement, tri, benne, nettoyage) qui apparaissent au devis. ③ « gratuit » conditionné à "
              "l'abandon de tous vos droits sur les objets, y compris ceux qui ont une valeur réelle."]),
            ("La question à poser : qui garde la valeur ?",
             ["Si une entreprise valorise ou revend des objets issus de votre logement, cette valeur doit "
              "être connue et discutée. Deux modèles honnêtes existent : soit la valorisation est déduite du "
              "devis de manière explicite, soit vous confiez les objets en connaissance de cause.",
              "Ce qui n'est pas acceptable : une évacuation où des objets de valeur disparaissent sans avoir "
              "été identifiés avec vous."]),
            ("Notre position",
             ["Nous ne promettons pas de débarras gratuit. Nous disons ce qui est inclus, ce qui ne l'est "
              "pas, et ce qui peut éventuellement réduire la facture : objets identifiés ensemble, "
              "orientation en don ou recyclerie, valorisation discutée avant intervention.",
              "Un devis clair, même payant, coûte souvent moins cher qu'un « gratuit » assorti de frais "
              "annexes découverts le jour de l'intervention."]),
        ],
        "faq": [
            ("Peut-on vraiment ne rien payer ?",
             "Cela arrive, mais c'est rare et conditionnel : il faut un volume d'objets revendables "
             "suffisant. Aucune entreprise honnête ne peut garantir la gratuité avant d'avoir vu le "
             "logement."),
            ("Comment vérifier qu'une offre est sérieuse ?",
             "Demandez un devis écrit mentionnant le volume, la durée, les frais annexes éventuels, le sort "
             "des objets de valeur et le traitement des gravats. Refusez les accords uniquement oraux."),
        ],
    },
]

ARTICLES_BY_SLUG = {a["slug"]: a for a in ARTICLES}
