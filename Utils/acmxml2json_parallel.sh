#!/bin/bash
# convert acm dl xml files to json in parallel
# usage: acmxml2json_parallel.sh list-acmxmlpath.txt <num-procs> 
# in which list-acmxmlurl.txt is a plain text file containing a list of paths of ACM DL XML files, one path per line
# <num-procs> is the number of processes 
# writepath is the directory to save the results

LISTFILE=$1
PROCS=$2

CMD="python3 acmxml2json.py "

# print the starting datetime
date
cat $LISTFILE | parallel --joblog parallel.log -P $PROCS $CMD "../{}"
# print the ending datetime
date
