#!/bin/bash

#parse the 2 arguments
n1=$1
n2=$2

#declare an array for total results

declare -a total=(0 0 0 0 0)
final_array=()

#if there are less or more than 2 arguments show the usage and exit the program
if [ $# -ne 2 ] 
    then echo "Usage: $0 <permission number> <days>"
    exit 1
fi


while true; do
    #the user inserts a catalog name
    read -p "Enter a catalog name or -1 to quit: " folder

    if [ $folder = -1 ];
        then break
    fi

    #1
    command=$(find $folder -perm $n1)
    count1=$(echo $command|wc -w)
    echo -e " \n1)Found $count1 files with $n1 permissions"
    echo $command


    #2
    #mtime=modified time
    #So we search for files

    command=$(find $folder -mtime -$n2)
    count2=$(echo $command|wc -w)
    echo  -e " \n2)Found $count2 files modified in the last $n2 days"
    echo $command



    #3
    #atime=accessed time
    command=$(find $folder -atime -$n2)
    count3=$(echo $command|wc -w)
    echo -e "\n3)Found $count3 files accessed in the last $n2 days"
    echo $command


    #4
    #according to this we can use type p for FIFO (aka named pipe) files and s for socket: https://www.gnu.org/software/findutils/manual/html_node/find_html/Type.html
    #we use -o 2 get 2 types
    command=$(find $folder -type p -o -type s)
    count4=$(echo $command|wc -w)
    echo -e " \n4) Found $count4 pipe(FIFO) or socket files"
    echo $command


    #5
    #the -empty flag shows only empty files
    command=$(find $folder -empty)
    count5=$(echo $command|wc -w)
    echo -e " \n5) Found $count5 empty files"
    echo $command

    #add to total
    total[0]=$((${total[0]} + $count1))
    total[1]=$((${total[1]} + $count2))
    total[2]=$((${total[2]} + $count3))
    total[3]=$((${total[3]} + $count4))
    total[4]=$((${total[4]} + $count5))
    
    #save the string with all the calculations in the array

    final_array+=("In $folder there are: \n $count1 files with $n1 permissions \
    \n $count2 files modified in the last $n2 days \
    \n $count3 files accessed in the last $n2 days \
    \n $count4 pipe or socket files \
    \n $count5 empty files")


done


#echo the results from 1 to 5

echo -e "In total: \n1)Found ${total[0]} files with $n1 permissions \n2)Found ${total[1]} files modified in the last $n2 days"
echo -e "3)Found ${total[2]} files accessed in the last $n2 days \n4)Found ${total[3]} pipe(FIFO) or socket files"
echo -e "5)Found ${total[4]} empty files \n\n"


for i in "${final_array[@]}"
do
    echo -e "$i"
done


