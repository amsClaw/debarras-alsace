// Tests de l'histoire 9 : syndrome de Diogène — carte de prestation renommée,
// section dédiée entre les prestations et le déroulé, septième question de FAQ.
import test from "node:test";
import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import path from "node:path";
import { lire, compter, RACINE } from "./outils.mjs";

const page = lire("index.html");
const css = lire("assets/style.css").replace(/\/\*[\s\S]*?\*\//g, "");

/** Extrait une section complète par son identifiant. */
function section(id) {
  return page.match(new RegExp(`<section\\b(?=[^>]*\\bid="${id}")[^>]*>[\\s\\S]*?<\\/section>`))?.[0];
}

/** Liste les couples { href, texte, class } des liens d'un fragment. */
function liens(fragment) {
  return [...fragment.matchAll(/<a\b([^>]*)href="([^"]*)"[^>]*>([^<]*)<\/a>/g)].map(([, attributs, href, texte]) => ({
    href,
    texte,
    classe: attributs.match(/class="([^"]*)"/)?.[1] ?? ""
  }));
}

const engrenages = [
  ["Sans jugement", "Aucune remarque, aucune photo sans accord. On parle avec la personne, pas de la personne."],
  ["En toute discrétion", "Véhicule sans marquage sur demande, horaires adaptés, confidentialité du début à la fin."],
  ["On garde ce qui compte", "Papiers, photos, souvenirs et objets de valeur mis de côté et remis en main propre."],
  ["Logement remis en état", "Tri, évacuation, dons et recyclage, puis nettoyage approfondi, en une ou plusieurs étapes."]
];

test("section #diogene : présente entre #prestations et #deroule et annoncée par son titre", () => {
  const diogene = section("diogene");
  assert.ok(diogene, "section #diogene attendue");

  assert.match(diogene, /aria-labelledby="diogene-titre"/);
  assert.match(diogene, /<h2 id="diogene-titre">/);
  assert.equal(compter(page, /id="diogene"/g), 1, "une seule section porte l'ancre #diogene");

  const position = (motif) => page.search(motif);
  const avant = position(/<section id="prestations"/);
  const diogenePosition = position(/<section id="diogene"/);
  const apres = position(/<section id="deroule"/);
  assert.ok(avant < diogenePosition, "la section Diogène vient après les prestations");
  assert.ok(diogenePosition < apres, "la section Diogène vient avant le déroulé");
});

test("colonne gauche : photo paresseuse dimensionnée et encadré « Vous êtes un proche ? »", () => {
  const diogene = section("diogene");
  const image = diogene.match(/<img\b[^>]*>/)?.[0];
  assert.ok(image, "la photo de la section est attendue");
  assert.match(image, /src="assets\/photos\/service-diogene\.jpg"/);
  assert.match(image, /alt="Pièce très encombrée avant intervention"/);
  assert.match(image, /loading="lazy"/);
  assert.match(image, /\bwidth="\d+"/, "largeur explicite attendue");
  assert.match(image, /\bheight="\d+"/, "hauteur explicite attendue");
  assert.ok(existsSync(path.join(RACINE, "assets/photos/service-diogene.jpg")), "photo présente dans le dépôt");

  assert.match(diogene, /<strong>Vous êtes un proche&nbsp;\?<\/strong>/);
  assert.match(diogene, /Évitez la confrontation&nbsp;: proposez votre aide plutôt que de l’imposer\./);
  assert.match(diogene, /avant même de parler de devis\./);
});

test("colonne droite : sur-titre, titre en deux phrases (seconde en italique) et paragraphe", () => {
  const diogene = section("diogene");
  assert.match(diogene, /<span class="sur-titre">Syndrome de Diogène<\/span>/);
  assert.match(diogene, /<h2 id="diogene-titre">Un logement devenu impossible à vivre&nbsp;\? <em>On vous aide, sans jugement\.<\/em><\/h2>/);
  assert.match(diogene, /Le syndrome de Diogène est une souffrance, pas un choix\./);
  assert.match(diogene, /nous intervenons avec tact, en accord avec la personne et à son rythme\./);
});

test("engagements : quatre cartes en grille 2 × 2, une seule colonne sous 600 px", () => {
  const diogene = section("diogene");
  assert.equal(compter(diogene, /class="diogene-engagement"/g), 4, "quatre engagements attendus");
  for (const [titre, texte] of engrenages) {
    assert.ok(diogene.includes(`<strong>${titre}</strong>`), `engagement attendu : ${titre}`);
    assert.ok(diogene.includes(texte), `texte attendu pour « ${titre} » : ${texte}`);
  }
  assert.match(css, /\.diogene-engagements\{[^}]*grid-template-columns:repeat\(2,minmax\(0,1fr\)\)/);
  assert.match(css, /@media\s*\(max-width:599\.98px\)[\s\S]*?\.diogene-engagements\{grid-template-columns:1fr\}/);
});

