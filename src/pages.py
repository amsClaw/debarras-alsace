# -*- coding: utf-8 -*-
"""Construction des pages du site."""
from data.site import (SITE, CTA, FAQ_GENERALE, FAQ_ACCUEIL, REALISATIONS_EXEMPLES, AVIS_MESSAGE,
                       CONTACT_INTRO, VALORISATION, VALORISATION_MESSAGE, POURQUOI_NOUS,
                       ZONES_PRESENTATION, HERO_ARGUMENTS, ETAPES)
from data.services import SERVICES, SERVICES_BY_SLUG, SERVICES_ACCUEIL
from data.villes import VILLES, VILLES_BY_SLUG
from data.situations import SITUATIONS
from data.articles import ARTICLES

from render import (Ctx, page, esc, ic, fil_ariane, bloc_entete, bloc_faq, bloc_cta_final, bloc_zone,
                    bloc_reassurance, bloc_process, cartes_services, cartes_situations, form_express,
                    form_complet, jsonld_localbusiness, jsonld_faq, jsonld_ariane, jsonld, _boutons_volume,
                    illus, figure_illus, avant_apres, photo)
from data.maquette import (HERO, CARTE, ZONE, SERVICES_MAQUETTE, SITUATIONS_MAQUETTE, PROCESS_MAQUETTE,
                           VALORISATION_MAQUETTE, REALISATIONS_MAQUETTE, AVIS_MAQUETTE, ZONES_MAQUETTE,
                           CTA_FINAL_MAQUETTE)
from illustrations import (ILLUS_SERVICE, ILLUS_SITUATION, ILLUS_ARTICLE, ILLUS_VILLE, REALISATIONS_ILLUS)

C = Ctx

_VILLE_PAR_NOM = {v["nom"]: v["slug"] for v in VILLES}


def _cta_devis(ctx, libelle=None):
    return '<a class="btn btn--accent" href="%s">%s</a>' % (ctx.l("contact-devis/"), esc(libelle or CTA["devis"]))


def _cta_appel(classe="btn--contour"):
    return '<a class="btn %s" href="tel:%s">Appeler le %s</a>' % (classe, SITE["telephone_lien"], esc(SITE["telephone"]))


