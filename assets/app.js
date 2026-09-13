/* Débarras Alsace — interactions (menu, vérification de zone, formulaire multi-étapes,
   photos, simulateur de volume). Aucune dépendance externe, aucun cookie tiers. */
(function () {
  "use strict";

  /* ---------- suivi des événements (prêt pour GA4 / Matomo, inactif tant que rien n'est branché) ---------- */
  function track(nom, params) {
    try {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: nom }, params || {}));
    } catch (e) { /* silencieux : le site ne doit jamais casser à cause du suivi */ }
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest ? ev.target.closest("a") : null;
    if (!a) return;
    var h = a.getAttribute("href") || "";
    if (h.indexOf("tel:") === 0) track("clic_telephone", { lien: h });
    if (h.indexOf("https://wa.me/") === 0 || h.indexOf("wa.me/") > 0) track("clic_whatsapp", { lien: h });
  }, true);

  /* ---------- menu mobile ---------- */
  var panneau = document.getElementById("panneau");
  var burger = document.querySelector("[data-menu-ouvrir]");
  var fermer = document.querySelector("[data-menu-fermer]");
  function ouvrirMenu() {
    if (!panneau) return;
    panneau.setAttribute("data-ouvert", "1");
    if (burger) burger.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
    var premier = panneau.querySelector("a, button");
    if (premier) premier.focus();
  }
  function fermerMenu() {
    if (!panneau) return;
    panneau.setAttribute("data-ouvert", "0");
    if (burger) { burger.setAttribute("aria-expanded", "false"); burger.focus(); }
    document.body.style.overflow = "";
  }
  if (burger) burger.addEventListener("click", ouvrirMenu);
  if (fermer) fermer.addEventListener("click", fermerMenu);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") fermerMenu(); });
  if (panneau) panneau.addEventListener("click", function (e) {
    if (e.target.tagName === "A") fermerMenu();
  });

  /* ---------- vérification de zone (codes postaux desservis) ---------- */
  var ZONES = window.DEBARRAS_ZONES || {};
  Array.prototype.forEach.call(document.querySelectorAll("[data-zone]"), function (bloc) {
    var champ = bloc.querySelector("input");
    var bouton = bloc.querySelector("button");
    var sortie = bloc.querySelector(".zone__resultat");
    if (!champ || !bouton || !sortie) return;
    function verifier() {
      var cp = (champ.value || "").trim();
      if (!/^\d{5}$/.test(cp)) {
        sortie.setAttribute("data-etat", "ko");
        sortie.textContent = "Indiquez un code postal à 5 chiffres (exemple : 67000).";
        return;
      }
      var ville = ZONES[cp];
      if (ville) {
        sortie.setAttribute("data-etat", "ok");
        sortie.textContent = "Bonne nouvelle : nous intervenons à " + ville + " (" + cp + "). Demandez votre devis gratuit ci-dessous.";
        track("zone_verifiee", { code_postal: cp, desservie: true });
      } else {
        sortie.setAttribute("data-etat", "ko");
        sortie.textContent = "Nous n'avons pas ce code postal dans notre zone habituelle : envoyez votre demande, nous vous dirons rapidement si nous pouvons intervenir.";
        track("zone_verifiee", { code_postal: cp, desservie: false });
      }
    }
    bouton.addEventListener("click", function (e) { e.preventDefault(); verifier(); });
    champ.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); verifier(); } });
  });

  /* ---------- simulateur de volume ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-simulateur]"), function (bloc) {
    var sortie = bloc.querySelector(".resultat-simulation");
    var boutons = bloc.querySelectorAll(".volume");
    Array.prototype.forEach.call(boutons, function (b) {
      b.addEventListener("click", function () {
        Array.prototype.forEach.call(boutons, function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        if (sortie) {
          sortie.setAttribute("data-etat", "ok");
          sortie.innerHTML = "<strong>" + b.getAttribute("data-libelle") + "</strong><br>" +
            "Volume approximatif : " + b.getAttribute("data-volume-m3") + " m³. " +
            "Estimation indicative pour situer le chantier — le devis définitif est établi après échange, " +
            "car l'étage, l'accès et le tri comptent autant que le volume.";
        }
        track("simulateur_volume", { volume: b.getAttribute("data-libelle") });
      });
    });
  });

  /* ---------- formulaire multi-étapes ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-formulaire]"), function (form) {
    var etapes = form.querySelectorAll(".bloc-etape");
    var points = form.querySelectorAll(".etapes__pt");
    var boutonsSuivant = form.querySelectorAll("[data-suivant]");
    var boutonsRetour = form.querySelectorAll("[data-retour]");
    var total = etapes.length;
    var courante = 0;
    var debutSignale = false;

    function afficher(i) {
      courante = Math.max(0, Math.min(total - 1, i));
      Array.prototype.forEach.call(etapes, function (bloc, k) {
        bloc.setAttribute("data-actif", k === courante ? "1" : "0");
      });
      Array.prototype.forEach.call(points, function (p, k) {
        p.setAttribute("data-actif", k === courante ? "1" : "0");
        p.setAttribute("data-fait", k < courante ? "1" : "0");
      });
      if (!debutSignale) { track("formulaire_debut"); debutSignale = true; }
      if (courante === total - 1) construireRecap();
      var cible = etapes[courante];
      if (cible) {
        var titre = cible.querySelector("h2, h3");
        if (titre) { titre.setAttribute("tabindex", "-1"); titre.focus({ preventScroll: true }); }
      }
      window.scrollTo({ top: form.getBoundingClientRect().top + window.pageYOffset - 90, behavior: "smooth" });
    }

    function validerEtape(i) {
      var bloc = etapes[i];
      if (!bloc) return true;
      var ok = true;
      Array.prototype.forEach.call(bloc.querySelectorAll("[required]"), function (champ) {
        var parent = champ.closest(".champ") || champ.parentNode;
        var vide = (champ.type === "radio" || champ.type === "checkbox") ? !bloc.querySelector('input[name="' + champ.name + '"]:checked') : !String(champ.value || "").trim();
        if (vide) {
          ok = false;
          if (parent && parent.classList) parent.classList.add("champ--erreur");
        } else if (parent && parent.classList) {
          parent.classList.remove("champ--erreur");
        }
      });
      var tel = bloc.querySelector('input[type="tel"]');
      if (tel && tel.value && tel.value.replace(/[^0-9+]/g, "").length < 9) {
        ok = false;
        var p = tel.closest(".champ");
        if (p) p.classList.add("champ--erreur");
      }
      var mail = bloc.querySelector('input[type="email"]');
      if (mail && mail.value && !/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(mail.value)) {
        ok = false;
        var m = mail.closest(".champ");
        if (m) m.classList.add("champ--erreur");
      }
      return ok;
    }

    Array.prototype.forEach.call(boutonsSuivant, function (b) {
      b.addEventListener("click", function (e) {
        e.preventDefault();
        if (validerEtape(courante)) {
          track("formulaire_etape", { etape: courante + 1 });
          afficher(courante + 1);
        }
      });
    });
    Array.prototype.forEach.call(boutonsRetour, function (b) {
      b.addEventListener("click", function (e) { e.preventDefault(); afficher(courante - 1); });
    });

    /* récapitulatif + e-mail prérempli (envoi réel branché en V1.1) */
    function valeur(champ) {
      if (champ.type === "radio") {
        var c = form.querySelector('input[name="' + champ.name + '"]:checked');
        return c ? (c.getAttribute("data-libelle") || c.value) : "";
      }
      if (champ.type === "checkbox") { return champ.checked ? "oui" : "non"; }
      if (champ.tagName === "SELECT") {
        var o = champ.options[champ.selectedIndex];
        return o ? o.text : "";
      }
      return String(champ.value || "").trim();
    }
    function donnees() {
      var vus = {};
      var paires = [];
      Array.prototype.forEach.call(form.querySelectorAll("input[name],select[name],textarea[name]"), function (champ) {
        if (champ.type === "file" || vus[champ.name]) return;
        vus[champ.name] = true;
        var v = valeur(champ);
        if (v) paires.push({ nom: champ.name, etiquette: (champ.getAttribute("data-etiquette") || champ.name), valeur: v });
      });
      return paires;
    }
    function construireRecap() {
      var rec = form.querySelector("[data-recap]");
      if (!rec) return;
      var paires = donnees();
      var html = "<dl>";
      paires.forEach(function (p) { html += "<dt>" + p.etiquette + "</dt><dd>" + p.valeur.replace(/</g, "&lt;") + "</dd>"; });
      html += "</dl>";
      var photos = form.querySelector("[data-photos-liste]");
      var nb = photos ? photos.children.length : 0;
      if (nb) html += "<p class=\"aide\">" + nb + " photo(s) sélectionnée(s) — elles ne peuvent pas être jointes automatiquement depuis cette page : indiquez-le dans votre e-mail ou envoyez-les par WhatsApp.</p>";
      rec.innerHTML = html;
      var corps = ["Demande de devis — " + document.title, ""].concat(paires.map(function (p) { return p.etiquette + " : " + p.valeur; }));
      corps.push("");
      corps.push("Photos : " + (nb ? nb + " sélectionnée(s) sur l'appareil (à joindre ou à envoyer par WhatsApp)" : "aucune"));
      var destinataire = form.getAttribute("data-email") || "";
      var lien = "mailto:" + destinataire + "?subject=" + encodeURIComponent("Demande de devis — débarras") +
        "&body=" + encodeURIComponent(corps.join("\n"));
      var envoi = form.querySelector("[data-envoi]");
      if (envoi) { envoi.setAttribute("href", lien); envoi.setAttribute("data-pret", "1"); }
      var copie = form.querySelector("[data-copier]");
      if (copie) {
        copie.onclick = function () {
          var texte = corps.join("\n");
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(texte).then(function () { copie.textContent = "Récapitulatif copié ✓"; });
          } else {
            var ta = document.createElement("textarea");
            ta.value = texte; document.body.appendChild(ta); ta.select();
            try { document.execCommand("copy"); copie.textContent = "Récapitulatif copié ✓"; } catch (e) { }
            document.body.removeChild(ta);
          }
          track("recap_copie");
        };
      }
      track("formulaire_recap", { nb_champs: paires.length });
    }

    /* photos : aperçu local, max 5 (l'envoi réel arrive avec le backend V1.1) */
    Array.prototype.forEach.call(form.querySelectorAll('input[type="file"]'), function (input) {
      input.addEventListener("change", function () {
        var liste = form.querySelector("[data-photos-liste]");
        if (!liste) return;
        liste.innerHTML = "";
        var fichiers = Array.prototype.slice.call(input.files || []).slice(0, 5);
        if ((input.files || []).length > 5) {
          var avert = form.querySelector("[data-photos-avert]");
          if (avert) avert.textContent = "5 photos maximum : seules les 5 premières sont prises en compte.";
        }
        fichiers.forEach(function (f) {
          tracker_puis_apercu(f, liste);
        });
        var etiquette = form.querySelector("[data-fichier-nom]");
        if (etiquette) {
          etiquette.textContent = fichiers.length
            ? fichiers.length + " photo" + (fichiers.length > 1 ? "s" : "") + " sélectionnée" + (fichiers.length > 1 ? "s" : "")
            : "Aucune photo sélectionnée";
        }
        track("photo_ajoutee", { nb: fichiers.length });
      });
    });
    function tracker_puis_apercu(fichier, conteneur) {
      if (!/^image\//.test(fichier.type)) return;
      var lecteur = new FileReader();
      lecteur.onload = function () {
        var img = document.createElement("img");
        img.alt = "Photo ajoutée : " + fichier.name;
        img.src = lecteur.result;
        conteneur.appendChild(img);
      };
      lecteur.readAsDataURL(fichier);
    }

    var formExpress = form.getAttribute("data-formulaire") === "express";
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validerEtape(courante)) return;
      construireRecap();
      var envoi = form.querySelector("[data-envoi]");
      if (envoi && envoi.getAttribute("data-pret") === "1") {
        track("formulaire_envoi", { mode: formExpress ? "express" : "complet" });
        window.location.href = envoi.getAttribute("href");
      }
    });
    afficher(0);
  });

  /* ---------- année du pied de page ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-annee]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
