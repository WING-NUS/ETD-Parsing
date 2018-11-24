#!/bin/bash
# The shell script is used to download RIS files from NCBI citation export API.
# The input file (pmidfile) contains a list of PMIDs, each in a new line. 
# The outputs are a number of .ris files under the downloaddir. 
# The script writes log files to "logfiles"
# One may modify the "opts" variable to output in a different format. 
# For a complete reference of this API, visit: https://api.ncbi.nlm.nih.gov/lit/ctxp
# For a web interface of this API, visit: https://api.ncbi.nlm.nih.gov/lit/ctxp 
# To use it, first edit env variables (see what they mean below), and then
# change the script mode to 755 and run a shell command 
# $ chmod 755 download-ncbi-citation-api.sh
# $ ./download-ncbi-citation-api.sh
# Notes: On 2018-11-24, this API is off-line. Only the web interface is available.
# This script may run several days or several weeks,depending on the list of the
# PMID file. 
# variables to be changed as needed
# pmidfile: path containing pmids each in a separate line
pmidfile="pmid-test.txt"
# downloaddir: directory where data to be downloaded, without a trailing slash
downloaddir="./downloads"

# variables not likely to be changed
logfile="download-ncbi-citation-api.log"
baseurl="https://www.ncbi.nlm.nih.gov/pmc/utils/ctxp?ids="
opts="&idtype=pmid&report=ris"
while IFS= read -r pmid
do
    url="$baseurl$pmid$opts"
    path="$downloaddir/$pmid.ris"
    curl -o $path $url
    timestamp=`date "+%Y-%m-%dT%H:%M:%S"`
    if grep -q "No resolvable IDs found" $path; then 
        rm $path
        echo "$timestamp No resolvable IDs found: $pmid" >> $logfile
    else 
        echo "$timestamp Download to: $path" >> $logfile
    fi
done < "$pmidfile"
