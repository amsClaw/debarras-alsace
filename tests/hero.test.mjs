// Tests de l'histoire 2 : en-tete et heros avec devis express.
//
// Lancement : `npm test`, soit `node --test tests/*.test.mjs`.

import test from "node:test";
import assert from "node:assert/strict";

import { lire, compter, RACINE } from "./outils.mjs";
import path from "node:path";
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const { composerMessage } = await import(pathToFileURL(path.join(RACINE, "assets", "message.js")));

const page = lire("index.html");
const config = lire("assets/config.js");

function extraire(motif) {
  const correspondance = config.match(motif);
  assert.ok(correspondance, `motif introuvable dans config.js : ${motif}`);
  return correspondance[1];
}

const TEL_INTERNATIONAL = extraire(/telInternational:\s*"([^"]+)"/);
const WHATSAPP = extraire(/whatsapp:\s*"([^"]+)"/);

test("en-tete : logo, navigation par ancres, telephone, bouton devis", () => {
  const entete = page.match(/<header[\s\S]*?<\/header>/)[0];

  for (const ancre of ["#prestations", "#deroule", "#prix", "#realisations", "#zone", "#faq"]) {
    assert.match(entete, new RegExp(`href="${ancre}"`), `l'ancre ${ancre} doit etre dans la navigation`);
  }

  assert.match(entete, new RegExp(`href="tel:\\+${TEL_INTERNATIONAL}"`), "le lien tel: doit utiliser le numero de config.js");
  assert.match(entete, /href="#devis"/, "le bouton devis doit pointer vers #devis");
  assert.match(entete, /Devis gratuit/, "le bouton devis gratuit est attendu");
});

