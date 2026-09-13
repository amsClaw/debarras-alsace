# -*- coding: utf-8 -*-
"""Illustrations vectorielles du site — style plat, palette de la charte.

Toutes les scènes sont dessinées ici (aucune image externe, aucune banque d'images) :
elles servent de visuels de démonstration en attendant les photos réelles de l'entreprise.
Le générateur écrit un fichier SVG par illustration dans assets/illus/.
"""

# --- palette ---
VERT = "#14532d"
VERT2 = "#1c6b3f"
VERT_CLAIR = "#8fd0a8"
VERT_PALE = "#e8f2ea"
ORANGE = "#e8622a"
ANTHRACITE = "#1f2937"
GRIS = "#6b7280"

MUR_AVANT = "#efeadf"
MUR_APRES = "#f6f4ee"
SOL_AVANT = "#ded5c3"
SOL_APRES = "#d8e0d6"
OMBRE = "rgba(31,41,55,.10)"

# couleurs d'objets « encombrés »
C_BOITE = "#b58e63"
C_BOITE2 = "#a37b52"
C_MEUBLE = "#8b8478"
C_MEUBLE2 = "#7a7367"
C_TISSU = "#9b8f83"
C_VIEUX = "#a89a86"
C_SOMBRE = "#6f6a61"

VITRE_AVANT = "#cbd5dc"
VITRE_APRES = "#cfe8d8"


def _svg(w, h, corps):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
            'width="%d" height="%d">%s</svg>' % (w, h, w, h, corps))


def _rect(x, y, w, h, fill, rx=0, opacite=None):
    o = ' opacity="%s"' % opacite if opacite else ""
    r = ' rx="%s"' % rx if rx else ""
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"%s%s/>' % (x, y, w, h, fill, r, o)


def _path(d, fill="none", stroke=None, sw=2, opacite=None, linejoin="round"):
    return ('<path d="%s" fill="%s"%s stroke-width="%s" stroke-linejoin="%s"%s/>'
            % (d, fill, ' stroke="%s"' % stroke if stroke else "", sw, linejoin,
               ' opacity="%s"' % opacite if opacite else ""))


def _circle(cx, cy, r, fill, stroke=None, sw=2, opacite=None):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s"%s%s/>'
            % (cx, cy, r, fill, ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else "",
               ' opacity="%s"' % opacite if opacite else ""))


def _ombre(x, y, w, rx=10):
    return _rect(x, y, w, 12, ANTHRACITE, rx=rx, opacite="0.08")


# --- primitives d'objets ---
def _carton(x, y, w=74, h=60, couleur=C_BOITE, rabat=True):
    s = [_ombre(x, y + h - 2, w)]
    s.append(_rect(x, y, w, h, couleur, rx=3))
    s.append(_rect(x, y, w, 9, couleur, rx=3, opacite="0.75"))
    if rabat:
        s.append(_path("M%s %s L%s %s L%s %s Z" % (x, y + 6, x + w / 2, y - 8, x + w, y + 6),
                       fill=couleur))
    s.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.4" opacity="0.35"/>'
             % (x + 6, y + h / 2, x + w - 6, y + h / 2, ANTHRACITE))
    return "".join(s)


def _etagere(x, y, w=150, h=190):
    s = [_ombre(x, y + h - 2, w)]
    s.append(_rect(x, y, w, h, C_MEUBLE, rx=3))
    for i in range(1, 4):
        s.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="3" opacity="0.5"/>'
                 % (x + 4, y + h * i / 4, x + w - 4, y + h * i / 4, ANTHRACITE))
    for i, (bx, by, bw) in enumerate([(6, 12, 30), (46, 8, 34), (94, 14, 42), (16, 60, 46),
                                      (76, 56, 60)]):
        s.append(_rect(x + bx, y + by, bw, 34, C_BOITE if i % 2 else C_VIEUX, rx=2))
    return "".join(s)


def _fauteuil(x, y, couleur=C_TISSU):
    s = [_ombre(x, y + 52, 108)]
    s.append(_rect(x + 6, y + 10, 96, 40, couleur, rx=10))
    s.append(_rect(x, y + 28, 14, 34, couleur, rx=7))
    s.append(_rect(x + 94, y + 28, 14, 34, couleur, rx=7))
    s.append(_rect(x + 12, y, 84, 26, couleur, rx=9))
    s.append(_rect(x + 18, y + 50, 8, 10, C_SOMBRE, rx=2))
    s.append(_rect(x + 82, y + 50, 8, 10, C_SOMBRE, rx=2))
    return "".join(s)


