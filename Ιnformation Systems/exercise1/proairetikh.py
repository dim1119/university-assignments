# Dimitrios Lazarakis E18089
a_list = [10, 12, 14, 14, 16, 28, 28, 30]


def removeDuplicates(alist):
    tmp = []
    for num in alist:
        if not (num in tmp):
            tmp.append(num)
    return tmp


def sortList(alist):
    """
    Bubble Sort Implementation
    """
    tmp = 0

    for i in range(0, len(alist)):
        is_sorted = True
        for j in range(len(alist)-i-1):
            if alist[j] > alist[j+1]:
                alist[j], alist[j+1] = alist[j+1], alist[j]
                is_sorted = False
        if is_sorted:
            break
    return alist


print("List: {}".format(a_list))
a_list = removeDuplicates(a_list)
print("List without duplicates: {}".format(a_list))

print("Sorted List {}".format(sortList(a_list)))
