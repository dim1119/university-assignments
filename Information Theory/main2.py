#################################################################
#prerequisites
#################################################################

#import from the previous file all the variables I will need
from main1 import log2, file, charcount, nplus1_distribution
#################################################################
#Question 3
#################################################################

#A

#copy the dictionary with the letters and their frequency
chars_encoded = charcount.copy()

#for every letter get its ascii value and convert it to a 8 bits 
for i in sorted(chars_encoded):
    chars_encoded[i] = format(ord(i),'010b')
    print(str(i) + " = " + chars_encoded[i])

#################################################################


#B

temp_count = 0

#copy the 2 character dictionary
TwoChars_encoded = nplus1_distribution.copy()

#count every entity of the dictionary and convert it to binary
for i in TwoChars_encoded:
    TwoChars_encoded = format(temp_count,'010b')
    temp_count += 1
    print(str(i[0]) + "->" + str(i[-1]) + " = " + TwoChars_encoded)



#################################################################


#C

#sort in decreasing order
from collections import OrderedDict


#sort the dictionary according to each letter's frequency in descending order
charcount= OrderedDict(sorted(charcount.items(),key=lambda k: k[1], reverse = True))

#import the file shannon.py
import shannon

#use the function encode from shannon.py
encoded = shannon.encode(charcount)

#make a copy of charcount
shannon_encoded = charcount.copy()


#assign every letter to its shannon encoded binary
count = 0
for i in shannon_encoded:
    shannon_encoded[i] = encoded[count]
    count += 1
    print("Shannon code of " + str(i) + " is " + str(shannon_encoded[i]))
 

#read the file and replace each letter with its encoded character
#in a new string

encoded_text = ""
for i in file:
    encoded_text += shannon_encoded[i]

from sys import getsizeof
print("Length with Shannon is " + str(len(encoded_text)) + " and " + str(getsizeof(encoded_text)) + " bytes")


#################################################################
#Question 4
#################################################################

#copy the original dictionary
shannon2 = charcount.copy()

#find the xn+1 of each letter and multiply the number of times it appears with xn+1
for i in charcount:
    countinstances = 0
    for j in nplus1_distribution:
        if i == j[-1]:
            countinstances += nplus1_distribution[j]
    if countinstances * charcount[i] != 0:
        shannon2[i] = charcount[i] * countinstances

#call encode from shannon.py
encoded2 = shannon.encode(shannon2)

#assign shannon code to each letter
count2 = 0
for i in shannon2:
    shannon2[i] = encoded2[count2]
    count2 += 1
    print("Improved Shannon code of " + str(i) + " is " + str(shannon2[i]))

#################################################################
#Question 5
#################################################################




print()
print("VALIDATE.TXT")
print()




from collections import Counter
file = open("validate.txt", "r", encoding='ascii', errors='ignore')
file = file.read()
#call Counter
charcount2 = Counter(file)
#sort the dictionary
charcount2= OrderedDict(sorted(charcount2.items(),key=lambda k: k[1], reverse = True))


#create a new dictionary and call shannon.encode
shannon3 = charcount2.copy()
encoded3 = shannon.encode(charcount2)


#assign code to each letter
count2 = 0
for i in shannon3:
    shannon3[i] = encoded3[count2]
    count2+=1
    print("Shannon code of " + str(i) + " is " + str(shannon_encoded[i]))




#improved shannon

#split text every 2 characters and call Counter
from textwrap import wrap
nplus1_split2 = wrap(file,2)
shannon4 = charcount2.copy()
nplus1_distribution2 = Counter(nplus1_split2)

#find the xn+1 of each character and multiply it with the time the character appears
for i in charcount2:
    countinstances = 0
    for j in nplus1_distribution2:
        if i == j[-1]:
            countinstances += nplus1_distribution2[j]
    if countinstances * charcount2[i] != 0:
        shannon4[i] = charcount2[i] * countinstances


#call encode from shannon.py
encoded4 = shannon.encode(shannon4)

#assign shannon code to each letter
count2 = 0
for i in shannon4:
    shannon4[i] = encoded4[count2]
    count2 += 1
    print("Improved Shannon code of " + str(i) + " is " + str(shannon2[i]))