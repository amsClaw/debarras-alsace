# -*- coding: utf-8 -*-
"""Rendu HTML du site — gabarits et composants (aucune dépendance externe)."""
import json

from data.site import (SITE, NAV, CTA, REASSURANCE, HERO_ARGUMENTS, ETAPES, VALORISATION,
                       VALORISATION_MESSAGE, POURQUOI_NOUS, ZONES_PRESENTATION, FAQ_GENERALE,
                       FAQ_ACCUEIL, REALISATIONS_EXEMPLES, AVIS_MESSAGE, CONTACT_INTRO)
from data.services import SERVICES, SERVICES_BY_SLUG, SERVICES_ACCUEIL
from data.villes import VILLES, VILLES_BY_SLUG
from data.situations import SITUATIONS, SITUATIONS_BY_SLUG
from data.articles import ARTICLES, ARTICLES_BY_SLUG

ICONES = {
    "maison": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M10 21v-6h4v6"/>',
    "immeuble": '<path d="M4 21V4h10v17"/><path d="M14 9h6v12h-6"/><path d="M7 8h4M7 12h4M7 16h4M17 13h1M17 17h1"/>',
    "cave": '<path d="M3 20h18"/><path d="M5 20V10h14v10"/><path d="M9 20v-6h6v6"/><path d="M8 10V7h8v3"/>',
    "grenier": '<path d="M3 10 12 4l9 6"/><path d="M5 10v10h14V10"/><path d="M9 20v-5h6v5"/><path d="M12 4v3"/>',
    "garage": '<path d="M3 20V9l9-5 9 5v11"/><path d="M6 20v-6h12v6"/><path d="M6 17h12"/>',
    "succession": '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/><path d="M9 12h6M9 16h6"/>',
    "coeur": '<path d="M12 20s-7-4.4-7-9.3A4.2 4.2 0 0 1 12 7.5a4.2 4.2 0 0 1 7 3.2C19 15.6 12 20 12 20z"/>',
    "main": '<path d="M6 20V11a2 2 0 1 1 4 0"/><path d="M10 11V6a2 2 0 1 1 4 0v5"/><path d="M14 11V8a2 2 0 1 1 4 0v8a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4v-1"/>',
    "camion": '<path d="M3 16V6h11v10"/><path d="M14 9h4l3 3v4h-7"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "bureau": '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/>',
    "propre": '<path d="M9 3h6l1 7H8z"/><path d="M7 10h10l1 11H6z"/><path d="M10 14h4"/>',
    "pelleteuse": '<path d="M3 20h12v-6H3z"/><path d="M15 14l4-7"/><path d="M17 5l4 3-3 4"/><circle cx="7" cy="20" r="2"/><circle cx="17" cy="20" r="2"/>',
    "marteau": '<path d="M14 3l7 7-3 3-7-7z"/><path d="M11 6 4 13v6h6l7-7"/>',
    "telephone": '<path d="M5 3h4l2 5-3 2a12 12 0 0 0 6 6l2-3 5 2v4a1 1 0 0 1-1 1A17 17 0 0 1 4 4a1 1 0 0 1 1-1z"/>',
    "whatsapp": '<path d="M12 3a9 9 0 0 0-7.7 13.6L3 21l4.6-1.2A9 9 0 1 0 12 3z"/><path d="M8.6 8.4c0 3.4 2.6 6 6 6 .6 0 1.3-.5 1.5-1.1l-1.6-.8-1 .9a4.3 4.3 0 0 1-1.9-1.9l.9-.9-.8-1.6c-.6.2-1.1.9-1.1 1.4z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "check": '<path d="m4 13 5 5L20 7"/>',
    "horloge": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "feuille": '<path d="M20 4c-9 0-15 4-15 11a5 5 0 0 0 5 5c7 0 10-6 10-16z"/><path d="M8 20c1-6 5-9 9-10"/>',
    "bouclier": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    "euro": '<circle cx="12" cy="12" r="9"/><path d="M15 9a4 4 0 0 0-6 0 5 5 0 0 0 0 6 4 4 0 0 0 6 0"/><path d="M8 11h5M8 13.5h5"/>',
    "carte": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "appareil": '<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>',
    "equipe": '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 6.5a3 3 0 0 1 0 5.9"/><path d="M17 20a6 6 0 0 0-2-4.5"/>',
    "etoile": '<path d="m12 4 2.4 5 5.6.8-4 3.9 1 5.5L12 16.6 7 19.2l1-5.5-4-3.9 5.6-.8z"/>',
    "recycle": '<path d="M7 19H5a2 2 0 0 1-1.7-3l1.6-2.6"/><path d="M10 5.5 12 3l2 2.5"/><path d="M14.6 19H19a2 2 0 0 0 1.7-3L19 13"/><path d="M9.5 9 6.8 13h5.4"/><path d="m14.5 15-2.7 4h5.4"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/>',
    "coche-cercle": '<circle cx="12" cy="12" r="9"/><path d="m8.5 12.5 2.5 2.5 4.5-5"/>',
    "fleche": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "croix": '<path d="M6 6l12 12M18 6 6 18"/>',
}


