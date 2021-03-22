ORIG_DIR=./out_flat/
TMP_DIR=./out_tmp/

rm -rf "$TMP_DIR"
mkdir "$TMP_DIR"

for name in $ORIG_DIR*; do
    img=${name##*/}
    cp "$ORIG_DIR/$img" "$TMP_DIR/$img"
    mogrify -resize 100x100 -colors 32 -depth 4 "$TMP_DIR/$img"
    for name2 in $TMP_DIR/*; do
        img2=${name2##*/}
        if [[ "$img" != "$img2" ]]; then
            ph=$(compare -metric phash "$TMP_DIR/$img" "$TMP_DIR/$img2" null: 2>&1)
            if  [[ $(echo "$ph < 5" | bc) -eq 1 ]]; then
                echo "$img and $img2 are similar"
            fi
        fi
    done
done
echo "Done"

rm -rf "$TMP_DIR"

# fdupes -frd .