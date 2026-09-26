// Débarras Alsace — V3, point d'entrée du site.
//
// Chargé en `type="module"` pour que les comportements de la page puissent vivre
// dans des modules à part (fonctions pures importables et testables), et non dans
// ce fichier. Cette histoire ajoute le formulaire « Devis express » : il envoie
// vers WhatsApp par défaut, avec un lien e-mail alternatif. Sous 768 px, le
// formulaire devient un parcours guidé en 3 étapes (amélioration progressive :
// sans JavaScript, toutes les étapes restent visibles d'un bloc).

import { composerMessage } from "./message.js";
import { verifierZone } from "./zone.js";
import { estimer } from "./volume.js";
import { etatInitial, etapeSuivante, etapePrecedente, NB_ETAPES } from "./etapes.js";

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

const champZone = document.getElementById("zone-code-postal");
const reponseZone = document.getElementById("zone-reponse");
if (champZone && reponseZone) {
  champZone.addEventListener("input", () => {
    champZone.value = champZone.value.replace(/\D/g, "").slice(0, 5);
    reponseZone.textContent = verifierZone(champZone.value);
  });
}

const radiosVolume = document.querySelectorAll('input[name="volume"]');
const tuileM3 = document.getElementById("estimateur-m3");
const tuileCamions = document.getElementById("estimateur-camions");
const tuileDuree = document.getElementById("estimateur-duree");
if (radiosVolume.length && tuileM3 && tuileCamions && tuileDuree) {
  const mettreAJour = (choix) => {
    const valeurs = estimer(choix);
    tuileM3.textContent = valeurs.m3;
    tuileCamions.textContent = valeurs.camions;
    tuileDuree.textContent = valeurs.duree;
  };
  radiosVolume.forEach((radio) => {
    radio.addEventListener("change", () => {
      if (radio.checked) mettreAJour(radio.value);
    });
  });
}

function champsDevis(donnees) {
  return {
    type: donnees.get("type") ?? "",
    codePostal: donnees.get("codePostal") ?? "",
    acces: donnees.get("acces") ?? "",
    telephone: donnees.get("telephone") ?? "",
    quand: donnees.get("quand") ?? ""
  };
}

if (form) {
  const boutonWhatsapp = form.querySelector(".devis-envoyer");
  if (boutonWhatsapp) {
    boutonWhatsapp.addEventListener("click", (evenement) => {
      evenement.preventDefault();

      const message = composerMessage(champsDevis(new FormData(form)));

      const whatsapp = window.DEBARRAS?.whatsapp ?? "";
      window.open(`https://wa.me/${whatsapp}?text=${encodeURIComponent(message)}`, "_blank", "noopener");
    });
  }

  const lienMail = form.querySelector(".devis-mail");
  if (lienMail) {
    lienMail.addEventListener("click", (evenement) => {
      evenement.preventDefault();

      const message = composerMessage(champsDevis(new FormData(form)));

      const mail = window.DEBARRAS?.mail ?? "";
      const sujet = encodeURIComponent("Demande de devis de débarras");
      window.location.href = `mailto:${mail}?subject=${sujet}&body=${encodeURIComponent(message)}`;
    });
  }

  // Parcours en 3 étapes, uniquement sous 768 px. Sans JavaScript (ou au-dessus
  // de 768 px), aucune classe n'est ajoutée : le CSS montre alors toutes les
  // étapes d'un bloc, comme la maquette desktop.
  const requeteMobile = window.matchMedia("(max-width: 767.98px)");
  const etapesEl = form.querySelectorAll(".devis-etape");
  const barreProgression = form.querySelector(".devis-progression-barre");
  const labelEtapeNumero = form.querySelector(".devis-etape-numero");
  const boutonRetour = form.querySelector(".devis-retour");
  const boutonContinuer = form.querySelector(".devis-continuer");
  const recap = form.querySelector(".devis-recap");
  let etat = etatInitial();

  function rendreEtape() {
    etapesEl.forEach((el) => {
      el.classList.toggle("devis-etape-active", Number(el.dataset.etape) === etat.etape);
    });
    if (barreProgression) barreProgression.style.width = `${Math.round((etat.etape / NB_ETAPES) * 100)}%`;
    if (labelEtapeNumero) labelEtapeNumero.textContent = String(etat.etape);
    if (boutonRetour) boutonRetour.hidden = etat.etape === 1;
    const derniereEtape = etat.etape === NB_ETAPES;
    if (boutonContinuer) boutonContinuer.hidden = derniereEtape;
    if (boutonWhatsapp) boutonWhatsapp.hidden = !derniereEtape;
    if (recap) recap.textContent = composerMessage(champsDevis(new FormData(form)));
  }

  function activerModeEtapes() {
    form.classList.add("mode-etapes");
    etat = etatInitial();
    rendreEtape();
  }

  function desactiverModeEtapes() {
    form.classList.remove("mode-etapes");
    if (boutonRetour) boutonRetour.hidden = true;
    if (boutonContinuer) boutonContinuer.hidden = true;
    if (boutonWhatsapp) boutonWhatsapp.hidden = false;
  }

  function configurerEtapes() {
    if (requeteMobile.matches) activerModeEtapes();
    else desactiverModeEtapes();
  }

  if (boutonRetour) {
    boutonRetour.addEventListener("click", () => {
      etat = etapePrecedente(etat);
      rendreEtape();
    });
  }
  if (boutonContinuer) {
    boutonContinuer.addEventListener("click", () => {
      etat = etapeSuivante(etat);
      rendreEtape();
    });
  }

  configurerEtapes();
  requeteMobile.addEventListener("change", configurerEtapes);
}
