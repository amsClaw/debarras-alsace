#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les photos du site Débarras Alsace en local (SDXL photoréaliste, Apple Silicon / MPS).

Usage :
    ~/diffusion-venv/bin/python tools/generer_photos.py [nom1 nom2 ...]

Sans argument : génère toutes les photos manquantes dans source-client/photos-hd/.
Les prompts sont en anglais (les modèles SDXL sont nettement meilleurs en anglais) et décrivent
exactement les visuels attendus par la maquette.
"""
import os
import sys
import time

import torch
from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline, DPMSolverMultistepScheduler
from huggingface_hub import hf_hub_download

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "source-client", "photos-hd")
os.makedirs(SORTIE, exist_ok=True)

MODELE = os.environ.get("MODELE_SDXL", "SG161222/RealVisXL_V4.0")
FICHIER = os.environ.get("FICHIER_SDXL", "RealVisXL_V4.0_fp16.safetensors")
DOSSIER_MODELES = os.path.expanduser("~/diffusion-modeles")

NEGATIF = ("text, letters, words, watermark, logo, logo on shirt, embroidery on clothing, brand name, "
           "writing on clothes, signature, ui, screenshot, cgi, 3d render, painting, illustration, cartoon, "
           "low resolution, blurry, deformed hands, extra fingers, mutated hands, extra limbs, bad anatomy, "
           "oversaturated, hdr, people looking at camera, distorted faces, messy composition")

STYLE = ("photorealistic photograph, documentary style, natural daylight, 35mm lens, sharp focus, "
         "realistic scene in France, plain work clothing without any logo or text, clean and professional")

# nom : (ratio [largeur, hauteur], graine, prompt)
PHOTOS = {
    "hero": ((1216, 832), 12,
             "wide establishing photograph, two removal workers in plain dark green work trousers and shirts "
             "seen from behind, one carrying stacked cardboard boxes, walking towards a green moving van with "
             "its rear doors open, parked in a paved street of an Alsatian town with brick houses, the two "
             "workers are on the RIGHT side of the frame leaving a broad empty area on the LEFT, morning "
             "light, " + STYLE),
    "service-maison": ((1216, 832), 21,
                       "exterior facade of an Alsatian house with garden and gravel driveway, shutters, trees, "
                       "blue sky, " + STYLE),
    "service-appartement": ((1216, 832), 22,
                            "bright apartment living room with sofa, coffee table, parquet floor, cardboard "
                            "moving boxes ready to go, " + STYLE),
    "service-cave": ((1216, 832), 23,
                     "cluttered cellar with wooden shelves full of old tools, crates, bottles and boxes, bare "
                     "light bulb, stone walls, " + STYLE),
    "service-succession": ((1216, 832), 24,
                           "two people seen from behind sorting cardboard boxes and household objects on a "
                           "table in a family home interior, " + STYLE),
    "service-deces": ((1216, 832), 25,
                      "quiet sober living room with an old armchair, floor lamp, closed cardboard boxes, "
                      "parquet floor, soft light, no people, " + STYLE),
    "service-diogene": ((1216, 832), 26,
                        "extremely cluttered room, tall stacks of objects and boxes from floor to ceiling, "
                        "narrow corridor, natural light from a window, no people, " + STYLE),
    "service-pro": ((1216, 832), 27,
                    "modern open space office with black chairs, desks, glass partitions and a few cardboard "
                    "boxes, no people, " + STYLE),
    "service-nettoyage": ((1216, 832), 28,
                          "freshly cleaned empty room, shiny floor, green plant in a pot, bucket and mop "
                          "leaning against the wall, bright daylight, " + STYLE),
    "situations": ((896, 1152), 31,
                   "worker seen from behind wearing a dark green polo shirt with a shoulder bag strap, "
                   "standing in front of an apartment building entrance in Strasbourg France, looking towards "
                   "a moving truck, " + STYLE),
    "process": ((896, 1152), 32,
                "tidy bright interior with green potted plants on the floor and on a shelf, a few stacked "
                "kraft cardboard boxes, clear floor, " + STYLE),
    "valorisation": ((1024, 1024), 33,
                     "close-up of two hands holding a young green plant seedling with soil, blurred background, "
                     "warm natural light, " + STYLE),
    "strasbourg": ((1344, 768), 34,
                   "Strasbourg France, Ponts Couverts and Vauban dam on the Ill river, cathedral spire in the "
                   "distance, traditional rooftops, early evening light, " + STYLE),
    "carte-alsace": ((1024, 1024), 35,
                     "flat vector style map illustration of the Bas-Rhin Alsace region in France, soft green "
                     "and beige tones, one location pin marker, minimalist, no text, " + STYLE),
    "real-appart-avant": ((768, 896), 41,
                          "cluttered apartment living room, rustic old furniture, lots of bric-a-brac, "
                          "cardboard boxes, worn wallpaper, window on the left, before a clearance, " + STYLE),
    "real-appart-apres": ((768, 896), 42,
                          "empty clean apartment living room, same window on the left, light walls, clean "
                          "parquet floor, nothing inside, after a clearance, " + STYLE),
    "real-maison-avant": ((768, 896), 43,
                          "cluttered dining room of an old house being cleared, stacked cardboard boxes, "
                          "an old sideboard, piles of papers, bric-a-brac and bags on the floor, worn "
                          "patterned wallpaper, window on the right, " + STYLE),
    "real-maison-apres": ((768, 896), 44,
                          "empty clean dining room of a house, same window on the right, clean tiled floor and "
                          "light walls, nothing inside, after a clearance, " + STYLE),
    "real-cave-avant": ((768, 896), 45,
                        "dark cluttered cellar with metal shelving, boxes, cables and old appliances, "
                        "concrete walls, before a clearance, " + STYLE),
    "real-cave-apres": ((768, 896), 46,
                        "empty swept cellar, bare concrete floor and walls, clear passage, small window "
                        "high up, after a clearance, " + STYLE),
}


def telecharger():
    """Récupère le fichier de modèle (mis en cache dans ~/diffusion-modeles)."""
    os.makedirs(DOSSIER_MODELES, exist_ok=True)
    chemin = os.path.join(DOSSIER_MODELES, FICHIER)
    if os.path.exists(chemin) and os.path.getsize(chemin) > 100 * 1024 * 1024:
        print("  modèle déjà téléchargé : %s (%.1f Go)" % (chemin, os.path.getsize(chemin) / 1e9), flush=True)
        return chemin
    print("  téléchargement de %s / %s (plusieurs Go, une seule fois)…" % (MODELE, FICHIER), flush=True)
    return hf_hub_download(repo_id=MODELE, filename=FICHIER, local_dir=DOSSIER_MODELES)


# « après » à produire en image-à-image depuis le « avant » correspondant : la pièce, les fenêtres et
# le sol restent identiques, seul le contenu disparaît. (force_dep = taux de transformation)
APRES = {
    "real-appart-apres": ("real-appart-avant", 0.88,
                          "completely empty room, bare swept parquet floor, absolutely nothing inside, no furniture, no "
                          "boxes, no objects, light bare walls, the window on the left with its radiator, "
                          "room emptied by professional cleaners, " + STYLE),
    "real-maison-apres": ("real-maison-avant", 0.88,
                          "completely empty room, bare swept tiled floor, absolutely nothing inside, no table, no chairs, "
                          "no cupboard, no objects, light bare walls, the window on the right, room emptied by "
                          "professional cleaners, " + STYLE),
    "real-cave-apres": ("real-cave-avant", 0.88,
                        "completely empty cellar, bare swept concrete floor, absolutely nothing on the shelves, no "
                        "boxes, no appliances, no jars, empty walls, the small window high up, cellar emptied by "
                        "professional cleaners, " + STYLE),
}


def charger_img2img(pipe):
    """Réutilise les composants déjà chargés (pas de second chargement du modèle)."""
    autre = StableDiffusionXLImg2ImgPipeline(**pipe.components)
    autre.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    autre.set_progress_bar_config(disable=True)
    return autre


def masque_contenu(largeur, hauteur):
    """Masque mou : blanc sur la zone de contenu (meubles/objets) à regénérer, noir sur le pourtour
    (murs, plafond, fenêtre, plinthe, bord du sol) qui doit rester au pixel près."""
    from PIL import Image, ImageDraw, ImageFilter
    m = Image.new("L", (largeur, hauteur), 0)
    d = ImageDraw.Draw(m)
    d.rectangle([int(largeur * 0.18), int(hauteur * 0.30), int(largeur * 0.82), int(hauteur * 0.86)], fill=255)
    return m.filter(ImageFilter.GaussianBlur(max(6, largeur // 40)))


def generer_apres(pipe, nom, force=False):
    """Produit un « après » en image-à-image depuis le « avant » (même pièce)."""
    from PIL import Image
    source_nom, force_dep, prompt = APRES[nom]
    chemin_source = os.path.join(SORTIE, source_nom + ".png")
    chemin = os.path.join(SORTIE, nom + ".png")
    if not os.path.exists(chemin_source):
        print("  %-22s source absente (%s) — ignoré" % (nom, source_nom), flush=True)
        return False
    if os.path.exists(chemin) and not force:
        print("  %-22s déjà présent — ignoré" % nom, flush=True)
        return False
    img2img = charger_img2img(pipe)
    image_source = Image.open(chemin_source).convert("RGB")
    generateur = torch.Generator(device="cpu").manual_seed(PHOTOS[nom][1])
    t = time.time()
    image = img2img(prompt=prompt, negative_prompt=NEGATIF, image=image_source, strength=force_dep,
                    num_inference_steps=32, guidance_scale=5.5, generator=generateur).images[0]
    # recomposition : hors de la zone de contenu, on garde la photo d'origine au pixel près
    # (murs, fenêtre, plinthe, bord du sol) -> la pièce est bien la même entre « avant » et « après »
    from PIL import Image
    masque = masque_contenu(image_source.width, image_source.height)
    image = Image.composite(image.convert("RGB"), image_source, masque)
    image.save(chemin)
    print("  %-22s %dx%d  %.0f s (depuis %s) -> %s"
          % (nom, image.width, image.height, time.time() - t, source_nom, chemin), flush=True)
    return True


def charger():
    print("chargement du modèle %s (%s)…" % (MODELE, FICHIER), flush=True)
    t = time.time()
    try:
        chemin = telecharger()
    except Exception as e:
        print("  téléchargement impossible (%s)" % str(e)[:120], flush=True)
        print("  tentative avec un autre fichier du dépôt…", flush=True)
        chemin = hf_hub_download(repo_id=MODELE, filename="RealVisXL_V4.0.safetensors",
                                 local_dir=DOSSIER_MODELES)
    pipe = StableDiffusionXLPipeline.from_single_file(
        chemin, torch_dtype=torch.float16, use_safetensors=True, add_watermarker=False)
    print("  modèle prêt (%.0f s)" % (time.time() - t), flush=True)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config, use_karras_sigmas=True)
    pipe.set_progress_bar_config(disable=True)
    if hasattr(pipe, "enable_attention_slicing"):
        pipe.enable_attention_slicing()
    if hasattr(pipe, "enable_vae_slicing"):
        pipe.enable_vae_slicing()
    pipe = pipe.to("mps")
    return pipe


def generer(pipe, nom, ratio, graine, prompt, pas=26, force=False):
    chemin = os.path.join(SORTIE, nom + ".png")
    if os.path.exists(chemin) and not force:
        print("  %-22s déjà présent — ignoré" % nom, flush=True)
        return False
    largeur, hauteur = ratio
    generateur = torch.Generator(device="cpu").manual_seed(graine)
    t = time.time()
    image = pipe(prompt=prompt, negative_prompt=NEGATIF, width=largeur, height=hauteur,
                 num_inference_steps=pas, guidance_scale=5.5, generator=generateur).images[0]
    image.save(chemin)
    print("  %-22s %dx%d  %.0f s  -> %s" % (nom, largeur, hauteur, time.time() - t, chemin), flush=True)
    return True


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    demandes = args or list(PHOTOS.keys())
    inconnus = [d for d in demandes if d not in PHOTOS]
    mode_apres = "--apres" in sys.argv
    if mode_apres:
        demandes = [n for n in (args or list(APRES.keys())) if n in APRES]
    inconnus = [d for d in demandes if d not in PHOTOS]
    if inconnus:
        print("noms inconnus :", inconnus)
        print("disponibles :", ", ".join(PHOTOS))
        sys.exit(1)
    pipe = charger()
    if mode_apres:
        print("regénération de %d visuel(s) « après » en image-à-image…" % len(demandes), flush=True)
        for nom in demandes:
            try:
                generer_apres(pipe, nom, force=True)
            except Exception as e:
                print("  ERREUR sur %s : %s" % (nom, str(e)[:160]), flush=True)
        print("terminé — dossier : %s" % SORTIE, flush=True)
        sys.exit(0)
    print("génération de %d visuel(s)…" % len(demandes), flush=True)
    for nom in demandes:
        ratio, graine, prompt = PHOTOS[nom]
        try:
            generer(pipe, nom, ratio, graine, prompt, force=force)
        except Exception as e:
            print("  ERREUR sur %s : %s" % (nom, str(e)[:160]), flush=True)
    print("terminé — dossier : %s" % SORTIE, flush=True)
