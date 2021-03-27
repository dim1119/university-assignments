#!/bin/bash

#create variables that counts the equations with 2 real roots and a rerun flag
count_real=0
rerun=0
while [[ $rerun != -1 ]]; do
    #User input for a,b,c
    read -p "Enter a: " a
    read -p "Enter b: " b
    read -p "Enter c: " c

    #using (( )) for arithmetics, calculate D
    Discriminant=$(($b ** 2 - 4 * $a * $c)) 

    #print the discriminant
    echo "The discriminant is: $Discriminant"
    

    
    if [ $Discriminant -gt 0 ]; then
        echo "There are 2 real roots"
        #append to count real
        count_real=$((count_real + 1))

    elif [ $Discriminant -eq 0 ]; then
        echo "There is a double root"

    else
        echo "There are 2 complex roots"
    fi
    
    #ask if the user wants to rerun the program
    read -p "Press ENTER to rerun or type -1 to exit: " rerun
done

#print the number of equations with 2 real roots
echo "The program has found $count_real equations with 2 real roots"
