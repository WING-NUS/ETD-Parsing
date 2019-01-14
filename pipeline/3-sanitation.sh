#!/usr/bin/env bash

# 1. Remove lines that doesn't start with < and ends with > or >[punct] and replace double spaces with single space
for d in $(ls); do echo $d && grep '^<.*>\W\?$' $d/output.txt | tr -s " " > $d/output.presanitised.txt; done
# 2. Change \t to /t
for d in $(ls); do echo $d && sed -i 's/\t/\/t/g' $d/output.presanitised.txt; done
# 3. Separate concatenated tags e.g. </tag1><tag2> to </tag1> <tag2>
for d in $(ls); do echo $d && sed -i -E 's/(\S*<\/[^<]+>)(<[^<]+>\S*)/\1 \2/g' $d/output.presanitised.txt; done
# 4. Move leading and trailing characters into the tags to create output.sanitised.txt
python sanitisation.py
# 5. Generate the indices in as "<styles>/<lineno>" using sklearn.model_selection.KFold
# and the training/val data
python generate_folds_indices.py
# 6. Generate seq2seq data from the indices
python generate_seq2seq_data_from_idx.py
# 7. Simple check on labels
cut -d$'\t' -f 2 folds/*/train.txt | sort | uniq
cut -d$'\t' -f 2 folds/*/val.txt | sort | uniq
# 8. Create compressed archive for training and validation data
tar cvfz etd_22_styles_0_001_frac.tar.gz folds/*/{val,train}.txt