# ------------------------------------------------------------------ accueil
def accueil(ctx):
    """Page d'accueil reconstruite à l'identique de la maquette client (textes + photos)."""
    c = ctx
    args_hero = "".join(
        '<li>%s<div><strong>%s</strong><span>%s</span></div></li>' % (ic(nom_icone), esc(titre), esc(sous))
        for nom_icone, titre, sous in HERO["arguments"])
    trust_zone = "".join(
        '<li>%s<div><strong>%s</strong><span>%s</span></div></li>' % (ic(nom_icone), esc(titre), esc(sous))
        for nom_icone, titre, sous in ZONE["reassurance"])
    cartes_services_maq = "".join(
        """<a class="carte-photo" href="%s">
  <span class="carte-photo__img">%s<span class="carte-photo__icone">%s</span></span>
  <span class="carte-photo__corps"><strong>%s</strong><span>%s</span></span>
</a>""" % (c.l("services/%s/" % slug), photo(c, nom_photo, titre), ic(nom_icone), esc(titre), esc(desc))
        for nom_photo, nom_icone, titre, desc, slug in SERVICES_MAQUETTE["cartes"])
    cartes_situations_maq = "".join(
        """<a class="carte-situation" href="%s">
  <span class="carte-situation__icone">%s</span>
  <strong>%s</strong><span>%s</span>
</a>""" % (c.l(("%s/" % slug) if "/" in slug else ("situations/%s/" % slug)), ic(nom_icone),
                esc(titre), esc(desc))
        for nom_icone, titre, desc, slug in SITUATIONS_MAQUETTE["cartes"])
    etapes_maq = "".join(
        """<article class="etape-maq">
  <span class="etape-maq__num">%02d</span><span class="etape-maq__icone">%s</span>
  <h3>%s</h3><p>%s</p>
</article>""" % (i, ic(nom_icone), esc(titre), esc(desc))
        for i, (nom_icone, titre, desc) in enumerate(PROCESS_MAQUETTE["etapes"], 1))
    valo_items = "".join('<li>%s<span>%s</span></li>' % (ic(nom_icone), esc(lib))
                         for nom_icone, lib in VALORISATION_MAQUETTE["items"])
    _sous_real = ["Succession : appartement vidé intégralement, meubles et objets triés.",
                  "Maison vidée en une journée, encombrants évacués et objets valorisables triés.",
                  "Cave dégagée : ferraille et encombrants évacués, sol balayé."]
    cartes_real = "".join(
        """<article class="carte-real">
  <figure>%s</figure>
  <p class="carte-real__titre">%s</p>
  <p class="carte-real__sous">%s</p>
</article>""" % (photo(c, avant, "Exemple d'intervention — %s" % titre, "carte-real__photo"), esc(titre),
                 esc(_sous_real[i % len(_sous_real)]))
        for i, (titre, avant, apres) in enumerate(REALISATIONS_MAQUETTE["cartes"]))
    cartes_avis = "".join(
        """<blockquote class="carte-avis">
  <span class="carte-avis__etoiles" aria-label="5 étoiles sur 5">%s</span>
  <p>« %s »</p>
  <footer>%s – %s</footer>
</blockquote>""" % (ic("etoile") * 5, esc(texte), esc(auteur), esc(ville))
        for texte, auteur, ville in AVIS_MAQUETTE["temoignages"])
    colonnes_zones = "".join(
        '<div class="zone-col"><strong>%s</strong><ul>%s</ul></div>'
        % (esc(titre), "".join("<li>%s</li>" % esc(l) for l in lignes if l))
        for titre, lignes in ZONES_MAQUETTE["colonnes"])
    types = "".join('<option>%s</option>' % esc(s["nom"]) for s in SERVICES)

    corps = """<section class="hero-maq">
  <div class="wrap hero-maq__grille">
    <div class="hero-maq__txt">
      <span class="hero-maq__badge">%s</span>
      <h1><span class="hero-maq__blanc">%s</span> <span class="hero-maq__vert">%s</span></h1>
      <p class="hero-maq__sous">%s</p>
      <ul class="hero-maq__args">%s</ul>
      <div class="hero-maq__cta">
        <a class="btn btn--accent" href="%s">%s &rarr;</a>
        <a class="btn btn--tel" href="tel:%s">%s %s</a>
      </div>
    </div>
    <form class="carte-devis" data-formulaire="express" data-email="%s" novalidate>
      <span class="carte-devis__badge">%s %s</span>
      <h2>%s</h2>
      <p class="carte-devis__sous">%s</p>
      <div class="bloc-etape" data-actif="1">
        <div class="champ">
          <label for="maq-type">%s</label>
          <select id="maq-type" name="type" data-etiquette="Type de débarras" required>
            <option value="">%s</option>%s
          </select>
          <p class="erreur">Indiquez le type de débarras.</p>
        </div>
        <div class="ligne-champs">
          <div class="champ">
            <label for="maq-cp">%s</label>
            <input type="text" id="maq-cp" name="code_postal" data-etiquette="Code postal" inputmode="numeric"
                   maxlength="5" placeholder="%s" required>
            <p class="erreur">Code postal à 5 chiffres.</p>
          </div>
          <div class="champ">
            <label for="maq-tel">%s</label>
            <input type="tel" id="maq-tel" name="telephone" data-etiquette="Téléphone" placeholder="%s" required>
            <p class="erreur">Numéro de téléphone à vérifier.</p>
          </div>
        </div>
        <div class="champ">
          <label for="maq-photos">%s</label>
          <label class="depot" for="maq-photos">
            <span class="depot__icone">%s</span>
            <span class="depot__txt">%s</span>
          </label>
          <input class="sr" type="file" id="maq-photos" name="photos" accept="image/*" multiple>
          <div class="miniatures" data-photos-liste></div>
        </div>
        <button class="btn btn--accent btn--large" type="button" data-suivant>%s &rarr;</button>
        <p class="carte-devis__mention">%s %s</p>
      </div>
      <div class="bloc-etape" data-actif="0">
        <div class="recap" data-recap></div>
        <div class="form-nav">
          <a class="btn btn--accent" href="#" data-envoi>Envoyer ma demande</a>
          <button class="btn btn--clair" type="button" data-copier>Copier</button>
          <a class="btn btn--clair" href="%s">WhatsApp</a>
        </div>
        <p class="aide mt-2">Votre demande part depuis votre messagerie (les photos restent sur votre appareil).</p>
      </div>
    </form>
  </div>
</section>

<section class="zone-bande">
  <div class="wrap zone-bande__grille">
    <div class="zone-bande__verif" data-zone>
      <h2>%s</h2>
      <p class="aide">%s</p>
      <div class="zone-bande__saisie">
        <input type="text" inputmode="numeric" maxlength="5" placeholder="%s" aria-label="Code postal">
        <button class="btn btn--vert" type="button">%s &rarr;</button>
      </div>
      <div class="zone__resultat" role="status" aria-live="polite"></div>
    </div>
    <ul class="zone-bande__trust">%s</ul>
  </div>
</section>

<section class="section section--blanc" id="services">
  <div class="wrap">
    <div class="entete-maq">
      <div>
        <span class="surtitre">%s</span>
        <h2>%s</h2>
        <p>%s</p>
      </div>
      <a class="btn btn--clair" href="%s">%s &rarr;</a>
    </div>
    <div class="grille-photos">%s</div>
  </div>
</section>

<section class="section section--beige">
  <div class="wrap">
    <div class="entete-maq">
      <div>
        <span class="surtitre">%s</span>
        <h2>%s</h2>
        <p>%s</p>
      </div>
      <a class="btn btn--clair" href="%s">%s &rarr;</a>
    </div>
    <div class="bloc-situation">
      <div class="grille-situations">%s</div>
      <div class="bloc-situation__photo">%s</div>
    </div>
  </div>
</section>

<section class="section section--blanc section-process">
  <div class="wrap">
    <div class="entete-maq">
      <div>
        <span class="surtitre">%s</span>
        <h2>%s<span class="chiffre">%s</span>%s</h2>
        <p>%s</p>
      </div>
      <a class="btn btn--accent" href="%s">%s &rarr;</a>
    </div>
    <div class="grille-etapes">%s</div>
  </div>
</section>

<section class="section section--vertcl">
  <div class="wrap bloc-valo">
    <div class="bloc-valo__photo">%s</div>
    <div>
      <span class="surtitre">%s</span>
      <h2>%s</h2>
      <p>%s</p>
      <ul class="valo-items">%s</ul>
      <div class="encart-partenaire">%s %s</div>
    </div>
  </div>
</section>

<section class="section section--blanc">
  <div class="wrap">
    <div class="entete-maq">
      <div>
        <h2>%s</h2>
        <p>%s</p>
      </div>
      <a class="btn btn--clair" href="%s">%s &rarr;</a>
    </div>
    <div class="grille-real">%s</div>
    <p class="legende legende--centre">Visuels d'illustration — les photos avant/après des chantiers
    réels de l'entreprise remplaceront ces images.</p>
  </div>
</section>

<section class="section section--beige">
  <div class="wrap">
    <div class="entete-maq">
      <div>
        <h2>%s</h2>
        <p class="note-google"><span class="etoiles">%s</span> <strong>%s</strong> %s</p>
      </div>
      <a class="btn btn--vert" href="%s">%s &rarr;</a>
    </div>
    <div class="grille-avis">%s</div>
  </div>
</section>

<section class="section section--blanc">
  <div class="wrap bloc-zones">
    <div class="bloc-zones__photos">
      <span class="badge-maq">%s</span>
      %s
      <div class="bloc-zones__carte">%s</div>
    </div>
    <div>
      <h2>%s</h2>
      <p>%s</p>
      <div class="grille-zones">%s</div>
      <div class="encart-zones"><strong>%s</strong><a class="lien-fleche" href="%s">%s &rarr;</a></div>
    </div>
  </div>
</section>
""" % (
        # hero
        esc(HERO["badge"]), HERO["titre_blanc"], esc(HERO["titre_vert"]), esc(HERO["texte"]), args_hero,
        c.l("contact-devis/"), esc(HERO["cta_principal"]), SITE["telephone_lien"], ic("telephone"),
        esc(HERO["cta_telephone"]),
        # carte
        SITE["email"], ic("doc"), esc(CARTE["badge"]), esc(CARTE["titre"]), esc(CARTE["sous_titre"]),
        esc(CARTE["champ_type"]), esc(CARTE["type_defaut"]), types,
        esc(CARTE["champ_cp"]), esc(CARTE["cp_placeholder"]), esc(CARTE["champ_tel"]), esc(CARTE["tel_placeholder"]),
        esc(CARTE["champ_photos"]), ic("appareil"), esc(CARTE["zone_depot"]), esc(CARTE["bouton"]),
        ic("bouclier"), esc(CARTE["mention"]), SITE["whatsapp_lien"],
        # zone
        esc(ZONE["titre"]), esc(ZONE["aide"]), esc(ZONE["placeholder"]), esc(ZONE["bouton"]), trust_zone,
        # services
        esc(SERVICES_MAQUETTE["surtitre"]), esc(SERVICES_MAQUETTE["titre"]), esc(SERVICES_MAQUETTE["texte"]),
        c.l("services/"), esc(SERVICES_MAQUETTE["cta"]), cartes_services_maq,
        # situations
        esc(SITUATIONS_MAQUETTE["surtitre"]), esc(SITUATIONS_MAQUETTE["titre"]), esc(SITUATIONS_MAQUETTE["texte"]),
        c.l("situations/"), esc(SITUATIONS_MAQUETTE["cta"]), cartes_situations_maq,
        photo(c, SITUATIONS_MAQUETTE["photo"], "Intervenant Débarras Alsace en intervention",
              classe="photo photo--haute"),
        # process
        esc(PROCESS_MAQUETTE["surtitre"]), esc(PROCESS_MAQUETTE["titre_avant"]),
        esc(PROCESS_MAQUETTE["titre_chiffre"]), esc(PROCESS_MAQUETTE["titre_apres"]),
        esc(PROCESS_MAQUETTE["sous_titre"]), c.l("contact-devis/"), esc(PROCESS_MAQUETTE["cta"]), etapes_maq,
        # valorisation
        photo(c, VALORISATION_MAQUETTE["photo"], "Jeune pousse : réemploi et valorisation",
              classe="photo photo--carree"),
        esc(VALORISATION_MAQUETTE["surtitre"]), esc(VALORISATION_MAQUETTE["titre"]),
        esc(VALORISATION_MAQUETTE["texte"]), valo_items, ic("euro"), esc(VALORISATION_MAQUETTE["encart"]),
        # réalisations
        esc(REALISATIONS_MAQUETTE["titre"]), esc(REALISATIONS_MAQUETTE["sous_titre"]), c.l("realisations/"),
        esc(REALISATIONS_MAQUETTE["cta"]), cartes_real,
        # avis
        esc(AVIS_MAQUETTE["titre"]), ic("etoile") * 5, esc(AVIS_MAQUETTE["note"]), esc(AVIS_MAQUETTE["nb_avis"]),
        c.l("avis-clients/"), esc(AVIS_MAQUETTE["cta"]), cartes_avis,
        # zones
        esc(ZONES_MAQUETTE["badge"]), photo(c, ZONES_MAQUETTE["photo"], "Strasbourg : la cathédrale et l'Ill",
                                            classe="photo photo--panorama"),
        photo(c, ZONES_MAQUETTE["carte"], "Carte de la zone d'intervention en Alsace", classe="photo--carte"),
        esc(ZONES_MAQUETTE["titre"]), esc(ZONES_MAQUETTE["sous_titre"]), colonnes_zones,
        esc(ZONES_MAQUETTE["encart"]), c.l("villes/"), esc(ZONES_MAQUETTE["cta"]),
    ) + _cta_final_maquette(c) + _bloc_faq_maquette(c)

    return page(ctx, "%s — débarras à Strasbourg et en Alsace | %s" % (SITE["nom"], SITE["baseline"]),
                "Débarras maison, appartement, cave, succession, après décès et locaux professionnels à "
                "Strasbourg et en Alsace. Devis gratuit, tri, valorisation, évacuation et nettoyage.",
                corps, jsonld_localbusiness() + jsonld_faq(FAQ_ACCUEIL))


