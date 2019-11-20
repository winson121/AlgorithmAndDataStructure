"""randomly select pivot
    split the list into two partition
    first part of partition less than pivot
    second part of the partition >= to pivot
"""
def quickSort(array, reverse=False):
    start = 0
    end = len(array)-1
    quickSortAux(array, reverse, start, end)

def quickSortAux(array, reverse, start, end):
    #partition the array while there are at least 2 elements
    if start < end:
        # sort the partition based on the pivot chosen
        boundary = partition(array, reverse, start, end) 
        # split array into 2 partition
        quickSortAux(array, reverse, start, boundary-1)
        quickSortAux(array, reverse, boundary+1, end)

def partition(array, reverse, start, end):
    # select mid as the pivot
    mid = (start + end) // 2
    pivot = array[mid]
    # exclude the pivot element from the array
    array[start], array[mid] = array[mid], array[start]
    # start with empty partition
    index = start
    for i in range(start+1, end+1):
        """
            when there is element < pivot, include it
            into the first partition and increase 
            the partition size by one
        """
        if not reverse:
            if array[i] < pivot:
                index += 1
                array[index], array[i] = array[i], array[index]
        else:
            if array[i] >= pivot:
                index += 1
                array[index], array[i] = array[i], array[index]    
    # move the pivot back to the end of the first partition
    array[index], array[start] = array[start], array[index]
    return index

if __name__ == "__main__":
    a = [1,7,3,56,0,9,12,-8,-5,12,34,57,31,16]
    quickSort(a, True)
    print(a)