def ic(nom, classe=""):
    corps = ICONES.get(nom, ICONES["coche-cercle"])
    cl = ' class="%s"' % classe if classe else ""
    return ('<svg%s viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>'
            % (cl, corps))


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- contexte de page
class Ctx(object):
    """Contexte de rendu : profondeur du répertoire pour les liens relatifs + page active."""

    def __init__(self, profondeur=0, actif="/"):
        self.profondeur = profondeur
        self.actif = actif

    def l(self, chemin):
        p = "../" * self.profondeur
        return p + chemin.lstrip("/")

    def abs(self, chemin):
        return SITE["url_base"] + "/" + chemin.lstrip("/")


# ---------------------------------------------------------------- composants
def _liens_nav(ctx):
    # Menu d'en-tête volontairement court : entre 1180 px et 1400 px, tout doit tenir
    # (Avis clients / À propos / FAQ restent accessibles par le pied de page et le menu mobile).
    principal = ["/", "/services/", "/situations/", "/villes/", "/tarifs/", "/realisations/",
                 "/blog/", "/contact-devis/"]
    entrees = [(lib, url) for lib, url in NAV if url in principal]
    html = ['<ul>']
    for lib, url in entrees:
        court = {"Zones d'intervention": "Zones", "Contact & devis": "Contact"}.get(lib, lib)
        if lib == "Nos services":
            html.append('<li class="nav__bloc"><a href="%s">%s</a><div class="nav__sous">' % (ctx.l(url), esc(lib)))
            for s in SERVICES:
                html.append('<a href="%s">%s</a>' % (ctx.l("services/%s/" % s["slug"]), esc(s["nom"])))
            html.append("</div></li>")
        elif lib == "Zones d'intervention":
            html.append('<li class="nav__bloc"><a href="%s">%s</a><div class="nav__sous">' % (ctx.l(url), esc(court)))
            for v in VILLES:
                html.append('<a href="%s">%s</a>' % (ctx.l("villes/%s/" % v["slug"]), esc(v["nom"])))
            html.append("</div></li>")
        else:
            marque = ' aria-current="page"' if ctx.actif == url else ""
            html.append('<li><a href="%s"%s>%s</a></li>' % (ctx.l(url), marque, esc(court)))
    html.append("</ul>")
    return "".join(html)