def _cta_final_maquette(ctx):
    return """<section class="cta-final-maq">
  <div class="wrap">
    <div class="cta-final-maq__boite">
      <span class="feuille-gauche">%s</span>
      <h2>%s</h2>
      <p>%s</p>
      <a class="btn btn--accent" href="%s">%s &rarr;</a>
      <p class="cta-final-maq__tel">%s %s</p>
      <span class="feuille-droite">%s</span>
    </div>
  </div>
</section>""" % (ic("feuille"), esc(CTA_FINAL_MAQUETTE["titre"]), esc(CTA_FINAL_MAQUETTE["texte"]),
                 ctx.l("contact-devis/"), esc(CTA_FINAL_MAQUETTE["bouton"]), ic("telephone"),
                 esc(CTA_FINAL_MAQUETTE["telephone"]), ic("feuille"))


def _bloc_faq_maquette(ctx):
    """La maquette renvoie la FAQ vers la page dédiée : on garde un bloc court et honnête."""
    return """<section class="section section--beige">
  <div class="wrap">
    %s
    <div class="faq">%s</div>
    <p class="mt-3"><a class="btn btn--clair" href="%s">Voir toutes les questions &rarr;</a></p>
  </div>
</section>""" % (bloc_entete("Questions fréquentes", "FAQ"), bloc_faq(FAQ_ACCUEIL[:4]), ctx.l("faq/"))


def _galerie_render(ctx, limite=6):
    html = ['<div class="cartes cartes--3">']
    for i, (ville, type_bien, volume, duree) in enumerate(REALISATIONS_EXEMPLES[:limite]):
        avant, apres = REALISATIONS_ILLUS[i % len(REALISATIONS_ILLUS)]
        html.append("""<article class="realisation">
  %s
  <div class="realisation__corps">
    <h3>%s</h3>
    <p style="color:var(--gris);font-size:.95rem">%s</p>
    <ul class="realisation__meta"><li>%s</li><li>%s</li></ul>
    <p class="legende">Illustration de démonstration — les photos réelles du chantier viendront ici</p>
  </div>
</article>""" % (avant_apres(ctx, avant, apres), esc(ville), esc(type_bien), esc(volume), esc(duree)))
    html.append("</div>")
    return "".join(html)


# ------------------------------------------------------------------ services
def page_services(ctx):
    c = ctx
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Nos prestations de débarras en Alsace</h1>
  <p class="page-hero__chapeau">Treize prestations, du débarras d'une cave à la démolition intérieure avant
  travaux. Chaque page détaille ce qui est inclus, le déroulement, les facteurs de prix et les questions
  courantes.</p>
  <div class="page-hero__actions">%s%s</div>
</div></section>
<section class="section section--blanc"><div class="wrap">
  %s
</div></section>
%s""" % (fil_ariane(c, [("Accueil", "/"), ("Nos services", None)]), _cta_devis(c), _cta_appel("btn--clair"),
         cartes_services(c, [s["slug"] for s in SERVICES], colonnes=3, avec_accroche=False),
         bloc_cta_final(c))
    return page(c, "Nos services de débarras en Alsace — 13 prestations | %s" % SITE["nom"],
                "Débarras maison, appartement, cave, grenier, garage, succession, après décès, Diogène, encombrants, locaux professionnels, nettoyage, curage et démolition intérieure en Alsace.",
                corps, jsonld_ariane(c, [("Accueil", "/"), ("Nos services", None)]))


def page_service(ctx, s):
    c = ctx
    ariane = [("Accueil", "/"), ("Nos services", "/services/"), (s["nom"], None)]
    autres = [x["slug"] for x in SERVICES if x["slug"] != s["slug"]][:3]
    faq = s["faq"]
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>%s</h1>
  <p class="page-hero__chapeau">%s</p>
  <div class="page-hero__actions">%s%s</div>
</div></section>

<section class="section section--serre section--blanc"><div class="wrap">%s</div></section>

<section class="section section--blanc"><div class="wrap deux-colonnes">
  <div class="contenu">
    <h2 class="mt-0">Ce que nous faisons</h2>
    <p>%s</p>
    <h2>Qui nous appelle pour cette prestation</h2>
    <ul>%s</ul>
    <h2>Ce qui est inclus</h2>
    <div class="bloc-liste"><ul>%s</ul></div>
    <h2>Comment se déroule l'intervention</h2>
    <div class="etapes-process">%s</div>
    <h2>Ce qui fait varier le prix</h2>
    <div class="bloc-liste"><ul>%s</ul></div>
    <p><a class="lien-fleche" href="%s">Voir la page Tarifs et les facteurs détaillés &rsaquo;</a></p>
    <h2>Questions fréquentes sur %s</h2>
    %s
  </div>
  <div class="colle-laterale">
    <div class="aside-carte">
      <h2>Devis gratuit pour %s</h2>
      <p>Décrivez votre situation en quelques étapes et ajoutez des photos. Réponse sous 24 h ouvrées.</p>
      <a class="btn btn--accent" href="%s">%s</a>
      <a class="btn btn--clair" href="tel:%s">Appeler le %s</a>
      <a class="btn btn--clair" href="%s">WhatsApp</a>
    </div>
    <div class="aside-carte">
      <h3>Pages liées</h3>
      <ul class="liste-simple">%s</ul>
    </div>
    <div class="aside-carte">
      <h3>Zones d'intervention</h3>
      <ul class="liste-simple">%s</ul>
      <a class="lien-fleche" href="%s">Toutes les villes &rsaquo;</a>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap">%s</div></section>
%s""" % (
        fil_ariane(c, ariane), esc(s["h1"]), esc(s["intro"].split(". ")[0] + "."),
        _cta_devis(c), _cta_appel("btn--clair"),
        figure_illus(c, ILLUS_SERVICE.get(s["slug"], "camion"),
                     "%s : intervention de débarras" % s["nom"],
                     legende="Illustration de démonstration — photo réelle à venir"),
        esc(s["intro"]),
        "".join("<li>%s</li>" % esc(x) for x in s["pour_qui"]),
        "".join("<li>%s<span>%s</span></li>" % (ic("check"), esc(x)) for x in s["inclus"]),
        "".join('<article class="etape-carte"><div class="etape-carte__num">%d</div><h3>%s</h3><p>%s</p></article>'
                % (i, esc(t), esc(x)) for i, (t, x) in enumerate(s["deroulement"], 1)),
        "".join("<li>%s%s</li>" % (ic("euro"), esc(x)) for x in s["facteurs"]),
        c.l("tarifs/"),
        esc(s["nom"].lower()), bloc_faq(faq),
        esc(s["nom"].lower()), c.l("contact-devis/"), esc(CTA["devis"]),
        SITE["telephone_lien"], esc(SITE["telephone"]), SITE["whatsapp_lien"],
        "".join('<li><a href="%s">%s</a></li>' % (c.l("services/%s/" % x), esc(SERVICES_BY_SLUG[x]["nom"])) for x in autres),
        "".join('<li><a href="%s">%s</a></li>' % (c.l("villes/%s/" % v["slug"]), esc(v["nom"])) for v in VILLES[:6]),
        c.l("villes/"),
        bloc_entete("Ces prestations vont souvent ensemble", "À découvrir"), _bloc_lie_services(c, autres),
    )
    ld = jsonld({
        "@context": "https://schema.org", "@type": "Service", "name": s["nom"],
        "description": s["meta"], "provider": {"@type": "LocalBusiness", "name": SITE["nom"],
                                               "telephone": SITE["telephone"]},
        "areaServed": [v["nom"] for v in VILLES],
        "url": c.abs("services/%s/" % s["slug"]),
    })
    return page(c, s["title"], s["meta"], corps,
                ld + jsonld_faq(faq) + jsonld_ariane(c, ariane))


