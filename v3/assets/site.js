// Débarras Alsace — V3, point d'entrée du site.
//
// Chargé en `type="module"` pour que les comportements de la page puissent vivre
// dans des modules à part (fonctions pures importables et testables), et non dans
// ce fichier. Cette histoire ajoute le formulaire « Devis express » : il envoie
// vers WhatsApp par défaut, avec un lien e-mail alternatif. À toute largeur, le
// formulaire devient un parcours guidé en 3 étapes (amélioration progressive :
// sans JavaScript, toutes les étapes restent visibles d'un bloc).

import { composerMessage } from "./message.js";
import { verifierZone } from "./zone.js";
import { estimer } from "./volume.js";
import { etatInitial, etapeSuivante, etapePrecedente, NB_ETAPES } from "./etapes.js";

// Contenus qui attendent une information de l'entreprise — fonctions pures, exportées
// pour les tests : elles lisent la configuration (window.DEBARRAS) et renvoient ce qu'il
// faut afficher, ou une valeur vide quand l'information n'a pas été fournie (le bloc
// correspondant reste alors masqué).
const texte = (valeur) => (typeof valeur === "string" ? valeur.trim() : valeur == null ? "" : String(valeur).trim());

/**
 * Avis clients : visibles seulement si au moins un avis réel est fourni.
 * @returns {{visible:boolean, temoignages:{texte:string, auteur:string}[], note:{note:string, nombre:string}|null, lien:string}}
 */
export function avisAffiches(config = {}) {
  const temoignages = (Array.isArray(config.avis) ? config.avis : [])
    .map((avis) => (typeof avis === "string" ? { texte: texte(avis), auteur: "" } : { texte: texte(avis?.texte), auteur: texte(avis?.auteur) }))
    .filter((avis) => avis.texte);
  const note = config.noteGoogle && texte(config.noteGoogle.note) && texte(config.noteGoogle.nombre)
    ? { note: texte(config.noteGoogle.note), nombre: texte(config.noteGoogle.nombre) }
    : null;
  const lien = /^https:\/\//.test(texte(config.lienAvisGoogle)) ? texte(config.lienAvisGoogle) : "";
  return { visible: temoignages.length > 0, temoignages, note, lien };
}

/** Ligne « commune · volume » du chantier n° `index` (0, 1, 2), ou "" si inconnue. */
export function ligneChantier(config = {}, index = 0) {
  return Array.isArray(config.chantiers) ? texte(config.chantiers[index]) : "";
}

/** Fourchette de prix validée par l'entreprise pour un choix de l'estimateur, ou "". */
export function fourchettePrix(config = {}, choix = "") {
  return config.fourchettes && typeof config.fourchettes === "object" ? texte(config.fourchettes[choix]) : "";
}

/** « Raison sociale · SIRET 123… » pour le pied de page, ou "" tant que rien n'est fourni. */
export function identiteEntreprise(config = {}) {
  const morceaux = [texte(config.raisonSociale), texte(config.siret) && `SIRET\u00a0${texte(config.siret)}`].filter(Boolean);
  return morceaux.join(" · ");
}

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
  document.querySelectorAll(".lien-mail").forEach((lien) => {
    lien.href = `mailto:${config.mail}`;
  });
  document.querySelectorAll(".texte-tel").forEach((el) => {
    el.textContent = config.tel;
  });
  document.querySelectorAll(".texte-mail").forEach((el) => {
    el.textContent = config.mail;
  });
  afficherContenusEntreprise(config);
}

// Blocs qui attendent une information de l'entreprise : masqués dans le HTML
// (attribut hidden), affichés seulement si config.js fournit la donnée.
function afficherContenusEntreprise(cfg) {
  const avis = avisAffiches(cfg);
  const modeleAvis = document.getElementById("modele-avis");
  if (modeleAvis && avis.visible) {
    const sectionAvis = modeleAvis.content.firstElementChild.cloneNode(true);
    const liste = sectionAvis.querySelector(".avis-emplacements");
    avis.temoignages.forEach(({ texte, auteur }) => {
      const citation = document.createElement("blockquote");
      citation.textContent = auteur ? `${texte} — ${auteur}` : texte;
      liste?.appendChild(citation);
    });
    const note = sectionAvis.querySelector(".avis-note");
    if (note && avis.note) {
      note.querySelector(".avis-note-valeur").textContent = avis.note.note;
      note.querySelector(".avis-note-nombre").textContent = avis.note.nombre;
      note.hidden = false;
    }
    const lien = sectionAvis.querySelector(".avis-lien");
    if (lien && avis.lien) {
      lien.href = avis.lien;
      lien.hidden = false;
    }
    modeleAvis.replaceWith(sectionAvis);
  }

  document.querySelectorAll(".realisation-lieu").forEach((el, index) => {
    const ligne = ligneChantier(cfg, index);
    if (ligne) {
      el.textContent = ligne;
      el.hidden = false;
    }
  });

  const identite = identiteEntreprise(cfg);
  const pied = document.querySelector(".pied-identite");
  if (pied && identite) {
    pied.textContent = identite;
    pied.hidden = false;
  }
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
  const notePrix = document.querySelector(".estimateur-note");
  const valeurPrix = document.getElementById("estimateur-prix");
  const mettreAJour = (choix) => {
    const valeurs = estimer(choix);
    tuileM3.textContent = valeurs.m3;
    tuileCamions.textContent = valeurs.camions;
    tuileDuree.textContent = valeurs.duree;
    // La fourchette de prix n'apparaît que si l'entreprise l'a validée (config.js).
    const fourchette = fourchettePrix(window.DEBARRAS, choix);
    if (notePrix && valeurPrix) {
      valeurPrix.textContent = fourchette;
      notePrix.hidden = !fourchette;
    }
  };
  radiosVolume.forEach((radio) => {
    radio.addEventListener("change", () => {
      if (radio.checked) mettreAJour(radio.value);
    });
  });
  const choixInitial = [...radiosVolume].find((radio) => radio.checked);
  if (choixInitial) mettreAJour(choixInitial.value);
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

  // Même parcours sur téléphone et ordinateur. Sans JavaScript, aucune classe
  // n'est ajoutée : toutes les étapes restent dans le flux, sans chevauchement.
  const etapesEl = form.querySelectorAll(".devis-etape");
  const barreProgression = form.querySelector(".devis-progression-barre");
  const labelEtapeNumero = form.querySelector(".devis-etape-numero");
  const boutonRetour = form.querySelector(".devis-retour");
  const boutonContinuer = form.querySelector(".devis-continuer");
  const recap = form.querySelector(".devis-recap");
  let etat = etatInitial();

  // Le récapitulatif reflète le message qui sera réellement envoyé : il doit donc
  // se mettre à jour à chaque saisie (téléphone, « quand »…), pas seulement lors
  // des changements d'étape.
  function mettreAJourRecap() {
    if (recap) recap.textContent = composerMessage(champsDevis(new FormData(form)));
  }

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
    mettreAJourRecap();
  }

  function activerModeEtapes() {
    form.classList.add("mode-etapes");
    etat = etatInitial();
    rendreEtape();
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

  activerModeEtapes();

  // Toute saisie (téléphone, « quand », accès, type…) met à jour le récapitulatif
  // immédiatement, sans attendre un changement d'étape.
  form.addEventListener("input", mettreAJourRecap);
  form.addEventListener("change", mettreAJourRecap);
}