def entete(ctx):
    liens = "".join('<a href="%s">%s</a>' % (ctx.l(u), esc(l)) for l, u in NAV)
    return """<a class="skip" href="#contenu">Aller au contenu</a>
<div class="bandeau-info">Devis gratuit et sans engagement — réponse sous 24 h ouvrées&nbsp;&middot;&nbsp;<a href="%s">%s</a>&nbsp;&middot;&nbsp;%s</div>
<header class="entete">
  <div class="wrap barre">
    <a class="marque" href="%s" aria-label="%s, accueil">
      <svg class="marque__logo" viewBox="0 0 48 48" fill="none" aria-hidden="true">
        <rect x="2" y="2" width="44" height="44" rx="12" fill="#14532d"/>
        <path d="M12 30l8-7 6 5 10-9" stroke="#8fd0a8" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M12 36h24" stroke="#e8622a" stroke-width="2.6" stroke-linecap="round"/>
      </svg>
      <span class="marque__txt"><span class="marque__nom">%s</span><span class="marque__base">%s</span></span>
    </a>
    <nav class="nav" aria-label="Navigation principale">%s</nav>
    <div class="entete__actions">
      <a class="entete__tel" href="tel:%s">%s<span>%s</span></a>
      <a class="btn btn--accent btn--sm" href="%s">Demander un devis</a>
      <button class="burger" type="button" data-menu-ouvrir aria-expanded="false" aria-controls="panneau" aria-label="Ouvrir le menu">%s</button>
    </div>
  </div>
</header>
<div class="panneau" id="panneau" data-ouvert="0" role="dialog" aria-label="Menu">
  <div class="panneau__tete">
    <strong>%s — %s</strong>
    <button class="panneau__fermer" type="button" data-menu-fermer aria-label="Fermer le menu">&times;</button>
  </div>
  <nav aria-label="Navigation mobile">%s</nav>
  <div class="panneau__cta">
    <a class="btn btn--accent" href="%s">%s</a>
    <a class="btn btn--vert" href="tel:%s">Appeler le %s</a>
    <a class="btn btn--clair" href="%s">WhatsApp</a>
  </div>
</div>""" % (
        ctx.l("contact-devis/"), CTA["devis"], esc(SITE["horaires"]),
        ctx.l(""), esc(SITE["nom"]), esc(SITE["nom"]), esc(SITE["baseline"]), _liens_nav(ctx),
        SITE["telephone_lien"], ic("telephone"), esc(SITE["telephone"]),
        ctx.l("contact-devis/"), ic("menu"),
        esc(SITE["nom"]), esc(SITE["baseline"]), liens,
        ctx.l("contact-devis/"), esc(CTA["devis"]), SITE["telephone_lien"], esc(SITE["telephone"]),
        SITE["whatsapp_lien"])


def pied(ctx):
    def colonne(titre, liens):
        return "<div><h3>%s</h3><ul>%s</ul></div>" % (titre, "".join(
            '<li><a href="%s">%s</a></li>' % (ctx.l(u), esc(l)) for l, u in liens))
    services = [(s["nom"], "services/%s/" % s["slug"]) for s in SERVICES]
    zones = [(v["nom"], "villes/%s/" % v["slug"]) for v in VILLES]
    entreprise = [("À propos", "a-propos/"), ("Réalisations", "realisations/"), ("Avis clients", "avis-clients/"),
                  ("Tarifs", "tarifs/"), ("FAQ", "faq/"), ("Blog", "blog/"), ("Contact & devis", "contact-devis/")]
    return """<footer class="pied">
  <div class="wrap">
    <div class="pied__colonnes">
      %s
      %s
      %s
      <div>
        <h3>Contact</h3>
        <ul>
          <li><a href="tel:%s">Téléphone : %s</a></li>
          <li><a href="tel:%s">Mobile : %s</a></li>
          <li><a href="%s">WhatsApp</a></li>
          <li><a href="mailto:%s">%s</a></li>
        </ul>
        <p style="font-size:.88rem">%s</p>
        <p style="font-size:.88rem">Zone : %s</p>
      </div>
    </div>
    <div class="pied__bas">
      <div>&copy; <span data-annee>2026</span> %s — %s. %s</div>
      <div class="pied__legal">
        <a href="%s">Mentions légales</a>
        <a href="%s">Politique de confidentialité</a>
        <a href="%s">Zones d'intervention</a>
      </div>
    </div>
  </div>
</footer>
<div class="barre-mobile" role="navigation" aria-label="Actions rapides">
  <a href="tel:%s">%s<span>Appeler</span></a>
  <a href="%s">%s<span>WhatsApp</span></a>
  <a href="%s" data-fort="1"%s>%s<span>Devis</span></a>
</div>""" % (
        colonne("Services", services), colonne("Zones", zones), colonne("Entreprise", entreprise),
        SITE["telephone_lien"], esc(SITE["telephone"]),
        SITE["mobile_lien"], esc(SITE["mobile"]),
        SITE["whatsapp_lien"], SITE["email"], esc(SITE["email"]),
        esc(SITE["horaires"]), esc(SITE["zone_texte"]),
        esc(SITE["nom"]), esc(SITE["baseline"]), esc(SITE["raison_sociale"]),
        ctx.l("mentions-legales/"), ctx.l("politique-confidentialite/"), ctx.l("villes/"),
        SITE["telephone_lien"], ic("telephone"), SITE["whatsapp_lien"], ic("whatsapp"),
        ctx.l("contact-devis/"),
        ' aria-current="page"' if ctx.actif == "/contact-devis/" else "", ic("doc"))