def _bloc_lie_services(ctx, slugs):
    return cartes_services(ctx, slugs, colonnes=3)


# ------------------------------------------------------------------ situations
def page_situations(ctx):
    c = ctx
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Vous êtes dans l'une de ces situations ?</h1>
  <p class="page-hero__chapeau">Le débarras lui-même change peu ; ce qui change, c'est le contexte, les
  délais et ce qu'il faut préserver. Choisissez la situation qui ressemble à la vôtre.</p>
  <div class="page-hero__actions">%s%s</div>
</div></section>
<section class="section section--blanc"><div class="wrap">%s</div></section>
%s""" % (fil_ariane(c, [("Accueil", "/"), ("Situations", None)]), _cta_devis(c), _cta_appel("btn--clair"),
         cartes_situations(c), bloc_cta_final(c))
    return page(c, "Situations : succession, déménagement, vente, urgence | %s" % SITE["nom"],
                "Débarras par situation en Alsace : succession, après décès, déménagement, vente immobilière, rénovation, fin de bail, urgence. Méthode et réponses adaptées à chaque cas.",
                corps, jsonld_ariane(c, [("Accueil", "/"), ("Situations", None)]))


def page_situation(ctx, s):
    c = ctx
    ariane = [("Accueil", "/"), ("Situations", "/situations/"), (s["nom"], None)]
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>%s</h1>
  <p class="page-hero__chapeau">%s</p>
  <div class="page-hero__actions">%s%s</div>
</div></section>
<section class="section section--serre section--blanc"><div class="wrap">%s</div></section>
<section class="section section--blanc"><div class="wrap deux-colonnes">
  <div class="contenu">
    <p>%s</p>
    <h2>Votre situation</h2>
    <ul>%s</ul>
    <h2>Comment nous y répondons</h2>
    <div class="bloc-liste"><ul>%s</ul></div>
    <h2>Questions fréquentes</h2>
    %s
  </div>
  <div class="colle-laterale">
    <div class="aside-carte">
      <h2>Demander un devis</h2>
      <p>Décrivez la situation en quelques étapes : nous vous répondons sur ce qui est réellement possible.</p>
      <a class="btn btn--accent" href="%s">%s</a>
      <a class="btn btn--clair" href="tel:%s">Appeler le %s</a>
      <a class="btn btn--clair" href="%s">WhatsApp</a>
    </div>
    <div class="aside-carte">
      <h3>Prestations adaptées</h3>
      <ul class="liste-simple">%s</ul>
    </div>
  </div>
</div></section>
%s""" % (
        fil_ariane(c, ariane), esc(s["h1"]), esc(s["intro"].split(". ")[0] + "."),
        _cta_devis(c), _cta_appel("btn--clair"),
        figure_illus(c, ILLUS_SITUATION.get(s["slug"], "camion"),
                     "Situation : %s" % s["nom"], legende="Illustration de démonstration"),
        esc(s["intro"]),
        "".join("<li>%s</li>" % esc(x) for x in s["situation"]),
        "".join("<li>%s<span>%s</span></li>" % (ic("check"), esc(x)) for x in s["reponses"]),
        bloc_faq(s["faq"]),
        c.l("contact-devis/"), esc(CTA["devis"]), SITE["telephone_lien"], esc(SITE["telephone"]),
        SITE["whatsapp_lien"],
        "".join('<li><a href="%s">%s</a></li>' % (c.l("services/%s/" % x), esc(SERVICES_BY_SLUG[x]["nom"]))
                for x in s["services_lies"]),
        bloc_cta_final(c, "Cette situation vous parle ?",
                       "Décrivez-la en quelques étapes, ajoutez des photos si vous en avez : nous vous dirons ce qui est faisable et à quel délai."),
    )
    return page(c, s["title"], s["meta"], corps,
                jsonld_faq(s["faq"]) + jsonld_ariane(c, ariane))


# ------------------------------------------------------------------ villes
def page_villes(ctx):
    c = ctx
    cartes = "".join(
        '<a class="ville-carte" href="%s"><strong>%s</strong><span>%s</span><span class="aide">%s</span></a>'
        % (c.l("villes/%s/" % v["slug"]), esc(v["nom"]), esc(v["cp"]), esc(v["courte"])) for v in VILLES)
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Zones d'intervention en Alsace</h1>
  <p class="page-hero__chapeau">%s</p>
  <div class="page-hero__actions">%s</div>
</div></section>
<section class="section section--blanc"><div class="wrap">
  <div class="villes">%s</div>
  <div class="notice mt-3">Votre commune n'est pas dans cette liste ? Envoyez votre demande : nous
  intervenons régulièrement dans le reste du Bas-Rhin et du Haut-Rhin selon la distance et le volume.</div>
</div></section>
<section class="section"><div class="wrap g2 grille" style="align-items:start">
  <div>%s</div>
  <div>%s</div>
