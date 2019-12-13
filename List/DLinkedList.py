class Node:
    def __init__(self, item, next=None, prev=None):
        self.item = item
        self.next = next
        self.prev = prev
    
    def __str__(self):
        string = "item: {}, next:{}".format(str(self.item), str(self.next))
        return string

class ListIterator:
    '''Iterator for the DLinkedList'''
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
    """Implementation of Doubly Linked List Data Structure

    Attributes:
        _head {array} -- a pointer to the DLinkedList Nodes
        _count {int} -- number of nodes in the DLinkedList
    
    Methods:
        __len__() -- return the number of Nodes in the DLinkedList
        __str()__ -- overloading the built in print function to print each item in the linked list in a single line seperated by newline
        __contains__(item) -- check if item is in the DLinkedList
        __getitem__(index) -- get the item from DLinkedList at position index
        __setitem__(index, item) -- set the item in Node at position index to the item in param
        __eq__(other) -- check if the DLinkedList is equal to the other list
        append(item) -- append item at the end of the DLinkedList.
                        item will be appended from the tail of the list
        prepend(item) -- prepend item at the front of the DLinkedList.
                         item will be prepended from the head of the list
        insert(index, item) -- insert item to the DlinkedList at position before index
        remove(item) -- find item in the DLinkedList and delete the first node containing the item from the List.
        delete(index) -- delete node at position index in the DLinkedList.
        sort(reverse=False) -- sort the DLinkedList in ascending order by default
    """
    def __init__(self):
        self._head = None
        self._tail = None
        self._count = 0

    def __iter__(self):
        return ListIterator(self._head)

    def __len__(self):
        '''return the number of Nodes in the DLinkedList'''
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

    def prepend(self, item):
        """prepend item at the front of the DLinkedList.
        item will be prepended from the head of the list
        
        Arguments:
            item {python object} -- item to prepend to the list
        """
        try:
            new = Node(item, self._head)
            self._head.prev = new
            self._head = new
        except:
            self._head = self._tail = Node(item)
        
        self._count += 1

    def insert(self, index, item):
        """insert item to the DLinkedList at position before index
        
        Arguments:
            index {int} -- positive or negative integer
            item {python object} -- item to be inserted to the list before index
        
        Raises:
            IndexError: raised if not a valid index
        """
        try:
            node = self._getNode(index)
            new = Node(item, node, node.prev)
            node.prev.next = new
            node.prev = new
        except IndexError:
            raise IndexError
        except AttributeError:
            new = Node(item, self._head)
            self._head.prev = new
            self._head = new

        self._count += 1

    def _removeNode(self, node):
        """remove the link of the selected node from the DLinkedList
        
        Arguments:
            node {Node} -- node that we want to remove from the list
        """
        try:
            #general case when node deleted is not 
            node.next.prev = node.prev
            node.prev.next = node.next
        except:
            # delete item when only one node exist
            if self._head == self._tail:
                self._tail = self._head = None
            # if deleted node is head, reset head 
            elif node.prev is None:
                self._head = node.next
                self._head.prev = None
            # if deleted item is tail, reset tail
            elif node.next is None:
                self._tail = node.prev
                self._tail.next = None
        self._count -= 1

    def delete(self, index):
        """delete node at position index in the DLinkedList.

        Arguments:
            index {int} -- index position of item to be deleted
        """
        node = self._getNode(index)
        self._removeNode(node)

    def remove(self, item):
        """find item in the DLinkedList and delete the first node containing the item from the List.
        
        Arguments:
            item {python object} -- item that we want to search in the DLinkedList
        """
        node = self._head
        for _ in range(len(self)):
            if node.item == item:
                self._removeNode(node)
                break
            node = node.next
        
            
    def _isempty(self):
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
        if not self._validIndex(index):
            raise IndexError
        elif index >= 0:
            return self._getNodePos(index)
        else:
            return self._getNodeNeg(index)

    def _validIndex(self, index):
        '''restrict the Index range so that it behave similar to python List Indexing'''
        return (0 <= index < len(self)) or (-len(self) <= index < 0)

    def sort(self, reverse=False):
        """sort the DLinkedList in ascending order by default
        
        Keyword Arguments:
            reverse {bool} -- if reverse is True, sort by descending order (default: {False})
        """
        self._mergeSort(reverse)

    def _mergeSort(self, reverse):
        start = 0
        end = len(self)-1
        head = self._head
        self._head = self._mergeSortAux(head, start, end, reverse)
    
    def _mergeSortAux(self, head, start, end, reverse):
        # if list is empty or only one element in the list, it is sorted
        if head is None or head.next is None:
            return head
        mid = (start+end)//2
        # split the DLinkedList into 2 half
        middleNode = self._getMiddle(head, start, mid)
        secondHalf = middleNode.next
        # remove the links between the splitted LinkedList
        middleNode.next.prev = None
        middleNode.next = None
        # keep splitting the sublist into two half
        left = self._mergeSortAux(head, start, mid, reverse)
        right = self._mergeSortAux(secondHalf, mid+1, end, reverse)
        # sort and merge the two sublist
        return self._mergeArray(left, right, reverse)
    
    def _getMiddle(self, head, start, end):
        '''function to get the middle node of the linkedlist'''
        middle = head
        counter = end-start
        while counter:
            middle = middle.next
            counter -= 1
        return middle

    def _mergeArray(self, left, right, reverse):
        # set tail to the end of either left or right since we don't know which one reaches the end first
        if left is None:
            # reaches the end of the left sublist and set the end as tail
            self._tail = right
            return right
        if right is None:
            # reaches the end of the right sublist and set the end as tail
            self._tail = left
            return left

        node = None
        if not reverse:
            if left.item <= right.item:
                node = left
                node.next = self._mergeArray(node.next, right, reverse)
                # set the prev link of next node to current node after we get the next node
                node.next.prev = node
            else:
                node = right
                node.next = self._mergeArray(left, node.next, reverse)
                node.next.prev = node
        else:
            if left.item > right.item:
                node = left
                node.next = self._mergeArray(node.next, right, reverse)
                # set the prev link of next node to current node after we get the next node
                node.next.prev = node
            else:
                node = right
                node.next = self._mergeArray(left, node.next, reverse)
                node.next.prev = node
        return node

if __name__ == "__main__":
    alpha = DLinkedList()