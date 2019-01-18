#!/usr/bin/env bash

# Set HOME
HOME=/diskA/yuanchuan

# Set the directory where the BibTeX files are
INPUT_PATH=~/data/ETD/extracted/journals

# Set the directory to store the generated strings
ANNOTATED_PATH=~/data/ETD/annotated/journals

BATCH_SIZE=100

# This file is needed to generate specific styles
for s in $(cat ~/data/ETD/annotated/1_2_issues_styles.txt);
do
  mkdir $ANNOTATED_PATH/$s && java -XX:ReservedCodeCacheSize=512m -cp "${CLASSPATH}:${SCALA_HOME}/lib/scala-library.jar:${HOME}/code/ETD/ref2bib-assembly-0.1.jar" sg.edu.nus.comp.wing.etd.Reference2Bibliography \
    -i $INPUT_PATH -p "*/*.bib" -B $BATCH_SIZE -s $s -o $ANNOTATED_PATH/$s/output.txt
done
