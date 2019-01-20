#!/usr/bin/env bash

# Set the directory where the BibTeX files are
INPUT_PATH=~/Downloads/data/ETD/extracted/etds

# Set the directory to store the generated strings
ANNOTATED_PATH=~/Downloads/data/ETD/annotated/etds

# Set the directory when the binary is
CODE_PATH=$(pwd)/code

BATCH_SIZE=50

STYLES=(apa elsevier-vancouver)
# This file is needed to generate specific styles
for s in ${STYLES[*]};
do
  if [[ ! -d $ANNOTATED_PATH/$s ]]; then
    mkdir $ANNOTATED_PATH/$s
  fi

  echo $s && java -XX:ReservedCodeCacheSize=512m -cp "${CLASSPATH}:${SCALA_HOME}/lib/scala-library.jar:$CODE_PATH/ref2bib-assembly-0.1.jar" sg.edu.nus.comp.wing.etd.Reference2Bibliography \
    -i $INPUT_PATH -p "*/*.bib" -B $BATCH_SIZE -s $s -o $ANNOTATED_PATH/$s/output.txt
done
