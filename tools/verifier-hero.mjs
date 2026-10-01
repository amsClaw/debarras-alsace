// H12 : géométrie réelle et contraste pixel par pixel sur le rendu Chromium.
// node tools/verifier-hero.mjs ; --servir pour rejouer le parcours filmé sur le même site.
// Playwright vient de l'image de recette, jamais des dépendances du produit.
import { createServer } from "node:http";
import { readFile, mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";

const racine = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const dossier = path.join(racine, "docs/captures");
const types = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".jpg": "image/jpeg", ".png": "image/png", ".woff2": "font/woff2" };
const serveur = createServer(async (req, res) => {
  let nom = decodeURIComponent(new URL(req.url, "http://localhost").pathname).replace(/^\/debarras-alsace(?=\/|$)/, "");
  if (nom === "/" || nom === "") nom = "/index.html";
  const fichier = path.resolve(racine, "." + nom);
  if (!fichier.startsWith(racine + path.sep)) { res.writeHead(403).end(); return; }
  try {
    const contenu = await readFile(fichier);
    res.writeHead(200, { "Content-Type": types[path.extname(fichier)] ?? "application/octet-stream" }).end(contenu);
  } catch {
    res.writeHead(404, { "Content-Type": "text/html" }).end(await readFile(path.join(racine, "404.html")));
  }
});
await new Promise((resolve) => serveur.listen(8080, "127.0.0.1", resolve));
const base = "http://127.0.0.1:8080/debarras-alsace/";
if (process.argv.includes("--servir")) {
  console.log(`Site prêt : ${base}`);
} else {
  let paquet;
  try { paquet = await import("playwright"); }
  catch { paquet = await import("/usr/local/lib/node_modules/playwright/index.js"); }
  const navigateur = await (paquet.default ?? paquet).chromium.launch();
  const rapport = { mesures: [], contrastes: [], maquettes: [] };
  const proche = (a, b) => Math.abs(a - b) <= 1;
  async function ouvrir(page) {
    await page.goto(base, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);
  }
  async function mesurer(page) {
    return page.evaluate(() => {
      const rect = (sel) => {
        const r = document.querySelector(sel).getBoundingClientRect();
        return { x: r.x, right: r.right, top: r.top + scrollY, bottom: r.bottom + scrollY, height: r.height, width: r.width };
      };
      return {
        largeur: innerWidth, document: document.documentElement.scrollWidth,
        entete: rect(".entete"), hero: rect(".hero"), grille: rect(".hero-grille"),
        photo: rect(".hero-photo"), titre: rect(".hero-titre"), badge: rect(".pastille"),
        texte: rect(".hero-texte"), garanties: rect(".reassurances"), devis: rect("#devis"),
        bouton: rect('.hero-boutons a[href="#devis"]'),
        limiteVisible: innerWidth < 768 ? rect(".barre-mobile").top : innerHeight,
        photoChargee: document.querySelector(".hero-photo").naturalWidth > 0,
        gapEntete: getComputedStyle(document.querySelector(".entete-devis")).gap,
        badgeTexte: document.querySelector(".pastille").textContent,
        couleurTitre: getComputedStyle(document.querySelector(".hero-titre")).color,
        couleurParagraphe: getComputedStyle(document.querySelector(".hero-paragraphe")).color,
      };
    });
  }
  function verifier(m) {
    const prefixe = `${m.largeur}px`;
    assert.equal(m.document, m.largeur, `${prefixe} : débordement horizontal`);
    assert.ok(m.photoChargee, `${prefixe} : photo non chargée`);
    assert.ok(proche(m.photo.width, m.largeur), `${prefixe} : photo pas pleine largeur`);
    assert.ok(proche(m.photo.top, m.entete.bottom), `${prefixe} : vide sous l’en-tête`);
    assert.equal(m.gapEntete, "0px", `${prefixe} : espace du bouton d’en-tête`);
    assert.match(m.badgeTexte, /, Bas\u2011Rhin$/);
    assert.equal(m.couleurTitre, "rgb(255, 255, 255)");
    assert.ok(m.devis.top >= m.entete.bottom && m.devis.bottom <= m.hero.bottom, `${prefixe} : devis hors du héros`);
    if (m.largeur < 900) {
      assert.equal(m.photo.height, 340);
      assert.ok(m.badge.top >= m.photo.top && m.titre.bottom <= m.photo.bottom, `${prefixe} : titre/badge hors photo`);
      assert.ok(m.texte.top >= m.photo.bottom + 24, `${prefixe} : texte hors fond clair`);
      assert.ok(m.devis.top >= m.garanties.bottom + 32, `${prefixe} : devis avant garanties`);
      if (m.largeur === 375) assert.ok(m.bouton.bottom <= m.limiteVisible, `${prefixe} : bouton masqué au premier écran`);
      assert.equal(m.couleurParagraphe, "rgb(61, 65, 58)");
    } else {
      assert.ok(proche(m.photo.height, m.hero.height), `${prefixe} : photo ne couvre pas le héros`);
      assert.ok(m.devis.x >= m.texte.right + 47, `${prefixe} : carte superposée au texte`);
      const centreGrille = (m.hero.top + 56 + m.hero.bottom - 72) / 2;
      assert.ok(proche((m.devis.top + m.devis.bottom) / 2, centreGrille), `${prefixe} : devis pas centré verticalement`);
      assert.equal(m.couleurParagraphe, "rgb(255, 255, 255)");
    }
    assert.ok(proche(m.grille.width, Math.min(1200, m.largeur - (m.largeur < 600 ? 32 : m.largeur < 1200 ? 48 : 0))), `${prefixe} : grille non conforme`);
  }
  async function contraste(page, largeur) {
    // Les rectangles de CHAQUE ligne de texte sont lus avant de rendre son encre transparente.
    // La seconde capture conserve photo, dégradé et badge : ses pixels sont le vrai fond rendu,
    // y compris les coins les plus lumineux (aucune moyenne, aucune couleur CSS théorique).
    const zones = await page.evaluate(() => {
      const selectors = innerWidth < 900 ? [".pastille", ".hero-titre"] : [".pastille", ".hero-titre", ".hero-paragraphe", ".hero-boutons .bouton-contour", ".reassurances li span"];
      return selectors.flatMap((sel) => [...document.querySelectorAll(sel)].map((el) => {
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        const rectangles = [];
        while (walker.nextNode()) {
          if (!walker.currentNode.textContent.trim()) continue;
          const range = document.createRange(); range.selectNodeContents(walker.currentNode);
          rectangles.push(...[...range.getClientRects()].map((r) => ({ x: r.x, y: r.y, right: r.right, bottom: r.bottom })));
        }
        return { nom: el.textContent.trim().replace(/\s+/g, " "), rectangles };
      }));
    });
    const style = await page.addStyleTag({ content: ".hero-texte,.hero-texte *{color:transparent!important;text-shadow:none!important}" });
    const png = (await page.screenshot()).toString("base64");
    await style.evaluate((el) => el.remove());
    const resultats = await page.evaluate(async ({ png, zones }) => {
      const image = new Image(); image.src = "data:image/png;base64," + png; await image.decode();
      const canvas = document.createElement("canvas"); canvas.width = image.width; canvas.height = image.height;
      const ctx = canvas.getContext("2d"); ctx.drawImage(image, 0, 0);
      const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
      const lineariser = (c) => { c /= 255; return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; };
      return zones.map(({ nom, rectangles }) => {
        let minimum = Infinity, echantillons = 0;
        for (const r of rectangles) {
          if (r.bottom > canvas.height || r.x < 0 || r.right > canvas.width) throw new Error(`Texte hors capture : ${nom}`);
          for (let y = Math.max(0, Math.floor(r.y)); y < Math.ceil(r.bottom); y++) {
            for (let x = Math.floor(r.x); x < Math.ceil(r.right); x++) {
              const i = (y * canvas.width + x) * 4;
              const luminance = .2126 * lineariser(pixels[i]) + .7152 * lineariser(pixels[i + 1]) + .0722 * lineariser(pixels[i + 2]);
              minimum = Math.min(minimum, 1.05 / (luminance + .05)); echantillons++;
            }
          }
        }
        return { nom, minimum: Number(minimum.toFixed(3)), echantillons };
      });
    }, { png, zones });
    for (const r of resultats) assert.ok(r.echantillons > 0 && r.minimum >= 4.5, `${largeur}px : contraste ${r.minimum} pour ${r.nom}`);
    rapport.contrastes.push({ largeur, zones: resultats });
  }
  try {
    await mkdir(dossier, { recursive: true });
    for (const largeur of [320, 360, 375, 390, 414, 599, 600, 768, 899, 900, 1024, 1199, 1200, 1280, 1440, 1441, 1920]) {
      const hauteur = largeur === 375 ? 812 : largeur === 1280 ? 860 : 900;
      const page = await navigateur.newPage({ viewport: { width: largeur, height: hauteur } });
      await ouvrir(page);
      const m = await mesurer(page); verifier(m);
      rapport.mesures.push({ largeur, hauteur, photo: m.photo.height, devisHaut: m.devis.top, devisBas: m.devis.bottom, boutonBas: m.bouton.bottom });
      if ([375, 1280, 1440].includes(largeur)) {
        await page.screenshot({ path: path.join(dossier, `h12-${largeur}.png`) });
        await contraste(page, largeur);
      }
      // Le même devis en 3 étapes : aucune position absolue ni hauteur figée pour la carte.
      await page.locator("#devis-cp").fill("67000");
      for (let etape = 2; etape <= 3; etape++) {
        await page.locator(".devis-continuer").click();
        verifier(await mesurer(page));
      }
      await page.close();
      const contexte = await navigateur.newContext({ javaScriptEnabled: false, viewport: { width: largeur, height: hauteur } });
      const sansJS = await contexte.newPage(); await ouvrir(sansJS); verifier(await mesurer(sansJS));
      assert.equal(await sansJS.locator(".devis-etape:visible").count(), 3);
      await contexte.close();
    }
    const page = await navigateur.newPage();
    // Lecture raster des quatre références obligatoires, conservées à côté des captures H12.
    for (const nom of ["C-ordinateur-1280.jpg", "C-grand-ecran-1440.jpg", "D-telephone-haut.jpg", "D-telephone-devis.jpg"]) {
      await page.goto(base);
      const reference = await page.evaluate(async (url) => {
        const image = new Image(); image.src = url; await image.decode();
        const canvas = document.createElement("canvas"); canvas.width = image.width; canvas.height = image.height;
        const ctx = canvas.getContext("2d"); ctx.drawImage(image, 0, 0);
        const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
        // Bornes de la longue zone blanche de la carte dans les maquettes C (fond photo sombre).
        const x = Math.floor(image.width * .75), lignesBlanches = [];
        for (let y = 90; y < Math.min(800, image.height); y++) {
          const i = (y * image.width + x) * 4;
          if (pixels[i] > 248 && pixels[i + 1] > 248 && pixels[i + 2] > 248) lignesBlanches.push(y);
        }
        return { width: image.width, height: image.height, lignesBlanches: lignesBlanches.length };
      }, base + "docs/maquette-hero/" + nom);
      rapport.maquettes.push({ nom, ...reference });
    }
    await page.close();
    await writeFile(path.join(dossier, "h12-verification.json"), JSON.stringify(rapport, null, 2) + "\n");
    console.log(JSON.stringify(rapport));
    console.log("H12 : géométrie, 3 étapes, repli sans JS et contraste raster conformes.");
  } finally {
    await navigateur.close(); await new Promise((resolve) => serveur.close(resolve));
  }
}
