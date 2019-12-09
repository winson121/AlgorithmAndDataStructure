class Node:
    def __init__(self, item, next=None, prev=None):
        self.item = item
        self.next = next
        self.prev = prev
    
    def __str__(self):
        string = "item: {}, next:{}".format(str(self.item), str(self.next))
        return string

class ListIterator:
    def __init__(self, head):
        self.current = head
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            item = self.current.item
            self.current = self.current.next
            return item
        except:
            raise StopIteration

class DLinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._count = 0

    def __iter__(self):
        return ListIterator(self._head)

    def __len__(self):
        return self._count
    
    def __str__(self):
        """overloading the built in print function to print each item in the linked list in a single line seperated by newline
        
        Returns:
            [string] -- return: string contains every element in the list printed in 1 line for each element
        """
        string = ""
        for i in range(len(self)):
            if i < len(self)-1:
                string += str(self[i]) + "\n"
            else:
                string += str(self[i])
        
        return string

    def __getitem__(self, index):
        """get the item from DLinkedList at position index
        
        Arguments:
            index {int} -- index of the item. can be positive or negative
        
        Raises:
            IndexError: raised when its not valid index
        
        Returns:
            [python object] -- return item refered by node at position index in DLinkedList
        """
        if self._validIndex(index):
            return self._getNode(index).item
        else:
            raise IndexError

    def __setitem__(self, index, item):
        """set the item in Node at position index to the item in param
        
        Arguments:
            index {int} -- index position of item we want to access
            item {python object} -- the item that we want to set on node at the position index 
        
        Raises:
            IndexError: raised when not valid index
        """
        if not self._validIndex(index):
            raise IndexError
        
        self._getNode(index).item = item
        

    def __contains__(self, item):
        """check if item is in the DLinkedList
        
        Arguments:
            item {python object} -- item that we want to check
        
        Returns:
            [bool] -- return True if item is in the list, otherwise return False
        """
        result = False
        node = self._head
        for _ in range(len(self)):
            if node.item == item:
                result = True
                break
            node = node.next

        return result

    def __eq__(self, other):
        """check if the DLinkedList is equal to the other list
        
        Arguments:
            other {List, DLinkedList} -- List or DLinkedList object that we want to compare
        
        Returns:
            [bool] -- return True when two List contains exactly same contents
        """
        stat = True
        if not isinstance(other, (DLinkedList, list)):
            stat = False
        elif len(other) != len(self):
            stat = False
        else:
            node = self._head
            for i in range(len(other)):
                if node.item != other[i]:
                    stat = False
                    break
        return stat
    
    def append(self, item):
        """append item at the end of the DLinkedList.
        item will be appended from the tail of the list
        
        Arguments:
            item {python object} -- item to append to the list
        """
        try:
            new = Node(item, prev=self._tail)
            self._tail.next = new
            self._tail = new
        except:
            self._head = self._tail = Node(item)
        
        self._count += 1

    def _isEmpty(self):
        return len(self) == 0

    def _getNodeNeg(self, index):
        """get the node in DLinkedList at position index from the end(tail) of the List
        index must be negative value
        
        Arguments:
            index {int} -- the negative integer position of node we want to get from the tail.
        
        Returns:
            [Node] -- node object at position index in DLinkedList
        """
        node = self._tail
        for _ in range(-1, index, -1):
            node = node.prev
            
        return node

    def _getNodePos(self, index):
        """get the node in DLinkedList at position index from the head of the list
        index must be zero or positive value
        
        Arguments:
            index {int} -- the positive position of node we want to get from the head.
        
        Raises:
            IndexError: raised when its not a valid index
        
        Returns:
            [Node] -- node object at position index in DLinkedList
        """
        node = self._head
        for _ in range(index):
            node = node.next
            
        return node

    def _getNode(self, index):
        """get the node at position index in the DLinkedList from the head or tail.
        if index < 0, self._getNodeNeg(index) is called to search list from the tail
        if index >= 0, self._getNodePos(index) is called to search list from the head
        
        Arguments:
            index {int} -- positive or negative integer position of the list
        
        Raises:
            IndexError: raised if not self._validIndex(index)
        
        Returns:
            [Node] -- return node at position index in linked list
        """
        if not self._validIndex:
            raise IndexError
        elif index >= 0:
            return self._getNodePos(index)
        else:
            return self._getNodeNeg(index)

    def _validIndex(self, index):
        return (0 <= index < len(self)) or (-len(self) <= index < 0)
    
if __name__ == "__main__":
    a = DLinkedList()
    