test("boutons : téléphone et WhatsApp identiques à ceux de l'en-tête, libellés attendus", () => {
  const diogene = section("diogene");
  const entete = page.match(/<header[\s\S]*?<\/header>/)?.[0];
  assert.ok(entete);
  const telEntete = entete.match(/href="(tel:[^"]+)"/)?.[1];
  assert.ok(telEntete, "l'en-tête porte le numéro d'appel de la page");

  // WhatsApp : une seule valeur de lien wa.me dans la page (hors paramètre de message).
  const whatsapps = [...new Set([...page.matchAll(/href="(https:\/\/wa\.me\/[^"?]+)/g)].map(([, href]) => href))];
  assert.equal(whatsapps.length, 1, "la page n'utilise qu'un seul compte WhatsApp");

  const actions = liens(diogene).filter((lien) => lien.classe.includes("bouton"));
  assert.equal(actions.length, 2, "deux boutons attendus dans la section");
  const appel = actions.find((lien) => lien.texte === "En parler en toute discrétion");
  const photos = actions.find((lien) => lien.texte === "Envoyer des photos");
  assert.ok(appel, "bouton « En parler en toute discrétion » attendu");
  assert.ok(photos, "bouton « Envoyer des photos » attendu");
  assert.equal(appel.href, telEntete, "le bouton d'appel reprend le numéro de l'en-tête");
  assert.equal(photos.href, whatsapps[0], "le bouton photos reprend le WhatsApp du reste de la page");
});

test("carte de prestation : titre Diogène, texte et lien vers #diogene", () => {
  const prestations = page.match(/<section id="prestations"[\s\S]*?<\/section>/)?.[0];
  assert.ok(prestations);
  const cartes = prestations.split('<article class="prestation-carte">');
  assert.equal(cartes.length - 1, 4, "quatre cartes de prestation attendues");
  const carte = cartes[4];
  assert.match(carte, /<h3>Diogène &amp; logement très encombré<\/h3>/);
  assert.match(carte, /Accumulation importante&nbsp;: intervention discrète, sans jugement, à votre rythme\./);
  assert.match(carte, /<a class="prestation-approche" href="#diogene">Notre approche, ci-dessous<\/a>/);
  assert.match(carte, /alt="Pièce très encombrée avant intervention"/);
  assert.equal(prestations.includes("Coordination avec les proches"), false, "l'ancienne accroche est remplacée par le lien");
});

test("FAQ : sept questions, celle sur le syndrome de Diogène juste avant « Et si je veux garder certaines choses ? »", () => {
  const faq = section("faq");
  assert.ok(faq);
  assert.equal(compter(faq, /<details(?:\s|>)/g), 7, "sept accordéons dans la FAQ");
  assert.equal(compter(faq, /<summary>/g), 7, "sept questions dans la FAQ");
  assert.match(
    faq,
    /<summary>Intervenez-vous en cas de syndrome de Diogène&nbsp;\?<\/summary>\s*<p>Oui, avec discrétion et sans jugement, en accord avec la personne concernée ou sa famille, et à son rythme\. Un premier échange par téléphone permet de préparer l’intervention\.<\/p>/
  );
  assert.ok(
    faq.indexOf("Intervenez-vous en cas de syndrome de Diogène&nbsp;?") < faq.indexOf("Et si je veux garder certaines choses&nbsp;?"),
    "la question Diogène précède la dernière question"
  );
  assert.equal(compter(page, /<details(?:\s|>)/g), 7);
});

test("aucune affirmation invérifiable : ni certification, ni désinfection, ni chiffre inventé", () => {
  for (const motif of ["Certibiocide", "certifié", "désinfection", "équipe formée"]) {
    assert.equal(compter(page, motif), 0, `index.html ne doit pas contenir « ${motif} »`);
  }
});

test("responsive : une colonne sous 900 px, gouttière commune, fond Diogène indépendant du contenu", () => {
  assert.match(section("diogene"), /class="bande bande-diogene"/);
  assert.match(section("diogene"), /class="diogene conteneur"/);
  assert.match(css, /\.bande\{[^}]*margin:0 auto 40px/);
  assert.match(css, /\.diogene\{[^}]*padding-block:64px/);
  assert.match(css, /\.bande\{[^}]*border-radius:32px/);
  assert.match(css, /\.bande-diogene\{background:#E4ECDF/);
  assert.match(css, /\.diogene\{[^}]*grid-template-columns:minmax\(0,\.85fr\) minmax\(0,1fr\)/);
  assert.match(css, /@media\s*\(max-width:899\.98px\)[\s\S]*?\.diogene\{[^}]*grid-template-columns:1fr/);
  assert.doesNotMatch(css, /\.diogene\{[^}]*margin:0 16px/, "la section ne doit pas ajouter sa propre marge à la gouttière");
  assert.match(css, /\.diogene-media img\{[^}]*max-width:100%|\.diogene-media img\{[^}]*width:100%/);
});
