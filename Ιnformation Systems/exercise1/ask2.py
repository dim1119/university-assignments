# Dimitrios Lazarakis E18089
my_dict = {"a": 10, "b": 20, "c": 30}


print("Sum is {}".format(sum(my_dict.values())))

my_list = [my_dict]


def count_list(mylist):
    print("Mean AVG {}".format(sum(mylist[0].values())/len(mylist[0])))


count_list(my_list)
