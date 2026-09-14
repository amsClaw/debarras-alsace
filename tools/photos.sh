#!/bin/bash
# Prépare les photos du site.
#
# 1) Si une photo haute définition existe dans source-client/photos-hd/ (même nom), elle est utilisée
#    telle quelle (recadrée en « cover » sur le bon rapport) : c'est la voie recommandée.
# 2) Sinon, on retombe sur la découpe de la maquette (source-client/photos/), agrandie proprement
#    (Lanczos + accentuation) : utilisable pour valider, mais basse résolution.
#
# Usage : bash tools/photos.sh
set -e
RACINE="$(cd "$(dirname "$0")/.." && pwd)"
MAQUETTE_PHOTOS="$RACINE/source-client/photos"
HD="$RACINE/source-client/photos-hd"
DEST="$RACINE/src/assets/photos"
mkdir -p "$DEST" "$HD"

# nom : largeur x hauteur de référence (rapport utilisé sur le site)
PHOTOS=(
  "hero:544:640"
  "service-maison:344:200" "service-appartement:344:200" "service-cave:344:200" "service-succession:336:200"
  "service-deces:344:216" "service-diogene:344:216" "service-pro:344:216" "service-nettoyage:336:216"
  "situations:264:416" "process:220:288" "valorisation:300:300" "strasbourg:500:280" "carte-alsace:300:280"
  "real-appart-avant:236:272" "real-appart-apres:232:272"
  "real-maison-avant:240:272" "real-maison-apres:236:272"
  "real-cave-avant:240:272" "real-cave-apres:236:272"
)

trouve_hd() { for ext in png jpg jpeg webp PNG JPG; do [ -f "$HD/$1.$ext" ] && { echo "$HD/$1.$ext"; return; }; done }

for entree in "${PHOTOS[@]}"; do
  nom="${entree%%:*}"; dims="${entree##*:}"; larg="${dims%%:*}"; haut="${dims##*:}"
  source_hd="$(trouve_hd "$nom" || true)"
  if [ -n "$source_hd" ]; then
    # photo fournie en HD : recadrage « cover » + léger piqué
    ffmpeg -loglevel error -y -i "$source_hd" \
      -vf "scale=${larg}:${haut}:force_original_aspect_ratio=increase,crop=${larg}:${haut},unsharp=5:5:0.4" \
      "$DEST/$nom.png"
    echo "HD   $nom  <- $(basename "$source_hd")"
  elif [ -f "$MAQUETTE_PHOTOS/$nom.png" ]; then
    # découpe de maquette : agrandissement Lanczos + accentuation mesurée
    ffmpeg -loglevel error -y -i "$MAQUETTE_PHOTOS/$nom.png" \
      -vf "scale=${larg}:${haut}:force_original_aspect_ratio=increase,crop=${larg}:${haut},scale=iw*1.6:ih*1.6:flags=lanczos,unsharp=5:5:0.7:5:5:0.0" \
      "$DEST/$nom.png"
    echo "maquette $nom (basse résolution — remplacer par une photo HD)"
  else
    echo "MANQUANT  $nom  (à déposer dans source-client/photos-hd/)"
  fi
done
echo
echo "Photos prêtes dans src/assets/photos — relancer : python3 tools/build.py"
