#!/bin/bash

#if there are less or more than 1 arguments show the usage and exit the program
if [ $# -ne 1 ]; then
    echo "Usage: $0 <integer>"
    exit 1
fi

#parse the argument
num=$1

#exit the program if the integer is not suitable
if [ $num -lt 1 ] || [ $num -gt 14 ]; then
    echo "The number needs to be >0 and =<14"
    exit 1
fi

#check if files ara found
lines=$(find . -newermt "$num:00" ! -newermt "$((num+1)):00"| wc -l)
echo "Found $lines files."


#if no lines are found exit the program, else make the directory
if [ $lines -eq 0 ]; then
    echo -e "Didn't find any files in the timeframe $num:00-$(($num+1)):00"
    exit 1
    elif [ ! -d "timefile" ]; then
        # only make the directory if it doesn't exist
        mkdir timefile
fi

#find all the files created between the hour given up to an hour later and copy them
find . -newermt "$num:00" ! -newermt "$((num+1)):00" -exec cp {} timefile \;
