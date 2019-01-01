#data/0/0000/ the split of .RIS files
search_dir=$1

#the location of the .BIB, .LBIB file to be gernated, give other address if folder need to be seperate 
temp_dir=$1

#the location for the .B2S
out_dir=$1 

csl_name_file=style_names
style_files='./styles/'

citeproc_tool_path='./'
citeproc_binary='citeproc-java-tool-1.0.1/bin/citeproc-java'


stage=1

if [ "$stage" == 0 ]
then
  for entry in "$search_dir"/*
  do
    if [ ${entry: -4} == ".ris" ]
	then
        BASE="${entry##*/}"
	ris2xml $entry | xml2bib > $temp_dir/${BASE%.*}.bib
        python align_data.py $temp_dir/${BASE%.*}.bib > $temp_dir/${BASE%.*}.lbib
        fi
  done
fi



if [ "$stage" == 1 ]
then
  #to store all csl names
  declare -a myarray

  # Load file into array.
  let i=0
  while IFS=$'\n' read -r line_data; do
    myarray[i]="${line_data%.*}"
    ((++i))
  done < $csl_name_file

  declare -a mask_array

  let j=0
    while [ $j -lt ${#myarray[@]} ]; do
    mask_array[j]=$RANDOM
    ((++j))
  done 


  # Use array to generate strings.
  for entry in "$temp_dir"/*
  do
    BASE="${entry##*/}"
    rm $out_dir/${BASE%.*}.b2s
    rm $out_dir/${BASE%.*}.sl
    let i=0
    while (( ${#myarray[@]} > i )); do
        if [ ${entry: -5} == ".lbib" ] && [ "${mask_array[i]}" -lt 20000 ]
          then
          $citeproc_tool_path$citeproc_binary bibliography -i $entry -s  "${myarray[i]}"  >>  $out_dir/${BASE%.*}.b2s
          if [ "$?" == 0 ]
             then
             a=$(grep 'category field' "$style_files${myarray[i]}".csl | tr -d '\n')
             echo "${myarray[i]}" $a>>  $out_dir/${BASE%.*}.sl
          fi
	fi
        ((i++))
    done
  done
fi