</div></section>
%s""" % (fil_ariane(c, [("Accueil", "/"), ("Zones d'intervention", None)]), esc(ZONES_PRESENTATION),
         _cta_devis(c), cartes,
         "<h2 class='mt-0'>Pourquoi une page par ville ?</h3>".replace("h3", "h2") +
         "<p>Chaque commune a ses contraintes : accès camion, type d'habitat, présence de caves, de "
         "dépendances ou de copropriétés. Ces différences changent la façon d'organiser un débarras — et "
         "elles sont utiles à connaître avant de demander un devis.</p>",
         bloc_zone(c), bloc_cta_final(c))
    return page(c, "Zones d'intervention : débarras en Alsace | %s" % SITE["nom"],
                "Débarras à Strasbourg, Illkirch, Ostwald, Lingolsheim, Schiltigheim, Bischheim, Hœnheim, Geispolsheim, Haguenau, Molsheim, Obernai et Sélestat. Détail par commune.",
                corps, jsonld_ariane(c, [("Accueil", "/"), ("Zones d'intervention", None)]))


def page_ville(ctx, v):
    c = ctx
    ariane = [("Accueil", "/"), ("Zones d'intervention", "/villes/"), (v["nom"], None)]
    faq = v["faq"]
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>%s</h1>
  <p class="page-hero__chapeau">Débarras à %s : %s.</p>
  <div class="page-hero__actions">%s%s</div>
</div></section>

<section class="section section--serre section--blanc"><div class="wrap">%s</div></section>

<section class="section section--blanc"><div class="wrap deux-colonnes">
  <div class="contenu">
    <h2 class="mt-0">Débarras à %s : ce qui change sur place</h2>
    <p>%s</p>
    <h2>Quartiers et secteurs desservis</h2>
    <ul class="pilules">%s</ul>
    <h2>Communes voisines où nous intervenons aussi</h2>
    <p>%s</p>
    <h2>Exemples de chantiers sur ce secteur</h2>
    <div class="cartes cartes--3">%s</div>
    <h2>Prestations les plus demandées à %s</h2>
    %s
    <h2>Questions fréquentes à %s</h2>
    %s
  </div>
  <div class="colle-laterale">
    <div class="aside-carte">
      <h2>Devis gratuit à %s</h2>
      <p>Indiquez votre code postal, l'étage et l'accès : c'est ce qui permet de chiffrer rapidement.</p>
      <a class="btn btn--accent" href="%s">%s</a>
      <a class="btn btn--clair" href="tel:%s">Appeler le %s</a>
      <a class="btn btn--clair" href="%s">WhatsApp</a>
    </div>
    <div class="aside-carte">%s</div>
    <div class="aside-carte">
      <h3>Villes voisines</h3>
      <ul class="liste-simple">%s</ul>
    </div>
  </div>
</div></section>
%s""" % (
        fil_ariane(c, ariane), esc(v["h1"]), esc(v["nom"]), esc(v["courte"]),
        _cta_devis(c), _cta_appel("btn--clair"),
        figure_illus(c, ILLUS_VILLE.get(v["slug"], "camion"),
                     "Débarras à %s : type d'habitat et chantier courant" % v["nom"],
                     legende="Illustration de démonstration — photo réelle à venir"),
        esc(v["nom"]), esc(v["intro"]),
        "".join("<li>%s</li>" % esc(q) for q in v["quartiers"]),
        esc("Nous intervenons également à " + ", ".join(v["communes_voisines"]) + "."),
        "".join("""<article class="realisation">
  <div class="media-vide">Photo à ajouter</div>
  <div class="realisation__corps">
    <h3>%s</h3><p style="color:var(--gris);font-size:.95rem">%s</p>
    <ul class="realisation__meta"><li>%s</li><li>%s</li></ul>
  </div>
</article>""" % (esc(t), esc(tb), esc(vol), esc(dur)) for t, tb, vol, dur in v["chantiers"]),
        esc(v["nom"]),
        cartes_services(c, ["debarras-maison", "debarras-appartement", "debarras-cave",
                            "debarras-succession", "debarras-encombrants", "nettoyage-apres-debarras"],
                        colonnes=3),
        esc(v["nom"]), bloc_faq(faq),
        esc(v["nom"]), c.l("contact-devis/"), esc(CTA["devis"]),
        SITE["telephone_lien"], esc(SITE["telephone"]), SITE["whatsapp_lien"],
        "<h3>À savoir sur place</h3><p>%s</p>" % esc(v["note_locale"]),
        "".join('<li><a href="%s">%s</a></li>' % (c.l("villes/%s/" % _VILLE_PAR_NOM[x]), esc(x))
                for x in v["communes_voisines"][:6] if x in _VILLE_PAR_NOM),
        bloc_entete("Autres communes desservies", "Zones", "Nous couvrons l'ensemble de l'Eurométropole et du Bas-Rhin."),
    ) + page_villes_compactes(c, v["slug"])
    ld = jsonld({
        "@context": "https://schema.org", "@type": "LocalBusiness", "name": SITE["nom"],
        "description": "Débarras à %s : maison, appartement, cave, succession, encombrants." % v["nom"],
        "url": c.abs("villes/%s/" % v["slug"]),
        "telephone": SITE["telephone"],
        "address": {"@type": "PostalAddress", "addressLocality": v["nom"], "postalCode": v["cp"].split(" ")[0],
                    "addressRegion": "Grand Est", "addressCountry": "FR"},
        "areaServed": [v["nom"]] + v["communes_voisines"],
    })
    return page(c, v["title"], v["meta"], corps, ld + jsonld_faq(faq) + jsonld_ariane(c, ariane))


def page_villes_compactes(ctx, sauf):
    cartes = "".join('<a class="ville-carte" href="%s"><strong>%s</strong><span>%s</span></a>'
                     % (ctx.l("villes/%s/" % v["slug"]), esc(v["nom"]), esc(v["cp"]))
                     for v in VILLES if v["slug"] != sauf)
    return '<section class="section"><div class="wrap"><div class="villes">%s</div></div></section>' % cartes


# ------------------------------------------------------------------ tarifs
def page_tarifs(ctx):
    c = ctx
    facteurs = [
        ("Volume à évacuer (m³)", "Une cave peut contenir plus qu'un appartement : le volume réel, pas la surface, fait le prix."),
        ("Étage et ascenseur", "Chaque étage sans ascenseur ajoute du temps de manutention, donc du coût."),
        ("Accès et stationnement", "Distance entre le logement et le camion, escaliers extérieurs, cour étroite, stationnement réglementé."),
        ("Nature des objets", "Mobilier et cartons ne coûtent pas le même traitement que gravats, pneus ou produits chimiques."),
        ("Niveau de tri demandé", "Un tri fin avec mise de côté et orientation en don prend plus de temps qu'une évacuation globale."),
        ("Nettoyage associé", "Le nettoyage après débarras est une prestation à part, moins coûteuse si elle est couplée."),
        ("Contraintes de délai", "Une intervention urgente, en soirée ou le week-end mobilise une équipe sur un créneau contraint."),
    ]
    faq = [
        ("Pourquoi ne pas afficher de prix au m³ ?",
         "Parce qu'un prix au m³ seul serait trompeur : deux volumes identiques peuvent coûter très "
         "différent selon l'étage, l'accès et le tri. Nous préférons un devis précis, gratuit, plutôt qu'un "
         "chiffre affiché qui ne serait pas tenu."),
        ("Le devis peut-il changer ?",
         "Il est établi sur ce que vous nous décrivez (photos, échange, visite). S'il reste des gravats "
         "cachés, un volume nettement supérieur ou des objets à traiter spécifiquement, nous vous le "
         "signalons avant de continuer et nous ajustons avec votre accord."),
        ("Le déplacement pour le devis est-il payant ?",
         "Non : le devis est gratuit et sans engagement. Pour les volumes importants, une visite sur place "
         "est recommandée, mais elle reste gratuite."),
        ("Existe-t-il une aide ou une déduction possible ?",
         "Certains objets valorisables peuvent réduire la facture, et le nettoyage associé peut, dans "
         "certains cas, relever d'un dispositif d'aide à domicile. Nous vous orientons vers les "
         "informations à vérifier selon votre situation — sans rien promettre à votre place."),
        ("Comment payer ?",
         "Les modalités (acompte éventuel, paiement à la fin de l'intervention, facture pour les "
         "professionnels) sont indiquées sur le devis avant toute intervention."),
    ]
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Prix d'un débarras à Strasbourg : comment ça se calcule</h1>
  <p class="page-hero__chapeau">Il n'existe pas de tarif unique : voici, honnêtement, ce qui fait varier le
  prix d'un débarras, et comment obtenir un chiffrage fiable.</p>
  <div class="page-hero__actions">%s%s</div>
</div></section>

