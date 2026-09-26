// Débarras Alsace — V3, composition du message « Devis express ».
//
// Fonction pure, sans effet de bord ni accès au DOM : elle prend les champs du
// formulaire et renvoie le texte du message, prêt à être encodé dans une URL
// wa.me ou mailto. Les champs vides ne sont pas insérés dans le message.

/**
 * @param {{type?: string, codePostal?: string, acces?: string, telephone?: string, quand?: string}} champs
 * @returns {string}
 */
export function composerMessage({ type = "", codePostal = "", acces = "", telephone = "", quand = "" } = {}) {
  const lignes = ["Bonjour, je souhaite un devis de débarras."];

  if (type.trim()) lignes.push(`Type : ${type.trim()}`);
  if (codePostal.trim()) lignes.push(`Code postal : ${codePostal.trim()}`);
  if (acces.trim()) lignes.push(`Accès : ${acces.trim()}`);
  if (telephone.trim()) lignes.push(`Téléphone : ${telephone.trim()}`);
  if (quand.trim()) lignes.push(`Quand : ${quand.trim()}`);

  return lignes.join("\n");
}
