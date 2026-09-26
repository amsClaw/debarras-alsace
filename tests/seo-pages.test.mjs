// Vérifications de préparation SEO, médias et pages annexes de la V3.
import test from "node:test";
import assert from "node:assert/strict";
import { readdirSync, statSync } from "node:fs";
import path from "node:path";
import { lire, RACINE } from "./outils.mjs";

const page = lire("index.html");
const config = lire("assets/config.js");
const htmlPages = readdirSync(RACINE).filter((nom) => nom.endsWith(".html"));

function meta(propriete) {
  return page.match(new RegExp(`<meta\\s+property="${propriete}"\\s+content="([^"]+)"`))?.[1];
}

test("SEO et Open Graph : titre, description, image, langue et canonical commenté", () => {
  const titre = page.match(/<title>([^<]+)<\/title>/)?.[1];
  const description = page.match(/<meta name="description" content="([^"]+)"/)?.[1];
  assert.ok(titre);
  assert.ok(titre.length <= 60);
  assert.match(titre, /Débarras/i);
  assert.match(titre, /Strasbourg/i);
  assert.ok(description && description.length >= 120 && description.length <= 160);
  assert.equal(meta("og:title"), titre);
  assert.equal(meta("og:description"), description);
  assert.equal(meta("og:image"), "assets/photos/hero.jpg");
  assert.equal(meta("og:locale"), "fr_FR");
  assert.match(page, /<link rel="canonical" href="https:\/\/\[domaine-du-site\]\/">/);
  assert.match(page, /Remplacer l'emplacement par le domaine officiel/);
  assert.match(page, /fonts\.googleapis\.com/);
  assert.match(page, /fonts\.gstatic\.com/);
  assert.match(page, /display=swap/);
});

test("JSON-LD LocalBusiness : données de zone, téléphone configuré et horaires sans avis", () => {
  const json = page.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)?.[1];
  assert.ok(json);
  const donnees = JSON.parse(json);
  assert.equal(donnees["@type"], "LocalBusiness");
  assert.equal(donnees.name, "Débarras Alsace");
  const telephoneConfig = config.match(/telInternational:\s*"([^"]+)"/)?.[1];
  assert.ok(telephoneConfig);
  assert.equal(donnees.telephone, telephoneConfig);
  assert.deepEqual(donnees.areaServed.map((zone) => zone.name), ["Bas-Rhin", "Haut-Rhin"]);
  const horaires = donnees.openingHoursSpecification[0];
  assert.deepEqual(horaires.dayOfWeek, ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]);
  assert.equal(horaires.opens, "08:00");
  assert.equal(horaires.closes, "19:00");
  assert.equal("aggregateRating" in donnees, false);
  assert.equal("review" in donnees, false);
});

test("images : chargement différé, dimensions explicites et héros prioritaire", () => {
  const images = [...page.matchAll(/<img\b[^>]*>/g)].map(([balise]) => balise);
  assert.ok(images.length > 1);
  const heros = images.filter((image) => /class="hero-photo"/.test(image));
  assert.equal(heros.length, 1);
  assert.match(heros[0], /fetchpriority="high"/);
  for (const image of images.filter((element) => !/class="hero-photo"/.test(element))) {
    assert.match(image, /loading="lazy"/);
    assert.match(image, /\bwidth="\d+"/);
    assert.match(image, /\bheight="\d+"/);
  }
});

test("poids cumulé des photos V3 inférieur ou égal à 1,5 Mo", () => {
  const dossier = path.join(RACINE, "assets/photos");
  const taille = readdirSync(dossier).reduce((total, nom) => total + statSync(path.join(dossier, nom)).size, 0);
  assert.ok(taille <= 1_500_000, `poids constaté : ${taille} octets`);
});

test("pages légales adaptées au style V3 et page 404 avec retour accueil", () => {
  const mentions = lire("mentions-legales.html");
  const confidentialite = lire("confidentialite.html");
  const erreur = lire("404.html");
  for (const legal of [mentions, confidentialite]) {
    assert.match(legal, /class="entete"/);
    assert.match(legal, /class="pied"/);
    assert.match(legal, /page-legale-contenu/);
  }
  for (const emplacement of ["[raison sociale]", "[adresse complète]", "[nom du représentant légal]", "[adresse e-mail]"]) {
    assert.ok(mentions.includes(emplacement) || confidentialite.includes(emplacement), `emplacement légal conservé : ${emplacement}`);
  }
  assert.match(erreur, /<h1>Cette page n'existe pas\.<\/h1>/);
  assert.match(erreur, /href="index\.html"[^>]*>Retour à l'accueil/);
});

test("tous les liens internes des pages HTML V3 pointent vers un fichier ou une ancre existante", () => {
  for (const nom of htmlPages) {
    const html = lire(`${nom}`);
    const source = path.join(RACINE, nom);
    const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]));
    const ancres = new Set([...html.matchAll(/<a\b[^>]*name="([^"]+)"/g)].map((match) => match[1]));
    for (const [, href] of html.matchAll(/<a\b[^>]*href="([^"]*)"/g)) {
      if (!href || href.startsWith("//") || /^[a-z][a-z\d+.-]*:/i.test(href)) continue;
      const [chemin, fragment] = href.split("#", 2);
      if (fragment && !chemin) {
        assert.ok(ids.has(decodeURIComponent(fragment)) || ancres.has(decodeURIComponent(fragment)), `${nom}: ancre #${fragment} absente`);
        continue;
      }
      if (!chemin) continue;
      const destination = path.resolve(path.dirname(source), decodeURIComponent(chemin.split("?")[0]));
      const fichier = destination.endsWith(path.sep) ? path.join(destination, "index.html") : destination;
      assert.ok(statSync(fichier, { throwIfNoEntry: false })?.isFile(), `${nom}: cible interne absente (${href})`);
      if (fragment && fichier.endsWith(".html")) {
        const cible = lire(path.relative(RACINE, fichier));
        const cibles = new Set([...cible.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]));
        assert.ok(cibles.has(decodeURIComponent(fragment)), `${nom}: ancre cible absente (${href})`);
      }
    }
  }
});

test("aucun fichier HTML hors des quatre pages du site et de docs/design/", () => {
  const attendues = new Set(["index.html", "mentions-legales.html", "confidentialite.html", "404.html"]);
  const trouvees = [];
  (function parcourir(dossier, relatif) {
    for (const entree of readdirSync(dossier, { withFileTypes: true })) {
      if (relatif === "" && [".git", "node_modules"].includes(entree.name)) continue;
      const chemin = path.join(dossier, entree.name);
      const cheminRelatif = relatif ? `${relatif}/${entree.name}` : entree.name;
      if (entree.isDirectory()) {
        if (cheminRelatif === "docs/design") continue;
        parcourir(chemin, cheminRelatif);
      } else if (entree.name.endsWith(".html")) {
        trouvees.push(cheminRelatif);
      }
    }
  })(RACINE, "");

  const inattendues = trouvees.filter((chemin) => !attendues.has(chemin));
  assert.deepEqual(inattendues, [], `fichiers HTML inattendus : ${inattendues.join(", ")}`);
});
