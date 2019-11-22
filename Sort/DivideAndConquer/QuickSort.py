def quickSort(array):
    start = 0
    end = len(array)-1
    quickSortAux(array, start, end)

def quickSortAux(array, start, end):
    #partition the array while there are at least 2 elements
    if start < end:
        # sort the partition based on the pivot chosen
        boundary = partition(array, start, end) 
        # split array into 2 partition
        quickSortAux(array, start, boundary-1)
        quickSortAux(array, boundary+1, end)

def partition(array, start, end):
    # select mid as the pivot
    mid = (start + end) // 2
    pivot = array[mid]
    # exclude the pivot element from the array
    array[start], array[mid] = array[mid], array[start]
    # start with empty partition
    index = start
    for i in range(start+1, end+1):
        # when there is element < pivot, include it
        # into the first partition and increase 
        # the partition size by one
        if array[i] < pivot:
            index += 1
            array[index], array[i] = array[i], array[index]
    # move the pivot back to the end of the first partition
    array[index], array[start] = array[start], array[index]
    return index