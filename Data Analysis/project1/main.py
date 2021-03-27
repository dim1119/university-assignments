
#import tqdm which creates the progress bar
from tqdm import tqdm   

#number of lines in the file
total_lines=68742193    


#open the uncompressed xml with read permission
file = open('dblp-2020-04-01.xml','r')



#create the progress bar and update it every 0.3 seconds
bar = tqdm(total= total_lines, mininterval=0.3, unit="  lines", initial=0)

#create a dictionary called yearlist that will store years and the publications of each
#with format year:number of publications
yearlist = {}
line = " "
while line:

    #save the line to a variable
    line = file.readline()

    #check if <year> and </year> are found in line
    if "<year>" in line and "</year>" in line:

        #split the line off the <year> and </year>
        year=line.split("<year>")[-1].split("</year>")[0]

        #check if that year is already in the dictionary
        if year in yearlist:
            #get the value of the publications of that year and add one
            yearlist[year] = yearlist.get(year)+1
        else:

            #if the year is not found in the dictionary, save 1 to that year in the dictionary
            yearlist[year] = 1

    #update the progress bar with each new line read
    bar.update()

#close the progress bar and the file
bar.close()
file.close() 
print("")


#Write the results to file with format <year>   <number of publications in that year>
with open('publications.txt','w') as output:
    print('#{}   {}'.format('Year','Publications'),file=output)
    for key in sorted(yearlist):
        print('{}   {}'.format(key,yearlist.get(key)),file=output)
        print('{}   {}'.format(key,yearlist.get(key)))