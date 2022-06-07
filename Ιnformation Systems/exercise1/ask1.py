# Dimitrios Lazarakis E18089
my_list = [100, 200, 300, 199, 99, 9]
a_list = [101, 202, 303]


def extendList(my_list, a_list):
    my_list.extend(a_list)


def sum_list(my_list):
    return sum(my_list)


def max_min_item(my_list):
    min = my_list[0]
    max = my_list[0]
    for i in my_list:
        if min > i:
            min = i
        elif max < i:
            max = i
    print("Min: {} Max: {}".format(min, max))

extendList(my_list, a_list)
print("Sum of list is {}".format(sum_list(my_list)))


max_min_item(my_list)
