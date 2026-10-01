// Estimateur de volume — fonction pure, aucune dépendance au DOM.
// Toutes les valeurs de la maquette vivent dans ce seul tableau.

export const VOLUMES = {
  cave: { label: "Cave / garage", m3: "3–8\u00a0m³", camions: "1", duree: "2–3\u00a0h" },
  studio: { label: "Studio", m3: "8–15\u00a0m³", camions: "1", duree: "½\u00a0journée" },
  t2: { label: "T2 – T3", m3: "15–30\u00a0m³", camions: "1–2", duree: "1\u00a0journée" },
  t4: { label: "T4 et +", m3: "30–45\u00a0m³", camions: "2–3", duree: "1–2\u00a0jours" },
  maison: { label: "Maison", m3: "40–80\u00a0m³", camions: "2–4", duree: "2–3\u00a0jours" },
  pro: { label: "Local pro", m3: "sur visite", camions: "—", duree: "selon accès" }
};

/**
 * Renvoie les valeurs d'estimation pour un choix donné.
 * Retombe sur T2 – T3 si le choix est inconnu (comportement sans JavaScript).
 * @param {string} choix clé de VOLUMES
 * @returns {{label:string, m3:string, camions:string, duree:string}}
 */
export function estimer(choix) {
  return VOLUMES[choix] ?? VOLUMES.t2;
}