def _canape(x, y, couleur=C_MEUBLE):
    s = [_ombre(x, y + 56, 190)]
    s.append(_rect(x, y + 16, 190, 44, couleur, rx=12))
    s.append(_rect(x + 4, y, 182, 30, couleur, rx=10))
    s.append(_rect(x + 10, y + 18, 80, 34, C_TISSU, rx=8, opacite="0.85"))
    s.append(_rect(x + 98, y + 18, 80, 34, C_TISSU, rx=8, opacite="0.85"))
    s.append(_rect(x + 8, y + 56, 10, 10, C_SOMBRE, rx=2))
    s.append(_rect(x + 172, y + 56, 10, 10, C_SOMBRE, rx=2))
    return "".join(s)


def _etabli(x, y, w=170):
    s = [_ombre(x, y + 62, w)]
    s.append(_rect(x, y, w, 12, C_MEUBLE2, rx=3))
    s.append(_rect(x + 8, y + 12, 10, 50, C_MEUBLE2))
    s.append(_rect(x + w - 18, y + 12, 10, 50, C_MEUBLE2))
    s.append(_rect(x + 24, y + 16, 34, 30, C_VIEUX, rx=2))
    s.append(_rect(x + 62, y + 22, 44, 24, C_BOITE, rx=2))
    s.append(_rect(x + 112, y + 14, 26, 34, C_SOMBRE, rx=3))
    return "".join(s)


def _pneu(x, y, r=34):
    return (_circle(x, y, r, "#3f3f46") + _circle(x, y, r * 0.45, MUR_AVANT))


def _velo(x, y):
    s = [_circle(x, y, 26, "none", ANTHRACITE, 4), _circle(x + 92, y, 26, "none", ANTHRACITE, 4)]
    s.append(_path("M%s %s L%s %s L%s %s M%s %s L%s %s" % (x, y, x + 46, y - 44, x + 92, y,
                                                          x + 46, y - 44, x + 60, y), stroke=C_SOMBRE, sw=4))
    s.append(_path("M%s %s l-14 -20" % (x + 46, y - 44), stroke=C_SOMBRE, sw=4))
    return "".join(s)


def _bureau(x, y, w=180):
    s = [_ombre(x, y + 58, w)]
    s.append(_rect(x, y, w, 12, C_MEUBLE, rx=3))
    s.append(_rect(x + 6, y + 12, 12, 46, C_MEUBLE2))
    s.append(_rect(x + w - 20, y + 12, 12, 46, C_MEUBLE2))
    s.append(_rect(x + 86, y + 12, 84, 46, C_MEUBLE2, rx=3))
    s.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1.6" opacity="0.5"/>'
             % (x + 90, y + 34, x + 166, y + 34, MUR_AVANT))
    s.append(_rect(x + 26, y - 34, 50, 34, C_SOMBRE, rx=3))
    s.append(_rect(x + 32, y - 28, 38, 22, "#93a5ad", rx=2))
    s.append(_rect(x + 34, y + 4, 26, 8, C_VIEUX, rx=2))
    return "".join(s)


def _chaise(x, y):
    s = [_ombre(x, y + 44, 44)]
    s.append(_rect(x + 4, y, 36, 26, C_MEUBLE, rx=4))
    s.append(_rect(x, y + 26, 44, 8, C_MEUBLE, rx=3))
    s.append(_rect(x + 6, y + 34, 6, 24, C_MEUBLE2))
    s.append(_rect(x + 32, y + 34, 6, 24, C_MEUBLE2))
    return "".join(s)