def fil_ariane(ctx, elements):
    morceaux = []
    for i, (lib, url) in enumerate(elements):
        if url and i < len(elements) - 1:
            morceaux.append('<a href="%s">%s</a>' % (ctx.l(url), esc(lib)))
        else:
            morceaux.append(esc(lib))
    return '<nav class="wrap fil" aria-label="Fil d\'Ariane">%s</nav>' % "<span>&rsaquo;</span>".join(morceaux)


def jsonld(bloc):
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(bloc, ensure_ascii=False, separators=(",", ":")))


def jsonld_localbusiness():
    return jsonld({
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "name": SITE["nom"], "description": SITE["promesse"],
        "url": SITE["url_base"] + "/", "telephone": SITE["telephone"],
        "email": SITE["email"],
        "address": {"@type": "PostalAddress", "addressLocality": "Strasbourg",
                    "postalCode": "67000", "addressRegion": "Grand Est", "addressCountry": "FR"},
        "areaServed": [v["nom"] for v in VILLES] + ["Bas-Rhin", "Alsace"],
        "openingHours": SITE["horaires"],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["nom"]}}
                       for s in SERVICES],
    })


def jsonld_faq(items):
    return jsonld({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items],
    })


def jsonld_ariane(ctx, elements):
    return jsonld({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": lib,
                             "item": ctx.abs(url) if url else ctx.abs(ctx.actif)}
                            for i, (lib, url) in enumerate(elements)],
    })


def page(ctx, titre, meta, corps, jsonld_sup=None, classe=""):
    return """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="theme-color" content="#14532d">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s/assets/og.svg">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="%sassets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="%sassets/style.css">
%s
</head>
<body class="%s">
%s
<main id="contenu">
%s
</main>
%s
<script>window.DEBARRAS_ZONES = %s;</script>
<script src="%sassets/app.js" defer></script>
</body>
</html>""" % (esc(titre), esc(meta), ctx.abs(ctx.actif), esc(SITE["nom"]), esc(titre), esc(meta),
              ctx.abs(ctx.actif), SITE["url_base"], ctx.l(""), ctx.l(""),
              jsonld_sup or "", classe, entete(ctx), corps, pied(ctx),
              json.dumps(json_localisations()), ctx.l(""))


def json_localisations():
    from data.site import CODES_POSTAUX
    return {k: v for k, v in CODES_POSTAUX.items() if k.isdigit()}


def bloc_entete(titre, surtitre=None, texte=None):
    h = ['<div class="entete-section">']
    if surtitre:
        h.append('<span class="surtitre">%s</span>' % esc(surtitre))
    h.append("<h2>%s</h2>" % esc(titre))
    if texte:
        h.append("<p>%s</p>" % esc(texte))
    h.append("</div>")
    return "".join(h)


def cartes_services(ctx, slugs, colonnes=4, avec_accroche=True):
    html = ['<div class="cartes cartes--%d">' % colonnes]
    for slug in slugs:
        s = SERVICES_BY_SLUG[slug]
        accroche = s.get("accroche") or (s["intro"].split(". ")[0] + ".")
        html.append("""<article class="carte">
  <div class="carte__icone">%s</div>
  <h3><a href="%s">%s</a></h3>
  <p>%s</p>
  <div class="carte__pied"><a class="lien-fleche" href="%s">%s &rsaquo;</a></div>
</article>""" % (ic(s["icone"]), ctx.l("services/%s/" % slug), esc(s["nom"]),
                 esc(accroche if avec_accroche else s["intro"]), ctx.l("services/%s/" % slug),
                 esc(CTA["service"])))
    html.append("</div>")
    return "".join(html)


