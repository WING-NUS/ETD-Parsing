#!/usr/bin/env bash

WORD_DIM=500
LOWER=1
CAP_DIM=1
ZEROES=1
PATH_TO_FOLDS=~/data/training/folds
PATH_TO_WB=~/data/embeddings/vectors_with_unk.kv
PATH_TO_TEST=~/data/test/blind_test/blind_test
PATH_TO_RESULTS=$(pwd)/results

for d in $(ls $PATH_TO_FOLDS);
do
  if [ $d -gt 0 ]
  then
    echo "Running fold #$d..." && python train.py \
    --train $PATH_TO_FOLDS/$d/train.txt \
    --test $PATH_TO_TEST \
    --dev $PATH_TO_FOLDS/$d/val.txt \
    --pre_emb $PATH_TO_WB \
    --word_dim $WORD_DIM \
    --lower $LOWER \
    --cap_dim $CAP_DIM \
    --zeros $ZEROES \
    --reload 1 > $PATH_TO_RESULTS/ETD_${WORD_DIM}_${LOWER}_${CAP_DIM}_${ZEROES}_fold_$d.out
  else
    echo "Running first fold" && python train.py \
    --train $PATH_TO_FOLDS/$d/train.txt \
    --test $PATH_TO_TEST \
    --dev $PATH_TO_FOLDS/$d/val.txt \
    --pre_emb $PATH_TO_WB \
    --word_dim $WORD_DIM \
    --lower $LOWER \
    --cap_dim $CAP_DIM \
    --zeros $ZEROES > $PATH_TO_RESULTS/ETD_${WORD_DIM}_${LOWER}_${CAP_DIM}_${ZEROES}_fold_$d.out
  fi

  if [[ $? -eq 0 ]]; then
    echo "$d fold has completed successfully."
  fi
done