test("en-tete : navigation et telephone masques sous 900 px (pas de menu burger)", () => {
  const feuille = lire("assets/style.css").replace(/\/\*[\s\S]*?\*\//g, "");

  assert.match(
    feuille,
    /@media \(max-width:899\.98px\)\{\s*\.entete-nav,\.entete-tel\{display:none\}/,
    "la navigation et le telephone doivent etre masques sous 900 px"
  );
  assert.doesNotMatch(feuille, /burger/i, "aucun menu burger n'est attendu");
});

test("heros : un seul <h1>, pastille, deux boutons, trois reassurances", () => {
  const main = page.match(/<main[\s\S]*?<\/main>/)[0];

  assert.equal(compter(page, /<h1[\s>]/), 1, "un seul <h1> sur la page");
  assert.match(main, /<h1[^>]*class="hero-titre"[^>]*>/, "le <h1> du heros est attendu");
  assert.match(main, /Vous montrez ce qui doit partir\./, "premiere phrase du titre");
  assert.match(main, /<em>On s’occupe du reste\.<\/em>/, "seconde phrase conservée");

  assert.match(main, /class="pastille"/, "la pastille est attendue");
  assert.match(main, /Entreprise locale/, "le texte de la pastille est attendu");

  assert.match(main, /href="#devis"[^>]*>\s*Obtenir mon devis gratuit/, "bouton devis gratuit vers #devis");
  assert.match(main, new RegExp(`href="https://wa\\.me/${WHATSAPP}"`), "bouton WhatsApp avec le numero de config.js");

  const reassurances = main.match(/<ul class="reassurances">[\s\S]*?<\/ul>/);
  assert.ok(reassurances, "la liste de reassurances est attendue");
  assert.equal(compter(reassurances[0], "<svg"), 3, "trois icones SVG en ligne");
  assert.match(reassurances[0], /Devis sous 24&nbsp;h/);
  assert.match(reassurances[0], /Prix ferme/);
  assert.match(reassurances[0], /Tri &amp; réemploi/);
});

test("heros : vraie photo prioritaire et carte devis indépendante", () => {
  const main = page.match(/<main[\s\S]*?<\/main>/)[0];

  const photo = main.match(/<img[^>]*class="hero-photo"[^>]*>/);
  assert.ok(photo, "la photo du heros est attendue");
  assert.match(photo[0], /src="assets\/photos\/hero\.jpg"/);
  assert.match(photo[0], /width="\d+"/, "la largeur doit etre renseignee");
  assert.match(photo[0], /height="\d+"/, "la hauteur doit etre renseignee");
  assert.match(photo[0], /alt="[^"]{10,}"/, "le texte alternatif doit etre descriptif");

  assert.ok(
    main.indexOf('class="hero-decor"') < main.indexOf('class="conteneur hero-grille"') && main.indexOf('class="hero-texte"') < main.indexOf('id="devis"'),
    "la photo est un décor distinct de la grille texte/devis"
  );
  assert.match(photo[0], /fetchpriority="high"/);
  assert.doesNotMatch(photo[0], /loading="lazy"/);
});

test("formulaire devis : 6 choix exclusifs avec labels", () => {
  const formulaire = page.match(/<form id="devis"[\s\S]*?<\/form>/)[0];

  assert.equal(compter(formulaire, /name="type"[^>]*type="radio"|type="radio" name="type"/), 6, "6 choix de type");
  assert.equal(compter(formulaire, /name="type"/), 6, "tous partagent le meme name (exclusifs)");

  for (const choix of ["Maison", "Appartement", "Cave · grenier", "Local pro", "Très encombré", "Autre"]) {
    assert.match(formulaire, new RegExp(`value="${choix.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}"`), `le choix ${choix} est attendu`);
  }
});

test("formulaire devis : code postal et telephone avec label, mention photos, boutons", () => {
  const formulaire = page.match(/<form id="devis"[\s\S]*?<\/form>/)[0];

  const champCp = formulaire.match(/<label for="([^"]+)">Code postal[\s\S]*?<\/label>/);
  assert.ok(champCp, "le champ Code postal doit avoir un label");
  assert.match(formulaire, new RegExp(`<input id="${champCp[1]}"`), "l'input Code postal doit correspondre au label");

  const champTel = formulaire.match(/<label for="([^"]+)">Téléphone[\s\S]*?<\/label>/);
  assert.ok(champTel, "le champ Telephone doit avoir un label");
  assert.match(formulaire, new RegExp(`<input id="${champTel[1]}"`), "l'input Telephone doit correspondre au label");

  assert.match(formulaire, /Ajoutez 2–3 photos dans WhatsApp après l’envoi/, "la mention photos est attendue");

  const boutonEnvoyer = formulaire.match(/<a[^>]*class="[^"]*devis-envoyer[^"]*"[^>]*>Envoyer sur WhatsApp<\/a>/);
  assert.ok(boutonEnvoyer, "le bouton d'envoi doit etre un lien wa.me fonctionnel sans JavaScript");
  assert.match(boutonEnvoyer[0], new RegExp(`href="https://wa\\.me/${WHATSAPP}`), "le lien de repli doit utiliser le numero WhatsApp de config.js");

  const lienMail = formulaire.match(/<a[^>]*class="devis-mail"[^>]*>Préférer l’e-mail<\/a>/);
  assert.ok(lienMail, "le lien e-mail est attendu");
  assert.match(lienMail[0], /href="mailto:moisenelson17@gmail\.com"/, "le lien e-mail doit rester fonctionnel sans JavaScript");
});

test("assets/message.js : composerMessage() est une fonction pure exportee", () => {
  assert.equal(typeof composerMessage, "function", "composerMessage doit etre exporte");

  assert.equal(
    composerMessage({ type: "Maison", codePostal: "67000", telephone: "0601020304" }),
    "Bonjour, je souhaite un devis de débarras.\nType : Maison\nCode postal : 67000\nTéléphone : 0601020304",
    "tous les champs presents doivent apparaitre dans l'ordre"
  );

  assert.equal(
    composerMessage({ type: "Maison" }),
    "Bonjour, je souhaite un devis de débarras.\nType : Maison",
    "les champs vides ou absents sont omis"
  );

  assert.equal(composerMessage({}), "Bonjour, je souhaite un devis de débarras.", "aucun champ ne fait planter la fonction");
});

test("assets/message.js : les caracteres speciaux sont encodes une fois passes en URL", () => {
  const message = composerMessage({ type: "Cave & grenier", codePostal: "67000" });
  const encode = encodeURIComponent(message);

  assert.match(encode, /Cave%20%26%20grenier/, "l'esperluette et les espaces doivent etre encodes");
  assert.doesNotMatch(encode, /\n/, "le retour a la ligne ne doit pas rester brut dans l'URL");
  assert.match(encode, /%0A/, "le retour a la ligne doit etre encode en %0A");
});