def cartes_situations(ctx):
    html = ['<div class="cartes cartes--3">']
    for s in SITUATIONS:
        html.append("""<article class="carte">
  <h3><a href="%s">%s</a></h3>
  <p>%s</p>
  <div class="carte__pied"><a class="lien-fleche" href="%s">Voir la situation &rsaquo;</a></div>
</article>""" % (ctx.l("situations/%s/" % s["slug"]), esc(s["nom"]), esc(s["intro"].split(". ")[0] + "."),
                 ctx.l("situations/%s/" % s["slug"])))
    html.append("</div>")
    return "".join(html)


def bloc_process():
    html = ['<div class="etapes-process">']
    for i, (titre, texte) in enumerate(ETAPES, 1):
        html.append('<article class="etape-carte"><div class="etape-carte__num">%d</div><h3>%s</h3><p>%s</p></article>'
                    % (i, esc(titre), esc(texte)))
    html.append("</div>")
    return "".join(html)


def bloc_faq(items, surtitre=None, titre=None):
    html = []
    if titre:
        html.append(bloc_entete(titre, surtitre))
    html.append('<div class="faq">')
    for q, a in items:
        html.append('<details><summary>%s</summary><div class="faq__corps"><p>%s</p></div></details>'
                    % (esc(q), esc(a)))
    html.append("</div>")
    return "".join(html)


def bloc_cta_final(ctx, titre="Besoin de vider un logement ?",
                   texte="Envoyez quelques photos et recevez une estimation. Nous vous répondons sous 24 h ouvrées."):
    return """<section class="section section--blanc"><div class="wrap"><div class="cta-final">
  <h2>%s</h2>
  <p>%s</p>
  <div class="cta-final__boutons">
    <a class="btn btn--accent" href="%s">%s</a>
    <a class="btn btn--contour" href="tel:%s">Appeler le %s</a>
    <a class="btn btn--contour" href="%s">%s</a>
  </div>
</div></div></section>""" % (esc(titre), esc(texte), ctx.l("contact-devis/"), esc(CTA["devis"]),
                            SITE["telephone_lien"], esc(SITE["telephone"]),
                            SITE["whatsapp_lien"], esc(CTA["whatsapp"]))


def bloc_reassurance():
    html = ['<div class="reassurance">']
    for titre, texte in REASSURANCE:
        html.append('<div class="reassurance__item">%s<div><strong>%s</strong><span>%s</span></div></div>'
                    % (ic("coche-cercle"), esc(titre), esc(texte)))
    html.append("</div>")
    return "".join(html)


def bloc_zone(ctx):
    return """<div class="zone" data-zone>
  <label for="cp-zone"><strong>Où se trouve votre débarras ?</strong> <span class="indice">(code postal)</span></label>
  <div class="ligne-champs">
    <input type="text" id="cp-zone" inputmode="numeric" pattern="[0-9]{5}" maxlength="5" placeholder="Exemple : 67000" aria-describedby="zone-aide">
    <button class="btn btn--vert" type="button">%s</button>
  </div>
  <p class="aide" id="zone-aide">Nous vérifions si votre commune fait partie de notre zone d'intervention habituelle.</p>
  <div class="zone__resultat" role="status" aria-live="polite"></div>
</div>""" % esc(CTA["zone"])


