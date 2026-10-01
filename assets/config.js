// Coordonnées et contenus de l'entreprise — SEUL ENDROIT à modifier : le reste du
// site les lit via `window.DEBARRAS` (les valeurs de secours écrites dans le HTML
// sont les mêmes, pour que les liens marchent aussi sans JavaScript).
//
// Tout ce qui attend une information de l'entreprise reste vide et n'est donc PAS
// affiché (décision d'Ams du 2026-10-01 : masquer plutôt qu'afficher des crochets).
// Remplir une valeur suffit à faire apparaître le bloc correspondant :
//   avis        : [{ texte: "…", auteur: "Prénom, commune" }]  → section « Ils nous ont fait confiance »
//   noteGoogle  : { note: "4,8", nombre: 23 }                  → ligne « Note Google » dans cette section
//   lienAvisGoogle : "https://…"                               → lien « Voir tous les avis sur Google »
//   chantiers   : ["Strasbourg · 25 m³", "…", "…"]             → ligne sous chaque avant/après (dans l'ordre)
//   fourchettes : { cave: "…", studio: "…", t2: "…", t4: "…", maison: "…", pro: "…" } → estimateur de volume
//   raisonSociale, siret                                       → pied de page
window.DEBARRAS = {
  tel: "06 99 54 49 26",
  telInternational: "33699544926",
  whatsapp: "33699544926",
  mail: "moisenelson17@gmail.com",
  avis: [],
  noteGoogle: null,
  lienAvisGoogle: "",
  chantiers: [],
  fourchettes: {},
  raisonSociale: "",
  siret: ""
};
