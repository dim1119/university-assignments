#Calculate the binary of each character using shannon
from math import log2

def encode(frequency):
    #reprisenting e1,e2,e3...
    list_e = []
    #the lengths of each character's conversion
    list_length = []
    keep = 0

    #cycle through all the characters, sum their frequency, 
    #append it to list_e and calculate each character's length
    for i in frequency:
        keep += frequency[i]
        list_e.append(keep)
        list_length.append(log2(1/frequency[i]))
    encoded = []

    #cycle through 2 lists and the contents of list_e are converted to binary and appended to encoded
    for value,length in zip(list_e,list_length):
        binary = bin(int(value))[2:]
        encoded.append(binary)

    
    return encoded