<section class="section section--blanc"><div class="wrap deux-colonnes">
  <div class="contenu">
    <h2 class="mt-0">Les 7 facteurs qui font le prix</h2>
    <div class="bloc-liste"><ul>%s</ul></div>
    <h2>Comment se construit un devis</h2>
    <p>Nous partons de votre description, de vos photos et si besoin d'une visite. Le devis indique le volume
    estimé, la durée prévue, ce qui est inclus (manutention, évacuation, tri, nettoyage) et ce qui ne l'est
    pas. C'est ce document qui fait foi : pas un prix annoncé au téléphone en trente secondes.</p>
    <h2>Estimation indicative en ligne</h2>
    <p>Le simulateur ci-dessous vous aide à situer votre volume. Il ne remplace pas un devis : il sert à
    savoir si l'on parle d'une remorque ou de plusieurs camions.</p>
    <div class="simulation" data-simulateur>
      %s
      <div class="volumes">%s</div>
      <div class="resultat-simulation" role="status" aria-live="polite"></div>
    </div>
    <h2 class="mt-3">Les questions à poser à n'importe quelle entreprise</h2>
    <ul>
      <li>Le prix est-il ferme pour le volume décrit ?</li>
      <li>Les gravats et les déchets de chantier sont-ils inclus ?</li>
      <li>Que se passe-t-il si le volume réel est plus important ?</li>
      <li>Les objets de valeur sont-ils mis de côté et documentés ?</li>
      <li>Le nettoyage est-il compris, ou facturé à part ?</li>
      <li>La facture mentionne-t-elle clairement la prestation ?</li>
    </ul>
    <div class="notice">Notre position : nous ne promettons jamais un débarras gratuit ni un rachat
    systématique. Ce qui peut réduire la facture (objets valorisables, tri, don) est discuté avant
    l'intervention et écrit sur le devis.</div>
    <h2>Questions fréquentes sur les tarifs</h2>
    %s
  </div>
  <div class="colle-laterale">
    <div class="aside-carte">
      <h2>Obtenir un chiffrage</h2>
      <p>Photos + description de l'accès = estimation rapide, gratuite et sans engagement.</p>
      <a class="btn btn--accent" href="%s">%s</a>
      <a class="btn btn--clair" href="tel:%s">Appeler le %s</a>
      <a class="btn btn--clair" href="%s">WhatsApp</a>
    </div>
    <div class="aside-carte">
      <h3>Articles liés</h3>
      <ul class="liste-simple">
        <li><a href="%s">Combien coûte un débarras à Strasbourg ?</a></li>
        <li><a href="%s">Débarras gratuit : est-ce vraiment possible ?</a></li>
        <li><a href="%s">Qui paie le débarras d'une succession ?</a></li>
      </ul>
    </div>
  </div>
</div></section>
%s""" % (
        fil_ariane(c, [("Accueil", "/"), ("Tarifs", None)]), _cta_devis(c, "Demander mon chiffrage"), _cta_appel("btn--clair"),
        "".join("<li>%s<span>%s</span></li>" % (ic("euro"), esc(t) + " — " + esc(x)) for t, x in facteurs),
        illus(c, "camion", "Camion de débarras : le volume se mesure en fractions de camion"),
        _boutons_volume(c), bloc_faq(faq),
        c.l("contact-devis/"), esc(CTA["devis"]), SITE["telephone_lien"], esc(SITE["telephone"]),
        SITE["whatsapp_lien"],
        c.l("blog/combien-coute-un-debarras-a-strasbourg/"), c.l("blog/debarras-gratuit-est-ce-possible/"),
        c.l("blog/qui-paie-le-debarras-dune-succession/"),
        bloc_cta_final(c),
    )
    return page(c, "Prix d'un débarras à Strasbourg : les facteurs | %s" % SITE["nom"],
                "Prix d'un débarras à Strasbourg et en Alsace : volume, étage, accès, nature des déchets, tri et nettoyage. Comprendre un devis avant de signer.",
                corps, jsonld_faq(faq) + jsonld_ariane(c, [("Accueil", "/"), ("Tarifs", None)]))


# ------------------------------------------------------------------ réalisations / avis
def page_realisations(ctx):
    c = ctx
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Nos réalisations en Alsace</h1>
  <p class="page-hero__chapeau">Type de bien, volume et durée : voici le format de nos comptes rendus de
  chantier. Les photographies avant/après seront ajoutées dès réception du lot photo de l'entreprise —
  nous n'utilisons pas d'images génériques à leur place.</p>
  <div class="page-hero__actions">%s%s</div>
</div></section>
<section class="section section--blanc"><div class="wrap">
  <div class="notice">Transparence : les exemples ci-dessous décrivent des formats d'intervention type
  (ville, type de bien, volume, durée). Les photos réelles avant/après et les détails de chantier seront
  publiés après accord du client.</div>
  <div class="mt-3">%s</div>
</div></section>
%s""" % (fil_ariane(c, [("Accueil", "/"), ("Réalisations", None)]), _cta_devis(c), _cta_appel("btn--clair"),
         _galerie_render(c, limite=6), bloc_cta_final(c))
    return page(c, "Réalisations — débarras en Alsace | %s" % SITE["nom"],
                "Exemples de débarras réalisés en Alsace : ville, type de bien, volume évacué et durée d'intervention. Photos avant/après à venir.",
                corps, jsonld_ariane(c, [("Accueil", "/"), ("Réalisations", None)]))


def page_avis(ctx):
    c = ctx
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Avis clients</h1>
  <p class="page-hero__chapeau">Notre règle est simple : aucun avis n'est affiché ici tant qu'il n'est pas
  réel, daté et vérifiable. Cet emplacement accueillera la fiche Google de l'entreprise.</p>
  <div class="page-hero__actions">%s</div>
</div></section>
<section class="section section--blanc"><div class="wrap">
  <div class="avis-vide">
    <p><strong>%s</strong></p>
    <p class="aide">Vous avez fait appel à nous ? Un avis laissé sur la fiche Google nous aide énormément —
    et il sera affiché ici tel quel.</p>
  </div>
  <div class="deux-colonnes mt-3">
    <div class="contenu">
      <h2 class="mt-0">Pourquoi nous n'affichons pas de faux avis</h2>
      <p>Beaucoup de sites affichent des notes ou des témoignages qui ne correspondent à rien de
      vérifiable. Cela fonctionne jusqu'au jour où un client s'en aperçoit — et cela abîme la confiance
      qu'un débarras demande justement d'avoir : quelqu'un qui vient chez vous, manipule vos affaires et
      voit ce que vous jetez.</p>
      <p>Nous préférons une page honnête, qui se remplira progressivement de vrais avis. Si vous nous avez
      sollicités récemment, un avis Google nous aidera à la remplir.</p>
      <h2>Ce que nous garantissons en attendant</h2>
      <ul>
        <li>Devis gratuit, détaillé et sans engagement.</li>
        <li>Aucune promesse de « débarras gratuit » ni de rachat automatique.</li>
        <li>Objets de valeur identifiés et mis de côté, jamais évacués sans votre accord.</li>
        <li>Devis et facture nominatifs, transmissibles au notaire ou à une assurance.</li>
      </ul>
    </div>
    <div class="colle-laterale">
      <div class="aside-carte">
        <h3>Laisser un avis</h3>
        <p>Le lien vers la fiche Google Business Profile sera ajouté ici dès qu'elle sera reliée au site.</p>
        <a class="btn btn--clair" href="%s">Nous contacter</a>
      </div>
    </div>
  </div>
