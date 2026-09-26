// Tests des sections finales de l'accueil V3 (histoire 5).
import test from "node:test";
import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import path from "node:path";
import { lire, compter, RACINE } from "./outils.mjs";

const page = lire("v3/index.html");
const css = lire("v3/assets/style.css").replace(/\/\*[\s\S]*?\*\//g, "");

function section(id) {
  return page.match(new RegExp(`<section\\b(?=[^>]*\\bid="${id}")[^>]*>[\\s\\S]*?<\\/section>`))?.[0];
}

test("réalisations : trois paires avant/après avec les six photos locales", () => {
  const realisations = section("realisations");
  assert.ok(realisations);
  assert.equal(compter(realisations, /<article class="realisation-carte">/g), 3);
  assert.equal(compter(realisations, /<figcaption>Avant<\/figcaption>/g), 3);
  assert.equal(compter(realisations, /<figcaption>Après<\/figcaption>/g), 3);
  for (const image of [
    "real-maison-avant.jpg", "real-maison-apres.jpg", "real-appart-avant.jpg",
    "real-appart-apres.jpg", "real-cave-avant.jpg", "real-cave-apres.jpg"
  ]) {
    assert.ok(realisations.includes(`assets/photos/${image}`), `photo attendue : ${image}`);
    assert.ok(existsSync(path.join(RACINE, "v3/assets/photos", image)), `fichier présent : ${image}`);
  }
  for (const titre of ["Maison familiale", "Appartement", "Cave"]) assert.ok(realisations.includes(titre));
  assert.equal(compter(realisations, /\[commune\] · \[volume\]/g), 3);
  assert.match(realisations, /Visuels d'illustration — remplacés par vos chantiers réels\./);
});

test("avis : preuves honnêtes en emplacements et lien Google marqué à remplacer", () => {
  const avis = page.match(/<section class="avis conteneur"[\s\S]*?<\/section>/)?.[0];
  assert.ok(avis);
  assert.match(avis, /Ils nous ont fait confiance/);
  assert.match(avis, /Note Google : <strong>\[note réelle\]<\/strong> · <strong>\[nombre réel\]<\/strong> avis/);
  assert.match(avis, /<a href="#">Voir tous les avis sur Google<\/a>/);
  assert.match(avis, /Remplacer # par le lien réel/);
  assert.equal(compter(avis, /<blockquote>/g), 3);
  assert.equal(compter(avis, /<blockquote>\s*\[[^\]]+\]\s*<\/blockquote>/g), 3);
  for (const n of [1, 2, 3]) assert.ok(avis.includes(`[Avis Google réel n°${n}`));
});

test("zone : douze communes en liste et invitation à appeler", () => {
  const zone = section("zone");
  assert.ok(zone);
  assert.match(zone, /<h2[^>]*>/);
  assert.match(zone, /Votre commune n'est pas listée \?/);
  const communes = ["Strasbourg", "Schiltigheim", "Illkirch", "Ostwald", "Lingolsheim", "Bischheim", "Hœnheim", "Geispolsheim", "Haguenau", "Molsheim", "Obernai", "Sélestat"];
  assert.equal(compter(zone, /<li>/g), 12);
  for (const commune of communes) assert.match(zone, new RegExp(`<li>${commune}<\\/li>`));
  assert.equal(compter(page, /id="zone"/g), 1, "la vérification du code postal ne partage pas l'ancre #zone");
});

test("FAQ : six accordéons natifs, première question ouverte et signes CSS", () => {
  const faq = section("faq");
  assert.ok(faq);
  assert.equal(compter(faq, /<details(?:\s|>)/g), 6);
  assert.equal(compter(faq, /<summary>/g), 6);
  assert.match(faq, /<details open>\s*<summary>Combien coûte un débarras \?/);
  assert.match(css, /\.faq-liste summary::after\{content:"\+"/);
  assert.match(css, /\.faq-liste details\[open\] summary::after\{content:"−"/);
  assert.match(css, /\.faq-liste summary::-webkit-details-marker\{display:none\}/);
});

test("appel final et pied de page : devis, téléphone, contact, horaires et pages légales", () => {
  const appel = page.match(/<section class="appel-final"[\s\S]*?<\/section>/)?.[0];
  const pied = page.match(/<footer[\s\S]*?<\/footer>/)?.[0];
  assert.ok(appel);
  assert.ok(pied);
  assert.match(appel, /Besoin de vider un logement \?/);
  assert.match(appel, /<a class="bouton appel-devis" href="#devis">Obtenir mon devis<\/a>/);
  assert.match(appel, /<a class="bouton appel-telephone lien-tel" href="tel:[^"]+">Appeler<\/a>/);
  assert.match(pied, /\[06 XX XX XX XX\]/);
  assert.match(pied, /\[contact@domaine\.fr\]/);
  assert.match(pied, /Lundi – samedi, 8 h – 19 h/);
  assert.match(pied, /href="mentions-legales\.html"/);
  assert.match(pied, /href="confidentialite\.html"/);
});
