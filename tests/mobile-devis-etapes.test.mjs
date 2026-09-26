// Tests de l'histoire 6 : barre mobile fixe et devis en 3 étapes.
import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { lire, compter, RACINE } from "./outils.mjs";

const { composerMessage } = await import(pathToFileURL(path.join(RACINE, "v3", "assets", "message.js")));
const { etatInitial, etapeSuivante, etapePrecedente, NB_ETAPES } = await import(
  pathToFileURL(path.join(RACINE, "v3", "assets", "etapes.js"))
);

const page = lire("v3/index.html");
const css = lire("v3/assets/style.css").replace(/\/\*[\s\S]*?\*\//g, "");
const js = lire("v3/assets/site.js");

test("barre mobile : nav Actions rapides avec 3 liens (appeler, whatsapp, devis)", () => {
  const nav = page.match(/<nav class="barre-mobile" aria-label="Actions rapides">[\s\S]*?<\/nav>/)?.[0];
  assert.ok(nav, "la barre d'actions rapides est attendue");
  assert.match(nav, /href="tel:[^"]+"/, "lien tel: attendu");
  assert.match(nav, /class="[^"]*lien-whatsapp[^"]*" href="https:\/\/wa\.me\/[^"]+"/, "lien wa.me attendu");
  assert.match(nav, /href="#devis"/, "lien vers le devis attendu");
  assert.equal(compter(nav, /<a /g), 3, "exactement 3 liens dans la barre");
});

test("barre mobile : fixée en bas sous 768px, absente au-delà, body avec padding-bottom", () => {
  assert.match(css, /\.barre-mobile\{display:none\}/, "la barre n'existe pas visuellement par défaut (desktop)");
  assert.match(
    css,
    /@media \(max-width:767\.98px\)\{[\s\S]*?\.barre-mobile\{position:fixed;left:0;right:0;bottom:0[\s\S]*?background:var\(--vert\)/,
    "la barre doit être fixée en bas, fond vert forêt, sous 768px"
  );
  assert.match(css, /@media \(max-width:767\.98px\)\{\s*body\{padding-bottom:76px\}/, "le body reçoit un padding-bottom sous 768px");
});

test("devis en 3 étapes : étape 2 propose Plain-pied / Ascenseur / Étage sans ascenseur", () => {
  const formulaire = page.match(/<form id="devis"[\s\S]*?<\/form>/)?.[0];
  assert.ok(formulaire);
  const etape2 = formulaire.match(/<div class="devis-etape" data-etape="2">[\s\S]*?(?=<div class="devis-etape" data-etape="3">)/)?.[0];
  assert.ok(etape2, "étape 2 attendue");
  for (const choix of ["Plain-pied", "Ascenseur", "Étage sans ascenseur"]) {
    assert.match(etape2, new RegExp(`value="${choix}"`), `choix d'accès attendu : ${choix}`);
  }
  assert.equal(compter(etape2, /name="acces"/g), 3, "3 choix exclusifs pour l'accès");
});

test("devis en 3 étapes : barre de progression, libellé « Étape n / 3 », boutons Continuer / Retour", () => {
  const formulaire = page.match(/<form id="devis"[\s\S]*?<\/form>/)?.[0];
  assert.match(formulaire, /class="devis-progression"/, "barre de progression attendue");
  assert.match(formulaire, /Étape <span class="devis-etape-numero">1<\/span> \/ 3/, "libellé d'étape attendu");
  assert.match(formulaire, /class="[^"]*devis-continuer[^"]*"[^>]*>Continuer</, "bouton Continuer attendu");
  assert.match(formulaire, /class="[^"]*devis-retour[^"]*"[^>]*>Retour</, "bouton retour attendu");
});

test("amélioration progressive : sans JavaScript, toutes les étapes sont visibles d'un bloc", () => {
  // Sans la classe .mode-etapes (ajoutée par site.js), le CSS ne masque aucune étape :
  // les règles qui cachent .devis-etape ne s'appliquent qu'au sélecteur .mode-etapes.
  assert.doesNotMatch(css, /(?<!\.mode-etapes )\.devis-etape\{[^}]*display:none/, "les étapes ne doivent pas être masquées sans la classe mode-etapes");
  assert.match(css, /\.carte-devis\.mode-etapes \.devis-etape\{display:none\}/, "le masquage par étape est conditionné à .mode-etapes");
  // L'envoi (lien wa.me) reste un vrai lien fonctionnel dans le HTML, sans JS.
  const formulaire = page.match(/<form id="devis"[\s\S]*?<\/form>/)?.[0];
  assert.match(formulaire, /href="https:\/\/wa\.me\/\d+\?text=/, "le lien d'envoi doit fonctionner sans JavaScript");
});

test("aucune largeur fixe > 360px hors media queries dans style.css", () => {
  // On retire les blocs @media pour ne garder que les règles de base (mobile-first) :
  // seules celles-ci doivent respecter la limite de 360px.
  const sansMedia = css.replace(/@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}/g, "");
  const motif = /(?:^|[;{])\s*(?:width|min-width)\s*:\s*(\d+)px/g;
  let correspondance;
  while ((correspondance = motif.exec(sansMedia))) {
    const valeur = Number(correspondance[1]);
    assert.ok(valeur <= 360, `largeur fixe hors media > 360px détectée : ${correspondance[0]}`);
  }
});

test("cibles cliquables : barre mobile et pastilles font au moins 44px de haut", () => {
  assert.match(css, /\.barre-mobile-lien\{[^}]*min-height:44px/, "les liens de la barre mobile doivent faire au moins 44px");
  assert.match(css, /\.pastille-radio span\{[^}]*min-height:44px/, "les pastilles radio doivent faire au moins 44px");
  assert.match(css, /\.bouton\{[^}]*height:56px/, "les boutons génériques font au moins 44px (56px)");
});

test("composerMessage inclut l'accès quand il est fourni (desktop compris)", () => {
  assert.equal(
    composerMessage({ type: "Maison", codePostal: "67000", acces: "Étage sans ascenseur", telephone: "0601020304" }),
    "Bonjour, je souhaite un devis de débarras.\nType : Maison\nCode postal : 67000\nAccès : Étage sans ascenseur\nTéléphone : 0601020304",
    "l'accès doit apparaître entre le code postal et le téléphone"
  );
  assert.equal(
    composerMessage({ type: "Maison" }),
    "Bonjour, je souhaite un devis de débarras.\nType : Maison",
    "sans accès, la ligne est omise (rétro-compatible)"
  );
});

test("site.js lit le champ acces du formulaire pour composer le message", () => {
  assert.match(js, /donnees\.get\("acces"\)/, "site.js doit lire le champ acces du FormData");
  assert.match(js, /import \{ composerMessage \} from ".\/message.js"/);
});

test("logique pure des étapes : etapeSuivante/etapePrecedente restent dans [1, 3]", () => {
  assert.equal(NB_ETAPES, 3);
  assert.deepEqual(etatInitial(), { etape: 1 });

  let etat = etatInitial();
  etat = etapeSuivante(etat);
  assert.equal(etat.etape, 2);
  etat = etapeSuivante(etat);
  assert.equal(etat.etape, 3);
  etat = etapeSuivante(etat);
  assert.equal(etat.etape, 3, "ne dépasse jamais la dernière étape");

  etat = etapePrecedente(etat);
  assert.equal(etat.etape, 2);
  etat = etapePrecedente(etat);
  assert.equal(etat.etape, 1);
  etat = etapePrecedente(etat);
  assert.equal(etat.etape, 1, "ne descend jamais sous la première étape");
});
