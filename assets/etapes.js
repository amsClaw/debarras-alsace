// Débarras Alsace — V3, logique pure du parcours de devis en 3 étapes (mobile).
//
// Aucun accès au DOM ici : seule la transition d'état est testée par cette
// fonction. Le rendu (afficher/masquer les blocs, mettre à jour la barre de
// progression) est fait par site.js, qui appelle etapeSuivante/etapePrecedente.

export const NB_ETAPES = 3;

/** @returns {{etape:number}} */
export function etatInitial() {
  return { etape: 1 };
}

/**
 * Avance d'une étape, sans jamais dépasser NB_ETAPES.
 * @param {{etape:number}} etat
 * @returns {{etape:number}}
 */
export function etapeSuivante(etat) {
  const actuelle = etat?.etape ?? 1;
  return { ...etat, etape: Math.min(NB_ETAPES, actuelle + 1) };
}

/**
 * Recule d'une étape, sans jamais descendre sous 1.
 * @param {{etape:number}} etat
 * @returns {{etape:number}}
 */
export function etapePrecedente(etat) {
  const actuelle = etat?.etape ?? 1;
  return { ...etat, etape: Math.max(1, actuelle - 1) };
}