def _plante(baseline, echelle=1.0, cx=360):
    """Plante posée au sol : `baseline` = ordonnée du contact avec le sol."""
    e = echelle
    pot_w, pot_h = 44 * e, 44 * e
    top = baseline - pot_h
    s = [_ombre(cx - pot_w / 2 - 5, baseline - 7, pot_w + 10)]
    s.append(_path("M%.0f %.0f L%.0f %.0f L%.0f %.0f L%.0f %.0f Z"
                   % (cx - pot_w / 2, top, cx + pot_w / 2, top, cx + pot_w / 2 - 5 * e, baseline,
                      cx - pot_w / 2 + 5 * e, baseline), fill="#b0744c"))
    s.append(_rect(cx - pot_w / 2 - 4, top - 9 * e, pot_w + 8, 13 * e, "#c08457", rx=4))
    for dx, dy in ((-30, -72), (0, -92), (30, -76), (-15, -84), (16, -88)):
        s.append(_path("M%.0f %.0f Q%.0f %.0f %.0f %.0f"
                       % (cx, top - 8 * e, cx + dx * e * 0.5, top + dy * e * 0.55,
                          cx + dx * e, top + dy * e), stroke=VERT2, sw=5.5 * e))
        s.append(_circle(cx + dx * e, top + dy * e, 7 * e, VERT if dy < -86 else VERT2))
    return "".join(s)


def _etincelles(x, y, couleur=VERT_CLAIR):
    s = []
    for dx, dy, r in ((0, 0, 3), (22, -14, 2), (-18, -8, 2), (12, 18, 2)):
        s.append(_circle(x + dx, y + dy, r, couleur))
    return "".join(s)


# --- décors de fond selon le type de local ---
def _fenetre(x, y, w, h, vitre, montants="#ffffff"):
    s = [_rect(x - 8, y - 8, w + 16, h + 16, montants, rx=4),
         _rect(x, y, w, h, vitre, rx=2),
         _rect(x + w / 2 - 4, y, 9, h, montants),
         _rect(x, y + h / 2 - 4, w, 9, montants)]
    return "".join(s)


def _porte_garage():
    s = [_rect(506, 130, 264, 300, "#cfc9bd", rx=6)]
    for i in range(4):
        s.append(_rect(516, 142 + i * 72, 244, 62, "#ded9cf", rx=4))
        s.append('<line x1="516" y1="%d" x2="760" y2="%d" stroke="%s" stroke-width="2" opacity="0.35"/>'
                 % (142 + i * 72, 142 + i * 72, ANTHRACITE))
    s.append(_rect(738, 300, 22, 8, "#8b8478", rx=3))
    s.append(_rect(0, 420, 800, 10, ANTHRACITE, opacite="0.10"))
    return "".join(s)


def _ampoule(cx=400):
    s = [_path("M%d 0 L%d 96" % (cx, cx), stroke=ANTHRACITE, sw=3)]
    s.append(_circle(cx, 108, 16, "#f6e7a8"))
    s.append(_rect(cx - 7, 120, 14, 12, "#9a958a", rx=3))
    return "".join(s)


def _mur_briques():
    lignes = []
    for i in range(1, 9):
        y = i * 48
        lignes.append('<line x1="0" y1="%d" x2="800" y2="%d" stroke="%s" stroke-width="2" opacity="0.16"/>'
                      % (y, y, ANTHRACITE))
        decalage = 0 if i % 2 else 60
        for j in range(8):
            x = decalage + j * 120
            lignes.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" opacity="0.16"/>'
                          % (x, y - 48, x, y, ANTHRACITE))
    return "".join(lignes)


def _balai(x, y):
    """Balai appuyé : `x, y` = haut du manche, la tête touche le sol (y + 168)."""
    s = [_ombre(x + 8, y + 160, 66)]
    s.append(_path("M%d %d L%d %d" % (x, y, x + 30, y + 168), stroke="#b0744c", sw=8))
    s.append(_path("M%d %d L%d %d L%d %d Z" % (x + 26, y + 158, x + 56, y + 176, x + 4, y + 176),
                   fill="#d9c9a3"))
    s.append(_rect(x - 4, y - 6, 12, 10, "#8b8478", rx=3))
    return "".join(s)


