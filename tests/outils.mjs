// Outils partagés par les tests du site.
// Aucune dépendance : uniquement la bibliothèque standard de Node.

import { readFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

// Racine du dépôt : le dossier qui contient `tests/`.
export const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

/** Les seules pages HTML publiées du site, toutes à la racine du dépôt. */
export const PAGES_SITE = ["index.html", "mentions-legales.html", "confidentialite.html", "404.html"];

/**
 * Chemins absolus des fichiers publiés du site : les pages racine et tout `assets/`.
 * @param {RegExp} [motif] filtre sur le nom de fichier
 * @returns {string[]}
 */
export function fichiersDuSite(motif = /./) {
  const fichiers = PAGES_SITE.filter((nom) => motif.test(nom)).map((nom) => path.join(RACINE, nom));
  (function parcourir(dossier) {
    for (const entree of readdirSync(dossier, { withFileTypes: true })) {
      const chemin = path.join(dossier, entree.name);
      if (entree.isDirectory()) parcourir(chemin);
      else if (motif.test(entree.name)) fichiers.push(chemin);
    }
  })(path.join(RACINE, "assets"));
  return fichiers;
}

/**
 * Renvoie le texte d'un fichier, désigné par son chemin relatif à la racine du dépôt.
 * @param {string} chemin ex. "index.html"
 * @returns {string}
 */
export function lire(chemin) {
  return readFileSync(path.join(RACINE, chemin), "utf8");
}

/**
 * Compte les occurrences d'un motif dans un texte.
 * Le motif peut être une chaîne (comparée littéralement) ou une expression régulière ;
 * dans les deux cas la recherche est globale — `/g` est ajouté si besoin, sinon
 * `String.match` renverrait les groupes de capture et non le nombre de correspondances.
 * @param {string} texte
 * @param {string|RegExp} motif
 * @returns {number}
 */
export function compter(texte, motif) {
  const drapeaux = motif instanceof RegExp ? motif.flags.replace(/[gy]/g, "") + "g" : "g";
  const source = motif instanceof RegExp ? motif.source : echapper(motif);
  return (texte.match(new RegExp(source, drapeaux)) ?? []).length;
}

/** Échappe les caractères qui auraient un sens particulier dans une expression régulière. */
function echapper(texte) {
  return String(texte).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
