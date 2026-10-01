// Mesures réelles du site (créé par H10), hors npm test et sans dépendance du produit.
// node tools/mesurer-site.mjs [--capturer=avant|apres] [--paliers]
// Playwright installé dans l'environnement de recette ; aucun navigateur téléchargé.
import { createServer } from "node:http";
import { readFile, mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const racine = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const largeurs = [320, 360, 375, 390, 414, 768, 1024, 1280, 1440, 1920];
// Vérifications additionnelles au voisinage exact des changements de mise en page.
if (process.argv.includes("--paliers")) largeurs.push(599, 600, 899, 900, 1199, 1200, 1279, 1441);
largeurs.sort((a, b) => a - b);
const capture = process.argv.find((arg) => arg.startsWith("--capturer="))?.split("=")[1];
if (capture && !["avant", "apres"].includes(capture)) throw new Error("Capture : avant ou apres attendu");
let paquet;
try { paquet = await import("playwright"); }
catch { paquet = await import("/usr/local/lib/node_modules/playwright/index.js"); }
const { chromium } = paquet.default ?? paquet;
const types = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".jpg": "image/jpeg", ".woff2": "font/woff2" };
const serveur = createServer(async (req, res) => {
  const chemin = path.resolve(racine, "." + decodeURIComponent(new URL(req.url, "http://localhost").pathname));
  if (!chemin.startsWith(racine + path.sep)) { res.writeHead(403).end(); return; }
  try {
    const donnees = await readFile(chemin);
    res.writeHead(200, { "Content-Type": types[path.extname(chemin)] ?? "application/octet-stream" }).end(donnees);
  } catch { res.writeHead(404).end(); }
});
await new Promise((resolve) => serveur.listen(0, "127.0.0.1", resolve));
const base = `http://127.0.0.1:${serveur.address().port}/`;
const navigateur = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
const erreurs = [];
const sorties = [];
const verifier = (ok, message) => { if (!ok) erreurs.push(message); };

