import sys
sys.path.append("..")
from referential_array import build_array
from Sort.DivideAndConquer.QuickSort import quickSort as QuickSort

class ArrayList:
    """Implementation of Array based List Data Structure

    Attributes:
        array {array} -- array of python references with the given size
        _count {int} -- the size of the array
    
    Methods:
        __len__() -- return the number of element in the ArrayList
        _isempty() -- check if the ArrayList is empty
        _isfull() -- check if the ArrayList is full
        __contains__(item) -- check if the item is in the ArrayList
        __getitem__(index) -- get the item at position index from ArrayList
        __setitem__(index, item) -- set the contain of ArrayList at position index to item
        __eq__(other) -- check if the ArrayList is equal to the other list
        append(item) -- append item at the end of the ArrayList if its not full already
        insert(index, item) -- insert item to ArrayList at position before index
        remove(item) -- remove the first occurence of item found in the list
        delete(index) -- remove item from the list at position index
        _shiftArrayRight(index) -- shift subarray from [index..len(self)] to the right by one step
        _shiftArrayLeft(index) -- shift subarray from[index..len(self)] to the left by one step
        _validIndex(index) -- restrict the Index range so that it behave similar to python List Indexing
        sort(reverse=False) -- use a stable sort on the ArrayList
    """

    def __init__(self, maxCapacity=10):
        """
        Keyword Arguments:
            maxCapacity {int} -- size of array (default: {10})
        """
        self.array = build_array(maxCapacity)
        self._count = 0
    
    def __len__(self):
        """return the number of element in the ArrayList
        
        Returns:
            self._count [int] -- the number of element in the ArrayList
        """
        return self._count
    
    def _isempty(self):
        """check if the ArrayList is empty
        
        Returns:
            [bool] -- return True if no item in the ArrayList, otherwise return False
        """
        return len(self) == 0
    
    def _isfull(self):
        """check if the ArrayList is full
        
        Returns:
            [bool] -- return True if number of items is more than or equal to 
                      the size of the ArrayList
        """
        return len(self) >= len(self.array)
    
    def __contains__(self, item):
        """check if the item is in the ArrayList
        
        Arguments:
            item {python object} -- item to be checked if it exit in the ArrayList
        
        Returns:
            [bool] -- return True if it exist, False otherwise

        Complexity:
            BestCase {O(1)} -- if the item is at the first element in the List
            WorstCase {O(N)} -- if the item is at the end of the list or doesn't exist
        """
        assert not self._isempty(); "list must not be empty"          
        for i in range(len(self)):
            if self.array[i] == item:
                return True
        return False

    def __getitem__(self, index):
        """get the item at position index from ArrayList
        
        Arguments:
            index {int} -- index of the item you want to get from the list
        
        Raises:
            IndexError: raise IndexError if index is out of range
        
        Returns:
            [python object] -- return item at position index
        
        Complexity:
            BestCase {O(1)} -- accessing the index position of list takes constant time
            WorstCase {O(1)} -- same as best case
        """
        if self._validIndex(index):
            return self.array[index]
        else:
            raise IndexError("list index out of range")

    def __setitem__(self, index, item):
        """set the contain of ArrayList at position index to item
        
        Arguments:
            index {int} -- index of the array we want to access
            item {python object} -- the item that we want to set on the array at index position
        
        Raises:
            IndexError: raised when index is out of range
        
        Complexity:
            BestCase {O(1)} -- take constant time to access the array
            WorstCase {O(1)} -- same as BestCase
        """
        if _validIndex(index)
            self.array[index] = item 
        else:
            raise IndexError("list index out of range") 
    
    def __eq__(self, other):
        """check if the ArrayList is equal to the other list
        
        Arguments:
            other {List, ArrayList} -- List or ArrayList object that we want to compare
        
        Returns:
            [bool] -- return True when two List contains exactly same contents
        
        Complexity:
            BestCase {O(1)} -- if the first element is not the same or other not a List or ArrayList
            WorstCase {O(N}) -- if the List is Equal
        """
        if not isinstance(self, other):
            return False
        
        for i in range(len(self)):
            if self.array[i] != other[i]:
                return False
        
        return True
        
    def append(self, item):
        """append item at the end of the ArrayList if its not full already
        
        Arguments:
            item {python object} -- item that you want to append on the List
        
        Complexity:
            BestCase {O(1)} -- accessing the Last Index of the List takes Constant time
            WorstCase {O(1)} -- same as BestCase
        """
        assert not self._isfull(); "Array is full"
        self.array[self._count] = item
        self._count += 1
        
    def insert(self, index, item):
        """insert item to ArrayList at position before index
        
        Arguments:
            index {int} -- index of the array that we want to insert the item before
            item {python object} -- the item that we want to insert to the List
        
        Raises:
            IndexError: raised if the index is out of range
        
        Complexity:
            BestCase {O(1)} -- when the insert operation is at the end of the List
            WorstCase {O(N)} -- when the item inserted at the start of the List
        """
        assert not self._isfull(), "array is full"
        if _validIndex(index):
            self._shiftArrayRight(index)
            self.array[index] = item
            self._count += 1
        else:
            raise IndexError
        

    def remove(self, item):
        """remove the first occurence of item found in the list
        
        Arguments:
            item {python object} -- the item that we want to remove from the List

        Complexity:
            BestCase {O(1)} -- if the frst occurences of item is at the end of the List
            WorstCase {O(N)} -- if the first occurences is at the start of the List 
        """
        assert not self._isempty(), "array is empty"
        for i in range(len(self)):
            if self.array[i] == item:
                self.delete(i)

    def delete(self, index):
        """remove the first occurence of item found in the list
        
        Arguments:
            index {int} -- index of the item in the array that we want to delete
        
        Raises:
            IndexError: raised when the index is out of range
        
        Complexity:
            BestCase {O(1)} -- if index == len(self)-1
            WorstCase {O(N)} -- if index is at the start of the List
        """
        if _validIndex(index):
            self._shiftArrayLeft(index)
            self._count -= 1
        else:
            raise IndexError

    def _shiftArrayRight(self, index):
        """shift subarray from [index..len(self)] to the right by one step
        
        Arguments:
            index {int} -- start position of the subarray we want to shift
        
        Complexity:
            BestCase {O(1)} -- if the index is of the Last element of the List
            WorstCase {O(N)} -- if we need to shift the whole array
        """
        if index < 0:
            index = index + len(self)
        for i in range(len(self), index, -1):
            self.array[i] = self.array[i-1]

    def _shiftArrayLeft(self, index):
        """shift subarray from [index..len(self)] to the left by one step
        
        Arguments:
            index {int} -- start position of the subarray we want to shift
        
        Complexity:
            BestCase {O(1)} -- if the index is of the Last element of the List
            WorstCase {O(N)} -- if we need to shift the whole array
        """
        if index < 0:
            index = index + len(self)
        for i in range(index, len(self)-1):
            self.array[i] = self.array[i+1]
    
    def _validIndex(self, index):
        """restrict the Index range so that it behave similar to python List Indexing
        
        Arguments:
            index {int} -- index of the array
        
        Returns:
            [bool] -- return True if positive or negative index not exceeds the number of item 
                      in the List
        """
        return (index >=0 and index < len(self) or (index <= -len(self) and index < 0)

    def sort(self, reverse=False):
        """use a stable sort on the ArrayList

        Current Sort Algorithm used is QuickSort with 
        pivot chosen at the middle of the list. 
        set reverse=True to Sort in descending order
        and reverse=False for ascending order
        
        Keyword Arguments:
            reverse {bool} -- the sorting order of the List (default: {False})
        
        Complexity:
            BestCase {O(NlogN)} -- if the pivot chosen always in the range of the list median
            WorstCase {O(N^2)} -- if the pivot chosen always nearly divide the partition the List
                                  to a list with one element and a list with n-1 elements
        """
        assert not self._isempty(), "List is empty"
        if not reverse:
            QuickSort(self.array)
        elif reverse:
            for i in range(len(self)):
                self.array[i] = -self.array[i]
            QuickSort(self.array)
            for i in range(len(self)):
                self.array[i] = -self.array[i]