</div></section>
%s""" % (fil_ariane(c, [("Accueil", "/"), ("Avis clients", None)]), _cta_devis(c),
         esc(AVIS_MESSAGE), c.l("contact-devis/"), bloc_cta_final(c))
    return page(c, "Avis clients — débarras en Alsace | %s" % SITE["nom"],
                "Avis clients de l'entreprise de débarras : nous n'affichons que des avis réels et vérifiables. Emplacement prêt pour la fiche Google.",
                corps, jsonld_ariane(c, [("Accueil", "/"), ("Avis clients", None)]))


# ------------------------------------------------------------------ à propos / faq
def page_a_propos(ctx):
    c = ctx
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>À propos</h1>
  <p class="page-hero__chapeau">Une entreprise de débarras locale, à Strasbourg et en Alsace : nous vidons,
  trions, évacuons et nettoyons — en expliquant ce que nous faisons de vos objets.</p>
  <div class="page-hero__actions">%s%s</div>
</div></section>
<section class="section section--blanc"><div class="wrap deux-colonnes">
  <div class="contenu">
    <div class="g2 grille mb-0">%s%s</div>
    <h2 class="mt-0">Notre façon de travailler</h2>
    <p>Un débarras n'est pas seulement un camion et de la force. C'est un moment où l'on entre chez
    quelqu'un, souvent après un décès, un déménagement contraint ou des années d'accumulation. Nous
    travaillons avec trois règles : ne rien jeter sans validation, documenter les objets de valeur, et
    laisser le logement dans un état utilisable.</p>
    <h2>Ce que nous faisons</h2>
    <ul>
      <li>Débarras de maisons, appartements, caves, greniers, garages et dépendances.</li>
      <li>Successions, après décès et situations de logement très encombré, avec discrétion.</li>
      <li>Enlèvement d'encombrants ponctuel, curage de locaux, démolition intérieure avant travaux.</li>
      <li>Nettoyage après débarras, pour une vente, une location ou une restitution de bail.</li>
    </ul>
    <h2>Notre engagement sur le tri</h2>
    <p>Ce qui peut être donné, réemployé ou recyclé l'est : c'est moins de volume envoyé en déchèterie et,
    lorsque des objets ont une valeur, une réduction possible de la facture. Nous ne promettons jamais un
    débarras gratuit : nous expliquons ce qui est possible et ce qui ne l'est pas.</p>
    <div class="notice">Cette page sera complétée avec les informations réelles de l'entreprise (raison
    sociale, ancienneté, équipe, certifications, assurances) dès qu'elles nous seront communiquées. Nous
    n'inventons ni ancienneté, ni nombre de chantiers, ni agrément.</div>
    <h2>Informations à venir</h2>
    <ul>
      <li>Raison sociale et coordonnées complètes.</li>
      <li>Équipe et véhicules (photos réelles).</li>
      <li>Assurances et certifications éventuelles.</li>
      <li>Zone d'intervention officielle et horaires.</li>
    </ul>
  </div>
  <div class="colle-laterale">
    <div class="aside-carte">
      <h2>Nous contacter</h2>
      <a class="btn btn--accent" href="%s">%s</a>
      <a class="btn btn--clair" href="tel:%s">Appeler le %s</a>
      <a class="btn btn--clair" href="%s">WhatsApp</a>
      <p class="aide mt-2">%s</p>
    </div>
  </div>
</div></section>
%s""" % (fil_ariane(c, [("Accueil", "/"), ("À propos", None)]), _cta_devis(c), _cta_appel("btn--clair"),
         illus(c, "equipe", "Équipe de débarras en intervention", classe="illus illus-hero"),
         illus(c, "camion", "Chargement du camion lors d'un débarras"),
         c.l("contact-devis/"), esc(CTA["devis"]), SITE["telephone_lien"], esc(SITE["telephone"]),
         SITE["whatsapp_lien"], esc(SITE["horaires"]), bloc_cta_final(c))
    return page(c, "À propos — entreprise de débarras en Alsace | %s" % SITE["nom"],
                "Entreprise de débarras à Strasbourg et en Alsace : méthode de travail, tri, valorisation et engagement de transparence.",
                corps, jsonld_ariane(c, [("Accueil", "/"), ("À propos", None)]))


def page_faq(ctx):
    c = ctx
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Questions fréquentes</h1>
  <p class="page-hero__chapeau">Les questions qu'on nous pose avant de confier un débarras : prix, délais,
  accès, objets de valeur, nettoyage, urgence.</p>
  <div class="page-hero__actions">%s%s</div>
</div></section>
<section class="section section--blanc"><div class="wrap">
  <div class="g2 grille" style="align-items:start">
    <div>%s</div>
    <div class="aside-carte">
      <h3>Votre question n'est pas là ?</h3>
      <p>Posez-la directement : nous répondons précisément, y compris quand la réponse est « ce n'est pas
      possible ».</p>
      <a class="btn btn--accent" href="%s">%s</a>
      <a class="btn btn--clair" href="tel:%s">Appeler le %s</a>
      <a class="btn btn--clair" href="%s">WhatsApp</a>
    </div>
  </div>
</div></section>
%s""" % (fil_ariane(c, [("Accueil", "/"), ("FAQ", None)]), _cta_devis(c), _cta_appel("btn--clair"),
         bloc_faq(FAQ_GENERALE), c.l("contact-devis/"), esc(CTA["devis"]),
         SITE["telephone_lien"], esc(SITE["telephone"]), SITE["whatsapp_lien"], bloc_cta_final(c))
    return page(c, "FAQ débarras — questions fréquentes | %s" % SITE["nom"],
                "Combien coûte un débarras, le devis est-il gratuit, peut-on envoyer des photos, que deviennent les meubles, intervenez-vous le week-end : nos réponses.",
                corps, jsonld_faq(FAQ_GENERALE) + jsonld_ariane(c, [("Accueil", "/"), ("FAQ", None)]))


# ------------------------------------------------------------------ blog
def page_blog(ctx):
    c = ctx
    cartes = "".join("""<article class="carte">
  %s
  <h3><a href="%s">%s</a></h3>
  <p>%s</p>
  <div class="carte__pied"><a class="lien-fleche" href="%s">Lire l'article &rsaquo;</a></div>
</article>""" % (illus(c, ILLUS_ARTICLE.get(a["slug"], "camion"), a["titre"], classe="illus carte__illus"),
                    c.l("blog/%s/" % a["slug"]), esc(a["titre"]), esc(a["chapeau"]),
                    c.l("blog/%s/" % a["slug"]))
        for a in ARTICLES)
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Conseils sur le débarras en Alsace</h1>
  <p class="page-hero__chapeau">Des réponses concrètes aux questions que se posent vraiment les personnes
  qui doivent vider un logement : prix, succession, gratuité annoncée, organisation.</p>
</div></section>
<section class="section section--blanc"><div class="wrap">
  <div class="cartes cartes--3">%s</div>
  <div class="notice mt-3">Les articles sont rédigés pour être utiles même si vous ne nous appelez pas :
  aucune promesse commerciale, aucun chiffre inventé. Les sujets suivants arrivent prochainement :
  vider une cave rapidement, que faire des meubles avant un déménagement, se débarrasser d'un canapé à
  Strasbourg, débarras avant vente immobilière, estimer un volume.</div>
</div></section>
%s""" % (fil_ariane(c, [("Accueil", "/"), ("Blog", None)]), cartes, bloc_cta_final(c))
    return page(c, "Blog — conseils débarras en Alsace | %s" % SITE["nom"],
                "Conseils et guides sur le débarras en Alsace : prix, succession, après décès, débarras gratuit, organisation pratique.",
                corps, jsonld_ariane(c, [("Accueil", "/"), ("Blog", None)]))


def page_article(ctx, a):
    c = ctx
    ariane = [("Accueil", "/"), ("Blog", "/blog/"), (a["titre"], None)]
    sections = "".join("<h2>%s</h2>%s" % (esc(t), "".join("<p>%s</p>" % esc(p) for p in paras))
                       for t, paras in a["sections"])
    ld = jsonld({
        "@context": "https://schema.org", "@type": "Article", "headline": a["titre"],
        "description": a["meta"], "datePublished": a["date"], "dateModified": a["date"],
        "inLanguage": "fr-FR", "url": c.abs("blog/%s/" % a["slug"]),
        "author": {"@type": "Organization", "name": SITE["nom"]},
        "publisher": {"@type": "Organization", "name": SITE["nom"]},
    })
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>%s</h1>
  <p class="page-hero__chapeau">%s</p>
</div></section>
<section class="section section--blanc"><div class="wrap deux-colonnes">
  <article class="article">
    <p class="article__meta">Publié le %s — lecture %d min</p>
    %s
    <p class="pave-chapeau">%s</p>
    %s
    <div class="article__faq">
      <h2>Questions fréquentes</h2>
      %s
    </div>
  </article>
  <div class="colle-laterale">
    <div class="aside-carte">
      <h2>Un débarras à organiser ?</h2>
      <p>Devis gratuit, réponse sous 24 h ouvrées. Envoyez quelques photos : c'est le plus rapide.</p>
      <a class="btn btn--accent" href="%s">%s</a>
      <a class="btn btn--clair" href="tel:%s">Appeler le %s</a>
      <a class="btn btn--clair" href="%s">WhatsApp</a>
    </div>
    <div class="aside-carte">
      <h3>À lire aussi</h3>
      <ul class="liste-simple">%s</ul>
    </div>
  </div>
