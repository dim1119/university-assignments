#!/bin/bash

#if there are less or more than 2 arguments show the usage and exit the program
if [ $# -ne 2 ]; then
    echo "Usage: $0 <file> <string>"
    exit 1
fi

#parse the 2 arguments
file=$1
string=$2

#count lines that the string is found in the beginning, in the middle and in the end
linecount=0
begins=0
ends=0
inmiddle=0

#declaring the arrays needed to save the line numbers
declare -a linesBegin
declare -a linesEnd
declare -a linesMiddle

# go through all the lines of the text file
while read line; do
    #count the lines
    linecount=$((linecount + 1))
    #we we will use wildcard matching

    #if line starts with string
    if [[ $line == $string* ]]; then
        begins=$((begins + 1))
        linesBegin+=($linecount)
    fi
    #if line has the string
    if [[ $line == *$string* ]]; then
        inmiddle=$((inmiddle + 1))
        linesMiddle+=($linecount)
    fi
    #if line ends with that string
    if [[ $line == *$string ]]; then
        ends=$((ends + 1))
        linesEnd+=($linecount)
    fi
done <$file

#echo all the line numbers from each array
echo -e "Lines that begin with the string $string: ${linesBegin[@]}\
        \nLines that have string $string: ${linesMiddle[@]}\
        \nLines that end with the string $string: ${linesEnd[@]}\
        "
#echo the total line count for each category
echo -e "\n\nIn total $begins begin with the string $string\
        \nIn total $inmiddle lines have string $string\
        \nIn total $ends end with the string $string\
        \n"