test("assets/site.js : compose le message et ouvre wa.me / mailto avec les coordonnees de config.js", () => {
  const source = lire("assets/site.js");

  assert.match(source, /import\s*\{\s*composerMessage\s*\}\s*from\s*"\.\/message\.js"/, "site.js doit importer composerMessage depuis message.js");
  assert.match(source, /window\.DEBARRAS/, "les coordonnees doivent venir de window.DEBARRAS");
  assert.match(source, /https:\/\/wa\.me\/\$\{[^}]*whatsapp[^}]*\}/, "le lien wa.me doit utiliser whatsapp de la config");
  assert.match(source, /mailto:\$\{[^}]*mail[^}]*\}/, "le lien mailto doit utiliser mail de la config");
  assert.match(source, /encodeURIComponent/, "le message doit etre encode dans l'URL");
});

// H10 : régressions de présentation, sans dépendance ni navigateur dans npm test.
const css = lire("assets/style.css").replace(/\/\*[\s\S]*?\*\//g, "");
test("H10 : le héros ne remet jamais sa gouttière horizontale à zéro", () => {
  const regles = [...css.matchAll(/\.hero-grille\{([^}]+)\}/g)].map((m) => m[1]);
  assert.ok(regles.some((r) => /padding-block:364px 48px/.test(r)), "340 px de photo, puis 24 px de marge");
  assert.ok(regles.every((r) => !/(?:^|;)padding:/.test(r)), "utiliser padding-block, pas un raccourci qui écrase les gouttières");
  assert.match(css, /main\{padding:0\}/, "pas de deuxième espace sous l'en-tête");
});

test("H10/H12 : devis dans le flux, sans marge négative ni chevauchement", () => {
  const regles = [...css.matchAll(/\.carte-devis\{([^}]+)\}/g)].map((m) => m[1]);
  assert.ok(regles.every((r) => !/position:absolute|bottom:0/.test(r)));
  assert.match(regles[0], /position:relative/);
  assert.match(regles[0], /margin:0/);
  assert.ok(regles.every((r) => !/margin[^;]*:-/.test(r)));
});

test("H10 : même parcours progressif sur téléphone et ordinateur, sans redémarrage au redimensionnement", () => {
  const js = lire("assets/site.js");
  assert.doesNotMatch(js, /matchMedia|requeteMobile/);
  assert.match(js, /activerModeEtapes\(\);/);
  const fin = css.slice(css.indexOf(".carte-devis.mode-etapes .devis-progression"));
  assert.doesNotMatch(fin, /@media/);
  assert.match(fin, /\.carte-devis\.mode-etapes \.devis-etape\{display:none\}/);
});

test("H10 : ordre HTML Diogène, titre et texte avant la photo et l'encadré", () => {
  const section = page.match(/<section id="diogene"[\s\S]*?<\/section>/)[0];
  assert.ok(section.indexOf('class="diogene-texte"') < section.indexOf('class="diogene-media"'));
  assert.ok(section.indexOf('id="diogene-titre"') < section.indexOf("<img"));
  assert.match(css, /\.diogene-media,\.diogene-texte\{grid-column:auto;grid-row:auto\}/);
});

test("H10 : libellés sous les icônes de la barre du bas", () => {
  const nav = page.match(/<nav class="barre-mobile"[\s\S]*?<\/nav>/)[0];
  assert.deepEqual([...nav.matchAll(/<span>([^<]+)<\/span>/g)].map((m) => m[1]), ["Appeler", "WhatsApp", "Devis"]);
  assert.match(css, /\.barre-mobile-lien\{[^}]*flex-direction:column/);
  assert.match(css, /scroll-padding-bottom:92px/);
});