async function ouvrir(page, nom = "index.html") {
  await page.goto(base + nom, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
}

async function mesures(page) {
  return page.evaluate(() => {
    const rect = (sel) => {
      const r = document.querySelector(sel).getBoundingClientRect();
      return { x: r.x, right: r.right, top: r.top + scrollY, bottom: r.bottom + scrollY, height: r.height, width: r.width };
    };
    const visible = (el) => el.getClientRects().length > 0;
    const lignes = (el) => {
      const positions = [];
      const textes = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      while (textes.nextNode()) {
        if (!textes.currentNode.textContent.trim()) continue;
        const range = document.createRange(); range.selectNodeContents(textes.currentNode);
        positions.push(...[...range.getClientRects()].filter((r) => r.width > 0).map((r) => Math.round(r.y)));
      }
      return new Set(positions).size;
    };
    const champs = [...document.querySelectorAll(".devis-etape")].filter(visible).map((el) => Number(el.dataset.etape));
    const entete = rect(".entete");
    const r = {
      ecran: innerWidth, document: document.documentElement.scrollWidth,
      entete: entete.height, lignesEntete: [...document.querySelectorAll(".marque-nom,.entete-nav a,.entete-tel,.entete-devis")].filter(visible).map(lignes),
      marque: rect(".marque").x, hero: rect(".hero-texte").x,
      espace: rect(".hero-photo").top - entete.bottom,
      devis: rect(".carte-devis"), photo: rect(".hero-photo"), hautHero: rect(".hero").top,
      etapes: champs, diogeneTexte: rect(".diogene-texte"), diogeneMedia: rect(".diogene-media"),
      conteneurs: [...document.querySelectorAll(".conteneur")].map((el) => {
        const r = el.getBoundingClientRect(); return { x: r.x, right: r.right };
      }),
      boutonsHero: [...document.querySelectorAll(".hero-boutons .bouton")].map((el) => {
        const r = el.getBoundingClientRect(); return { width: r.width, height: r.height, lignes: lignes(el) };
      }),
      tuiles: [...document.querySelectorAll(".estimateur-tuile strong")].map((el) => ({ texte: el.textContent, lignes: lignes(el), tient: el.scrollWidth <= el.clientWidth })),
      puces: [...document.querySelectorAll(".estimateur-choix .pastille-radio span")].map((el) => ({ lignes: lignes(el), tient: el.scrollWidth <= el.clientWidth })),
      cibles: [...document.querySelectorAll(".pied a,.devis-mail,.prestation-approche")].filter(visible).map((el) => el.getBoundingClientRect().height),
      bandeVide: rect(".pied").top - rect(".appel-final").bottom,
      barre: rect(".barre-mobile").height,
      reserve: parseFloat(getComputedStyle(document.body).paddingBottom),
      polices: [...document.fonts].map((f) => ({ famille: f.family, statut: f.status })),
      debordements: [...document.querySelectorAll("body *")].filter((el) => visible(el) && el.getBoundingClientRect().right > innerWidth + 1).map((el) => el.tagName + "." + el.className)
    };
    return r;
  });
}

async function planche(page, largeur) {
  await page.evaluate(() => scrollTo(0, 0));
  const images = [{ titre: "Haut de page", png: (await page.screenshot()).toString("base64") }];
  // La barre reste présente sur le haut de page ; ne pas la répéter sur les sections.
  await page.addStyleTag({ content: ".barre-mobile{visibility:hidden}" });
  for (const [titre, sel] of [["Estimateur", ".carte-estimateur"], ["Diogène", "#diogene"]]) {
    images.push({ titre, png: (await page.locator(sel).screenshot()).toString("base64") });
  }
  const composition = await navigateur.newPage({ viewport: { width: largeur, height: 900 } });
  const png = await composition.evaluate(async ({ images, largeur, capture }) => {
    const sources = await Promise.all(images.map(async ({ png }) => {
      const img = new Image(); img.src = "data:image/png;base64," + png; await img.decode(); return img;
    }));
    const canvas = document.createElement("canvas"); canvas.width = largeur;
    canvas.height = sources.reduce((h, img) => h + img.height + 40, 0);
    const ctx = canvas.getContext("2d"); ctx.fillStyle = "#F5F0E6"; ctx.fillRect(0, 0, canvas.width, canvas.height);
    let y = 0;
    sources.forEach((img, i) => {
      ctx.fillStyle = "#1E3A2B"; ctx.fillRect(0, y, largeur, 40);
      ctx.fillStyle = "#FFFFFF"; ctx.font = "bold 14px sans-serif";
      ctx.fillText(`H10 ${capture} · ${largeur} px · ${images[i].titre}`, 12, y + 26);
      y += 40; ctx.drawImage(img, (largeur - img.width) / 2, y); y += img.height;
    });
    return canvas.toDataURL("image/png").split(",")[1];
  }, { images, largeur, capture });
  await composition.close();
  const dossier = path.join(racine, "docs/captures"); await mkdir(dossier, { recursive: true });
  await writeFile(path.join(dossier, `h10-${capture}-${largeur}.png`), Buffer.from(png, "base64"));
}

try {
  for (const largeur of largeurs) {
    const page = await navigateur.newPage({ viewport: { width: largeur, height: 900 } });
    const jsErreurs = []; page.on("pageerror", (e) => jsErreurs.push(e.message));
    await ouvrir(page);
    const m = await mesures(page);
    if (capture === "avant") {
      sorties.push({ largeur, document: m.document, entete: m.entete, gouttiere: m.hero, espace: m.espace, devisHaut: Math.round(m.devis.top) });
      if ([375, 768, 1280, 1920].includes(largeur)) await planche(page, largeur);
      await page.close();
      continue;
    }
    const gutter = largeur < 600 ? 16 : largeur < 1200 ? 24 : (largeur - 1200) / 2;
    const proche = (a, b) => Math.abs(a - b) <= 1;
    const prefixe = `${largeur}px`;
    verifier(m.document === largeur, `${prefixe} : débordement ${m.document}px`);
    if (m.document !== largeur) console.error(prefixe, m.debordements);
    verifier(m.entete <= (largeur < 900 ? 72 : 96) && m.lignesEntete.every((n) => n === 1), `${prefixe} : en-tête multilignes`);
    verifier(proche(m.hero, gutter) && proche(m.marque, gutter), `${prefixe} : gouttière héros/en-tête`);
    verifier(m.conteneurs.every((r) => proche(r.x, gutter) && proche(r.right, largeur - gutter)), `${prefixe} : alignement des sections`);
    verifier(m.devis.top >= m.hautHero && m.devis.top >= m.entete, `${prefixe} : devis recouvre l'en-tête`);
    verifier(m.etapes.join() === "1", `${prefixe} : devis non guidé`);
    if (largeur < 900) {
      verifier(proche(m.espace, 0), `${prefixe} : vide avant la photo mobile ${m.espace}px`);
      verifier(m.diogeneTexte.bottom <= m.diogeneMedia.top, `${prefixe} : Diogène dans le mauvais ordre`);
      verifier(m.devis.top >= m.photo.bottom + 16, `${prefixe} : devis chevauche la photo mobile`);
    } else {
      verifier(m.devis.top >= m.photo.top && m.devis.bottom <= m.photo.bottom, `${prefixe} : devis hors de la bande photo`);
    }
    if (largeur < 900) {
      verifier(m.boutonsHero.every((r) => proche(r.width, largeur - 2 * gutter) && r.height === 56 && r.lignes === 1), `${prefixe} : boutons héros`);
    }
    if (largeur < 600) {
      verifier(m.cibles.every((h) => h >= 44), `${prefixe} : cibles tactiles <44px`);
    }
    verifier(m.tuiles.every((t) => t.lignes === 1 && t.tient) && m.puces.every((t) => t.lignes === 1 && t.tient), `${prefixe} : estimateur déborde/coupe`);
    verifier(proche(m.bandeVide, 0), `${prefixe} : bande vide avant le pied`);
    verifier(m.reserve >= m.barre, `${prefixe} : contenu caché par la barre mobile`);
    // Les trois étapes sont réellement exercées, y compris les valeurs du récapitulatif.
    await page.locator("#devis-cp").fill("67000");
    await page.locator(".devis-continuer").click();
    verifier((await mesures(page)).etapes.join() === "2", `${prefixe} : étape 2 absente`);
    await page.locator('input[name="acces"][value="Ascenseur"] + span').click();
    await page.locator(".devis-continuer").click();
    await page.locator("#devis-tel").fill("0601020304");
    await page.locator("#devis-quand").fill("avant fin octobre");
    const m3 = await mesures(page);
    verifier(m3.etapes.join() === "3" && m3.document === largeur && m3.devis.top >= m3.entete, `${prefixe} : étape 3`);
    const recap = await page.locator(".devis-recap").innerText();
    verifier(recap.includes("0601020304") && recap.includes("avant fin octobre") && recap.includes("Ascenseur"), `${prefixe} : récapitulatif non actualisé`);
    if (largeur < 768) {
      await page.locator(".devis-mail").evaluate((el) => el.scrollIntoView({ block: "end" }));
      const accessible = await page.evaluate(() => document.querySelector(".devis-mail").getBoundingClientRect().bottom <= document.querySelector(".barre-mobile").getBoundingClientRect().top);
      verifier(accessible, `${prefixe} : dernière ligne du devis masquée par la barre`);
    }
    await page.locator(".devis-retour").click(); await page.locator(".devis-retour").click();
    verifier(await page.locator("#devis-cp").inputValue() === "67000", `${prefixe} : retour perd les valeurs`);
    // Tous les choix d'estimateur, pas seulement la valeur initiale.
    for (const choix of ["cave", "studio", "t2", "t4", "maison", "pro"]) {
      await page.locator(`#volume-${choix} + span`).click();
      const actuel = await mesures(page);
      verifier(actuel.document === largeur && actuel.tuiles.every((t) => t.lignes === 1 && t.tient), `${prefixe} : tuiles ${choix}`);
    }
    verifier(jsErreurs.length === 0, `${prefixe} : erreurs JS ${jsErreurs.join()}`);
    sorties.push({ largeur, document: m.document, entete: m.entete, gouttiere: m.hero, espace: m.espace, devisHaut: Math.round(m.devis.top), etapes: "1→2→3→2→1", diogene: largeur < 900 ? m.diogeneTexte.bottom <= m.diogeneMedia.top : "desktop", polices: [...new Set(m.polices.filter((f) => f.statut === "loaded").map((f) => f.famille))].join(", ") });
    if (capture && [375, 768, 1280, 1920].includes(largeur)) {
      await ouvrir(page); await planche(page, largeur);
    }
    await page.close();
    const contexte = await navigateur.newContext({ javaScriptEnabled: false, viewport: { width: largeur, height: 900 } });
    const sansJS = await contexte.newPage(); await ouvrir(sansJS);
    const sans = await mesures(sansJS);
    verifier(sans.etapes.join() === "1,2,3" && sans.document === largeur && sans.devis.top >= sans.entete, `${prefixe} : repli sans JS`);
    await contexte.close();
    for (const nom of ["mentions-legales.html", "confidentialite.html", "404.html"]) {
      const annexe = await navigateur.newPage({ viewport: { width: largeur, height: 900 } }); await ouvrir(annexe, nom);
      const legal = await annexe.evaluate(() => ({ largeur: document.documentElement.scrollWidth, hauteur: document.querySelector(".entete").getBoundingClientRect().height, logo: document.querySelector(".marque").getBoundingClientRect().x }));
      verifier(legal.largeur === largeur && legal.hauteur <= (largeur < 900 ? 72 : 96) && proche(legal.logo, gutter), `${prefixe} : ${nom}`);
      await annexe.close();
    }
  }
} finally {
  await navigateur.close(); await new Promise((resolve) => serveur.close(resolve));
}
console.table(sorties);
console.log(JSON.stringify({ mesures: sorties, erreurs }, null, 2));
if (erreurs.length) { console.error(erreurs.join("\n")); process.exitCode = 1; }
else console.log(capture === "avant" ? "H10 : état initial capturé (constats, sans verdict de conformité)." : "H10 : toutes les mesures, étapes, annexes et replis sans JS sont conformes.");
