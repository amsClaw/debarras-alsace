// Tests du socle V3 (histoire 1) : paquet npm, outils de test, jetons de design,
// squelette de page et interdits de contenu.
//
// Lancement : `npm test`, soit `node --test tests/*.test.mjs`.
// Le motif glob désigne le dossier `tests/` : sur Node 22, un dossier passé en
// argument est résolu comme un module à charger au lieu d'être exploré
// (nodejs/node#64555), donc la forme `node --test tests/` échoue en MODULE_NOT_FOUND.

import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";

import { lire, compter, RACINE } from "./outils.mjs";

// Lecture mémoïsée : un fichier manquant fait échouer le test qui l'utilise,
// sans empêcher la collecte des autres tests.
const cache = new Map();
function texte(chemin) {
  if (!cache.has(chemin)) cache.set(chemin, lire(chemin));
  return cache.get(chemin);
}

/** Feuille de style sans ses commentaires (pour ne pas tester du texte commenté). */
function cssUtile() {
  return texte("v3/assets/style.css").replace(/\/\*[\s\S]*?\*\//g, "");
}

test("package.json : privé, module ES, script de test, aucune dépendance", () => {
  const pkg = JSON.parse(texte("package.json"));

  assert.equal(pkg.private, true, "le paquet doit être marqué private");
  assert.equal(pkg.type, "module", "le paquet doit être en modules ES");
  assert.equal(
    pkg.scripts?.test,
    "node --test tests/*.test.mjs",
    "le script test doit lancer le runner Node sur tests/ (motif glob : un dossier en argument est cassé sur Node 22)"
  );

  for (const champ of ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]) {
    assert.equal(pkg[champ], undefined, `aucune dépendance n'est attendue (${champ})`);
  }
});

test("tests/outils.mjs : lire() lit depuis la racine du dépôt, compter() compte juste", async () => {
  const outils = await import("./outils.mjs");

  assert.equal(typeof outils.lire, "function", "lire() doit être exporté");
  assert.equal(typeof outils.compter, "function", "compter() doit être exporté");

  assert.match(outils.lire("v3/index.html"), /<html lang="fr">/);
  assert.match(outils.lire("package.json"), /"private": true/);

  assert.equal(outils.compter("ababab", "ab"), 3, "chaîne répétée");
  assert.equal(outils.compter("a.b.c", "."), 2, "une chaîne est comparée littéralement, pas comme un motif");
  assert.equal(outils.compter("aaa", "b"), 0, "motif absent");
  assert.equal(outils.compter("x1y2z3", /\d/), 3, "motif sans drapeau /g");
  assert.equal(outils.compter("x1y2z3", /\d/g), 3, "motif avec drapeau /g");
});

