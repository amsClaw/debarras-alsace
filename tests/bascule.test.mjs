// Histoire 8 : la V3 devient le site — pages à la racine, V1/V2 retirées,
// plan du site et robots.txt à jour.
import test from "node:test";
import assert from "node:assert/strict";
import { existsSync, readdirSync } from "node:fs";
import path from "node:path";
import { lire, RACINE, PAGES_SITE } from "./outils.mjs";

const BASE = "https://amsclaw.github.io/debarras-alsace/";

/** Tous les fichiers du dépôt (hors .git et node_modules), chemins relatifs à la racine. */
function fichiersDuDepot() {
  const resultat = [];
  (function parcourir(dossier) {
    for (const entree of readdirSync(dossier, { withFileTypes: true })) {
      if ([".git", "node_modules", ".worktrees"].includes(entree.name)) continue;
      const chemin = path.join(dossier, entree.name);
      if (entree.isDirectory()) parcourir(chemin);
      else resultat.push(path.relative(RACINE, chemin).split(path.sep).join("/"));
    }
  })(RACINE);
  return resultat;
}

test("bascule : les pages du site sont à la racine et le dossier v3/ n'existe plus", () => {
  for (const nom of PAGES_SITE) assert.ok(existsSync(path.join(RACINE, nom)), `${nom} à la racine`);
  for (const fichier of ["config.js", "site.js", "style.css", "message.js", "etapes.js", "volume.js", "zone.js"]) {
    assert.ok(existsSync(path.join(RACINE, "assets", fichier)), `assets/${fichier}`);
  }
  assert.equal(existsSync(path.join(RACINE, "v3")), false, "v3/ supprimé");
});

test("bascule : seules les quatre pages du site, les maquettes et le cahier de recette HTML existent", () => {
  const html = fichiersDuDepot().filter((f) => f.endsWith(".html"));
  const intrus = html.filter((f) => !PAGES_SITE.includes(f) && f !== "CAHIER_DE_RECETTE.html" && !f.startsWith("docs/design/"));
  assert.deepEqual(intrus, []);
  for (const nom of PAGES_SITE) assert.ok(html.includes(nom));
});

test("bascule : V1, V2 et leurs outils de génération sont retirés, les outils photo conservés", () => {
  const retires = [
    "a-propos", "avis-clients", "blog", "contact-devis", "faq", "mentions-legales", "politique-confidentialite",
    "realisations", "services", "situations", "tarifs", "villes", "src", "v2", "v2_src",
    "tools/build.py", "tools/build_v2.py", "tools/smoke.py", "tools/mesurer-v3.mjs", "assets/app.js"
  ];
  for (const chemin of retires) assert.equal(existsSync(path.join(RACINE, chemin)), false, `${chemin} retiré`);
  for (const chemin of ["docs", "source-client", "tools/generer_photos.py", "tools/photos.sh", "tools/mesurer-site.mjs"]) {
    assert.ok(existsSync(path.join(RACINE, chemin)), `${chemin} conservé`);
  }
});

test("sitemap.xml : uniquement l'accueil et les deux pages légales, chacune existante", () => {
  const sitemap = lire("sitemap.xml");
  const adresses = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(([, loc]) => loc);
  assert.deepEqual(adresses, [BASE, `${BASE}mentions-legales.html`, `${BASE}confidentialite.html`]);
  for (const adresse of adresses) {
    const fichier = adresse.slice(BASE.length) || "index.html";
    assert.ok(existsSync(path.join(RACINE, fichier)), `${fichier} existe`);
  }
});

test("robots.txt référence le plan du site ; l'accueil est indexable", () => {
  const robots = lire("robots.txt");
  assert.match(robots, new RegExp(`^Sitemap: ${BASE.replace(/[.]/g, "\\.")}sitemap\\.xml$`, "m"));
  assert.doesNotMatch(robots, /^Disallow:\s*\/\s*$/m, "le site n'est pas fermé aux robots");
  assert.doesNotMatch(lire("index.html"), /noindex/i, "aucune balise noindex sur l'accueil");
});
