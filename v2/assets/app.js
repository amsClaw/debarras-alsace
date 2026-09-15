/* Débarras Alsace — V2 : apparition douce + formulaire express qui prépare le message WhatsApp.
   Aucun serveur, aucune dépendance. Le formulaire ne prétend rien envoyer : il compose le message
   et ouvre WhatsApp (ou l'e-mail) avec le texte prêt — le visiteur garde la main. */
(function () {
  'use strict';

  var TEL = (window.DEBARRAS && window.DEBARRAS.tel) || '33612345678';
  var MAIL = (window.DEBARRAS && window.DEBARRAS.mail) || 'contact@debarras-alsace.fr';

  /* ---------- apparition douce au défilement ---------- */
  var elements = document.querySelectorAll('.rev');
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('vu'); obs.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    Array.prototype.forEach.call(elements, function (el) { obs.observe(el); });
  } else {
    Array.prototype.forEach.call(elements, function (el) { el.classList.add('vu'); });
  }

  /* ---------- formulaire express -> message prêt à envoyer ---------- */
  var form = document.getElementById('form-express');
  if (!form) { return; }

  var champCommune = form.querySelector('#f-commune');
  var champType = form.querySelector('#f-type');
  var champTel = form.querySelector('#f-tel');
  var champPrec = form.querySelector('#f-precisions');
  var zoneApercu = document.getElementById('apercu');

  function message() {
    var lignes = ['Bonjour, je souhaite un devis pour un débarras.'];
    if (champType.value) { lignes.push('Prestation : ' + champType.value + '.'); }
    if (champCommune.value.trim()) { lignes.push('Commune / code postal : ' + champCommune.value.trim() + '.'); }
    if (champPrec.value.trim()) { lignes.push('Précisions : ' + champPrec.value.trim() + '.'); }
    if (champTel.value.trim()) { lignes.push('Je peux être rappelé au ' + champTel.value.trim() + '.'); }
    lignes.push('Je peux envoyer des photos de la pièce.');
    return lignes.join('\n');
  }

  function rafraichir() {
    var txt = message();
    var wa = document.getElementById('lien-wa');
    var ml = document.getElementById('lien-mail');
    if (wa) { wa.href = 'https://wa.me/' + TEL + '?text=' + encodeURIComponent(txt); }
    if (ml) {
      ml.href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent('Demande de devis — débarras') +
                '&body=' + encodeURIComponent(txt);
    }
    if (zoneApercu) { zoneApercu.textContent = txt; }
  }

  Array.prototype.forEach.call([champCommune, champType, champTel, champPrec], function (c) {
    if (c) { c.addEventListener('input', rafraichir); c.addEventListener('change', rafraichir); }
  });
  rafraichir();

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    rafraichir();
    var wa = document.getElementById('lien-wa');
    if (wa) { window.location.href = wa.href; }
  });
  /* ---------- année du pied de page ---------- */
  var an = document.getElementById('annee');
  if (an) { an.textContent = new Date().getFullYear(); }
})();
