#!/usr/bin/env bash

# 1. Remove lines that doesn't start with < and ends with > or >[punct] and replace double spaces with single space
# 2. Change \t to /t
for f in */output.txt; do
  echo $f && grep '^<[a-z\-]*>.*\W$' $f | sed 's/\\t/\/t/g' | grep -E '<([^<]+)>.*</\1>' > ${f%output.txt}/output.no_invalid_rows.txt;
done

# 4. Move leading and trailing characters into the tags to create output.sanitised.txt
python sanitisation.py
# 5. Generate the indices in as "<styles>/<lineno>" using sklearn.model_selection.KFold
# and the training/val data
python generate_folds_indices.py
# 6. Generate seq2seq data from the indices
python generate_seq2seq_data_from_idx.py
# 7. Simple check on labels
cut -d$'\t' -f 2 data/training/folds/*/train.txt | sort | uniq
cut -d$'\t' -f 2 data/training/folds/*/val.txt | sort | uniq
# 8. Create compressed archive for training and validation data
tar cvfz etd_22_styles_0_001_frac.tar.gz folds/*/{val,train}.txt

grep '^<.*>\W\?$' output.txt | tr -s " " | sed 's/\\t/\/t/g' | sed -E 's/(\S*<\/[^<]+>)(<[^<]+>\S*)/\1 \2/g' > output.presanitised.txt