test("H10 : boutons héros pleine largeur et liens secondaires de 44 px", () => {
  assert.match(css, /\.hero-boutons\{flex-direction:column\}/);
  assert.match(css, /\.hero-boutons \.bouton\{width:100%/);
  assert.match(css, /\.devis-mail,\.prestation-approche\{[^}]*min-height:44px/);
  assert.match(css, /\.pied a\{[^}]*min-height:44px/);
});

test("H10 : marque et bouton d'en-tête compacts, aucun retour de navigation", () => {
  assert.match(css, /\.marque\{[^}]*white-space:nowrap/);
  assert.match(css, /\.entete-nav\{[^}]*white-space:nowrap/);
  assert.match(css, /\.marque-zone,\.entete-devis-long\{display:none\}/);
  for (const nom of ["mentions-legales", "confidentialite"]) {
    assert.match(lire(`${nom}.html`), /class="bouton bouton-brique entete-devis" href="index.html">Accueil</);
  }
});

test("H10 : les métadonnées des réalisations passent à la ligne, jamais hors de leur carte", () => {
  assert.match(css, /\.realisation-meta\{[^}]*flex-wrap:wrap/);
});

test("H12 : décor pleine largeur, photo cover et deux dégradés dédiés", () => {
  assert.match(css, /\.hero-photo\{[^}]*width:100%;height:100%;object-fit:cover/);
  assert.match(css, /--hero-voile:linear-gradient\(90deg/);
  assert.match(css, /--hero-voile-mobile:linear-gradient\(180deg/);
  assert.match(css, /\.hero-decor::after\{[^}]*background:var\(--hero-voile-mobile\)/);
  assert.match(css, /@media \(min-width:900px\)[\s\S]*?\.hero-decor\{inset:0;height:100%\}/);
});

test("H12 : titre et badge uniques sur la photo, devis après les garanties", () => {
  const accroche = page.match(/<div class="hero-accroche">[\s\S]*?<\/div>/)[0];
  assert.match(accroche, /class="pastille"/);
  assert.match(accroche, /class="hero-titre"/);
  assert.equal(compter(page, 'class="hero-accroche"'), 1);
  assert.ok(page.indexOf('class="reassurances"') < page.indexOf('id="devis"'));
  assert.match(css, /\.hero-accroche\{[^}]*height:340px/);
});

test("H12 : grille desktop centrée, texte clair et WhatsApp contour blanc", () => {
  assert.match(css, /\.hero-grille\{display:grid;[^}]*align-items:center/);
  assert.match(css, /\.hero-paragraphe,\.hero \.reassurances li,\.hero \.reassurances li span\{color:var\(--hero-clair\)\}/);
  assert.match(css, /\.hero-boutons \.bouton-contour\{border-color:var\(--hero-clair\);color:var\(--hero-clair\)\}/);
  assert.match(css, /\.hero-titre em\{font-style:normal;[^}]*color:inherit/);
});

test("H12 : bouton d’en-tête sans gap parasite et Bas‑Rhin insécable", () => {
  assert.match(css, /\.entete-devis\{[^}]*gap:0/);
  assert.match(page, /Devis<span class="entete-devis-long"> gratuit<\/span>/);
  const badge = page.match(/<span class="pastille">([^\n]+)/)[1];
  assert.match(badge, /, <span class="mot-insecable">Bas\u2011Rhin<\/span>/);
  assert.doesNotMatch(badge, /Bas -|Bas\s+-|Bas-\s+Rhin/);
});

test("H12 : cahiers accessibles, douze cas HTML et validation explicite", () => {
  const guide = lire("CAHIER_DE_RECETTE.html");
  assert.equal(compter(guide, '<input type="checkbox">'), 12);
  assert.match(guide, /aucun identifiant ni mot de passe/i);
  assert.match(guide, /node tools\/verifier-hero\.mjs --servir/);
  assert.doesNotMatch(guide, /<script[^>]*src=|<link[^>]*href=|<img[^>]*src=/i, "cahier autonome");
  for (const document of [guide, lire("docs/CAHIER_DE_RECETTE.md")]) {
    assert.match(document, /je valide H12 du projet debarras-alsace/);
  }
});

test("H12 : captures du haut de page aux trois dimensions demandées", () => {
  for (const [largeur, hauteur] of [[375, 812], [1280, 860], [1440, 900]]) {
    const png = readFileSync(path.join(RACINE, `docs/captures/h12-${largeur}.png`));
    assert.equal(png.subarray(1, 4).toString(), "PNG");
    assert.equal(png.readUInt32BE(16), largeur);
    assert.equal(png.readUInt32BE(20), hauteur);
  }
});
