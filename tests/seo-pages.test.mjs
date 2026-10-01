// Vérifications de préparation SEO, médias et pages annexes de la V3.
import test from "node:test";
import assert from "node:assert/strict";
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { lire, compter, RACINE } from "./outils.mjs";

const page = lire("v3/index.html");
const config = lire("v3/assets/config.js");
const htmlPages = readdirSync(path.join(RACINE, "v3")).filter((nom) => nom.endsWith(".html"));

function meta(propriete) {
  return page.match(new RegExp(`<meta\\s+property="${propriete}"\\s+content="([^"]+)"`))?.[1];
}

test("SEO et Open Graph : titre, description, image, langue et canonical absolus", () => {
  const titre = page.match(/<title>([^<]+)<\/title>/)?.[1];
  const description = page.match(/<meta name="description" content="([^"]+)"/)?.[1];
  assert.ok(titre);
  assert.ok(titre.length <= 60);
  assert.match(titre, /Débarras/i);
  assert.match(titre, /Strasbourg/i);
  assert.ok(description && description.length >= 120 && description.length <= 160);
  assert.equal(meta("og:title"), titre);
  assert.equal(meta("og:description"), description);
  assert.equal(meta("og:image"), "https://amsclaw.github.io/debarras-alsace/assets/photos/hero.jpg");
  assert.equal(meta("og:url"), "https://amsclaw.github.io/debarras-alsace/");
  assert.equal(meta("og:locale"), "fr_FR");
  assert.match(page, /<link rel="canonical" href="https:\/\/amsclaw\.github\.io\/debarras-alsace\/">/);
});

test("JSON-LD LocalBusiness : données de zone, téléphone configuré et horaires sans avis", () => {
  const json = page.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)?.[1];
  assert.ok(json);
  const donnees = JSON.parse(json);
  assert.equal(donnees["@type"], "LocalBusiness");
  assert.equal(donnees.name, "Débarras Alsace");
  const telephoneConfig = config.match(/telInternational:\s*"([^"]+)"/)?.[1];
  assert.ok(telephoneConfig);
  assert.equal(donnees.telephone, `+${telephoneConfig}`);
  assert.equal(donnees.email, config.match(/mail:\s*"([^"]+)"/)?.[1]);
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
  const dossier = path.join(RACINE, "v3/assets/photos");
  const taille = readdirSync(dossier).reduce((total, nom) => total + statSync(path.join(dossier, nom)).size, 0);
  assert.ok(taille <= 1_500_000, `poids constaté : ${taille} octets`);
});

test("pages légales adaptées au style V3 et page 404 avec retour accueil", () => {
  const mentions = lire("v3/mentions-legales.html");
  const confidentialite = lire("v3/confidentialite.html");
  const erreur = lire("v3/404.html");
  for (const legal of [mentions, confidentialite]) {
    assert.match(legal, /class="entete"/);
    assert.match(legal, /class="pied"/);
    assert.match(legal, /page-legale-contenu/);
  }
  for (const emplacement of ["[raison sociale]", "[forme juridique]", "[adresse complète]", "[numéro SIRET]", "[nom du représentant légal]"]) {
    assert.ok(mentions.includes(emplacement) || confidentialite.includes(emplacement), `emplacement légal conservé : ${emplacement}`);
  }
  assert.match(erreur, /<h1>Cette page n’existe pas\.<\/h1>/);
  assert.match(erreur, /href="index\.html"[^>]*>Retour à l’accueil/);
});

