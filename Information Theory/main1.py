#################################################################
#Question 1
#################################################################
# A

# open the file in reading mode
from collections import Counter
file = open("test.txt", "r", encoding='ascii', errors='ignore')

# read the contents of file
file = file.read()

# print the length of the file, while converting the integer to string to concatenate
print("There are " + str(len(file)) + " characters")


#################################################################

# B

# make an array with all the possible symbols
symbols = [".", ","]

# make a variable to count the occurrences
count = 0

# for every character in file if that character is in the array of symbols add one to count
for character in file:
    if character in symbols:
        count += 1

# print the count, while converting the integer to string to concatenate
print("The symbol count is " + str(count))


#################################################################


# C


# make a dictionary called charcount and add to it every character and the time they appear
charcount = Counter(file)


# for every character in charcount, print the characters that are letters and the times they appear in alphabettical order
for i in sorted(charcount):
    print(i, charcount[i])


#################################################################


# D

#calculate the number of all characters
sumofvalue = sum((charcount[value] for value in charcount))

for i in sorted(charcount):
    #print the probability of each character
    print("p(" + str(i) + ") = " + str(round(charcount[i] / sumofvalue,3)))

#################################################################


#E

#import form the log base 10 module
from math import log2

#cycle through the dictionary
for i in sorted(charcount):
    #make a temporary variable
    temp = charcount[i] / sumofvalue
    #calculate the entropy
    print("The entropy of " + i + " is " + str(-temp * log2(temp)))




#################################################################
#Question 2
#################################################################

#A


from textwrap import wrap



#split temp file every 2 characters
nplus1_split = wrap(file,2)

#use Counter from collections like before but now every 2 characters. Then sort it 
nplus1_distribution = Counter(nplus1_split)

#go through the new list and divide the times that something appeared by the length of the document and then print it
for i in nplus1_distribution:
    nplus1_distribution[i] = float(nplus1_distribution[i] / sumofvalue)
    print("Distribution of p(" + str(i[0]) + "," + str(i[-1]) + ") = " + str(round(nplus1_distribution[i],6)))

#################################################################






#B 

#calculate the entropy using the above list, then print each result
for i in nplus1_distribution:
    temp_entropy =  -1 * nplus1_distribution[i] * log2(nplus1_distribution[i])
    print("Entropy of H(" + str(i[0]) + "," + str(i[-1]) + ") = " + str(round(temp_entropy,6)))
    #check if entropy*2 of the first letter is bigger than the distribution
    if temp_entropy < 2* charcount.get(i[0]):
        print("     The Entropy times 2 of " + str(i[0]) + " is bigger than the distribution")
    else :
        print("     The Entropy times 2 of " + str(i[0]) + " is smaller than the distribution")
#################################################################



#C 
# done right above

#################################################################


#D

#calculating H(xn/xn+1) for every 2 characters

for i in nplus1_distribution:
    temp = -1  * nplus1_distribution[i] * log2(nplus1_distribution[i])
    print("P(" + str(i[0]) + "," + str(i[-1]) + ") entropy = " + str(round(temp,6)) ) 

print(len(file))