def _scene(kind, etat):
    """Pièce vue de face : décor adapté au type de local, contenu selon avant/après."""
    avant = etat == "avant"
    murs = {"appartement": (MUR_AVANT, MUR_APRES), "maison": (MUR_AVANT, MUR_APRES),
            "cave": ("#ded6c6", "#e8e4da"), "grenier": ("#e6dfd0", "#f0ede6"),
            "garage": ("#dcd8d0", "#e9e7e2"), "pro": ("#eae7e0", "#f3f1ec")}
    sols = {"appartement": (SOL_AVANT, SOL_APRES), "maison": (SOL_AVANT, SOL_APRES),
            "cave": ("#cfc6b4", "#dcd9cd"), "grenier": ("#d8cfbc", "#e2ded3"),
            "garage": ("#cfccc6", "#deddd9"), "pro": ("#d9d5cc", "#e4e2dc")}
    mur = murs[kind][0 if avant else 1]
    sol = sols[kind][0 if avant else 1]
    s = [_rect(0, 0, 800, 600, mur), _rect(0, 430, 800, 170, sol)]
    s.append(_rect(0, 420, 800, 10, ANTHRACITE, opacite="0.10"))

    # décor
    if kind in ("appartement", "maison", "pro"):
        s.append(_fenetre(548, 96, 186, 168, VITRE_AVANT if avant else VITRE_APRES))
        if not avant:
            s.append(_path("M556 256 L726 256 L636 430 L470 430 Z", fill="#fdf6e3", opacite="0.5"))
    elif kind == "cave":
        s.append(_mur_briques())
        s.append(_ampoule(400))
    elif kind == "grenier":
        s.append(_path("M0 150 L400 40 L800 150", fill="none", stroke="#b8b0a0", sw=12))
        s.append(_path("M400 40 L400 150", stroke="#b8b0a0", sw=10))
        s.append(_circle(400, 200, 52, VITRE_AVANT if avant else VITRE_APRES))
        s.append(_circle(400, 200, 52, "none", "#b8b0a0", 10))
    elif kind == "garage":
        s.append(_porte_garage())

    # contenu
    if kind == "appartement":
        if avant:
            s.append(_etagere(66, 200))
            s.append(_carton(250, 380, 82, 50))
            s.append(_carton(330, 396, 66, 34, C_BOITE2))
            s.append(_carton(268, 330, 58, 50, C_VIEUX))
            s.append(_fauteuil(420, 350))
            s.append(_carton(690, 372, 74, 58, C_VIEUX))
            s.append(_rect(120, 520, 120, 10, C_TISSU, rx=5))
        else:
            s.append(_plante(508, 1.7, cx=250))
            s.append(_etincelles(430, 300))
            s.append(_etincelles(620, 340))
    elif kind == "maison":
        if avant:
            s.append(_canape(90, 340))
            s.append(_carton(300, 372, 84, 58))
            s.append(_carton(392, 392, 60, 38, C_BOITE2))
            s.append(_carton(320, 310, 56, 56, C_VIEUX))
            s.append(_etagere(520, 214, 140, 182))
        else:
            s.append(_plante(508, 1.85, cx=240))
            s.append(_etincelles(470, 320))
    elif kind == "cave":
        if avant:
            s.append(_etagere(70, 210, 168, 200))
            s.append(_carton(280, 386, 80, 44, C_BOITE2))
            s.append(_carton(272, 336, 66, 50, C_VIEUX))
            s.append(_velo(430, 404))
            s.append(_carton(660, 372, 76, 58))
        else:
            s.append(_etincelles(320, 330))
            s.append(_balai(96, 262))
    elif kind == "grenier":
        if avant:
            s.append(_carton(110, 366, 86, 64, C_VIEUX))
            s.append(_carton(206, 388, 64, 42, C_BOITE2))
            s.append(_carton(150, 300, 62, 60, C_BOITE))
            s.append(_etagere(300, 220, 140, 180))
            s.append(_chaise(500, 380))
            s.append(_carton(620, 380, 70, 50, C_SOMBRE))
        else:
            s.append(_etincelles(360, 320))
            s.append(_balai(676, 262))
    elif kind == "garage":
        if avant:
            s.append(_pneu(150, 396))
            s.append(_pneu(220, 416, 22))
            s.append(_etabli(300, 360, 180))
            s.append(_carton(520, 376, 78, 54))
            s.append(_carton(600, 396, 60, 34, C_BOITE2))
            s.append(_path("M690 130 L740 130 L740 400 L690 400 Z", fill="#b59a6f"))
            for i in range(1, 6):
                s.append('<line x1="690" y1="%s" x2="740" y2="%s" stroke="%s" stroke-width="5"/>'
                         % (130 + i * 45, 130 + i * 45, "#dcd8d0"))
        else:
            s.append(_etincelles(360, 300))
            s.append(_balai(120, 262))
    elif kind == "pro":
        if avant:
            s.append(_bureau(70, 366, 190))
            s.append(_chaise(286, 376))
            s.append(_bureau(390, 366, 190))
            s.append(_chaise(600, 376))
            s.append(_carton(660, 388, 66, 42, C_BOITE))
        else:
            s.append(_etincelles(360, 320))
            s.append(_etincelles(560, 360))
    return _svg(800, 600, "".join(s))