test("tous les liens internes des pages HTML V3 pointent vers un fichier ou une ancre existante", () => {
  for (const nom of htmlPages) {
    const html = lire(`v3/${nom}`);
    const source = path.join(RACINE, "v3", nom);
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

// ——— Histoire 11 : vraies coordonnées, aucun crochet visible, typographie française,
// référencement absolu, page 404 en profondeur, polices hébergées. ———

const BASE = "https://amsclaw.github.io/debarras-alsace/";
const pages = readdirSync(path.join(RACINE, "v3")).filter((nom) => nom.endsWith(".html"));
const module = (nom) => import(pathToFileURL(path.join(RACINE, "v3", "assets", nom)).href);
const { verifierZone } = await module("zone.js");
const { VOLUMES } = await module("volume.js");
// site.js est le point d'entrée de la page : on l'importe avec un document vide pour
// n'exercer que ses fonctions pures exportées.
globalThis.window ??= {};
globalThis.document ??= { querySelector: () => null, querySelectorAll: () => [], getElementById: () => null };
const { avisAffiches, ligneChantier, fourchettePrix, identiteEntreprise, appliquerCoordonnees, texteRecap } = await module("site.js");
const { composerMessage } = await module("message.js");

function configuration() {
  const fenetre = {};
  new Function("window", lire("v3/assets/config.js"))(fenetre);
  return fenetre.DEBARRAS;
}

/** Texte que voit le visiteur : sans <head>, scripts, commentaires ni éléments `hidden`. */
function texteVisible(html) {
  let corps = html.replace(/<head>[\s\S]*?<\/head>/, "").replace(/<script\b[\s\S]*?<\/script>/g, "").replace(/<template\b[\s\S]*?<\/template>/g, "").replace(/<!--[\s\S]*?-->/g, "");
  // Retire chaque élément portant l'attribut hidden, avec son contenu (balises imbriquées comprises).
  let correspondance;
  while ((correspondance = corps.match(/<([a-z0-9]+)\b[^>]*\shidden(?:\s|>|=)[^>]*>?/i))) {
    const balise = correspondance[1];
    const debut = correspondance.index;
    const motif = new RegExp(`<\\/?${balise}\\b[^>]*>`, "gi");
    motif.lastIndex = debut;
    let profondeur = 0;
    let fin = corps.length;
    for (let m; (m = motif.exec(corps)); ) {
      profondeur += m[0].startsWith("</") ? -1 : 1;
      if (profondeur === 0) { fin = m.index + m[0].length; break; }
    }
    corps = corps.slice(0, debut) + corps.slice(fin);
  }
  return corps.replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, "\u00a0").replace(/&amp;/g, "&").replace(/[ \t\r\n]+/g, " ");
}

test("config.js : vraies coordonnées de l'entreprise, au seul endroit prévu", () => {
  const config = configuration();
  assert.equal(config.tel, "06 99 54 49 26");
  assert.equal(config.telInternational, "33699544926");
  assert.equal(config.whatsapp, "33699544926");
  assert.equal(config.mail, "moisenelson17@gmail.com");
  assert.deepEqual(config.avis, [], "aucun avis inventé");
});

test("coordonnées : tous les liens tel:, wa.me et mailto: des pages utilisent config.js", () => {
  const { telInternational, whatsapp, mail } = configuration();
  for (const nom of pages) {
    const html = lire(`v3/${nom}`);
    for (const motif of ["33000000000", "XX XX", "contact@domaine", "[téléphone]", "[adresse e-mail]", "[06 "]) {
      assert.equal(compter(html, motif), 0, `${nom} : « ${motif} » ne doit plus apparaître`);
    }
    for (const [, numero] of html.matchAll(/href="tel:\+?(\d+)"/g)) assert.equal(numero, telInternational, `${nom} : tel:`);
    for (const [, numero] of html.matchAll(/href="https:\/\/wa\.me\/(\d+)/g)) assert.equal(numero, whatsapp, `${nom} : wa.me`);
    for (const [, adresse] of html.matchAll(/href="mailto:([^"?]+)/g)) assert.equal(adresse, mail, `${nom} : mailto:`);
  }
  assert.equal(compter(page, /href="tel:\+33699544926"/g), 5, "en-tête, Diogène, appel final, barre du bas, pied de page");
  assert.equal(compter(page, /href="https:\/\/wa\.me\/33699544926/g), 4, "héros, envoi du devis, Diogène, barre du bas");
  assert.equal(compter(page, /href="mailto:moisenelson17@gmail\.com"/g), 2, "devis et pied de page");
  assert.match(page, /<span class="texte-tel">06 99 54 49 26<\/span>/, "numéro affiché dans l'en-tête");
});

test("site.js : le devis WhatsApp / e-mail et les textes affichés lisent window.DEBARRAS", () => {
  const js = lire("v3/assets/site.js");
  assert.match(js, /wa\.me\/\$\{whatsapp\}\?text=/);
  assert.match(js, /mailto:\$\{mail\}\?subject=/);
  assert.match(js, /\.texte-tel[\s\S]*?config\.tel/);
  assert.match(js, /\.texte-mail[\s\S]*?config\.mail/);
  assert.match(js, /\.lien-mail[\s\S]*?mailto:\$\{config\.mail\}/);
});

test("accueil : aucun emplacement entre crochets dans le texte visible ni dans le <head>", () => {
  const visible = texteVisible(page);
  assert.ok(visible.includes("Débarras Alsace") && visible.length > 3000, "le texte visible est bien extrait");
  assert.deepEqual(visible.match(/\[[^\]]*\]/g) ?? [], []);
  const tete = page.match(/<head>[\s\S]*?<\/head>/)[0].replace(/<script\b[\s\S]*?<\/script>/, "");
  assert.doesNotMatch(tete, /\[[^\]]*\]/, "aucun emplacement dans le <head>");
  const jsonLd = JSON.parse(page.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  assert.doesNotMatch(JSON.stringify(jsonLd), /\[[^\]"]*\]/);
  assert.ok(visible.includes("Photos d’illustration."), "mention d'illustration pour le visiteur");
  assert.doesNotMatch(page, /remplacés par vos chantiers réels/);
});

test("blocs en attente de l'entreprise : masqués par défaut, réaffichés par un seul réglage de config.js", () => {
  const vide = configuration();
  assert.equal(avisAffiches(vide).visible, false, "avis: [] masque la section");
  assert.equal(ligneChantier(vide, 0), "");
  assert.equal(fourchettePrix(vide, "t2"), "");
  assert.equal(identiteEntreprise(vide), "");

  const rempli = {
    ...vide,
    avis: [{ texte: "Équipe ponctuelle.", auteur: "Claire, Obernai" }, "  ", { texte: "" }],
    noteGoogle: { note: "4,8", nombre: 12 },
    lienAvisGoogle: "https://g.page/exemple",
    chantiers: ["Strasbourg · 25 m³"],
    fourchettes: { t2: "à partir de …" },
    raisonSociale: "Débarras Alsace SAS",
    siret: "123"
  };
  const avis = avisAffiches(rempli);
  assert.equal(avis.visible, true);
  assert.deepEqual(avis.temoignages, [{ texte: "Équipe ponctuelle.", auteur: "Claire, Obernai" }], "les avis vides sont ignorés");
  assert.deepEqual(avis.note, { note: "4,8", nombre: "12" });
  assert.equal(avis.lien, "https://g.page/exemple");
  assert.equal(avisAffiches({ ...rempli, lienAvisGoogle: "javascript:alert(1)" }).lien, "", "seul un lien https est accepté");
  assert.equal(ligneChantier(rempli, 0), "Strasbourg · 25 m³");
  assert.equal(ligneChantier(rempli, 1), "");
  assert.equal(fourchettePrix(rempli, "t2"), "à partir de …");
  assert.equal(identiteEntreprise(rempli), "Débarras Alsace SAS · SIRET\u00a0123");

  const js = lire("v3/assets/site.js");
  assert.match(js, /modeleAvis\.replaceWith\(sectionAvis\)/);
  assert.match(js, /notePrix\.hidden = !fourchette/);
  assert.match(js, /textContent = auteur \?/, "les avis sont insérés en texte, jamais en HTML");
  assert.doesNotMatch(js, /innerHTML/);
  const css = lire("v3/assets/style.css");
  assert.match(css, /\.realisation-meta p\[hidden\],\.estimateur-note\[hidden\],\.pied-identite\[hidden\]\{display:none\}/);
});

test("typographie : apostrophes courbes dans le texte visible de toutes les pages", () => {
  for (const nom of pages) {
    const visible = texteVisible(lire(`v3/${nom}`));
    assert.deepEqual(visible.match(/\w'\w/g) ?? [], [], `${nom} : apostrophe droite`);
  }
  for (const [nom, attribut] of pages.flatMap((nom) => [...lire(`v3/${nom}`).matchAll(/\b(?:alt|aria-label|content|placeholder)="([^"]*)"/g)].map(([, v]) => [nom, v]))) {
    assert.doesNotMatch(attribut, /\w'\w/, `${nom} : apostrophe droite dans « ${attribut} »`);
  }
});

test("typographie : espaces insécables entre nombre et unité et avant ? ! : ;", () => {
  const unite = /\d[ ](?:h|m³|km|min|secondes|chiffres|jours?|journée)(?![\wÀ-ÿ])/;
  const ponctuation = /[^\s\u00a0][ ][?!:;](?=\s|$)/;
  for (const nom of pages) {
    const visible = texteVisible(lire(`v3/${nom}`));
    assert.doesNotMatch(visible, unite, `${nom} : espace ordinaire avant une unité`);
    assert.doesNotMatch(visible, ponctuation, `${nom} : espace ordinaire avant ? ! : ;`);
  }
  assert.match(page, /Devis sous 24&nbsp;h/);
  assert.match(page, /8&nbsp;h – 19&nbsp;h/);
  assert.match(page, /Camion 20&nbsp;m³/);
  assert.match(page, /15–30&nbsp;m³/);
  assert.match(page, /1&nbsp;journée/);

  const textesProduits = [verifierZone("67000"), verifierZone("13000"), verifierZone("67"), ...Object.values(VOLUMES).flatMap((v) => [v.m3, v.duree])];
  for (const phrase of textesProduits) {
    assert.doesNotMatch(phrase, unite, `zone.js / volume.js : « ${phrase} »`);
    assert.doesNotMatch(phrase, / [?!:;]/, `zone.js : « ${phrase} »`);
  }
  assert.equal(verifierZone("67000"), "Oui, nous intervenons chez vous. Devis gratuit sous 24\u00a0h.");
});

test("référencement : canonical, og:url et og:image absolus sur la base du sitemap", () => {
  const sitemap = lire("sitemap.xml");
  assert.ok(sitemap.includes(`<loc>${BASE}</loc>`), "même base que sitemap.xml");
  assert.match(page, new RegExp(`<link rel="canonical" href="${BASE.replace(/[.]/g, "\\.")}">`));
  assert.match(page, new RegExp(`<meta property="og:url" content="${BASE.replace(/[.]/g, "\\.")}">`));
  const image = page.match(/<meta property="og:image" content="([^"]+)">/)[1];
  assert.equal(image, `${BASE}assets/photos/hero.jpg`);
  assert.ok(existsSync(path.join(RACINE, "v3", new URL(image).pathname.replace("/debarras-alsace/", ""))), "l'image de partage existe");
  const donnees = JSON.parse(page.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  assert.equal(donnees.telephone, "+33699544926");
  assert.equal(donnees.email, "moisenelson17@gmail.com");
  assert.equal(donnees.url, BASE);
});

test("page 404 : feuille de style, liens et images résolus à n'importe quelle profondeur d'adresse", () => {
  const erreur = lire("v3/404.html");
  const base = erreur.match(/<base href="([^"]+)">/)?.[1];
  assert.equal(base, "/debarras-alsace/", "une base sur la racine du site, quelle que soit la profondeur");
  assert.match(erreur, /<script>if \(!location\.pathname\.startsWith\("\/debarras-alsace\/"\)\) document\.querySelector\("base"\)\.href = "\.\/";<\/script>/, "aperçu local hors /debarras-alsace/ : base ramenée au dossier de la page");
  assert.ok(erreur.indexOf("<base ") < erreur.indexOf('rel="stylesheet"'), "la base précède la feuille de style");
  const references = [...erreur.matchAll(/\b(?:href|src)="([^"]+)"/g)].map(([, url]) => url).filter((url) => url !== base);
  assert.ok(references.length >= 4);
  for (const profondeur of ["https://amsclaw.github.io/debarras-alsace/x", "https://amsclaw.github.io/debarras-alsace/a/b/c", "https://amsclaw.github.io/debarras-alsace/a/b/c/d/"]) {
    for (const reference of references) {
      // Le navigateur résout d'abord la base contre l'adresse de la page, puis chaque lien contre la base.
      const cible = new URL(reference, new URL(base, profondeur));
      assert.ok(cible.href.startsWith(BASE), `${reference} depuis ${profondeur} → ${cible.href}`);
      const fichier = cible.pathname.replace("/debarras-alsace/", "") || "index.html";
      assert.ok(statSync(path.join(RACINE, "v3", fichier), { throwIfNoEntry: false })?.isFile(), `${reference} → v3/${fichier} existe`);
    }
  }
});

test("polices hébergées : aucun appel à Google Fonts, woff2 locaux en font-display:swap", () => {
  const fichiers = [];
  (function parcourir(dossier) {
    for (const entree of readdirSync(dossier, { withFileTypes: true })) {
      const chemin = path.join(dossier, entree.name);
      if (entree.isDirectory()) parcourir(chemin);
      else if (/\.(html|css|js)$/.test(entree.name)) fichiers.push(chemin);
    }
  })(path.join(RACINE, "v3"));
  for (const fichier of fichiers) {
    const contenu = readFileSync(fichier, "utf8");
    assert.doesNotMatch(contenu, /fonts\.(googleapis|gstatic)\.com/, `${path.relative(RACINE, fichier)} appelle Google Fonts`);
  }
  const css = lire("v3/assets/style.css");
  const faces = [...css.matchAll(/@font-face\{([^}]*)\}/g)].map(([, regle]) => regle);
  assert.equal(faces.length, 3);
  for (const regle of faces) {
    assert.match(regle, /font-display:swap/);
    const fichier = regle.match(/url\("([^"]+\.woff2)"\)/)?.[1];
    assert.ok(fichier, "source woff2 attendue");
    const chemin = path.join(RACINE, "v3/assets", fichier);
    assert.ok(existsSync(chemin), `${fichier} présent`);
    assert.equal(readFileSync(chemin).subarray(0, 4).toString("latin1"), "wOF2", `${fichier} est un vrai woff2`);
  }
  for (const famille of ["font-family:Fraunces", 'font-family:"Public Sans"']) {
    assert.ok(faces.some((r) => r.includes(famille)), famille);
  }
  assert.match(lire("v3/confidentialite.html"), /polices de caractères sont hébergées sur le site lui-même&nbsp;: aucune requête n’est envoyée à Google Fonts/);
});

test("mentions légales : hébergeur et contact remplis, champs de l'entreprise signalés", () => {
  const mentions = lire("v3/mentions-legales.html");
  assert.match(mentions, /Hébergeur&nbsp;: GitHub Pages — GitHub, Inc\./);
  assert.match(mentions, /88 Colin P\. Kelly Jr\. Street, San Francisco, CA 94107, États-Unis/);
  assert.match(mentions, /href="mailto:moisenelson17@gmail\.com"/);
  assert.match(mentions, /href="tel:\+33699544926"/);
  assert.doesNotMatch(mentions, /\[nom de l’hébergeur\]|\[adresse de l’hébergeur\]/);
  for (const champ of ["[raison sociale]", "[forme juridique]", "[adresse complète]", "[numéro SIRET]", "[nom du représentant légal]"]) {
    assert.ok(mentions.includes(champ), `champ signalé : ${champ}`);
  }
  const questions = lire("docs/QUESTIONS_OUVERTES.md");
  for (const champ of ["raison sociale", "forme juridique", "adresse", "SIRET", "directeur de la publication"]) {
    assert.ok(questions.toLowerCase().includes(champ.toLowerCase()), `QUESTIONS_OUVERTES liste : ${champ}`);
  }
});

/** Document minimal : chaque <a class="…"> du HTML devient un élément modifiable (href, textContent). */
function documentDe(html) {
  const liens = [...html.matchAll(/<a\b([^>]*)>([\s\S]*?)<\/a>/g)].map(([, attributs, contenu]) => ({
    classes: (attributs.match(/class="([^"]*)"/)?.[1] ?? "").split(/\s+/),
    href: attributs.match(/href="([^"]*)"/)?.[1] ?? "",
    textContent: contenu
  }));
  return { liens, querySelectorAll: (selecteur) => liens.filter((lien) => lien.classes.includes(selecteur.replace(/^\./, ""))) };
}

test("pages légales : les coordonnées suivent config.js (liens et textes), secours identiques sans JS", () => {
  const essai = { tel: "01 23 45 67 89", telInternational: "33123456789", whatsapp: "33123456789", mail: "test@example.invalid" };
  for (const nom of ["mentions-legales.html", "confidentialite.html", "index.html"]) {
    const html = lire(`v3/${nom}`);
    assert.match(html, /<script src="assets\/config\.js" defer><\/script>\s*<script type="module" src="assets\/site\.js"><\/script>/, `${nom} : config.js puis site.js chargés`);
    const doc = documentDe(html);
    // Les deux liens du devis (envoi WhatsApp, « Préférer l’e-mail ») sont reconstruits au clic par site.js.
    const contacts = doc.liens.filter((lien) => /^(tel:|mailto:|https:\/\/wa\.me\/)/.test(lien.href) && !lien.classes.some((c) => c === "devis-envoyer" || c === "devis-mail"));
    assert.ok(contacts.length >= 2, `${nom} : liens de contact présents`);
    for (const lien of contacts) {
      assert.ok(lien.classes.some((c) => ["lien-tel", "lien-mail", "lien-whatsapp"].includes(c)), `${nom} : ${lien.href} doit être relié à config.js`);
    }
    appliquerCoordonnees(doc, essai);
    for (const lien of contacts) {
      assert.ok([`tel:+${essai.telInternational}`, `mailto:${essai.mail}`, `https://wa.me/${essai.whatsapp}`].includes(lien.href), `${nom} : ${lien.href} suit la configuration`);
    }
    for (const lien of doc.querySelectorAll(".texte-tel")) assert.equal(lien.textContent, essai.tel);
    for (const lien of doc.querySelectorAll(".texte-mail")) assert.equal(lien.textContent, essai.mail);
  }
  for (const nom of ["mentions-legales.html", "confidentialite.html"]) {
    const doc = documentDe(lire(`v3/${nom}`));
    assert.equal(doc.querySelectorAll(".texte-tel").length, 1, `${nom} : numéro affiché relié`);
    assert.equal(doc.querySelectorAll(".texte-mail").length, 1, `${nom} : e-mail affiché relié`);
  }
});

test("récapitulatif du devis (étape 3) : insécable avant « : », message envoyé inchangé", () => {
  const champs = { type: "Maison", codePostal: "67000", acces: "Plain-pied", telephone: "06 12 34 56 78", quand: "Cette semaine ?" };
  const recap = texteRecap(champs);
  assert.match(recap, /Type\u00a0: Maison/);
  assert.match(recap, /Accès\u00a0: Plain-pied/);
  assert.match(recap, /Code postal\u00a0: 67000/);
  assert.match(recap, /semaine\u00a0\?/);
  assert.doesNotMatch(recap, / [:;?!]/, "aucune espace ordinaire avant : ; ? !");
  assert.equal(recap.replace(/\u00a0/g, " "), composerMessage(champs), "même contenu que le message envoyé");
  assert.match(composerMessage(champs), /Type : Maison/, "le message WhatsApp / e-mail reste en texte brut");
  assert.match(lire("v3/assets/site.js"), /recap\.textContent = texteRecap\(/, "le récapitulatif affiché passe par texteRecap");
});
