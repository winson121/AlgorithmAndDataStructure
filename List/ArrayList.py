from referential_array import build_array
from Sort.DivideAndConquer.QuickSort import quickSort as QuickSort

class ArrayList:
    def __init__(self, maxCapacity=10):
        self.array = build_array(maxCapacity)
        self._count = 0
    
    def __len__(self):
        return self._count
    
    def _isempty(self):
        return len(self) == 0
    
    def _isfull(self):
        return len(self) >= len(self.array)
    
    def __contains__(self, item):
        assert not self._isempty(); "list must not be empty"          
        for i in range(len(self)):
            if self.array[i] == item:
                return True
        return False

    def __getitem__(self, index):
        try:
            return self.array[index]
        except IndexError:
            raise IndexError("list index out of range")
        except TypeError:
            raise TypeError("list indices must be integers or slices, not", type(index))

    def __setitem__(self, index, item):
        try:
            self.array[index] = item 
        except IndexError:
            raise IndexError("list index out of range") 
    
    def __eq__(self, other):
        if not isinstance(self, other):
            return False
        
        for i in range(len(self)):
            if self.array[i] != other[i]:
                return False
        
        return True
        
    def append(self, item):
        assert not self._isfull(); "Array is full"
        self.array[self._count] = item
        self._count += 1
        
    def insert(self, index, item):
        assert not self._isfull(), "array is full"
        try:
            self._shiftArrayRight(index)
            self.array[index] = item
            self._count += 1
        except IndexError:
            raise IndexError
        

    def remove(self, item):
        assert not self._isempty(), "array is empty"
        for i in range(len(self)):
            if self.array[i] == item:
                self.delete(i)

    def delete(self, index):
        try:
            self._shiftArrayLeft(index)
            self._count -= 1
        except IndexError:
            raise IndexError

    def _shiftArrayRight(self, index):
        if index > len(self):
            raise IndexError
        for i in range(len(self), index, -1):
            self.array[i] = self.array[i-1]

    def _shiftArrayLeft(self, index):
        if index > len(self):
            raise IndexError
        for i in range(index, len(self)-1):
            self.array[i] = self.array[i+1]
    
    def sort(self):
        assert not self._isempty(), "List is empty"
        QuickSort(self.array)
if __name__=="__main__":
    a = ArrayList()