</div></section>
%s""" % (fil_ariane(c, ariane), esc(a["titre"]), esc(a["date"] and a["meta"]),
         esc(a["date"]), max(2, len(a["sections"]) * 2 + 2),
         figure_illus(c, ILLUS_ARTICLE.get(a["slug"], "camion"), a["titre"],
                      legende="Illustration de démonstration"),
         esc(a["chapeau"]), sections, bloc_faq(a["faq"]),
         c.l("contact-devis/"), esc(CTA["devis"]), SITE["telephone_lien"], esc(SITE["telephone"]),
         SITE["whatsapp_lien"],
         "".join('<li><a href="%s">%s</a></li>' % (c.l("blog/%s/" % x["slug"]), esc(x["titre"]))
                 for x in ARTICLES if x["slug"] != a["slug"]),
         bloc_cta_final(c))
    return page(c, a["title"], a["meta"], corps, ld + jsonld_faq(a["faq"]) + jsonld_ariane(c, ariane))


# ------------------------------------------------------------------ contact
def page_contact(ctx):
    c = ctx
    coordonnees = """<div class="aside-carte">
      <h3>Coordonnées</h3>
      <ul class="liste-simple">
        <li><a href="tel:%s">Téléphone : %s</a></li>
        <li><a href="tel:%s">Mobile : %s</a></li>
        <li><a href="%s">WhatsApp : %s</a></li>
        <li><a href="mailto:%s">%s</a></li>
        <li>Horaires : %s</li>
        <li>Zone : %s</li>
      </ul>
      <p class="aide mt-2">Ces coordonnées sont en cours de validation avec l'entreprise : elles
      correspondent à la maquette de référence et seront remplacées par les numéros définitifs.</p>
    </div>""" % (SITE["telephone_lien"], esc(SITE["telephone"]), SITE["mobile_lien"], esc(SITE["mobile"]),
                 SITE["whatsapp_lien"], esc(SITE["mobile"]), SITE["email"], esc(SITE["email"]),
                 esc(SITE["horaires"]), esc(SITE["zone_texte"]))
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Demander un devis gratuit</h1>
  <p class="page-hero__chapeau">%s</p>
</div></section>
<section class="section section--blanc"><div class="wrap deux-colonnes">
  <div>%s</div>
  <div class="colle-laterale">%s<div class="aside-carte">
      <h3>Vérifier ma zone</h3>
      %s
    </div>
  </div>
</div></section>
%s""" % (fil_ariane(c, [("Accueil", "/"), ("Contact & devis", None)]), esc(CONTACT_INTRO),
         form_complet(c), coordonnees, bloc_zone(c), bloc_cta_final(c))
    return page(c, "Contact et devis gratuit — débarras en Alsace | %s" % SITE["nom"],
                "Demander un devis de débarras gratuit en Alsace : formulaire en 7 étapes avec photos, ou contact direct par téléphone et WhatsApp.",
                corps, jsonld_localbusiness() + jsonld_ariane(c, [("Accueil", "/"), ("Contact & devis", None)]))


# ------------------------------------------------------------------ pages légales + 404
def page_mentions(ctx):
    c = ctx
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Mentions légales</h1>
</div></section>
<section class="section section--blanc"><div class="wrap contenu">
  <div class="notice">Page à compléter : les informations légales définitives (raison sociale, SIRET,
  adresse du siège, responsable de publication, hébergeur) seront renseignées dès réception des
  informations officielles de l'entreprise.</div>
  <h2>Éditeur du site</h2>
  <ul>
    <li>Raison sociale : <strong>%s</strong></li>
    <li>SIRET : %s</li>
    <li>Adresse : %s</li>
    <li>Téléphone : %s</li>
    <li>E-mail : %s</li>
  </ul>
  <h2>Hébergement</h2>
  <p>Site statique hébergé sur GitHub Pages (GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco,
  CA 94107, États-Unis). Aucun traitement serveur des données du visiteur n'est réalisé par ce site.</p>
  <h2>Propriété intellectuelle</h2>
  <p>Les contenus (textes, mise en page, éléments graphiques) sont protégés. Toute reproduction sans
  autorisation est interdite. Les visuels de démonstration utilisés en attendant les photographies réelles
  de l'entreprise ne représentent pas de chantier de l'entreprise.</p>
  <h2>Responsabilité</h2>
  <p>Les informations publiées sur ce site (prestations, méthode, facteurs de prix) sont fournies à titre
  indicatif. Seul le devis signé engage les parties.</p>
</div></section>""" % (fil_ariane(c, [("Accueil", "/"), ("Mentions légales", None)]),
                       esc(SITE["raison_sociale"]), esc(SITE["siret"]), esc(SITE["adresse"]),
                       esc(SITE["telephone"]), esc(SITE["email"]))
    return page(c, "Mentions légales | %s" % SITE["nom"],
                "Mentions légales du site de débarras à Strasbourg et en Alsace.", corps)


def page_confidentialite(ctx):
    c = ctx
    corps = """<section class="page-hero"><div class="wrap">
  %s
  <h1>Politique de confidentialité</h1>
</div></section>
<section class="section section--blanc"><div class="wrap contenu">
  <h2 class="mt-0">Quelles données sont collectées</h2>
  <p>Le formulaire de devis vous demande : type de débarras, localisation, volume estimé, accès, délai,
  coordonnées et éventuellement des photos. Ces informations servent uniquement à répondre à votre demande
  et à établir un devis.</p>
  <h2>Comment elles sont traitées</h2>
  <p>Dans cette version du site, le formulaire prépare votre demande et l'envoie depuis <em>votre</em>
  messagerie : aucune donnée n'est stockée sur un serveur du site. Les photos que vous sélectionnez restent
  sur votre appareil tant que vous ne les joignez pas vous-même à votre message ou à votre envoi WhatsApp.</p>
  <p>Lorsque l'envoi direct sera mis en service, les données seront transmises par e-mail à l'entreprise et
  conservées le temps nécessaire au traitement de la demande, puis supprimées sur simple demande.</p>
  <h2>Cookies</h2>
  <p>Ce site ne dépose aucun cookie publicitaire ni traceur tiers. Un outil de mesure d'audience pourra être
  ajouté ultérieurement ; il sera alors soumis à votre consentement explicite.</p>
  <h2>Vos droits</h2>
  <p>Vous pouvez demander l'accès, la rectification ou la suppression des informations que vous nous avez
  transmises, en écrivant à %s. Nous répondons dans les meilleurs délais.</p>
  <h2>Contact</h2>
  <p>%s — %s</p>
</div></section>""" % (fil_ariane(c, [("Accueil", "/"), ("Politique de confidentialité", None)]),
                       esc(SITE["email"]), esc(SITE["nom"]), esc(SITE["adresse"]))
    return page(c, "Politique de confidentialité | %s" % SITE["nom"],
                "Politique de confidentialité : quelles données sont collectées par le formulaire de devis et comment elles sont utilisées.", corps)


def page_404(ctx):
    c = ctx
    corps = """<section class="page-hero"><div class="wrap">
  <h1>Cette page n'existe pas (ou plus)</h1>
  <p class="page-hero__chapeau">Le lien est peut-être incomplet. Voici les pages les plus utiles :</p>
  <div class="page-hero__actions">%s</div>
</div></section>
<section class="section section--blanc"><div class="wrap">
  %s
</div></section>""" % (_cta_devis(c), cartes_services(c, SERVICES_ACCUEIL[:4], colonnes=4))
    return page(c, "Page introuvable | %s" % SITE["nom"],
                "Page introuvable. Retrouvez nos prestations de débarras et nos zones d'intervention en Alsace.", corps)
