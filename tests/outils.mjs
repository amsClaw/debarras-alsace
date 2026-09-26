// Outils partagés par les tests du site (V3).
// Aucune dépendance : uniquement la bibliothèque standard de Node.

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

// Racine du dépôt : le dossier qui contient `tests/`.
export const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

/**
 * Renvoie le texte d'un fichier, désigné par son chemin relatif à la racine du dépôt.
 * @param {string} chemin ex. "v3/index.html"
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
