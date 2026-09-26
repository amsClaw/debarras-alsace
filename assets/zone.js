// Vérification locale et pure de la zone desservie.
export function verifierZone(cp) {
  if (!/^\d{5}$/.test(cp)) return "Saisissez un code postal à 5 chiffres.";
  if (cp.startsWith("67") || cp.startsWith("68")) {
    return "Oui, nous intervenons chez vous. Devis gratuit sous 24 h.";
  }
  return "Hors de notre zone habituelle : appelez-nous, on vous dit tout de suite.";
}