def form_express(ctx):
    types = "".join('<option>%s</option>' % esc(s["nom"]) for s in SERVICES)
    return """<form class="hero__formulaire" data-formulaire="express" data-email="%s" novalidate>
  <h2>Estimation rapide</h2>
  <p class="aide">Trois informations suffisent pour être rappelé. Vous pourrez tout préciser ensuite.</p>
  <div class="bloc-etape" data-actif="1">
    <div class="champ">
      <label for="ex-type">Quel type de débarras ?</label>
      <select id="ex-type" name="type" data-etiquette="Type de débarras" required>%s</select>
      <p class="erreur">Indiquez le type de débarras.</p>
    </div>
    <div class="ligne-champs">
      <div class="champ">
        <label for="ex-cp">Code postal</label>
        <input type="text" id="ex-cp" name="code_postal" data-etiquette="Code postal" inputmode="numeric" maxlength="5" required>
        <p class="erreur">Code postal à 5 chiffres.</p>
      </div>
      <div class="champ">
        <label for="ex-tel">Téléphone</label>
        <input type="tel" id="ex-tel" name="telephone" data-etiquette="Téléphone" required>
        <p class="erreur">Numéro de téléphone à vérifier.</p>
      </div>
    </div>
    <div class="champ">
      <label for="ex-photos">Ajoutez quelques photos <span class="indice">(facultatif, 5 maximum)</span></label>
      <label class="fichier" for="ex-photos">
        <span class="fichier__bouton">%s Choisir des photos</span>
        <span class="fichier__nom" data-fichier-nom>Aucune photo sélectionnée</span>
      </label>
      <input class="sr" type="file" id="ex-photos" name="photos" accept="image/*" multiple>
      <div class="miniatures" data-photos-liste></div>
    </div>
    <button class="btn btn--accent btn--large" type="button" data-suivant>Recevoir mon estimation</button>
    <div class="form-nav" style="display:none"><a class="btn btn--accent" href="#" data-envoi>Envoyer par e-mail</a></div>
    <p class="aide" style="margin-top:10px">Devis gratuit et sans engagement. Vos coordonnées servent uniquement à vous répondre.</p>
  </div>
  <div class="bloc-etape" data-actif="0" style="display:none">
    <div class="recap" data-recap></div>
    <div class="form-nav">
      <a class="btn btn--accent" href="#" data-envoi>Envoyer ma demande par e-mail</a>
      <button class="btn btn--clair" type="button" data-copier>Copier le récapitulatif</button>
      <a class="btn btn--clair" href="%s">WhatsApp</a>
    </div>
    <p class="aide mt-2">Cette première version prépare votre demande et l'envoie depuis votre messagerie
    (les photos restent sur votre appareil). L'envoi direct depuis le site arrive avec le branchement serveur.</p>
  </div>
</form>""" % (SITE["email"], types, ic("appareil"), SITE["whatsapp_lien"])