# --- scènes autonomes ---
def _camion(remplissage=None):
    s = [_rect(0, 470, 800, 130, SOL_APRES), _rect(0, 0, 800, 470, "#f4f2ec")]
    s.append(_path("M40 200 L360 200 L360 430 L40 430 Z", fill=VERT))
    s.append(_rect(52, 214, 296, 176, VERT_PALE, rx=6))
    if remplissage is None:
        s.append(_carton(70, 300, 72, 106))
        s.append(_carton(150, 316, 62, 90, C_BOITE2))
        s.append(_carton(222, 288, 66, 118, C_VIEUX))
        s.append(_etincelles(200, 250, VERT_CLAIR))
    else:
        hauteur = int(176 * remplissage / 100.0)
        s.append(_rect(52, 390 - hauteur, 296, hauteur, ORANGE, rx=4, opacite="0.85"))
    # cabine
    s.append(_path("M360 250 L470 250 L520 306 L520 430 L360 430 Z", fill=VERT2))
    s.append(_path("M382 268 L462 268 L498 310 L382 310 Z", fill="#cfe8d8"))
    s.append(_rect(486, 330, 26, 34, "#f4f2ec", rx=4))
    # roues
    for cx in (150, 300, 430):
        s.append(_circle(cx, 436, 40, "#2b2b31"))
        s.append(_circle(cx, 436, 16, "#9ca3af"))
    s.append(_rect(20, 430, 760, 8, ANTHRACITE, rx=4, opacite="0.12"))
    return _svg(800, 600, "".join(s))


def _equipe():
    s = [_rect(0, 470, 800, 130, SOL_APRES), _rect(0, 0, 800, 470, "#f4f2ec")]
    # armoire à l'arrière
    s.append(_rect(600, 190, 150, 250, C_MEUBLE, rx=4))
    s.append('<line x1="675" y1="190" x2="675" y2="440" stroke="%s" stroke-width="3" opacity="0.4"/>' % ANTHRACITE)
    # personne 1 (dos tourné, porte un carton)
    s.append(_circle(220, 226, 30, "#e0b48f"))
    s.append(_path("M180 470 L188 300 q32 -24 64 0 L262 470 Z", fill=VERT2))
    s.append(_rect(196, 258, 52, 62, C_BOITE, rx=5))
    # personne 2 (tient un meuble)
    s.append(_circle(430, 232, 28, "#c98f65"))
    s.append(_path("M392 470 L400 306 q30 -22 60 0 L468 470 Z", fill=VERT))
    s.append(_rect(300, 300, 120, 74, C_TISSU, rx=12))
    s.append(_path("M396 318 L372 336 M462 318 L486 336", stroke="#c98f65", sw=14))
    s.append(_rect(286, 372, 12, 10, C_SOMBRE, rx=2))
    s.append(_rect(422, 372, 12, 10, C_SOMBRE, rx=2))
    s.append(_etincelles(560, 220))
    return _svg(800, 600, "".join(s))


