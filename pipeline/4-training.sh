#!/usr/bin/env bash

WORD_DIM=500
LOWER=1
CAP_DIM=1
ZEROES=1
PATH_TO_FOLDS="~/data/ETD/training/folds"
PATH_TO_WB="../data/vectors_with_unk.kv"
PATH_TO_TEST="~/data/ETD/test/cora_test"

for d in $(ls folds);
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
    --reload 1 > ETD_$WORD_DIM_$LOWER_$CAP_DIM_$ZEROES_fold_$d.out
  else
    echo "Running first fold" && python train.py \
    --train $PATH_TO_FOLDS/$d/train.txt \
    --test $PATH_TO_TEST \
    --dev $PATH_TO_FOLDS/$d/val.txt \
    --pre_emb $PATH_TO_WB \
    --word_dim $WORD_DIM \
    --lower $LOWER \
    --cap_dim $CAP_DIM \
    --zeros $ZEROES > ETD_$WORD_DIM_$LOWER_$CAP_DIM_$ZEROES_fold_$d.out
  fi

  if [[ $? -eq 0 ]]; then
    echo "$d fold has completed successfully."
  fi
done
