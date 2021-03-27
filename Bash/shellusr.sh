#!/bin/bash

if [ $# -ne 1 ] 
    then echo "Usage: $0 <shell>"
    exit 1
fi


awk -F: -v shell="$1" '{if( $7 == shell ) print $1,$3}' /etc/passwd