def form_complet(ctx):
    def choix(nom, etiquette, options, requis=True, aide=None):
        champs = "".join(
            '<div class="champ"><label for="%s-%d">%s</label><input type="radio" id="%s-%d" name="%s" value="%s" data-libelle="%s"%s style="width:20px;height:20px">%s</div>'
            % (nom, i, esc(lib), nom, i, nom, esc(lib), esc(lib), " required" if requis and i == 0 else "",
               '<p class="erreur">Choisissez une option.</p>')
            for i, lib in enumerate(options))
        return champs

    types = [s["nom"] for s in SERVICES] + ["Autre situation"]
    return """<form class="aside-carte" data-formulaire="complet" data-email="%s" novalidate>
  <div class="etapes" aria-hidden="true">
    %s
  </div>
  <div class="bloc-etape" data-actif="1">
    <h2>1. Votre besoin</h2>
    <div class="champ">
      <label for="f-type">Type de débarras *</label>
      <select id="f-type" name="type_debarras" data-etiquette="Type de débarras" required>
        <option value="">Choisissez…</option>%s
      </select>
      <p class="erreur">Indiquez le type de débarras.</p>
    </div>
    <p class="aide">Situation particulière ? Précisez-le dans le message de la dernière étape.</p>
    <div class="form-nav"><button class="btn btn--accent" type="button" data-suivant>Continuer</button></div>
  </div>
  <div class="bloc-etape" data-actif="0">
    <h2>2. Localisation</h2>
    <div class="champ">
      <label for="f-adresse">Adresse ou rue <span class="indice">(facultatif à ce stade)</span></label>
      <input type="text" id="f-adresse" name="adresse" data-etiquette="Adresse">
    </div>
    <div class="ligne-champs">
      <div class="champ">
        <label for="f-cp">Code postal *</label>
        <input type="text" id="f-cp" name="code_postal" data-etiquette="Code postal" inputmode="numeric" maxlength="5" required>
        <p class="erreur">Code postal à 5 chiffres.</p>
      </div>
      <div class="champ">
        <label for="f-ville">Ville *</label>
        <input type="text" id="f-ville" name="ville" data-etiquette="Ville" required>
        <p class="erreur">Indiquez la ville.</p>
      </div>
    </div>
    <div class="form-nav">
      <button class="btn btn--clair" type="button" data-retour>Retour</button>
      <button class="btn btn--accent" type="button" data-suivant>Continuer</button>
    </div>
  </div>
  <div class="bloc-etape" data-actif="0">
    <h2>3. Volume estimé</h2>
    <div class="champ">
      <label for="f-volume">Quel volume approximatif ? *</label>
      <select id="f-volume" name="volume" data-etiquette="Volume estimé" required>
        <option value="">Choisissez…</option>
        <option>Petite quantité (quelques objets)</option>
        <option>5 à 10 m³ (une pièce ou une cave)</option>
        <option>10 à 20 m³ (un appartement)</option>
        <option>20 à 40 m³ (une maison partielle)</option>
        <option>Plus de 40 m³ (maison complète ou local)</option>
        <option>Je ne sais pas</option>
      </select>
      <p class="erreur">Indiquez une estimation, même approximative.</p>
    </div>
    <div class="simulation" data-simulateur>
      <p class="mb-0"><strong>Ou choisissez visuellement :</strong></p>
      <div class="volumes mt-2">
        %s
      </div>
      <div class="resultat-simulation" role="status" aria-live="polite"></div>
    </div>
    <div class="form-nav">
      <button class="btn btn--clair" type="button" data-retour>Retour</button>
      <button class="btn btn--accent" type="button" data-suivant>Continuer</button>
    </div>
  </div>
  <div class="bloc-etape" data-actif="0">
    <h2>4. Accès</h2>
    <div class="champ">
      <label for="f-acces">Où se situe l'accès ? *</label>
      <select id="f-acces" name="acces" data-etiquette="Accès" required>
        <option value="">Choisissez…</option>
        <option>Rez-de-chaussée</option>
        <option>Étage avec ascenseur</option>
        <option>Étage sans ascenseur</option>
        <option>Accès difficile (ruelle, cour, escalier étroit)</option>
        <option>Sous-sol ou cave</option>
      </select>
      <p class="erreur">Indiquez la configuration d'accès.</p>
    </div>
    <div class="champ">
      <label for="f-distance">Distance entre le camion et l'entrée <span class="indice">(facultatif)</span></label>
      <input type="text" id="f-distance" name="distance_camion" data-etiquette="Distance camion / entrée" placeholder="Exemple : accès direct, 20 m, escalier extérieur…">
    </div>
    <div class="form-nav">
      <button class="btn btn--clair" type="button" data-retour>Retour</button>
      <button class="btn btn--accent" type="button" data-suivant>Continuer</button>
    </div>
  </div>
  <div class="bloc-etape" data-actif="0">
    <h2>5. Délai</h2>
    <div class="champ">
      <label for="f-delai">Quand souhaitez-vous intervenir ? *</label>
      <select id="f-delai" name="delai" data-etiquette="Délai souhaité" required>
        <option value="">Choisissez…</option>
        <option>Urgent (24 à 72 h)</option>
        <option>Cette semaine</option>
        <option>Ce mois-ci</option>
        <option>Je suis flexible</option>
      </select>
      <p class="erreur">Indiquez un délai, même indicatif.</p>
    </div>
    <div class="form-nav">
      <button class="btn btn--clair" type="button" data-retour>Retour</button>
      <button class="btn btn--accent" type="button" data-suivant>Continuer</button>
    </div>
  </div>
  <div class="bloc-etape" data-actif="0">
    <h2>6. Photos</h2>
    <div class="champ">
      <label for="f-photos">Ajoutez vos photos <span class="indice">(jusqu'à 5, depuis votre téléphone)</span></label>
      <label class="fichier" for="f-photos">
        <span class="fichier__bouton">%s Choisir des photos</span>
        <span class="fichier__nom" data-fichier-nom>Aucune photo sélectionnée</span>
      </label>
      <input class="sr" type="file" id="f-photos" name="photos" accept="image/*" multiple>
      <p class="aide" data-photos-avert>Les photos prises au téléphone sont les bienvenues : elles accélèrent l'estimation.</p>
      <div class="miniatures" data-photos-liste></div>
    </div>
    <div class="form-nav">
      <button class="btn btn--clair" type="button" data-retour>Retour</button>
      <button class="btn btn--accent" type="button" data-suivant>Continuer</button>
    </div>
  </div>
  <div class="bloc-etape" data-actif="0">
    <h2>7. Vos coordonnées</h2>
    <div class="ligne-champs">
      <div class="champ">
        <label for="f-nom">Prénom et nom *</label>
        <input type="text" id="f-nom" name="nom" data-etiquette="Nom" required>
        <p class="erreur">Indiquez votre nom.</p>
      </div>
      <div class="champ">
        <label for="f-tel">Téléphone *</label>
        <input type="tel" id="f-tel" name="telephone" data-etiquette="Téléphone" required>
        <p class="erreur">Numéro de téléphone à vérifier.</p>
      </div>
    </div>
    <div class="champ">
      <label for="f-email">E-mail <span class="indice">(facultatif)</span></label>
      <input type="email" id="f-email" name="email" data-etiquette="E-mail">
      <p class="erreur">Adresse e-mail à vérifier.</p>
    </div>
    <div class="champ">
      <label for="f-message">Message <span class="indice">(facultatif)</span></label>
      <textarea id="f-message" name="message" data-etiquette="Message" placeholder="Étage, contraintes d'accès, objets à conserver, délai imposé…"></textarea>
    </div>
    <label class="case"><input type="checkbox" name="rgpd" value="oui" data-etiquette="Accord de contact"> J'accepte d'être recontacté au sujet de ma demande. Mes données ne servent qu'à traiter celle-ci.</label>
    <div class="form-nav">
      <button class="btn btn--clair" type="button" data-retour>Retour</button>
      <button class="btn btn--accent" type="button" data-suivant>Voir le récapitulatif</button>
    </div>
  </div>
  <div class="bloc-etape" data-actif="0">
    <h2>Votre demande</h2>
    <p class="aide">Vérifiez les informations, puis envoyez la demande. Si les photos ne sont pas jointes
    automatiquement, indiquez-le dans le message ou envoyez-les par WhatsApp.</p>
    <div class="recap" data-recap></div>
    <div class="form-nav">
      <button class="btn btn--clair" type="button" data-retour>Modifier</button>
      <a class="btn btn--accent" href="#" data-envoi>Envoyer ma demande</a>
      <button class="btn btn--clair" type="button" data-copier>Copier</button>
    </div>
  </div>
</form>""" % (SITE["email"],
              "".join('<span class="etapes__pt"><span class="etapes__num">%d</span>%s</span>'
                      % (i + 1, t) for i, t in enumerate(["Besoin", "Lieu", "Volume", "Accès", "Délai", "Photos", "Contact", "Envoi"])),
              "".join("<option>%s</option>" % esc(t) for t in types),
              _boutons_volume(), ic("appareil"))


def _boutons_volume():
    options = [
        ("1/8 de camion", "environ 2 à 3", 12),
        ("1/4 de camion", "environ 4 à 6", 25),
        ("1/2 camion", "environ 8 à 12", 50),
        ("3/4 de camion", "environ 12 à 16", 75),
        ("Camion complet", "environ 18 à 22", 100),
    ]
    html = []
    for libelle, m3, pct in options:
        html.append("""<button class="volume" type="button" aria-pressed="false" data-libelle="%s"
        data-volume-m3="%s"><span class="volume__jauge"><span><i style="width:%d%%"></i></span></span>
        <span class="volume__txt"><strong>%s</strong><span>%s m³</span></span></button>"""
                    % (esc(libelle), esc(m3), pct, esc(libelle), esc(m3)))
    return "".join(html)