def _tri():
    s = [_rect(0, 470, 800, 130, SOL_APRES), _rect(0, 0, 800, 470, "#f4f2ec")]
    # trois bacs
    for i, (x, couleur, libelle) in enumerate([(70, VERT, "don"), (300, "#2563a8", "recyclage"),
                                               (530, ORANGE, "valorisation")]):
        s.append(_path("M%s 300 L%s 452 L%s 452 L%s 300 Z" % (x, x + 16, x + 164, x + 180), fill=couleur))
        s.append(_rect(x, 288, 180, 18, couleur, rx=4, opacite="0.75"))
        s.append(_rect(x + 40, 240, 100, 44, "#ffffff", rx=8, opacite="0.85"))
        if i == 0:
            s.append(_circle(x + 70, 262, 12, VERT2))
        elif i == 1:
            s.append(_path("M%s 262 l10 -10 l10 10 l10 -10" % (x + 60), stroke="#2563a8", sw=4))
        else:
            s.append(_rect(x + 60, 252, 20, 20, ORANGE, rx=4))
            s.append(_rect(x + 86, 246, 34, 26, ORANGE, rx=4, opacite="0.6"))
    # flèche circulaire
    s.append(_path("M400 150 a70 70 0 1 1 -60 36", stroke=VERT2, sw=7))
    s.append(_path("M330 176 l14 -22 l16 22 Z", fill=VERT2))
    return _svg(800, 600, "".join(s))


def _nettoyage():
    s = [_rect(0, 430, 800, 170, "#f2efe7"), _rect(0, 0, 800, 430, MUR_APRES)]
    s.append(_rect(548, 96, 186, 168, "#ffffff", rx=4))
    s.append(_rect(556, 104, 170, 152, VITRE_APRES, rx=2))
    s.append(_path("M556 256 L726 256 L636 430 L470 430 Z", fill="#fdf6e3", opacite="0.55"))
    # seau et serpillière
    s.append(_path("M300 380 L470 380 L450 466 L320 466 Z", fill="#4b8fd6"))
    s.append(_rect(296, 368, 178, 16, "#3d7cbe", rx=5))
    s.append(_path("M390 368 L400 250 L412 250 L420 368", stroke="#b0744c", sw=9))
    s.append(_path("M400 250 L330 430", stroke="#d6d3cd", sw=12))
    s.append(_etincelles(560, 330))
    s.append(_etincelles(240, 260))
    s.append(_plante(466, 1.2, cx=210))
    return _svg(800, 600, "".join(s))


def _succession():
    s = [_rect(0, 430, 800, 170, SOL_AVANT), _rect(0, 0, 800, 430, MUR_AVANT)]
    s.append(_rect(548, 96, 186, 168, "#e7e2d6", rx=4))
    s.append(_rect(556, 104, 170, 152, VITRE_AVANT, rx=2))
    s.append(_rect(636, 104, 9, 152, "#e7e2d6"))
    s.append(_rect(556, 174, 170, 9, "#e7e2d6"))
    # fauteuil, lampe, cartons ouverts, cadre
    s.append(_fauteuil(120, 330, C_TISSU))
    s.append(_path("M420 200 L420 380", stroke=C_SOMBRE, sw=6))
    s.append(_path("M380 380 L460 380 L444 200 L396 200 Z", fill="#d9c9a3"))
    s.append(_rect(396, 370, 68, 12, C_MEUBLE2, rx=4))
    s.append(_carton(540, 372, 78, 58))
    s.append(_carton(630, 392, 58, 38, C_BOITE2))
    s.append(_rect(230, 150, 96, 74, "#ffffff", rx=3))
    s.append(_rect(238, 158, 80, 58, "#b9c7cf", rx=2))
    # boîte à souvenirs ouverte
    s.append(_rect(300, 400, 92, 30, C_VIEUX, rx=3))
    s.append(_carton(310, 366, 30, 34, "#e3d5bd", rabat=False))
    return _svg(800, 600, "".join(s))


def _chantier():
    s = [_rect(0, 430, 800, 170, "#e6e1d6"), _rect(0, 0, 800, 430, MUR_AVANT)]
    # cloison en cours de démolition
    s.append(_rect(120, 140, 220, 290, "#e2ddd1"))
    s.append(_path("M120 300 L250 260 L340 320 L340 430 L120 430 Z", fill="#cfc9bb"))
    for i in range(4):
        s.append(_rect(120 + i * 56, 140, 10, 160, "#cdc6b6"))
    s.append(_rect(360, 140, 60, 290, "#d8d2c4"))
    # gravats au sol
    for x, y, w in ((150, 400, 54), (215, 412, 40), (270, 404, 62), (345, 414, 46), (410, 408, 52)):
        s.append(_rect(x, y, w, 22, "#b7b0a2", rx=7))
    # brouette et outils
    s.append(_path("M480 400 L600 400 L580 452 L500 452 Z", fill="#8a4a2a"))
    s.append(_circle(508, 462, 16, "#3f3f46"))
    s.append(_path("M600 400 L660 372", stroke="#8a4a2a", sw=7))
    s.append(_path("M660 300 L690 372", stroke="#b0744c", sw=8))
    s.append(_rect(686, 366, 30, 12, "#6b7280", rx=3))
    # poussière
    for x, y, r in ((180, 330, 4), (240, 300, 3), (300, 350, 4), (400, 320, 3), (450, 360, 4)):
        s.append(_circle(x, y, r, "#ffffff", opacite="0.6"))
    return _svg(800, 600, "".join(s))


