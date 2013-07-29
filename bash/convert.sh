#!/bin/bash
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

function swf_to_mp3_convert() {
    for file in `ls "$1"`
    do
        if [ -d "$1"/"$file" ]
        then
            swf_to_mp3_convert "$1""/""$file"
        else
	  if [ ${file##*.} = 'swf' ]
	  then
	    echo "Converting " "$1""/""$file"
	    ffmpeg -i "$1""/""$file" "$1""/"`basename "$file" .swf`".mp3"
	    rm "$1"/"$file"
	  fi
        fi
    done
}

swf_to_mp3_convert ./ 
IFS=$SAVEIFS
