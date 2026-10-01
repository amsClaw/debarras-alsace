// Parcours filmé de Débarras Alsace (barreau `video` de l'usine) — le cahier de recette de H8
// (bascule de la V3 corrigée par H10 et H11). Voir outil.cjs pour les règles.
// Chaque histoire qui touche une page AJOUTE ses étapes ici, sans retirer celles des autres.
const { filmer } = require('./outil.cjs');

const TEL = '+33699544926';
const WA = 'https://wa.me/33699544926';
const MAIL = 'moisenelson17@gmail.com';

// Le site est publié sous https://amsclaw.github.io/debarras-alsace/ : l'usine le sert sous le
// même chemin (/debarras-alsace/), sinon la page introuvable (base href) ne peut pas être vérifiée.
const CHEMIN = process.env.CHEMIN_SITE ?? '/debarras-alsace';

filmer(async ({ page, etape, ecran, URL_APP: RACINE, dansLEcran, pasDeDebordement }) => {
  const URL_APP = `${RACINE}${CHEMIN}`;
  const telephone = ecran.largeur < 900;
  const visible = (sel) => page.locator(sel).filter({ visible: true }).first();
  const texte = (t) => page.getByText(t, { exact: false }).filter({ visible: true }).first();
  const lienPopup = async (action) => {
    const [popup] = await Promise.all([page.context().waitForEvent('page', { timeout: 8000 }), action()]);
    return popup.url();
  };

  await etape('Cas 1 · La page d’accueil', async () => {
    await page.goto(`${URL_APP}/`);
    await texte('Vous montrez ce qui doit partir').waitFor();
    await visible('.carte-devis').waitFor();
    await pasDeDebordement(page);
    const crochets = (await page.evaluate(() => document.body.innerText)).match(/\[[^\]\n]{2,60}\]/g);
    if (crochets) throw new Error(`texte entre crochets visible : ${crochets.slice(0, 3).join(', ')}`);
  });

  await etape('Cas 14 · En-tête sur une ligne', async () => {
    const h = await page.locator('header.entete').evaluate((e) => e.getBoundingClientRect().height);
    if (h > (telephone ? 72 : 96)) throw new Error(`en-tête de ${Math.round(h)} px de haut (sur plusieurs lignes)`);
    if (!telephone) {
      const lignes = await page.locator('.entete-nav a').evaluateAll((liens) => liens.map((a) => [a.textContent.trim(), a.getClientRects().length]));
      const coupes = lignes.filter(([, n]) => n > 1).map(([t]) => t);
      if (coupes.length) throw new Error(`menu sur plusieurs lignes : ${coupes.join(', ')}`);
      const tel = await visible('.entete-tel').textContent();
      if (!/06\s?99\s?54\s?49\s?26/.test(tel.replace(/[  ]/g, ' '))) throw new Error(`numéro de l'en-tête : « ${tel.trim()} »`);
    }
  }, { capture: false });

  if (!telephone) {
    await etape('Cas 13 · Le devis ne recouvre pas l’en-tête', async () => {
      const [entete, carte] = await Promise.all([
        page.locator('header.entete').evaluate((e) => e.getBoundingClientRect().bottom),
        page.locator('.carte-devis').evaluate((e) => e.getBoundingClientRect().top),
      ]);
      if (carte < entete) throw new Error(`la carte devis commence à ${Math.round(carte)} px, sous l'en-tête qui finit à ${Math.round(entete)} px`);
    }, { capture: false });
  }

  if (telephone) {
    await etape('H12 · Le titre est sur la photo et le bouton de devis est visible dès l’ouverture (téléphone)', async () => {
      await page.evaluate(() => document.fonts.ready);
      const m = await page.evaluate(() => {
        const rect = (sel) => document.querySelector(sel).getBoundingClientRect();
        const photo = rect('.hero-photo'), titre = rect('.hero-titre'), badge = rect('.pastille');
        const bouton = rect('.hero-boutons a[href="#devis"]');
        const barre = document.querySelector('.barre-mobile');
        const limite = barre && getComputedStyle(barre).display !== 'none' ? rect('.barre-mobile').top : innerHeight;
        return { surPhoto: badge.top >= photo.top && titre.bottom <= photo.bottom, visible: bouton.top >= 0 && bouton.bottom <= limite };
      });
      if (!m.surPhoto || !m.visible) throw new Error('titre hors photo ou bouton de devis caché au premier écran');
      await pasDeDebordement(page);
    });
  } else {
    await etape('H12 · La carte de devis est entière et ne chevauche pas la photo ni l’en-tête (ordinateur)', async () => {
      const m = await page.evaluate(() => {
        const rect = (sel) => document.querySelector(sel).getBoundingClientRect();
        const carte = rect('#devis'), hero = rect('.hero'), texte = rect('.hero-texte');
        const entete = rect('.entete'), photo = rect('.hero-photo');
        return { entiere: carte.top >= entete.bottom && carte.bottom <= hero.bottom && carte.right <= innerWidth,
          distincte: carte.left >= texte.right, decor: Math.abs(photo.width - innerWidth) < 1 && Math.abs(photo.height - hero.height) < 1 };
      });
      // La photo est le décor de TOUTE la bande : pas de carte à cheval sur un bord d’image.
      if (!m.entiere || !m.distincte || !m.decor) throw new Error('carte hors bande ou non distincte de la colonne de texte');
      await dansLEcran(page, page.locator('#devis'), 'Carte de devis entière');
    });
  }

  await etape('H12 · Bouton d’en-tête compact et Bas‑Rhin sans espace parasite', async () => {
    const details = await page.evaluate(() => ({ gap: getComputedStyle(document.querySelector('.entete-devis')).gap,
      badge: document.querySelector('.pastille').textContent }));
    if (details.gap !== '0px' || !/, Bas\u2011Rhin$/.test(details.badge)) throw new Error('espacement d’en-tête ou trait d’union de Bas‑Rhin incorrect');
  }, { capture: false });

  await etape('Cas 2 et 8 · Devis en 3 étapes jusqu’à WhatsApp', async () => {
    await page.locator('#devis').scrollIntoViewIfNeeded();
    if (telephone) await visible('.barre-mobile-devis').click();
    await texte('Étape 1').waitFor();
    await page.locator('.carte-devis label', { hasText: 'Maison' }).first().click();
    await page.locator('#devis-cp').fill('67000');
    await visible('.devis-continuer').click();
    await texte('Étape 2').waitFor();
    await visible('.devis-retour').click();
    if ((await page.locator('#devis-cp').inputValue()) !== '67000') throw new Error('« Retour » a perdu le code postal');
    await visible('.devis-continuer').click();
    await visible('.devis-continuer').click();
    await texte('Étape 3').waitFor();
    await page.locator('#devis-tel').fill('06 12 34 56 78');
    const url = await lienPopup(() => visible('.devis-envoyer').click());
    // wa.me redirige vers api.whatsapp.com/send/?phone=… : les deux sont la bonne conversation.
    const adresse = new URL(url);
    const numero = adresse.hostname === 'wa.me' ? adresse.pathname.slice(1) : adresse.searchParams.get('phone');
    if (numero !== '33699544926') throw new Error(`WhatsApp ouvert vers ${url.slice(0, 80)}`);
    const message = adresse.searchParams.get('text') || '';
    if (!/Maison/.test(message) || !/67000/.test(message)) throw new Error(`message du devis incomplet : « ${message.slice(0, 120)} »`);
  });

  await etape('Cas 3 · Zone hors secteur et zone desservie', async () => {
    await page.locator('#zone-code-postal').scrollIntoViewIfNeeded();
    await page.locator('#zone-code-postal').fill('13000');
    await page.locator('#zone-reponse', { hasText: 'Hors de notre zone' }).waitFor();
    await page.locator('#zone-code-postal').fill('67400');
    await page.locator('#zone-reponse', { hasText: 'nous intervenons' }).waitFor();
  });

  await etape('Cas 4 et 18 · Estimateur de volume lisible', async () => {
    const valeurs = [];
    for (const choix of ['studio', 'maison', 'cave']) {
      await page.locator(`label:has(#volume-${choix})`).click();
      valeurs.push(await page.locator('#estimateur-m3').textContent());
    }
    if (new Set(valeurs).size < 3) throw new Error(`le volume ne change pas : ${valeurs.join(' / ')}`);
    const debordes = await page.locator('.estimateur-tuile, .estimateur-choix label').evaluateAll((els) => els
      .filter((e) => e.scrollWidth > e.clientWidth + 1).map((e) => e.textContent.trim().slice(0, 20)));
    if (debordes.length) throw new Error(`texte qui dépasse de sa case : ${debordes.join(', ')}`);
    if (/€/.test(await page.locator('#prix').innerText())) throw new Error('un prix en euros est affiché');
    await pasDeDebordement(page);
  });

  await etape('Cas 5 et 19 · Section Diogène', async () => {
    await texte('Notre approche, ci-dessous').click();
    await page.locator('#diogene-titre').waitFor();
    if (telephone) {
      const [titre, media] = await Promise.all([
        page.locator('#diogene-titre').evaluate((e) => e.getBoundingClientRect().top),
        page.locator('.diogene-media').evaluate((e) => e.getBoundingClientRect().top),
      ]);
      if (media < titre) throw new Error('la photo de la section Diogène passe avant son titre');
    }
    await texte('Vous êtes un proche').waitFor();
  });

  await etape('Cas 6 · La FAQ (7 questions)', async () => {
    const details = page.locator('.faq details');
    if ((await details.count()) !== 7) throw new Error(`${await details.count()} questions au lieu de 7`);
    await details.nth(1).locator('summary').click();
    if (!(await details.nth(1).evaluate((d) => d.open))) throw new Error('la deuxième question ne s’ouvre pas');
    await page.locator('#faq-titre').scrollIntoViewIfNeeded();
  });

  if (telephone) {
    await etape('Cas 7 et 20 · Barre du bas avec libellés', async () => {
      for (const mot of ['Appeler', 'WhatsApp', 'Devis']) await page.locator('.barre-mobile', { hasText: mot }).waitFor();
      await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
      await page.waitForTimeout(300);
      const [barre, pied] = await Promise.all([
        page.locator('.barre-mobile').evaluate((e) => e.getBoundingClientRect().top),
        page.locator('footer.pied').evaluate((e) => e.getBoundingClientRect().bottom),
      ]);
      if (pied > barre + 2) throw new Error('le bas du pied de page est caché sous la barre');
    });
  }

  await etape('Cas 21 à 23 · Vrais numéro, WhatsApp et e-mail', async () => {
    const liens = await page.evaluate(() => [...document.querySelectorAll('a[href^="tel:"], a[href*="wa.me"], a[href^="mailto:"]')].map((a) => a.getAttribute('href')));
    const faux = liens.filter((h) => !(h === `tel:${TEL}` || h.startsWith(WA) || h.startsWith(`mailto:${MAIL}`)));
    if (!liens.length || faux.length) throw new Error(`liens de contact incorrects : ${faux.slice(0, 3).join(', ') || 'aucun lien'}`);
  }, { capture: false });

  await etape('Cas 15 et 27 · « 24 h » et ponctuation insécables', async () => {
    const t = await page.evaluate(() => document.body.innerText);
    const coupables = t.match(/\d (h|m³|journée)\b|\S ([?!:;])(?=\s|$)/g);
    if (coupables) throw new Error(`espace ordinaire avant une unité ou une ponctuation : ${[...new Set(coupables)].slice(0, 4).join(' | ')}`);
    if (/'/.test(t.replace(/https?:\S+/g, ''))) throw new Error('apostrophe droite dans le texte visible');
  }, { capture: false });

  await etape('Cas 9, 25 et 26 · Pages légales', async () => {
    await page.goto(`${URL_APP}/mentions-legales.html`);
    await texte('GitHub').waitFor();
    await texte(MAIL).waitFor();
    await pasDeDebordement(page);
    const h = await page.locator('header').first().evaluate((e) => e.getBoundingClientRect().height);
    if (h > (telephone ? 72 : 96)) throw new Error(`en-tête des mentions légales de ${Math.round(h)} px`);
    await page.goto(`${URL_APP}/confidentialite.html`);
    await page.getByText(/héberg/i).first().waitFor();
    if (/fonts\.(googleapis|gstatic)/.test(await page.content())) throw new Error('la page appelle encore Google Fonts');
  });

  await etape('Cas 12 · Page introuvable en profondeur', async () => {
    await page.goto(`${URL_APP}/a/b/c`);
    await texte('Cette page n’existe pas').waitFor();
    const fond = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    if (/rgba\(0, 0, 0, 0\)|rgb\(255, 255, 255\)/.test(fond)) throw new Error(`la page introuvable a perdu sa mise en forme (fond ${fond})`);
  });
});
