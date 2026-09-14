#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Générateur du site Débarras Alsace.

Usage : python3 tools/build.py
Sortie : site statique à la racine du dépôt (GitHub Pages -> /), hors docs/, src/, tools/.
Aucune dépendance externe (stdlib uniquement).
"""
import hashlib
import os
import re
import shutil
import sys
from datetime import date

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))

from data.site import SITE, FAQ_GENERALE  # noqa: E402
from data.services import SERVICES  # noqa: E402
from data.villes import VILLES  # noqa: E402
from data.situations import SITUATIONS  # noqa: E402
from data.articles import ARTICLES  # noqa: E402
from illustrations import CATALOGUE  # noqa: E402
import render  # noqa: E402
import pages  # noqa: E402

DOSSIERS_SORTIE = ["services", "villes", "situations", "blog", "tarifs", "realisations",
                   "avis-clients", "a-propos", "faq", "contact-devis", "mentions-legales",
                   "politique-confidentialite", "assets", "photos"]
FICHIERS_SORTIE = ["index.html", "404.html", "sitemap.xml", "robots.txt"]

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
<rect width="48" height="48" rx="11" fill="#14532d"/>
<path d="M11 31l8-7 6 5 10-9" fill="none" stroke="#8fd0a8" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M11 37h26" stroke="#e8622a" stroke-width="3.4" stroke-linecap="round"/>
</svg>"""

