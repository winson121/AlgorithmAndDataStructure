def mergeSort(array):
    start = 0
    end = len(array)-1
    temp = [None] * len(array)
    mergeSortAux(array, temp, start, end)

def mergeSortAux(array, temp, start, end):
    # merge the array into two half while the list is not single element
    if start < end:
        mid = (start + end) // 2
        mergeSortAux(array, temp, start, mid)
        mergeSortAux(array, temp, mid+1, end)
        # merge the sorted subarray together to form a bigger sorted subarray
        mergeArray(array, temp, start, mid, end)

        # copy the sorted subarray to the original array
        for i in range(start, end+1):
            array[i] = temp[i]

def mergeArray(array, temp, start, mid, end):
    left = start
    right = mid+1
    for i in range(start, end+1):
        # if the left subarray is empty, append the element from right subarray to temp
        if left > mid:
            temp[i] = array[right]
            right += 1
        # if the right subarray is empty, append the element from left subarray to temp
        elif right > end:
            temp[i] = array[left]
            left += 1
        # if current element from the right subarray bigger than left subarray
        # append left subarray to temp 
        elif array[left] < array[right]:
            temp[i] = array[left]
            left += 1
        else:
            temp[i] = array[right]
            right += 1