def _grenier_vide():
    s = [_rect(0, 0, 800, 600, MUR_APRES), _rect(0, 430, 800, 170, SOL_APRES)]
    s.append(_path("M0 150 L400 40 L800 150", fill="none", stroke="#c9c3b5", sw=12))
    s.append(_path("M400 40 L400 150", stroke="#c9c3b5", sw=10))
    s.append(_rect(548, 96, 186, 168, "#ffffff", rx=4))
    s.append(_rect(556, 104, 170, 152, VITRE_APRES, rx=2))
    s.append(_etincelles(300, 300))
    s.append(_plante(430, 1.1, cx=330))
    return _svg(800, 600, "".join(s))


# --- catalogue : nom logique -> SVG ---
def _catalogue():
    scenes = {}
    for kind in ("appartement", "maison", "cave", "grenier", "garage", "pro"):
        for etat in ("avant", "apres"):
            scenes["%s-%s" % (kind, etat)] = _scene(kind, etat)
    scenes["camion"] = _camion()
    scenes["equipe"] = _equipe()
    scenes["tri"] = _tri()
    scenes["nettoyage"] = _nettoyage()
    scenes["succession"] = _succession()
    scenes["chantier"] = _chantier()
    scenes["grenier-vide"] = _grenier_vide()
    for i, pct in enumerate((12, 25, 50, 75, 100), start=1):
        scenes["camion-niveau-%d" % i] = _camion(pct)
    return scenes


CATALOGUE = _catalogue()

# illustrations par page/prestation
ILLUS_SERVICE = {
    "debarras-maison": "maison-avant",
    "debarras-appartement": "appartement-avant",
    "debarras-cave": "cave-avant",
    "debarras-grenier": "grenier-avant",
    "debarras-garage": "garage-avant",
    "debarras-succession": "succession",
    "debarras-apres-deces": "succession",
    "debarras-diogene": "cave-avant",
    "debarras-encombrants": "camion",
    "debarras-professionnel": "pro-avant",
    "nettoyage-apres-debarras": "nettoyage",
    "curage": "cave-apres",
    "demolition-interieure": "chantier",
}

ILLUS_SITUATION = {
    "demenagement": "camion",
    "succession": "succession",
    "deces": "succession",
    "vente-immobiliere": "maison-apres",
    "renovation": "chantier",
    "expulsion": "appartement-avant",
    "urgence": "camion",
}

ILLUS_ARTICLE = {
    "combien-coute-un-debarras-a-strasbourg": "camion",
    "vider-une-maison-apres-un-deces": "succession",
    "qui-paie-le-debarras-dune-succession": "maison-avant",
    "debarras-gratuit-est-ce-possible": "tri",
}

ILLUS_VILLE = {
    "strasbourg": "appartement-avant",
    "illkirch-graffenstaden": "maison-avant",
    "ostwald": "maison-avant",
    "lingolsheim": "appartement-avant",
    "schiltigheim": "appartement-avant",
    "bischheim": "maison-avant",
    "hoenheim": "garage-avant",
    "geispolsheim": "grenier-avant",
    "haguenau": "maison-avant",
    "molsheim": "cave-avant",
    "obernai": "maison-avant",
    "selestat": "appartement-avant",
}

# réalisations : paires avant/après par exemple
REALISATIONS_ILLUS = [
    ("appartement-avant", "appartement-apres"),
    ("cave-avant", "cave-apres"),
    ("maison-avant", "maison-apres"),
    ("garage-avant", "garage-apres"),
    ("grenier-avant", "grenier-vide"),
    ("pro-avant", "pro-apres"),
]
