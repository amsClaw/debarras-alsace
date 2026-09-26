// Tests de l'histoire 4 : le prix en clair et l'estimateur de volume de la page V3.
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { lire, compter, RACINE } from "./outils.mjs";

const { estimer, VOLUMES } = await import(pathToFileURL(path.join(RACINE, "v3", "assets", "volume.js")));
const page = lire("v3/index.html");

test("estimer : les six choix renvoient les valeurs de la maquette", () => {
  assert.deepEqual(estimer("cave"), { label: "Cave / garage", m3: "3–8 m³", camions: "1", duree: "2–3 h" });
  assert.deepEqual(estimer("studio"), { label: "Studio", m3: "8–15 m³", camions: "1", duree: "½ journée" });
  assert.deepEqual(estimer("t2"), { label: "T2 – T3", m3: "15–30 m³", camions: "1–2", duree: "1 journée" });
  assert.deepEqual(estimer("t4"), { label: "T4 et +", m3: "30–45 m³", camions: "2–3", duree: "1–2 jours" });
  assert.deepEqual(estimer("maison"), { label: "Maison", m3: "40–80 m³", camions: "2–4", duree: "2–3 jours" });
  assert.deepEqual(estimer("pro"), { label: "Local pro", m3: "sur visite", camions: "—", duree: "selon accès" });
});

test("estimer : un choix inconnu retombe sur T2 – T3 (comportement sans JavaScript)", () => {
  assert.deepEqual(estimer("inconnu"), VOLUMES.t2);
  assert.deepEqual(estimer(undefined), VOLUMES.t2);
});

test("prix : section en deux colonnes sur fond vert forêt avec les trois cas", () => {
  const section = page.match(/<section id="prix"[\s\S]*?<\/section>/)?.[0];
  assert.ok(section, "section prix attendue");
  assert.match(section, /<span class="sur-titre sur-titre-clair">Le prix, en clair<\/span>/);
  assert.match(section, /<h2[^>]*>Un débarras n'est pas toujours payant\.<\/h2>/);
  for (const cas of ["Indemnisé", "Gratuit", "Payant"]) {
    assert.ok(section.includes(`<strong>${cas}</strong>`), `cas attendu : ${cas}`);
  }
  const css = lire("v3/assets/style.css").replace(/\/\*[\s\S]*?\*\//g, "");
  assert.match(css, /\.prix\{[^}]*grid-template-columns:repeat\(2,minmax\(0,1fr\)\)/);
  assert.match(css, /\.prix\{[^}]*border-radius:32px/);
  assert.match(css, /\.prix\{[^}]*background:var\(--vert\)/);
  assert.match(css, /@media\s*\(max-width:899\.98px\)[\s\S]*?\.prix\{grid-template-columns:1fr/);
});

test("estimateur : six boutons radio exclusifs, T2 – T3 sélectionné par défaut", () => {
  const section = page.match(/<section id="prix"[\s\S]*?<\/section>/)?.[0];
  assert.match(section, /Estimez votre volume/);
  assert.match(section, /ordre de grandeur/);
  assert.equal(compter(section, /name="volume"/g), 6);
  for (const valeur of ["cave", "studio", "t2", "t4", "maison", "pro"]) {
    assert.ok(section.includes(`value="${valeur}"`), `choix attendu : ${valeur}`);
  }
  const champT2 = section.match(/<input type="radio" name="volume" value="t2"[^>]*>/)?.[0];
  assert.match(champT2, /checked/);
  for (const valeur of ["cave", "studio", "t4", "maison", "pro"]) {
    const champ = section.match(new RegExp(`<input type="radio" name="volume" value="${valeur}"[^>]*>`))?.[0];
    assert.doesNotMatch(champ, /checked/);
  }
});

test("estimateur : les tuiles affichent les valeurs T2 – T3 sans JavaScript", () => {
  const section = page.match(/<section id="prix"[\s\S]*?<\/section>/)?.[0];
  assert.match(section, /id="estimateur-m3">15–30 m³</);
  assert.match(section, /id="estimateur-camions">1–2</);
  assert.match(section, /id="estimateur-duree">1 journée</);
});

test("estimateur : fourchette de prix en emplacement, bouton vers #devis, aucun prix inventé", () => {
  const section = page.match(/<section id="prix"[\s\S]*?<\/section>/)?.[0];
  assert.match(section, /Fourchette de prix pour ce volume : <strong>\[fourchette validée par l'entreprise\]<\/strong>/);
  assert.match(section, /<a class="bouton bouton-brique estimateur-cta" href="#devis">Recevoir mon prix ferme<\/a>/);
  assert.doesNotMatch(page, /\d+ ?€/);
});

test("estimateur : site.js met à jour les tuiles au choix, sans dupliquer les données", () => {
  const js = lire("v3/assets/site.js");
  assert.match(js, /import \{ estimer \} from ".\/volume.js"/);
  assert.match(js, /estimer\(choix\)/);
});
