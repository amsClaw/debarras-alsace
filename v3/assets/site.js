// Débarras Alsace — V3, point d'entrée du site.
//
// Chargé en `type="module"` pour que les comportements de la page puissent vivre
// dans des modules à part (fonctions pures importables et testables), et non dans
// ce fichier. Cette histoire ajoute le formulaire « Devis express » : il envoie
// vers WhatsApp par défaut, avec un lien e-mail alternatif.

import { composerMessage } from "./message.js";

// Les liens tel: et wa.me ont déjà un lien fonctionnel dans le HTML (mêmes
// valeurs que config.js) : cette mise à jour ne fait que refléter une éventuelle
// modification de window.DEBARRAS sans avoir à toucher le HTML.
const config = window.DEBARRAS;
if (config) {
  document.querySelectorAll(".lien-tel").forEach((lien) => {
    lien.href = `tel:+${config.telInternational}`;
  });
  document.querySelectorAll(".lien-whatsapp").forEach((lien) => {
    lien.href = `https://wa.me/${config.whatsapp}`;
  });
}

const form = document.getElementById("devis");

if (form) {
  form.addEventListener("submit", (evenement) => {
    evenement.preventDefault();

    const donnees = new FormData(form);
    const message = composerMessage({
      type: donnees.get("type") ?? "",
      codePostal: donnees.get("codePostal") ?? "",
      telephone: donnees.get("telephone") ?? ""
    });

    const whatsapp = window.DEBARRAS?.whatsapp ?? "";
    window.open(`https://wa.me/${whatsapp}?text=${encodeURIComponent(message)}`, "_blank", "noopener");
  });

  const lienMail = form.querySelector(".devis-mail");
  if (lienMail) {
    lienMail.addEventListener("click", (evenement) => {
      evenement.preventDefault();

      const donnees = new FormData(form);
      const message = composerMessage({
        type: donnees.get("type") ?? "",
        codePostal: donnees.get("codePostal") ?? "",
        telephone: donnees.get("telephone") ?? ""
      });

      const mail = window.DEBARRAS?.mail ?? "";
      const sujet = encodeURIComponent("Demande de devis de débarras");
      window.location.href = `mailto:${mail}?subject=${sujet}&body=${encodeURIComponent(message)}`;
    });
  }
}