test("v3/index.html : en-tête de document complet et polices de la maquette", () => {
  const page = texte("v3/index.html");

  assert.match(page, /^<!doctype html>/i, "la page commence par un doctype");
  assert.match(page, /<html lang="fr">/, "la page est déclarée en français");
  assert.match(page, /<meta charset="utf-8">/i, "l'encodage est déclaré");
  assert.match(
    page,
    /<meta name="viewport" content="width=device-width, initial-scale=1">/,
    "la balise viewport mobile est attendue"
  );

  const titre = page.match(/<title>([\s\S]*?)<\/title>/);
  assert.ok(titre, "un <title> est attendu");
  assert.ok(titre[1].trim().length > 0, "le <title> ne doit pas être vide");

  const description = page.match(/<meta name="description" content="([^"]*)">/);
  assert.ok(description, "une <meta name=\"description\"> est attendue");
  assert.ok(description[1].trim().length > 0, "la description ne doit pas être vide");

  const polices = page.match(/https:\/\/fonts\.googleapis\.com\/css2\?[^"]+/);
  assert.ok(polices, "le lien Google Fonts est attendu");
  assert.match(
    polices[0],
    /family=Fraunces:ital,opsz,wght@0,9\.\.144,500;0,9\.\.144,600;1,9\.\.144,500/,
    "Fraunces 500/600 + italique 500, comme la maquette"
  );
  assert.match(
    polices[0],
    /family=Public\+Sans:wght@400;500;600;700/,
    "Public Sans 400 à 700, comme la maquette"
  );
});

test("v3/index.html : feuille de style puis config.js (defer) puis site.js (module)", () => {
  const page = texte("v3/index.html");

  assert.match(page, /<link rel="stylesheet" href="assets\/style\.css">/, "la feuille de style est liée");

  const baliseConfig = page.match(/<script[^>]*src="assets\/config\.js"[^>]*>/);
  assert.ok(baliseConfig, "config.js doit être chargé");
  assert.ok(/defer/.test(baliseConfig[0]), "config.js doit être chargé en defer");
  assert.ok(
    !/type="module"/.test(baliseConfig[0]),
    "config.js est un script classique : il doit rester utilisable si les modules échouent"
  );

  assert.match(
    page,
    /<script type="module" src="assets\/site\.js"><\/script>/,
    "site.js doit être chargé en module ES (fonctions pures importables par les tests)"
  );

  const positionCss = page.indexOf("assets/style.css");
  const positionConfig = page.indexOf("assets/config.js");
  const positionSite = page.indexOf("assets/site.js");
  assert.ok(
    positionCss < positionConfig && positionConfig < positionSite,
    "l'ordre attendu est : style.css, puis config.js, puis site.js"
  );
});

test("v3/assets/style.css : les jetons du « Système visuel » sont sur :root", () => {
  const racine = cssUtile().match(/:root\{([\s\S]*?)\}/);
  assert.ok(racine, "un bloc :root est attendu");

  const attendus = {
    "--vert": "#1E3A2B",
    "--vert-2": /#2F5A40|#2A4A37/,
    "--papier": "#F5F0E6",
    "--papier-2": "#EDE5D5",
    "--encre": "#1F221E",
    "--texte-2": "#3D413A",
    "--discret": "#5B5F57",
    "--brique": "#B5461B",
    "--trait": /#D6CCB6|#E2D9C6/,
    "--titres": /Fraunces/,
    "--texte": /Public Sans/
  };

  for (const [jeton, attendu] of Object.entries(attendus)) {
    const declaration = racine[1].match(new RegExp(`${jeton.replace(/-/g, "\\-")}\\s*:\\s*([^;]+);`));
    assert.ok(declaration, `le jeton ${jeton} doit être défini sur :root`);

    const valeur = declaration[1].trim();
    if (attendu instanceof RegExp) {
      assert.match(valeur, attendu, `valeur inattendue pour ${jeton} : ${valeur}`);
    } else {
      assert.equal(
        valeur.toUpperCase(),
        attendu.toUpperCase(),
        `valeur inattendue pour ${jeton} : ${valeur}`
      );
    }
  }
});

test("v3/assets/style.css : page en Public Sans sur fond papier, conteneur 1200 px responsive", () => {
  const feuille = cssUtile();

  const corps = feuille.match(/body\{[^}]*\}/);
  assert.ok(corps, "une règle body est attendue");
  assert.match(corps[0], /font-family:var\(--texte\)/, "le corps de page est en Public Sans (--texte)");
  assert.match(corps[0], /background:var\(--papier\)/, "le fond de page est le papier (--papier)");

  // Comparaison sur la feuille sans espaces : elle reste lisible pour un humain
  // tout en rendant le contrôle insensible au formatage.
  const compact = feuille.replace(/\s+/g, "");
  assert.match(compact, /\.conteneur\{[^}]*max-width:1200px/, "le conteneur est limité à 1200 px");
  assert.match(
    compact,
    /@media\(max-width:767(\.98)?px\)\{\.conteneur\{[^}]*padding:016px/,
    "16 px de marge latérale sous 768 px"
  );
  assert.match(
    compact,
    /@media\(min-width:144[01]px\)\{\.conteneur\{[^}]*padding:0120px/,
    "120 px de marge latérale au-delà de 1440 px"
  );
});

test("v3/assets/config.js : les coordonnées sont centralisées dans window.DEBARRAS", () => {
  const source = texte("v3/assets/config.js");

  assert.match(source, /window\.DEBARRAS\s*=/, "window.DEBARRAS doit être défini");
  assert.match(source, /seul endroit/i, "un commentaire doit dire que c'est le seul endroit à modifier");

  const fenetre = {};
  new Function("window", source)(fenetre);
  assert.deepEqual(fenetre.DEBARRAS, {
    tel: "[06 XX XX XX XX]",
    telInternational: "33000000000",
    whatsapp: "33000000000",
    mail: "[contact@domaine.fr]"
  });
});

test("v3/index.html : en-tête, un seul h1 dans <main>, pied de page complet", () => {
  const page = texte("v3/index.html");

  const entete = page.match(/<header[\s\S]*?<\/header>/);
  assert.ok(entete, "un <header> est attendu");
  assert.match(entete[0], /<svg/, "le logo maison (SVG) est attendu dans l'en-tête");
  assert.match(entete[0], /Débarras Alsace/, "le nom de l'entreprise est attendu dans l'en-tête");
  assert.match(entete[0], /Strasbourg &amp; toute l'Alsace/, "la zone couverte est attendue dans l'en-tête");

  assert.equal(compter(page, /<h1[\s>]/), 1, "la page ne doit contenir qu'un seul <h1>");

  const contenu = page.match(/<main[\s\S]*?<\/main>/);
  assert.ok(contenu, "un <main> est attendu");
  assert.equal(compter(contenu[0], /<h1[\s>]/), 1, "le <h1> doit être dans <main>");
  assert.match(contenu[0], /<h1[^>]*>\s*\S/, "le <h1> provisoire ne doit pas être vide");

  const pied = page.match(/<footer[\s\S]*?<\/footer>/);
  assert.ok(pied, "un <footer> est attendu");
  assert.match(pied[0], /\[Raison sociale\]/, "l'emplacement [Raison sociale] est attendu");
  assert.match(pied[0], /\[SIRET\]/, "l'emplacement [SIRET] est attendu");

  assert.ok(
    page.indexOf("<header") < page.indexOf("<main") && page.indexOf("<main") < page.indexOf("<footer"),
    "l'ordre attendu est : en-tête, contenu, pied de page"
  );
});

test("v3/ : aucune fausse preuve sociale (note, nombre d'avis, étoiles)", () => {
  // Les motifs sont assemblés à l'exécution : les mots recherchés n'apparaissent
  // donc nulle part dans le dépôt, et un grep de contrôle — sur v3/ ou sur tout le
  // dépôt — reste exploitable au lieu de tomber sur ce fichier de test.
  const motifsInterdits = [
    ...["4,0", "4,9"].map((note) => note + "/5"),
    "150" + "+ avis",
    "étoi" + "les"
  ];

  const fichiers = [];
  (function parcourir(dossier) {
    for (const entree of readdirSync(dossier, { withFileTypes: true })) {
      const chemin = path.join(dossier, entree.name);
      if (entree.isDirectory()) parcourir(chemin);
      else if (/\.(html|css|js|mjs|json|svg|txt|md)$/.test(entree.name)) fichiers.push(chemin);
    }
  })(path.join(RACINE, "v3"));

  assert.ok(fichiers.length > 0, "v3/ doit contenir au moins un fichier texte à contrôler");

  for (const fichier of fichiers) {
    const contenu = readFileSync(fichier, "utf8");
    for (const motif of motifsInterdits) {
      assert.equal(
        compter(contenu, motif),
        0,
        `${path.relative(RACINE, fichier)} ne doit pas contenir « ${motif} » (rien d'inventé)`
      );
    }
  }
});
