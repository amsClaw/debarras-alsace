#!/bin/bash
# Prépare les photos du site.
#
# 1) Si une photo existe dans source-client/photos-hd/ (même nom, png/jpg/webp), elle est utilisée :
#    recadrage « cover » au rapport du site, redimensionnement pour les écrans haute densité, export JPEG.
# 2) Sinon, on retombe sur la découpe de la maquette (source-client/photos/), agrandie proprement
#    (Lanczos + accentuation) : utilisable pour valider, mais basse résolution.
#
# Sortie : src/assets/photos/<nom>.jpg  (JPEG qualité 84 — ~10x plus léger que le PNG à taille égale)
# Usage  : bash tools/photos.sh && python3 tools/build.py
set -e
RACINE="$(cd "$(dirname "$0")/.." && pwd)"
MAQUETTE_PHOTOS="$RACINE/source-client/photos"
HD="$RACINE/source-client/photos-hd"
DEST="$RACINE/src/assets/photos"
mkdir -p "$DEST" "$HD"

# nom : largeur x hauteur de sortie (2x la taille d'affichage = net sur écran Retina)
PHOTOS=(
  "hero:1100:900"
  "service-maison:720:420" "service-appartement:720:420" "service-cave:720:420" "service-succession:700:420"
  "service-deces:720:450" "service-diogene:720:450" "service-pro:720:450" "service-nettoyage:700:450"
  "situations:560:880" "process:480:620" "valorisation:640:640" "strasbourg:1000:560" "carte-alsace:480:450"
  "real-appart-avant:500:580" "real-appart-apres:490:580"
  "real-maison-avant:510:580" "real-maison-apres:500:580"
  "real-cave-avant:510:580" "real-cave-apres:500:580"
)

trouve_hd() { for ext in png PNG jpg jpeg JPG webp; do [ -f "$HD/$1.$ext" ] && { echo "$HD/$1.$ext"; return; }; done; }

# on repart d'un dossier propre : plus de .png périmés à côté des .jpg
rm -f "$DEST"/*.png "$DEST"/*.jpg

for entree in "${PHOTOS[@]}"; do
  nom="${entree%%:*}"; dims="${entree##*:}"; larg="${dims%%:*}"; haut="${dims##*:}"
  source_hd="$(trouve_hd "$nom" || true)"
  if [ -n "$source_hd" ]; then
    # photo générée en haute définition : recadrage « cover » + léger piqué
    ffmpeg -loglevel error -y -i "$source_hd" \
      -vf "scale=${larg}:${haut}:force_original_aspect_ratio=increase,crop=${larg}:${haut},unsharp=5:5:0.4" \
      -q:v 4 "$DEST/$nom.jpg"
    echo "HD   $nom  <- $(basename "$source_hd")"
  elif [ -f "$MAQUETTE_PHOTOS/$nom.png" ]; then
    # découpe de maquette : agrandissement Lanczos + accentuation mesurée
    ffmpeg -loglevel error -y -i "$MAQUETTE_PHOTOS/$nom.png" \
      -vf "scale=${larg}:${haut}:force_original_aspect_ratio=increase,crop=${larg}:${haut},scale=iw*1.4:ih*1.4:flags=lanczos,unsharp=5:5:0.7:5:5:0.0" \
      -q:v 4 "$DEST/$nom.jpg"
    echo "maquette $nom (basse résolution — remplacer par une photo HD)"
  else
    echo "MANQUANT  $nom  (à déposer dans source-client/photos-hd/)"
  fi
done
echo
echo "Photos prêtes dans src/assets/photos ($(du -sh "$DEST" | cut -f1)) — relancer : python3 tools/build.py"
