// Tests de l'histoire 3 : zone, prestations, déroulé et médias de la page V3.
import test from "node:test";
import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { lire, compter, RACINE } from "./outils.mjs";

const { verifierZone } = await import(pathToFileURL(path.join(RACINE, "v3", "assets", "zone.js")));
const page = lire("v3/index.html");

test("verifierZone : départements 67 et 68 couverts, autres codes hors zone, saisie incomplète en attente", () => {
  const couvert = "Oui, nous intervenons chez vous. Devis gratuit sous 24 h.";
  assert.equal(verifierZone("67000"), couvert);
  assert.equal(verifierZone("68100"), couvert);
  assert.equal(verifierZone("75001"), "Hors de notre zone habituelle : appelez-nous, on vous dit tout de suite.");
  assert.equal(verifierZone("67"), "Saisissez un code postal à 5 chiffres.");
  assert.equal(verifierZone(""), "Saisissez un code postal à 5 chiffres.");
});

test("zone : champ accessible limité à cinq chiffres, réponse annoncée poliment et vérification interactive", () => {
  const champ = page.match(/<input id="zone-code-postal"[^>]*>/)?.[0];
  assert.ok(champ, "champ code postal visible attendu");
  assert.match(champ, /aria-label="Votre code postal"/);
  assert.match(champ, /maxlength="5"/);
  assert.match(champ, /pattern="\[0-9\]\{5\}"/);
  assert.match(page, /id="zone-reponse"[^>]*aria-live="polite"/);
  assert.match(lire("v3/assets/site.js"), /replace\(\/\\D\/g, ""\)\.slice\(0, 5\)/, "les caractères non numériques et au-delà de 5 chiffres sont retirés");
});

test("prestations : quatre cartes article avec leurs contenus et photos paresseuses", () => {
  const section = page.match(/<section id="prestations"[\s\S]*?<\/section>/)?.[0];
  assert.ok(section, "section prestations attendue");
  assert.match(section, /Ce que nous débarrassons/);
  assert.match(section, /<h2[^>]*>Du studio au local professionnel/);
  assert.equal(compter(section, /<article\b/g), 4);
  for (const titre of ["Maison &amp; appartement", "Cave, grenier &amp; garage", "Bureaux &amp; locaux", "Logement très encombré"]) {
    assert.ok(section.includes(titre), `titre attendu : ${titre}`);
  }
  assert.equal(compter(section, /loading="lazy"/g), 4);
  assert.match(section, /Aussi\s*:/);
  assert.equal(compter(section, /class="prestations-aussi"[\s\S]*?<span>/g), 1);
  for (const activite of ["Succession &amp; après décès", "Vente immobilière", "Déménagement", "Nettoyage après débarras", "Encombrants"]) {
    assert.ok(section.includes(activite), `pastille attendue : ${activite}`);
  }
});

test("déroulé : trois étapes numérotées et garantie d'absence d'avance", () => {
  const section = page.match(/<section id="deroule"[\s\S]*?<\/section>/)?.[0];
  assert.ok(section, "section déroulé attendue");
  const liste = section.match(/<ol[^>]*>([\s\S]*?)<\/ol>/)?.[1];
  assert.ok(liste, "liste ordonnée attendue");
  assert.equal(compter(liste, /<li\b/g), 3);
  for (const numero of ["01", "02", "03"]) assert.ok(liste.includes(`>${numero}</span>`));
  assert.match(lire("v3/assets/style.css"), /\.deroule-numero\{[^}]*color:var\(--brique\)[^}]*font-style:italic/);
  assert.match(section, /Aucune avance à verser/);
});

test("images de v3/index.html : chaque alt est renseigné et chaque fichier existe", () => {
  const images = [...page.matchAll(/<img\b([^>]*)>/g)];
  assert.ok(images.length > 0, "la page doit contenir des images");
  for (const [index, image] of images.entries()) {
    const src = image[1].match(/\bsrc="([^"]+)"/)?.[1];
    const alt = image[1].match(/\balt="([^"]*)"/)?.[1];
    assert.ok(alt?.trim(), `image ${index + 1}: alt descriptif obligatoire`);
    assert.ok(src && existsSync(path.join(RACINE, "v3", src)), `image ${index + 1}: fichier introuvable (${src})`);
  }
});

test("grille prestations : quatre colonnes, deux sous 1100 px, une sous 600 px", () => {
  const css = lire("v3/assets/style.css").replace(/\/\*[\s\S]*?\*\//g, "");
  assert.match(css, /\.prestations-grille\{[^}]*grid-template-columns:repeat\(4,minmax\(0,1fr\)\)/);
  assert.match(css, /@media\s*\(max-width:1099\.98px\)[\s\S]*?\.prestations-grille\{grid-template-columns:repeat\(2,minmax\(0,1fr\)\)/);
  assert.match(css, /@media\s*\(max-width:599\.98px\)[\s\S]*?\.prestations-grille,\.deroule-etapes\{grid-template-columns:1fr\}/);
});
