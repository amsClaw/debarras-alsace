#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke test : chaque URL du sitemap doit répondre 200, avoir un title unique et un H1."""
import re
import sys
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8100"
sitemap = urllib.request.urlopen(BASE + "/sitemap.xml", timeout=20).read().decode()
urls = re.findall(r"<loc>(.*?)</loc>", sitemap)
print("URLs dans le sitemap :", len(urls))

titres, problemes = {}, []
for u in urls:
    chemin = u.replace("https://amsclaw.github.io/debarras-alsace", "") or "/"
    try:
        with urllib.request.urlopen(BASE + chemin, timeout=20) as r:
            code, html = r.status, r.read().decode()
    except Exception as e:
        problemes.append("%s -> ERREUR %s" % (chemin, e))
        continue
    t = re.search(r"(?is)<title>(.*?)</title>", html)
    h1 = re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", html)
    titre = re.sub(r"<[^>]+>", "", t.group(1)).strip() if t else "(sans titre)"
    titres.setdefault(titre, []).append(chemin)
    if code != 200:
        problemes.append("%s -> HTTP %s" % (chemin, code))
    if len(h1) != 1:
        problemes.append("%s -> %d H1" % (chemin, len(h1)))
    print("  %s  %-58s %s" % (code, chemin, titre[:64]))

for t, ou in titres.items():
    if len(ou) > 1:
        problemes.append("TITLE identique : %s -> %s" % (t[:50], ou))

# ressources statiques
for res in ["/assets/style.css", "/assets/app.js", "/assets/favicon.svg", "/assets/og.svg", "/robots.txt"]:
    try:
        with urllib.request.urlopen(BASE + res, timeout=20) as r:
            print("  %s  %s" % (r.status, res))
    except Exception as e:
        problemes.append("ressource %s -> %s" % (res, e))

# page 404 (fichier dédié)
try:
    with urllib.request.urlopen(BASE + "/404.html", timeout=20) as r:
        print("  %s  /404.html" % r.status)
except Exception as e:
    problemes.append("404.html -> %s" % e)

print()
if problemes:
    print("PROBLEMES (%d) :" % len(problemes))
    for p in problemes:
        print("  -", p)
    sys.exit(1)
print("OK — toutes les pages répondent 200, titles uniques, un seul H1 par page.")