OG = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#123f24"/><stop offset="1" stop-color="#1c6b3f"/></linearGradient></defs>
<rect width="1200" height="630" fill="url(#g)"/>
<rect x="72" y="72" width="76" height="76" rx="18" fill="#ffffff" opacity="0.14"/>
<path d="M92 118l14-12 10 8 18-16" fill="none" stroke="#8fd0a8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<text x="180" y="128" font-family="Helvetica,Arial,sans-serif" font-size="40" font-weight="700" fill="#ffffff">DEBARRAS ALSACE</text>
<text x="72" y="300" font-family="Helvetica,Arial,sans-serif" font-size="62" font-weight="700" fill="#ffffff">Vous nous montrez ce qui doit partir.</text>
<text x="72" y="380" font-family="Helvetica,Arial,sans-serif" font-size="62" font-weight="700" fill="#ffd9c6">On s'occupe du reste.</text>
<text x="72" y="470" font-family="Helvetica,Arial,sans-serif" font-size="34" fill="#cfe3d6">Debarras Strasbourg &amp; Alsace - devis gratuit sous 24 h</text>
<rect x="72" y="520" width="360" height="66" rx="33" fill="#e8622a"/>
<text x="112" y="564" font-family="Helvetica,Arial,sans-serif" font-size="30" font-weight="700" fill="#ffffff">Demander un devis</text>
</svg>"""


def ecrire(chemin_relatif, contenu):
    chemin = os.path.join(RACINE, chemin_relatif)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


def nettoyer():
    for d in DOSSIERS_SORTIE:
        shutil.rmtree(os.path.join(RACINE, d), ignore_errors=True)
    for f in FICHIERS_SORTIE:
        p = os.path.join(RACINE, f)
        if os.path.exists(p):
            os.remove(p)


def empreinte_assets():
    h = hashlib.sha1()
    for f in ("src/assets/style.css", "src/assets/maquette.css", "src/assets/app.js"):
        with open(os.path.join(RACINE, f), "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()[:8]


def construire():
    nettoyer()
    render.set_version(empreinte_assets())
    urls = []
    pages_ecrites = []

    def poser(chemin_url, contenu, ctx_profondeur):
        rel = ("index.html" if chemin_url == "/" else chemin_url.strip("/") + "/index.html")
        ecrire(rel, contenu)
        pages_ecrites.append(rel)
        urls.append(chemin_url)

    # accueil
    ctx = render.Ctx(0, "/")
    poser("/", pages.accueil(ctx), 0)

    # hubs
    poser("/services/", pages.page_services(render.Ctx(1, "/services/")), 1)
    poser("/villes/", pages.page_villes(render.Ctx(1, "/villes/")), 1)
    poser("/situations/", pages.page_situations(render.Ctx(1, "/situations/")), 1)
    poser("/tarifs/", pages.page_tarifs(render.Ctx(1, "/tarifs/")), 1)
    poser("/realisations/", pages.page_realisations(render.Ctx(1, "/realisations/")), 1)
    poser("/avis-clients/", pages.page_avis(render.Ctx(1, "/avis-clients/")), 1)
    poser("/a-propos/", pages.page_a_propos(render.Ctx(1, "/a-propos/")), 1)
    poser("/faq/", pages.page_faq(render.Ctx(1, "/faq/")), 1)
    poser("/blog/", pages.page_blog(render.Ctx(1, "/blog/")), 1)
    poser("/contact-devis/", pages.page_contact(render.Ctx(1, "/contact-devis/")), 1)
    poser("/mentions-legales/", pages.page_mentions(render.Ctx(1, "/mentions-legales/")), 1)
    poser("/politique-confidentialite/", pages.page_confidentialite(render.Ctx(1, "/politique-confidentialite/")), 1)

    # pages filles (profondeur 2)
    for s in SERVICES:
        u = "/services/%s/" % s["slug"]
        poser(u, pages.page_service(render.Ctx(2, u), s), 2)
    for v in VILLES:
        u = "/villes/%s/" % v["slug"]
        poser(u, pages.page_ville(render.Ctx(2, u), v), 2)
    for s in SITUATIONS:
        u = "/situations/%s/" % s["slug"]
        poser(u, pages.page_situation(render.Ctx(2, u), s), 2)
    for a in ARTICLES:
        u = "/blog/%s/" % a["slug"]
        poser(u, pages.page_article(render.Ctx(2, u), a), 2)

    # 404 (à la racine, liens relatifs au plus court)
    ecrire("404.html", pages.page_404(render.Ctx(0, "/404")))

    # assets
    os.makedirs(os.path.join(RACINE, "assets"), exist_ok=True)
    shutil.copy(os.path.join(RACINE, "src/assets/style.css"), os.path.join(RACINE, "assets/style.css"))
    shutil.copy(os.path.join(RACINE, "src/assets/maquette.css"), os.path.join(RACINE, "assets/maquette.css"))
    shutil.copy(os.path.join(RACINE, "src/assets/app.js"), os.path.join(RACINE, "assets/app.js"))
    ecrire("assets/favicon.svg", FAVICON)
    ecrire("assets/og.svg", OG)

    # photos découpées dans la maquette client (source-client/photos -> assets/photos)
    dossier_photos = os.path.join(RACINE, "src/assets/photos")
    if os.path.isdir(dossier_photos):
        cible = os.path.join(RACINE, "assets/photos")
        os.makedirs(cible, exist_ok=True)
        for nom in os.listdir(dossier_photos):
            if nom.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                shutil.copy(os.path.join(dossier_photos, nom), os.path.join(cible, nom))

    # illustrations vectorielles générées (visuels de démonstration, cf. docs/FRONT_SPEC.md)
    for nom, svg in CATALOGUE.items():
        ecrire("assets/illus/%s.svg" % nom, svg)

    # sitemap + robots
    aujourdhui = date.today().isoformat()
    entrees = "".join(
        "  <url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq>"
        "<priority>%s</priority></url>\n"
        % (SITE["url_base"], u, aujourdhui, "1.0" if u == "/" else ("0.8" if u.count("/") <= 2 else "0.6"))
        for u in urls)
    ecrire("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % entrees)
    ecrire("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE["url_base"])

    return pages_ecrites, urls


def controler(pages_ecrites, urls):
    """Contrôles automatiques : promesses interdites, titres/meta/H1 uniques, liens internes."""
    interdits = [
        (r"d[ée]barras\s+100\s*%\s*gratuit", "promesse de gratuité"),
        (r"garantie?\s+de\s+gratuit[ée]", "promesse de gratuité"),
        (r"rachat\s+garanti", "promesse de rachat"),
        (r"intervention\s+en\s+24\s*h\s+garantie", "délai garanti"),
    ]
    titres, metas, h1s = {}, {}, {}
    problemes = []
    liens_internes = set()
    for rel in pages_ecrites:
        p = os.path.join(RACINE, rel)
        html = open(p, encoding="utf-8").read()
        for motif, nom in interdits:
            if re.search(motif, html, re.I):
                problemes.append("PROMESSE INTERDITE (%s) dans %s" % (nom, rel))
        t = re.search(r"(?is)<title>(.*?)</title>", html)
        d = re.search(r'(?is)<meta name="description" content="(.*?)"', html)
        h1 = re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", html)
        cle = rel
        if t:
            titres.setdefault(t.group(1).strip(), []).append(cle)
        else:
            problemes.append("TITLE MANQUANT : %s" % rel)
        if d:
            metas.setdefault(d.group(1).strip(), []).append(cle)
        else:
            problemes.append("META DESCRIPTION MANQUANTE : %s" % rel)
        if len(h1) != 1:
            problemes.append("H1 : %d trouvé(s) dans %s" % (len(h1), rel))
        else:
            h1s.setdefault(re.sub(r"<[^>]+>", "", h1[0]).strip(), []).append(cle)
        for lien in re.findall(r'(?is)href="([^"#?]+)"', html):
            if lien.startswith(("http", "mailto:", "tel:")):
                continue
            cible = os.path.normpath(os.path.join(os.path.dirname(p), lien))
            liens_internes.add(cible)
        for src in re.findall(r'(?is)src="([^"#?]+)"', html):
            if src.startswith(("http", "data:")):
                continue
            cible = os.path.normpath(os.path.join(os.path.dirname(p), src))
            liens_internes.add(cible)
    for libelle, table in (("TITLE", titres), ("META DESCRIPTION", metas), ("H1", h1s)):
        for valeur, ou in table.items():
            if len(ou) > 1:
                problemes.append("%s DUPLIQUÉ (%s) : %s" % (libelle, valeur[:60], ou))
    for cible in sorted(liens_internes):
        if not os.path.exists(cible):
            problemes.append("LIEN MORT : %s" % cible.replace(RACINE + "/", ""))

    # garde-fou : un asset vidé ou tronqué casse tout le style du site sans erreur visible
    for rel in ("assets/style.css", "assets/maquette.css", "assets/app.js",
                "src/assets/style.css", "src/assets/maquette.css", "src/assets/app.js"):
        p = os.path.join(RACINE, rel)
        if os.path.exists(p) and os.path.getsize(p) < 2000:
            problemes.append("ASSET SUSPECT (tronqué ?) : %s = %d octets" % (rel, os.path.getsize(p)))
    return problemes


if __name__ == "__main__":
    ecrites, urls = construire()
    print("Pages générées : %d" % len(ecrites))
    for rel in ecrites:
        print("   %s" % rel)
    print("URLs dans le sitemap : %d" % len(urls))
    problemes = controler(ecrites, urls)
    if problemes:
        print("\n⚠️  %d problème(s) :" % len(problemes))
        for p in problemes:
            print("   - %s" % p)
        sys.exit(1)
    print("\n✅ Contrôles automatiques : titres/meta/H1 uniques, liens internes valides, aucune promesse interdite.")
