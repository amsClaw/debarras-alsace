// Vérification locale et pure de la zone desservie.
// Typographie française : espace insécable (\u00a0) entre un nombre et son unité
// et avant « : », « ? », « ! », « ; ».
export function verifierZone(cp) {
  if (!/^\d{5}$/.test(cp)) return "Saisissez un code postal à 5\u00a0chiffres.";
  if (cp.startsWith("67") || cp.startsWith("68")) {
    return "Oui, nous intervenons chez vous. Devis gratuit sous 24\u00a0h.";
  }
  return "Hors de notre zone habituelle\u00a0: appelez-nous, on vous dit tout de suite.";
}
