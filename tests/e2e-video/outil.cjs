// Parcours filmé de Débarras Alsace — outil commun (barreau `video` de l'usine, essai du 2026-10-01).
//
// L'usine rejoue `parcours.cjs` sur la version exacte de la carte, contre l'application démarrée
// par le barreau `start` (base de démonstration fictive), dans l'image des ouvriers (Chromium +
// Playwright). Elle archive la vidéo, les captures et `rapport.json`, que le juge regarde et
// qu'Ams voit avant sa recette. Une étape ratée fait échouer la carte.
//
// Règles : une étape = une action ou une vérification qu'un utilisateur comprendrait
// (« Toucher Famille », « Le bouton Suppr. est visible ») ; au plus 10 captures par largeur
// (20 au total) : `capture: false` pour les étapes intermédiaires ; aucune donnée réelle.
//
// En local (sans l'usine) : lancer l'application de démonstration, puis
//   URL_APP=http://localhost:8080 node tests/e2e-video/parcours.cjs
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const URL_APP = (process.env.URL_APP || 'http://localhost:8080').replace(/\/$/, '');
const SORTIE = process.env.SORTIE || path.join(__dirname, 'sortie');
// Pause après chaque étape : sans elle, la vidéo dure une seconde et personne ne peut la suivre.
const PAUSE_MS = Number(process.env.PAUSE_MS || 1200);
const LARGEURS = [
  { nom: 'telephone', largeur: 375, hauteur: 812 },
  { nom: 'ordinateur', largeur: 1280, hauteur: 800 },
];

// Échoue si l'élément n'est pas visible ET entièrement dans la largeur de l'écran
// (un bouton « Suppr. » poussé hors de l'écran est invisible pour l'utilisateur).
async function dansLEcran(page, locator, libelle) {
  await locator.first().waitFor({ state: 'visible', timeout: 5000 });
  const boite = await locator.first().boundingBox();
  const largeur = page.viewportSize().width;
  if (!boite || boite.x < 0 || boite.x + boite.width > largeur + 1) {
    throw new Error(`${libelle} est hors de l'écran (${boite ? Math.round(boite.x) + '→' + Math.round(boite.x + boite.width) : '?'} px pour ${largeur} px)`);
  }
}

// Échoue si la page est plus large que l'écran (elle glisse de côté sous le doigt).
async function pasDeDebordement(page) {
  const { doc, ecran } = await page.evaluate(() => ({ doc: document.documentElement.scrollWidth, ecran: window.innerWidth }));
  if (doc > ecran + 1) throw new Error(`la page fait ${doc} px de large pour un écran de ${ecran} px`);
}

async function filmer(scenario) {
  fs.mkdirSync(SORTIE, { recursive: true });
  const etapes = [];
  const navigateur = await chromium.launch();
  try {
    for (const ecran of LARGEURS) {
      const ctx = await navigateur.newContext({
        viewport: { width: ecran.largeur, height: ecran.hauteur }, locale: 'fr-FR',
        recordVideo: { dir: SORTIE, size: { width: ecran.largeur, height: ecran.hauteur } },
      });
      const page = await ctx.newPage();
      page.setDefaultTimeout(10000);
      page.setDefaultNavigationTimeout(15000);
      // WhatsApp, appel, e-mail : on lit le lien, rien ne part (fenêtres fermées aussitôt).
      ctx.on('page', (fenetre) => { if (fenetre !== page) fenetre.close().catch(() => {}); });
      const etape = async (nom, action, { capture = true } = {}) => {
        const fichier = path.join(SORTIE, `${String(etapes.length + 1).padStart(2, '0')}-${ecran.nom}-${nom.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\W+/g, '-').toLowerCase()}.png`);
        try {
          await action();
          await page.waitForTimeout(PAUSE_MS);
          if (capture) await page.screenshot({ path: fichier });
          etapes.push({ nom, largeur: ecran.largeur, ok: true, capture: capture ? path.basename(fichier) : null });
        } catch (erreur) {
          await page.screenshot({ path: fichier }).catch(() => {});
          etapes.push({ nom, largeur: ecran.largeur, ok: false, message: String(erreur.message).split('\n')[0].slice(0, 240), capture: path.basename(fichier) });
        }
      };
      try {
        await scenario({ page, etape, ecran, URL_APP, dansLEcran, pasDeDebordement });
      } finally {
        await ctx.close();
      }
    }
  } finally {
    await navigateur.close();
  }
  fs.writeFileSync(path.join(SORTIE, 'rapport.json'), JSON.stringify({ etapes }, null, 2));
  const ratees = etapes.filter((e) => !e.ok);
  for (const e of etapes) console.log(`${e.ok ? 'ok  ' : 'ÉCHEC'} ${e.largeur} px — ${e.nom}${e.ok ? '' : ' : ' + e.message}`);
  console.log(`${etapes.length} étape(s), ${ratees.length} en échec — sortie : ${SORTIE}`);
  process.exitCode = ratees.length ? 1 : 0;
}

module.exports = { filmer, dansLEcran, pasDeDebordement, URL_APP };
