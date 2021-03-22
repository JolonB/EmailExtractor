TMP_DIR=./comb_out_tmp/

rm -rf $TMP_DIR
mkdir $TMP_DIR
cp -r ./comb_out/* $TMP_DIR

cd $TMP_DIR
echo "Begin resize"
mogrify -resize 100x100 -colors 32 -depth 4 *
echo "Finish resize"
echo "Begin compare"
for img in *; do
    for img2 in *; do
        if [[ $img != $img2 ]]; then
            ph=$(compare -metric phash "$img" "$img2" null: 2>&1)
            if  [[ $(echo "$ph < 2" | bc) -eq 1 ]]; then
                echo "$img and $img2 are similar"
            fi
        fi
    done
done
echo "Finish compare"

# fdupes -frd .