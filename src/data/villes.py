# -*- coding: utf-8 -*-
"""12 pages villes — contenu réellement distinct : quartiers, communes voisines,
type d'habitat, contraintes locales et exemples de chantiers."""

VILLES = [
    {
        "slug": "strasbourg", "nom": "Strasbourg", "cp": "67000 / 67100 / 67200",
        "courte": "la ville centre, ses quartiers et ses immeubles anciens",
        "h1": "Débarras à Strasbourg (67000)",
        "title": "Débarras à Strasbourg — devis gratuit, intervention rapide",
        "meta": "Débarras à Strasbourg : appartements, maisons de quartier, caves et dépendances. Tri, évacuation et nettoyage. Devis gratuit, contraintes de stationnement gérées.",
        "intro": (
            "Strasbourg cumule deux réalités très différentes selon le quartier : des immeubles anciens du "
            "centre et de la Neustadt, avec des cages d'escalier étroites et des caves voûtées, et des "
            "ensembles plus récents à Cronenbourg, au Neudorf ou à la Meinau, où le volume se joue surtout "
            "sur les étages et les ascenseurs. Nous adaptons l'intervention à chacune de ces configurations : "
            "protection des sols et des rampes d'escalier, démontage de meubles quand la porte palière est "
            "trop étroite, repérage du meilleur point de chargement, créneau adapté aux zones à stationnement "
            "réglementé."),
        "quartiers": ["Neudorf", "Krutenau", "Esplanade", "Orangerie", "Cronenbourg", "Koenigshoffen",
                      "Robertsau", "Gare", "Meinau", "Neustadt"],
        "communes_voisines": ["Schiltigheim", "Bischheim", "Illkirch-Graffenstaden", "Ostwald", "Lingolsheim",
                              "Hœnheim", "Eckbolsheim", "Mundolsheim"],
        "chantiers": [
            ("Appartement 3 pièces, Esplanade", "Succession, cave et balcon inclus", "10 à 20 m³", "1 jour"),
            ("Maison de quartier, Robertsau", "Débarras complet avant vente", "20 à 40 m³", "2 jours"),
            ("Cave voûtée, Neustadt", "Encombrants, bouteilles et mobilier", "5 à 10 m³", "Demi-journée"),
        ],
        "note_locale": (
            "À Strasbourg, la contrainte n'est presque jamais le volume : c'est le chemin jusqu'au camion. "
            "Le stationnement se prépare (zones payantes, îlots piétons, cours intérieures), et l'ascenseur "
            "doit parfois être réservé auprès du syndic."),
        "faq": [
            ("Intervenez-vous dans les quartiers à stationnement réglementé ?",
             "Oui. Nous anticipons le point de chargement et, lorsque c'est nécessaire, nous vous indiquons "
             "quelle autorisation demander à la mairie ou au syndic."),
            ("Pouvez-vous monter par la cage d'escalier si l'ascenseur est trop petit ?",
             "Oui. Les meubles volumineux sont démontés si besoin, et les escaliers sont protégés avant "
             "passage."),
        ],
    },
    {
        "slug": "illkirch-graffenstaden", "nom": "Illkirch-Graffenstaden", "cp": "67400",
        "courte": "pavillons, campus et zones d'activité",
        "h1": "Débarras à Illkirch-Graffenstaden (67400)",
        "title": "Débarras à Illkirch-Graffenstaden — devis gratuit",
        "meta": "Débarras à Illkirch-Graffenstaden : pavillons, appartements proches du campus, locaux professionnels du parc d'innovation. Tri et évacuation, devis gratuit.",
        "intro": (
            "Illkirch-Graffenstaden mélange des pavillons avec jardin, souvent occupés depuis plusieurs "
            "décennies, des résidences proches du campus universitaire, et des locaux d'activité autour du "
            "parc d'innovation. Cela donne trois types de chantiers très différents : le garage et la cave "
            "d'un pavillon familial, l'appartement meublé d'un étudiant qui part, et le local professionnel "
            "à vider avant un changement de bail. Nous nous déplaçons avec le même souci de tri et de "
            "traçabilité des évacuations dans les trois cas."),
        "quartiers": ["Centre", "Graffenstaden", "Baggersee", "Zone d'innovation", "Quai des Pêcheurs"],
        "communes_voisines": ["Strasbourg", "Ostwald", "Geispolsheim", "Lingolsheim", "Eschau", "Fegersheim"],
        "chantiers": [
            ("Pavillon avec cave et garage, Graffenstaden", "Débarras complet", "20 à 40 m³", "2 jours"),
            ("Local professionnel, parc d'innovation", "Curage avant fin de bail", "Plus de 40 m³", "2 jours"),
            ("Studio meublé près du campus", "Débarras rapide entre deux locataires", "5 à 10 m³", "Demi-journée"),
        ],
        "note_locale": (
            "Les pavillons d'Illkirch cachent souvent un garage et une cave qui n'ont pas été vidés depuis "
            "longtemps : c'est là que se trouve l'essentiel du volume, et souvent aussi l'outillage à "
            "conserver."),
        "faq": [
            ("Intervenez-vous dans les locaux professionnels du parc d'innovation ?",
             "Oui, sur créneaux convenus, y compris en dehors des heures d'ouverture, avec devis et facture "
             "nominatifs."),
            ("Combien de temps pour un pavillon complet ?",
             "En général une à deux journées selon le volume, le nombre de dépendances (cave, garage, "
             "grenier) et le niveau de tri souhaité."),
        ],
    },
    {
        "slug": "ostwald", "nom": "Ostwald", "cp": "67540",
        "courte": "lotissements et maisons de l'après-guerre",
        "h1": "Débarras à Ostwald (67540)",
        "title": "Débarras à Ostwald — devis gratuit, intervention locale",
        "meta": "Débarras à Ostwald : maisons de lotissement, caves, garages et dépendances. Manutention, tri et évacuation. Devis gratuit et sans engagement.",
        "intro": (
            "Ostwald est une commune de maisons, beaucoup construites entre les années 1960 et 1990, avec "
            "des sous-sols complets, des garages accolés et parfois un atelier. Le volume est rarement "
            "visible depuis l'extérieur : il est sous la maison. Nous commençons donc par évaluer les "
            "niveaux (sous-sol, rez-de-chaussée, étage, dépendances) pour proposer un devis réaliste et un "
            "nombre de passages cohérent."),
        "quartiers": ["Centre", "Wihrel", "Zone du Pôle Sud", "Bords de l'Ill"],
        "communes_voisines": ["Strasbourg", "Illkirch-Graffenstaden", "Lingolsheim", "Geispolsheim"],
        "chantiers": [
            ("Maison avec sous-sol complet", "Débarras cave, garage et atelier", "20 à 40 m³", "2 jours"),
            ("Appartement en résidence", "Succession, meubles et électroménager", "5 à 10 m³", "Demi-journée"),
            ("Abri de jardin et remise", "Encombrants et outillage", "5 m³", "2 heures"),
        ],
        "note_locale": (
            "Beaucoup de sous-sols d'Ostwald servent de dépôt depuis des années : cartons, conserves, "
            "meubles démontés et matériel de bricolage. C'est le poste le plus volumineux du chantier."),
        "faq": [
            ("Le sous-sol est encombré sur toute la hauteur, est-ce un problème ?",
             "Non : nous travaillons par zones et descendons les encombrants par l'accès camion. Si l'accès "
             "est trop bas, nous convenons d'un point de dépose intermédiaire."),
            ("Faut-il tout sortir avant votre passage ?",
             "Surtout pas : c'est justement notre travail. Il suffit de nous indiquer ce que vous souhaitez "
             "garder."),
        ],
    },
    {
        "slug": "lingolsheim", "nom": "Lingolsheim", "cp": "67380",
        "courte": "cités, pavillons et bords de Bruche",
        "h1": "Débarras à Lingolsheim (67380)",
        "title": "Débarras à Lingolsheim — devis gratuit, intervention rapide",
        "meta": "Débarras à Lingolsheim : appartements en cité, pavillons, caves et box. Tri, manutention et évacuation soignée. Devis gratuit sous 24 h.",
        "intro": (
            "Lingolsheim présente un habitat varié : immeubles collectifs à proximité de la gare et du "
            "centre, lotissements de pavillons vers l'ouest, et de nombreuses caves et box individuels. "
            "Dans les collectifs, la question est celle des parties communes et des créneaux ; dans les "
            "pavillons, celle du débarras complet avec dépendances. Nous avons l'habitude des deux et "
            "adaptons l'équipe comme la durée."),
        "quartiers": ["Centre", "Gare", "Ouest", "Bords de Bruche"],
        "communes_voisines": ["Strasbourg", "Ostwald", "Illkirch-Graffenstaden", "Eckbolsheim", "Holtzheim"],
        "chantiers": [
            ("Appartement en collectif, centre", "Débarras avant restitution de bail", "10 à 20 m³", "1 jour"),
            ("Cave et box individuels", "Vidage complet", "5 à 10 m³", "Demi-journée"),
            ("Pavillon avec jardin", "Mobilier de jardin, remise et cave", "10 à 20 m³", "1 jour"),
        ],
        "note_locale": (
            "Les box et caves de Lingolsheim sont souvent accessibles en sous-sol avec une rampe : un accès "
            "véhicule direct évite beaucoup de manutention et raccourcit l'intervention."),
        "faq": [
            ("Pouvez-vous vider uniquement une cave ou un box ?",
             "Oui. Un débarras partiel est fréquent : quelques mètres cubes suffisent à retrouver de l'espace "
             "utile."),
            ("Prévenez-vous la copropriété ?",
             "Nous vous indiquons ce qu'il faut transmettre au syndic (créneau, point de chargement, "
             "protection des accès) avant l'intervention."),
        ],
    },
    {
        "slug": "schiltigheim", "nom": "Schiltigheim", "cp": "67300",
        "courte": "ancienne ville brassicole, forte densité",
        "h1": "Débarras à Schiltigheim (67300)",
        "title": "Débarras à Schiltigheim — devis gratuit, immeubles et maisons",
        "meta": "Débarras à Schiltigheim : immeubles de rapport, anciennes maisons de brasseurs, caves et greniers. Tri et évacuation, devis gratuit.",
        "intro": (
            "Schiltigheim est dense : immeubles de rapport, anciennes maisons ouvrières et bâtiments liés à "
            "l'histoire brassicole de la ville. Les cages d'escalier y sont souvent étroites et les cours "
            "intérieures parfois difficiles d'accès, ce qui impose de préparer précisément le parcours des "
            "encombrants. Nous commençons toujours par un repérage du chemin entre le logement et le camion : "
            "c'est ce qui fait la différence sur un chantier en centre-ville."),
        "quartiers": ["Centre", "Halles", "Adelshoffen", "Ouest", "Est"],
        "communes_voisines": ["Strasbourg", "Bischheim", "Hœnheim", "Souffelweyersheim", "Mundolsheim"],
        "chantiers": [
            ("Immeuble de rapport, centre", "Débarras de deux appartements", "Plus de 40 m³", "3 jours"),
            ("Maison de ville ancienne", "Grenier, cave et cour", "20 à 40 m³", "2 jours"),
            ("Appartement 2 pièces, Halles", "Succession, mobilier et cartons", "5 à 10 m³", "Demi-journée"),
        ],
        "note_locale": (
            "À Schiltigheim, le stationnement et la largeur des accès comptent autant que le volume. Un "
            "camion qui ne peut pas approcher peut doubler le temps de manutention : nous le vérifions avant "
            "de chiffrer."),
        "faq": [
            ("Le camion peut-il approcher de l'entrée ?",
             "Nous le vérifions sur place ou sur photos. Si l'accès est impossible, nous prévoyons un point "
             "de dépose intermédiaire et la main-d'œuvre correspondante."),
            ("Intervenez-vous en plusieurs passages ?",
             "Oui, notamment pour les immeubles de rapport ou les successions à traiter par étapes."),
        ],
    },
    {
        "slug": "bischheim", "nom": "Bischheim", "cp": "67800",
        "courte": "quartiers résidentiels et zones d'activité",
        "h1": "Débarras à Bischheim (67800)",
        "title": "Débarras à Bischheim — devis gratuit, maisons et locaux",
        "meta": "Débarras à Bischheim : maisons, appartements et locaux d'activité. Caves, garages et dépendances vidés, encombrants évacués. Devis gratuit.",
        "intro": (
            "Bischheim combine des quartiers résidentiels avec des maisons souvent prolongées par un garage "
            "et une cave, et des zones d'activité où se trouvent ateliers et entrepôts. La proximité de "
            "Strasbourg et de l'autoroute facilite l'accès des camions, ce qui raccourcit les interventions "
            "tout en permettant des volumes importants sur une même journée."),
        "quartiers": ["Centre", "Ouest", "Zones d'activité", "Bords de l'Ill"],
        "communes_voisines": ["Schiltigheim", "Hœnheim", "Strasbourg", "Reichstett", "Souffelweyersheim"],
        "chantiers": [
            ("Maison avec garage et cave", "Débarras complet avant vente", "20 à 40 m³", "2 jours"),
            ("Atelier en zone d'activité", "Curage et évacuation de matériel", "Plus de 40 m³", "2 jours"),
            ("Appartement en collectif", "Désencombrement et enlèvement d'encombrants", "5 à 10 m³", "Demi-journée"),
        ],
        "note_locale": (
            "Sur Bischheim et Hœnheim, l'accès camion est généralement simple : c'est un avantage pour les "
            "volumes importants, qui peuvent être traités plus rapidement qu'en centre-ville de Strasbourg."),
        "faq": [
            ("Prenez-vous en charge les locaux d'activité ?",
             "Oui : ateliers, entrepôts et bureaux, avec devis et facture nominatifs, et possibilité "
             "d'intervenir le soir ou le week-end."),
            ("Intervenez-vous aussi à Hœnheim ?",
             "Oui, Hœnheim fait partie de nos zones d'intervention habituelles autour de Strasbourg."),
        ],
    },
    {
        "slug": "hoenheim", "nom": "Hœnheim", "cp": "67800",
        "courte": "petite commune, lotissements récents",
        "h1": "Débarras à Hœnheim (67800)",
        "title": "Débarras à Hœnheim — devis gratuit, intervention locale",
        "meta": "Débarras à Hœnheim : maisons de lotissement, appartements récents, caves et garages. Enlèvement d'encombrants et débarras complet, devis gratuit.",
        "intro": (
            "Hœnheim est une commune compacte, bien desservie par le tram, avec des lotissements récents et "
            "des maisons de taille moyenne. Les chantiers y sont souvent plus simples d'accès qu'à "
            "Strasbourg : garages, caves et abris de jardin à vider, appartements à désencombrer avant un "
            "déménagement. Nous intervenons régulièrement en complément d'un déménagement déjà organisé."),
        "quartiers": ["Centre", "Lotissements", "Bords du canal"],
        "communes_voisines": ["Bischheim", "Schiltigheim", "Strasbourg", "Reichstett", "Mundolsheim"],
        "chantiers": [
            ("Maison de lotissement", "Cave, garage et abri de jardin", "10 à 20 m³", "1 jour"),
            ("Appartement récent", "Désencombrement avant déménagement", "5 à 10 m³", "Demi-journée"),
            ("Garage seul", "Mobilier, cartons et outillage hors d'usage", "5 m³", "2 heures"),
        ],
        "note_locale": (
            "Sur ces chantiers, le tri est souvent rapide : beaucoup d'objets sont encore en bon état et "
            "peuvent être orientés vers le don ou la recyclerie plutôt que vers l'évacuation."),
        "faq": [
            ("Pouvez-vous intervenir après le passage des déménageurs ?",
             "Oui, c'est un cas fréquent : ils emportent le mobilier conservé, nous évacuons tout le reste, y "
             "compris ce qui n'entre pas dans le camion de déménagement."),
            ("Faites-vous les petits volumes ?",
             "Oui, à partir de quelques objets, dans le cadre d'un créneau planifié."),
        ],
    },
    {
        "slug": "geispolsheim", "nom": "Geispolsheim", "cp": "67118",
        "courte": "village, corps de ferme et zone commerciale",
        "h1": "Débarras à Geispolsheim (67118)",
        "title": "Débarras à Geispolsheim — devis gratuit, maisons et fermes",
        "meta": "Débarras à Geispolsheim : maisons de village, corps de ferme, dépendances et locaux commerciaux. Tri, évacuation de gros volumes, devis gratuit.",
        "intro": (
            "Geispolsheim conjugue un village ancien, des corps de ferme avec granges et hangars, et une "
            "grande zone commerciale. Les volumes y sont souvent plus importants qu'en ville : granges, "
            "étables anciennes, hangars agricoles, réserves de commerce. Ces chantiers demandent une "
            "organisation en phases, avec évacuation progressive et parfois benne sur place."),
        "quartiers": ["Centre", "Fort-Louis", "Zone commerciale", "Hameaux"],
        "communes_voisines": ["Illkirch-Graffenstaden", "Ostwald", "Eschau", "Fegersheim", "Lipsheim", "Entzheim"],
        "chantiers": [
            ("Corps de ferme, grange et étable", "Curage de dépendances agricoles", "Plus de 40 m³", "3 jours"),
            ("Réserve de commerce, zone commerciale", "Évacuation de mobilier et cartons", "20 à 40 m³", "1 jour"),
            ("Maison de village", "Débarras complet avec cave et grenier", "20 à 40 m³", "2 jours"),
        ],
        "note_locale": (
            "Sur les corps de ferme, la difficulté vient des volumes et de la nature des déchets (bois, "
            "ferraille, gravats, parfois amiante à faire vérifier par un spécialiste avant toute "
            "intervention)."),
        "faq": [
            ("Évacuez-vous la ferraille et le bois de grange ?",
             "Oui, ces matériaux sont triés et orientés vers les filières adaptées (ferraille, bois). Les "
             "volumes sont chiffrés au repérage."),
            ("Et si le bâtiment contient de l'amiante ?",
             "Nous n'intervenons pas sur l'amiante : un diagnostic par un spécialiste est nécessaire avant "
             "tout travail. Nous pouvons signaler les matériaux suspects lors du repérage."),
        ],
    },
    {
        "slug": "haguenau", "nom": "Haguenau", "cp": "67500",
        "courte": "deuxième ville du Bas-Rhin, habitat varié",
        "h1": "Débarras à Haguenau (67500)",
        "title": "Débarras à Haguenau — devis gratuit, maisons et appartements",
        "meta": "Débarras à Haguenau : maisons, appartements, caves et locaux. Tri, manutention, évacuation et nettoyage. Devis gratuit sous 24 h.",
        "intro": (
            "Deuxième commune du Bas-Rhin par sa population, Haguenau présente un centre ancien dense, des "
            "quartiers résidentiels étendus et des maisons plus rurales en périphérie, entre forêt et "
            "zones agricoles. Les chantiers y sont souvent des débarras complets de maison avec cave, "
            "grenier et dépendances, ou des successions dans le centre ancien où le stationnement demande "
            "de l'anticipation."),
        "quartiers": ["Centre historique", "Marxenhouse", "Bildstoeckel", "Saint-Joseph", "Harthouse"],
        "communes_voisines": ["Schweighouse-sur-Moder", "Bischwiller", "Kaltenhouse", "Marienthal", "Niederbronn"],
        "chantiers": [
            ("Maison complète, quartier Saint-Joseph", "Succession avec cave et grenier", "20 à 40 m³", "2 jours"),
            ("Appartement, centre historique", "Débarras et nettoyage avant location", "10 à 20 m³", "1 jour"),
            ("Maison rurale en périphérie", "Granges, remises et extérieurs", "Plus de 40 m³", "3 jours"),
        ],
        "note_locale": (
            "Sur Haguenau et sa périphérie, les volumes sont souvent plus importants que dans "
            "l'Eurométropole : il est fréquent de prévoir plusieurs passages plutôt qu'une seule journée "
            "très longue."),
        "faq": [
            ("Intervenez-vous aussi dans les communes autour de Haguenau ?",
             "Oui : Schweighouse, Bischwiller, Kaltenhouse, Marienthal et communes voisines font partie de "
             "notre zone habituelle."),
            ("Combien de temps pour une maison complète ?",
             "Comptez généralement deux à trois jours selon le volume, les dépendances et le niveau de tri."),
        ],
    },
    {
        "slug": "molsheim", "nom": "Molsheim", "cp": "67120",
        "courte": "centre ancien, vignoble et patrimoine industriel",
        "h1": "Débarras à Molsheim (67120)",
        "title": "Débarras à Molsheim — devis gratuit, maison et caveau",
        "meta": "Débarras à Molsheim : maisons anciennes, caves, caveaux et dépendances viticoles. Tri respectueux et évacuation soignée. Devis gratuit.",
        "intro": (
            "Molsheim associe un centre ancien avec des maisons à cour intérieure, des caves parfois "
            "voûtées, un passé industriel lié à l'automobile et un environnement viticole. Les débarras y "
            "concernent souvent des maisons de famille avec beaucoup d'objets anciens : mobilier, outillage, "
            "bouteilles, archives. Le tri y prend une place particulière, avec des pièces qui méritent un "
            "regard avant décision."),
        "quartiers": ["Centre ancien", "Bugatti", "Quartier des Remparts", "Vignoble"],
        "communes_voisines": ["Dorlisheim", "Mutzig", "Ergersheim", "Altorf", "Rosheim", "Avolsheim"],
        "chantiers": [
            ("Maison ancienne avec cour", "Débarras complet et cave voûtée", "20 à 40 m³", "2 jours"),
            ("Caveau viticole", "Retrait de matériel et bouteilles", "10 à 20 m³", "1 jour"),
            ("Appartement, centre", "Succession et mise de côté d'objets anciens", "10 m³", "Demi-journée"),
        ],
        "note_locale": (
            "À Molsheim comme dans le vignoble, certains objets ont une valeur réelle (mobilier ancien, "
            "outillage, vins). Nous les identifions et les mettons de côté plutôt que de les évacuer : c'est "
            "vous qui décidez."),
        "faq": [
            ("Que faites-vous des bouteilles anciennes ?",
             "Elles sont mises de côté et photographiées pour vous. Aucune évacuation n'a lieu sans votre "
             "accord sur ce type d'objet."),
            ("Intervenez-vous dans les villages viticoles voisins ?",
             "Oui : Dorlisheim, Mutzig, Rosheim, Altorf, Ergersheim et communes voisines."),
        ],
    },
    {
        "slug": "obernai", "nom": "Obernai", "cp": "67210",
        "courte": "ville touristique et vigneronne",
        "h1": "Débarras à Obernai (67210)",
        "title": "Débarras à Obernai — devis gratuit, maisons et locations",
        "meta": "Débarras à Obernai : maisons vigneronnes, résidences secondaires et locations touristiques. Débarras complet, évacuation et nettoyage, devis gratuit.",
        "intro": (
            "Obernai est une ville touristique : maisons vigneronnes du centre médiéval, résidences "
            "secondaires, meublés de tourisme et commerces. Les débarras y ont souvent une contrainte de "
            "calendrier : il faut libérer le logement entre deux saisons locatives, avant une vente, ou "
            "après un changement d'exploitation. Les accès piétons du centre imposent une manutention "
            "organisée, souvent à la brouette jusqu'au point de chargement."),
        "quartiers": ["Centre médiéval", "Remparts", "Sainte-Odile", "Zone d'activité"],
        "communes_voisines": ["Barr", "Bernardswiller", "Ottrott", "Rosheim", "Bischoffsheim", "Goxwiller"],
        "chantiers": [
            ("Maison vigneronne, centre", "Débarras avant mise en vente", "20 à 40 m³", "2 jours"),
            ("Meublé de tourisme", "Renouvellement complet du mobilier", "10 à 20 m³", "1 jour"),
            ("Résidence secondaire", "Débarras et nettoyage de fin de saison", "5 à 10 m³", "Demi-journée"),
        ],
        "note_locale": (
            "Dans le centre d'Obernai, l'accès camion est limité : nous prévoyons un point de dépose et un "
            "cheminement court, ce qui évite de doubler la durée d'intervention."),
        "faq": [
            ("Intervenez-vous entre deux locations touristiques ?",
             "Oui, avec un créneau serré : nous pouvons intervenir sur une journée unique pour rendre le "
             "logement disponible le soir."),
            ("Les meubles en bon état peuvent-ils être donnés ?",
             "Oui, c'est souvent le cas pour du mobilier de meublé récent : nous l'orientons vers le don ou "
             "la recyclerie."),
        ],
    },
    {
        "slug": "selestat", "nom": "Sélestat", "cp": "67600",
        "courte": "centre ancien et quartiers en développement",
        "h1": "Débarras à Sélestat (67600)",
        "title": "Débarras à Sélestat — devis gratuit, appartements et maisons",
        "meta": "Débarras à Sélestat : appartements du centre ancien, maisons, caves et locaux. Tri, évacuation et nettoyage, devis gratuit et intervention planifiée.",
        "intro": (
            "Sélestat, entre Ill et vignoble, réunit un centre ancien avec des immeubles souvent datés, des "
            "quartiers résidentiels plus récents et des zones d'activité. Nous y intervenons surtout pour "
            "des appartements à vider dans le cadre d'une succession ou d'une restitution de bail, et pour "
            "des maisons avec cave à désencombrer. Les délais y sont généralement plus souples qu'à "
            "Strasbourg, ce qui permet de planifier confortablement."),
        "quartiers": ["Centre ancien", "Heyden", "Vignoble", "Zones d'activité"],
        "communes_voisines": ["Scherwiller", "Châtenois", "Kintzheim", "Ebersheim", "Muttersholtz", "Villé"],
        "chantiers": [
            ("Appartement, centre ancien", "Succession, mobilier et cave", "10 à 20 m³", "1 jour"),
            ("Maison avec cave et grenier", "Débarras complet avant location", "20 à 40 m³", "2 jours"),
            ("Local commercial", "Curage après changement d'activité", "20 à 40 m³", "1 jour"),
        ],
        "note_locale": (
            "Sur Sélestat et sa couronne (Scherwiller, Châtenois, Kintzheim), les interventions se "
            "planifient facilement : c'est utile pour les successions où plusieurs personnes doivent être "
            "disponibles le même jour."),
        "faq": [
            ("Intervenez-vous dans les villages autour de Sélestat ?",
             "Oui : Scherwiller, Châtenois, Kintzheim, Ebersheim, Muttersholtz, Villé et communes voisines."),
            ("Pouvez-vous nous laisser le temps de trier avant d'évacuer ?",
             "Oui. Nous pouvons intervenir en deux temps : un premier passage pour le tri et le repérage, un "
             "second pour l'évacuation."),
        ],
    },
]

VILLES_BY_SLUG = {v["slug"]: v for v in VILLES}
