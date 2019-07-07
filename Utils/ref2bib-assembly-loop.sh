#!/usr/bin/env bash
# how to run this script:
# $ sh ref2bib-assembly-loop.sh [a list of subfolders inside INPUT_PATH]
# e.g., 
# $ sh ref2bib-assembly-loop.sh file1.txt
# in which file1.txt contains lines like below:
# /wuresearch/projects/neural-parscit/BibTeXGenerator-v3-output/719
# /wuresearch/projects/neural-parscit/BibTeXGenerator-v3-output/234
# /wuresearch/projects/neural-parscit/BibTeXGenerator-v3-output/345
#
# $ find $INPUT_PATH -maxdepth 1 -type d | cut -c63-
#
# Set the directory where the BibTeX files are
#INPUT_PATH=/wuresearch/projects/neural-parscit/BibTeXGenerator-output-subfolder

# Set the directory to store the generated strings
ANNOTATED_PATH=/home/jwu/projects/neural-parscit/src/ref2bib-assembly-loop-conf

# Set the directory when the binary is
CODE_PATH=./

# Do not change BATCH_SIZE
BATCH_SIZE=100

# all styles 
# african-online-scientific-information-systems-harvard annual-reviews apa cambridge-university-press-author-date chicago-author-date current-opinion elsevier-harvard elsevier-vancouver ieee nature oxford-the-university-of-new-south-wales springer-humanities-author-date springer-mathphys-brackets springerprotocols taylor-and-francis-harvard-x wiley-vch-books modern-language-association-7th-edition
STYLES=(african-online-scientific-information-systems-harvard annual-reviews apa cambridge-university-press-author-date chicago-author-date current-opinion elsevier-harvard elsevier-vancouver ieee nature oxford-the-university-of-new-south-wales springer-humanities-author-date springer-mathphys-brackets springerprotocols taylor-and-francis-harvard-x wiley-vch-books modern-language-association-7th-edition)

while read line
do
    d="${line##*/}"
    for s in ${STYLES[*]};
    do  
        if [[ ! -d $ANNOTATED_PATH/$s ]]; then
            mkdir $ANNOTATED_PATH/$s
        fi
        OUTFILE="$ANNOTATED_PATH/$s/output_$d.txt"
        echo $line $OUTFILE

        echo $s && java -XX:ReservedCodeCacheSize=1024m -cp "${CLASSPATH}:${SCALA_HOME}/lib/scala-library.jar:$CODE_PATH/ref2bib-assembly-0.1.1.jar" sg.edu.nus.comp.wing.etd.Reference2Bibliography \
    -i $line -p "*.bib" -B $BATCH_SIZE -s $s -o $OUTFILE
    done
done < $1
