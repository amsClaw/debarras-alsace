#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère la V2 « épurée » du site Débarras Alsace dans le dossier v2/ (publié sur /v2/).

Principes : une seule page d'atterrissage + les pages légales, mobile d'abord, zéro dépendance,
aucune donnée inventée (pas de prix, pas de note, pas d'avis).

Usage : python3 tools/build_v2.py
"""
import os
import shutil
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))
from data.site import SITE  # source de vérité des coordonnées (déjà marquée A_COMPLETER)

SORTIE = os.path.join(RACINE, "v2")
PHOTOS_SRC = os.path.join(RACINE, "src", "assets", "photos")
CSS_SRC = os.path.join(RACINE, "v2_src", "style.css")
JS_SRC = os.path.join(RACINE, "v2_src", "app.js")

PHOTOS = ["hero.jpg", "service-maison.jpg", "service-cave.jpg", "service-pro.jpg",
          "service-diogene.jpg", "valorisation.jpg"]

NOM = SITE["nom"]
BASE = SITE["baseline"]
TEL_AFFICHE = SITE["telephone"]
TEL_LIEN = SITE["telephone_lien"]
WHATSAPP = SITE["whatsapp_lien"]
MAIL = SITE["email"]
URL = SITE["url_base"] + "/v2/"

ICONE_TEL = ('<svg width="19" height="19" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
             '<path d="M6.6 3h2.6l1.5 3.7-1.8 1.3a12 12 0 0 0 5.1 5.1l1.3-1.8L19 12.8v2.6c0 1-.8 1.8-1.8 1.8A14.8 14.8 0 0 1 3.8 4.8C3.8 3.9 4.6 3 5.5 3z" '
             'fill="currentColor"/></svg>')
ICONE_WA = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            '<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm0 2a8 8 0 1 1-4.2 14.8l-.4-.2-3 .8.8-2.9-.2-.4A8 8 0 0 1 12 4z" fill="currentColor"/>'
            '<path d="M8.5 7.6c.3 0 .5.1.7.5l.7 1.3c.1.3.1.5-.1.7l-.5.6c-.2.2-.2.4 0 .7.5.8 1.2 1.5 2.1 2 .3.2.5.2.7 0l.6-.6c.2-.2.4-.2.7-.1l1.4.7c.3.1.4.3.4.6v.9c0 .4-.3.7-.7.7-.5 0-1.5-.2-3-1.2a9 9 0 0 1-3.6-4c-.3-.7-.4-1.4-.4-1.8 0-.4.3-.7.7-.7z" fill="currentColor"/></svg>')
ICONE_COCHE = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
               '<path d="M20 6.5 9.5 17 4 11.5" stroke="#8fd0a8" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICONE_MAIL = ('<svg width="19" height="19" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
              '<path d="M3 6h18v12H3z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>'
              '<path d="m3.5 7 8.5 6 8.5-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>')
ICONE_LIEU = ('<svg width="19" height="19" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
              '<path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11z" stroke="currentColor" stroke-width="1.8"/>'
              '<circle cx="12" cy="10" r="2.6" stroke="currentColor" stroke-width="1.8"/></svg>')
LOGO = ('<svg width="34" height="34" viewBox="0 0 48 48" fill="none" aria-hidden="true">'
        '<rect width="48" height="48" rx="11" fill="#14532d"/>'
        '<path d="M10 24 24 12l14 12" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M14 23v14h20V23" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M24 33c-5 0-7.4-3-7.4-7.5 4.5 0 7.4 3 7.4 7.5z" fill="#8fd0a8"/>'
        '<path d="M24 33c4.5-1.5 6.6-4.5 6.6-8.8-4.1.2-6.6 3.3-6.6 8.8z" fill="#4fae76"/>'
        '</svg>')

PRESTATIONS = [
    ("Maison & appartement", "service-maison.jpg",
     "Logement complet ou quelques pièces : meubles, vaisselle, textiles, électroménager, bibelots.",
     ["Succession, vente ou déménagement", "Étages sans ascenseur : on gère"]),
    ("Cave, grenier & garage", "service-cave.jpg",
     "Encombrants, ferraille, cartons, vieux outils et objets accumulés depuis des années.",
     ["Accès difficiles et petits volumes", "Évacuation en déchetterie professionnelle"]),
    ("Bureaux & locaux", "service-pro.jpg",
     "Mobilier, archives, matériel informatique : fin de bail, déménagement ou remise à neuf.",
     ["Devis pour les professionnels", "Intervention hors horaires d'ouverture"]),
    ("Logements très encombrés", "service-diogene.jpg",
     "Situations complexes, accumulation importante : intervention discrète, sans jugement.",
     ["Équipe habituée à ces situations", "Coordination possible avec vos proches"]),
]

ETAPES = [
    ("Vous nous décrivez", "Un appel, ou quelques photos envoyées par WhatsApp. Deux minutes suffisent pour se faire une idée juste."),
    ("Vous recevez un prix ferme", "Sous 24 h, gratuitement et sans engagement. Le montant annoncé ne bouge pas le jour de l'intervention."),
    ("On s'occupe de tout", "Évacuation, tri, valorisation des objets et nettoyage. Vous n'avez rien à porter ni à transporter."),
]

PRIX = [
    ("Débarras indemnisé", "La valeur des objets récupérés dépasse le coût du travail : la prestation ne vous coûte rien, et une somme peut même vous être reversée."),
    ("Débarras gratuit", "La valeur des objets couvre exactement la prestation : vous ne payez rien."),
    ("Débarras payant", "Quand il n'y a rien à valoriser, le prix dépend du volume, de l'accessibilité et des frais de déchetterie. Le montant est fixé avant l'intervention."),
]

COMMUNES = ["Strasbourg", "Schiltigheim", "Illkirch", "Ostwald", "Lingolsheim", "Bischheim", "Haguenau", "Molsheim"]

TYPES = ["Maison ou appartement", "Cave, grenier ou garage", "Bureaux ou locaux professionnels",
         "Logement très encombré", "Autre situation"]


def entete():
    return """<header class="entete">
  <div class="wrap entete__in">
    <a class="marque" href="index.html" aria-label="%s, accueil">
      %s
      <span><span class="marque__nom">%s</span><span class="marque__base">%s</span></span>
    </a>
    <nav class="menu" aria-label="Sections">
      <a href="#prestations">Prestations</a>
      <a href="#fonctionnement">Déroulé</a>
      <a href="#prix">Prix</a>
      <a href="#zone">Zone</a>
      <a href="#devis">Devis</a>
    </nav>
    <a class="appel-icone" href="tel:%s" aria-label="Appeler le %s">%s<span class="appel-texte">%s</span></a>
  </div>
</header>""" % (NOM, LOGO, NOM, BASE, TEL_LIEN, TEL_AFFICHE, ICONE_TEL, TEL_AFFICHE)


def barre_mobile():
    return """<div class="barre" role="navigation" aria-label="Actions rapides">
  <a class="btn--vert" href="tel:%s">%s Appeler</a>
  <a class="btn--plein" href="%s" target="_blank" rel="noopener">%s WhatsApp</a>
</div>""" % (TEL_LIEN, ICONE_TEL, WHATSAPP, ICONE_WA)


def pied():
    return """<footer class="pied">
  <div class="wrap">
    <p class="pied__titre">%s — %s</p>
    <div class="pied__infos">
      <p>%s</p>
      <p><a href="tel:%s">%s</a> · <a href="mailto:%s">%s</a></p>
      <p>%s</p>
    </div>
    <p class="pied__legal">
      <a href="mentions-legales.html">Mentions légales</a>
      <a href="confidentialite.html">Confidentialité</a>
      <a href="../">Voir l'ancienne version du site</a>
      <span>© <span id="annee">2026</span> %s</span>
    </p>
  </div>
</footer>""" % (NOM, BASE, SITE["zone_texte"], TEL_LIEN, TEL_AFFICHE, MAIL, MAIL, SITE["horaires"], NOM)


def page(titre, description, corps, page_nom="index.html"):
    return """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="%s%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="website">
<link rel="stylesheet" href="assets/style.css?v=2a">
<!-- Coordonnées de démonstration : téléphone et e-mail à remplacer par les données réelles du client
     avant toute mise en production (voir docs/QUESTIONS_OUVERTES.md). -->
</head>
<body>
%s
%s
%s
<script src="assets/app.js?v=2a" defer></script>
</body>
</html>
""" % (titre, description, URL, page_nom, titre, description, entete(), corps, barre_mobile())


def accueil():
    puces = "".join("<li>%s<span>%s</span></li>" % (ICONE_COCHE, t) for t in [
        "Devis gratuit sous 24 h, sans engagement",
        "Déplacement et estimation offerts",
        "Tri et valorisation : un maximum d'objets sauvés de la benne",
    ])
    prestations = "".join("""<article class="carte rev">
      <img src="assets/photos/%s" alt="%s" loading="lazy" decoding="async">
      <div class="carte__txt">
        <h3>%s</h3>
        <p>%s</p>
        <ul>%s</ul>
      </div>
    </article>""" % (img, titre, titre, texte, "".join("<li>%s</li>" % i for i in items))
        for titre, img, texte, items in PRESTATIONS)
    etapes = "".join("""<article class="etape rev">
      <h3>%s</h3>
      <p>%s</p>
    </article>""" % (t, d) for t, d in ETAPES)
    prix = "".join("""<article class="prix__cas rev">
      <h3>%s</h3>
      <p>%s</p>
    </article>""" % (t, d) for t, d in PRIX)
    communes = "".join("<span>%s</span>" % c for c in COMMUNES)
    types = "".join("<option>%s</option>" % t for t in TYPES)

    corps = """<main>
  <section class="heros">
    <div class="wrap heros__in">
      <h1>Votre débarras à Strasbourg et en Alsace, <em>simple et sans stress</em>.</h1>
      <p class="heros__sous">Vous montrez ce qui doit partir. On évacue, on trie, on valorise et on laisse
      la pièce propre. Prix ferme annoncé avant l'intervention.</p>
      <ul class="puces">%s</ul>
      <div class="heros__actions">
        <a class="btn btn--plein" href="#devis">Demander un devis gratuit</a>
        <a class="btn btn--ligne" href="tel:%s">%s %s</a>
      </div>
      <p class="heros__note">Intervention à Strasbourg, dans l'Eurométropole et dans tout le Bas-Rhin.</p>
    </div>
  </section>

  <section class="section" id="prestations">
    <div class="wrap">
      <h2 class="rev">Ce que nous débarrassons</h2>
      <p class="rev" style="margin-top:10px; color:var(--gris)">Du studio au local professionnel, avec ou sans accès facile.</p>
      <div class="grille-prestations">%s</div>
    </div>
  </section>

  <section class="section section--beige" id="fonctionnement">
    <div class="wrap">
      <h2 class="rev">Comment ça se passe</h2>
      <p class="rev" style="margin-top:10px; color:var(--gris)">Trois étapes, aucune surprise.</p>
      <div class="etapes">%s</div>
      <div class="encart rev" style="margin-top:24px">
        <strong>Aucune avance à verser.</strong>
        <p>Vous payez une fois l'intervention terminée, quand la pièce est vidée et propre.</p>
      </div>
    </div>
  </section>

  <section class="section" id="prix">
    <div class="wrap">
      <h2 class="rev">Comment le prix est fixé</h2>
      <p class="rev" style="margin-top:10px; color:var(--gris)">Le débarras n'est pas toujours payant : cela dépend de ce qu'il y a à récupérer.</p>
      <div class="prix">%s</div>
      <div class="encart rev" style="margin-top:24px">
        <strong>Le calcul, en clair.</strong>
        <p>Volume à évacuer + accessibilité (étage, distance de stationnement) + part d'objets valorisables.
        Vous recevez un montant ferme avant l'intervention, jamais une estimation qui gonfle sur place.</p>
      </div>
    </div>
  </section>

  <section class="section section--vertcl" id="zone">
    <div class="wrap">
      <h2 class="rev">Où nous intervenons</h2>
      <p class="rev" style="margin-top:10px; color:var(--gris)">%s</p>
      <div class="communes rev">%s</div>
      <p class="zone__note rev">Votre commune n'apparaît pas ?
        <a href="tel:%s">Appelez-nous</a> : la réponse prend trente secondes.</p>
    </div>
  </section>

  <section class="section" id="devis">
    <div class="wrap">
      <h2 class="rev">Demander un devis gratuit</h2>
      <p class="rev" style="margin-top:10px; color:var(--gris)">Remplissez trois champs : le message part
      déjà rédigé sur WhatsApp (ou par e-mail). Ajoutez deux ou trois photos de la pièce, c'est ce qui
      nous permet d'annoncer un prix juste.</p>
      <div class="contact">
        <form id="form-express" class="rev" novalidate>
          <div class="champ">
            <label for="f-commune">Votre commune ou code postal</label>
            <input id="f-commune" name="commune" type="text" inputmode="text" autocomplete="address-level2" placeholder="Ex. : Strasbourg 67000">
          </div>
          <div class="champ">
            <label for="f-type">Type de prestation</label>
            <select id="f-type" name="type">%s</select>
          </div>
          <div class="champ">
            <label for="f-tel">Votre téléphone</label>
            <input id="f-tel" name="telephone" type="tel" inputmode="tel" autocomplete="tel" placeholder="Pour vous rappeler">
          </div>
          <div class="champ">
            <label for="f-precisions">Précisions <span style="font-weight:400; color:var(--gris)">(facultatif)</span></label>
            <input id="f-precisions" name="precisions" type="text" placeholder="Ex. : cave au 2e sous-sol, meubles et cartons">
          </div>
          <div class="contact__alt">
            <a class="btn btn--plein btn--bloc" id="lien-wa" href="%s" target="_blank" rel="noopener">%s Envoyer sur WhatsApp</a>
            <a class="btn btn--ligne btn--bloc" id="lien-mail" href="mailto:%s">%s Envoyer par e-mail</a>
          </div>
          <p class="aide" style="margin-top:12px">Rien n'est envoyé automatiquement depuis cette page :
            votre messagerie s'ouvre avec le message prêt, à vous de le confirmer (ou de le modifier).</p>
          <details style="margin-top:14px">
            <summary style="cursor:pointer; font-weight:650; color:var(--vert2); font-size:.94rem">Voir le message qui sera envoyé</summary>
            <p class="aide" id="apercu" aria-live="polite" style="margin-top:8px; white-space:pre-line"></p>
          </details>
        </form>
        <div class="rev">
          <div class="contact__direct">
            <a class="lien-direct" href="tel:%s">%s<span><strong>%s</strong><span>Appel direct, du lundi au samedi</span></span></a>
            <a class="lien-direct" href="%s" target="_blank" rel="noopener">%s<span><strong>WhatsApp</strong><span>Envoyez vos photos en 10 secondes</span></span></a>
            <a class="lien-direct" href="mailto:%s">%s<span><strong>%s</strong><span>Réponse sous 24 h ouvrées</span></span></a>
          </div>
          <div class="encart" style="margin-top:16px">
            <strong>%s</strong>
            <p>%s</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>

%s""" % (puces, TEL_LIEN, ICONE_TEL, TEL_AFFICHE, prestations, etapes, prix,
         SITE["zone_texte"], communes, TEL_LIEN, types, WHATSAPP, ICONE_WA, MAIL, ICONE_MAIL,
         TEL_LIEN, ICONE_TEL, TEL_AFFICHE, WHATSAPP, ICONE_WA, MAIL, ICONE_MAIL, MAIL,
         SITE["horaires"], "Un doute sur ce qu'il faut garder ? Nous trions devant vous et nous mettons de côté ce qui a de la valeur : bijoux, papiers importants, objets de famille.", pied())

    jsonld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"HomeAndGardenBusiness",
 "name":"%s","description":"Débarras de maisons, appartements, caves et locaux à Strasbourg et en Alsace.",
 "telephone":"%s","email":"%s","areaServed":["Strasbourg","Eurométropole de Strasbourg","Bas-Rhin","Alsace"],
 "address":{"@type":"PostalAddress","addressLocality":"Strasbourg","postalCode":"67000","addressCountry":"FR"},
 "url":"%s"}
</script>""" % (NOM, SITE["telephone_lien"], MAIL, URL)
    return page("%s — débarras simple et sans stress à Strasbourg" % NOM,
                "Débarras de maisons, appartements, caves et locaux à Strasbourg et en Alsace. Devis gratuit "
                "sous 24 h, prix ferme, tri et valorisation inclus.",
                corps + jsonld, "index.html")


def page_texte(titre, paragraphes, nom):
    corps = """<main class="section">
  <div class="wrap" style="max-width:760px">
    <h1>%s</h1>
    %s
    <p style="margin-top:24px"><a href="index.html">&larr; Retour à l'accueil</a></p>
  </div>
</main>
%s""" % (titre, "".join('<p class="rev" style="margin-top:14px; color:var(--gris)">%s</p>' % p
                        for p in paragraphes), pied())
    return page("%s — %s" % (titre, NOM), paragraphes[0][:150], corps, nom)


def construire():
    if os.path.exists(SORTIE):
        shutil.rmtree(SORTIE)
    os.makedirs(os.path.join(SORTIE, "assets", "photos"))

    shutil.copy(CSS_SRC, os.path.join(SORTIE, "assets", "style.css"))
    shutil.copy(JS_SRC, os.path.join(SORTIE, "assets", "app.js"))
    for p in PHOTOS:
        shutil.copy(os.path.join(PHOTOS_SRC, p), os.path.join(SORTIE, "assets", "photos", p))

    ecrire("index.html", accueil())
    ecrire("mentions-legales.html", page_texte("Mentions légales", [
        "Éditeur du site : %s%s, %s." % (SITE["raison_sociale"], ", SIRET %s" % SITE["siret"] if SITE["siret"] != "A_COMPLETER" else "", SITE["adresse"]),
        "Contact : %s — %s." % (TEL_AFFICHE, MAIL),
        "Directeur de la publication : A_COMPLETER (représentant légal de l'entreprise).",
        "Hébergement : GitHub Pages — GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.",
        "Propriété intellectuelle : l'ensemble des contenus de ce site (textes, visuels, code) est protégé. "
        "Toute reproduction sans autorisation écrite est interdite.",
        "Visuels : images d'illustration générées pour la présentation du site ; elles ne représentent pas "
        "des chantiers réels de l'entreprise et seront remplacées par des photos de chantiers.",
    ], "mentions-legales.html"))
    ecrire("confidentialite.html", page_texte("Politique de confidentialité", [
        "Ce site ne dépose aucun cookie de mesure d'audience ni de publicité, et ne collecte aucune donnée "
        "à votre insu.",
        "Le formulaire de devis ne transmet rien à nos serveurs : il prépare un message que vous envoyez "
        "vous-même depuis WhatsApp ou votre logiciel de messagerie. Les informations que vous y saisissez "
        "(commune, type de prestation, téléphone, précisions) ne nous parviennent que par ce message.",
        "Les données transmises (coordonnées, description du besoin, photos) servent uniquement à établir le "
        "devis et à organiser l'intervention. Elles ne sont ni revendues ni transmises à des tiers, et sont "
        "conservées uniquement le temps nécessaire au suivi commercial.",
        "Conformément au RGPD, vous pouvez demander l'accès, la rectification ou la suppression de vos "
        "données en écrivant à %s." % MAIL,
        "Responsable du traitement : A_COMPLETER (représentant légal de l'entreprise).",
    ], "confidentialite.html"))
    ecrire("404.html", page_texte("Page introuvable", [
        "La page que vous cherchez n'existe pas (ou plus).",
        "Le plus simple : revenez à l'accueil, ou appelez-nous directement au %s." % TEL_AFFICHE,
    ], "404.html"))
    ecrire("sitemap.xml", """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>%s</loc></url>
</urlset>""" % URL)
    return SORTIE


def ecrire(nom, contenu):
    with open(os.path.join(SORTIE, nom), "w", encoding="utf-8") as f:
        f.write(contenu)
    print("  %-26s %6d octets" % (nom, len(contenu.encode("utf-8"))))


if __name__ == "__main__":
    dossier = construire()
    total = sum(os.path.getsize(os.path.join(d, f))
                for d, _, fs in os.walk(dossier) for f in fs)
    print("\nV2 construite dans %s (%.0f Ko au total)" % (dossier, total / 1024.0))
