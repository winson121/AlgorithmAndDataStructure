from DLinkedList import DLinkedList
class Stack:
    def __init__(self):
        """implementation of Stack ADT with DLinkedList

        Attributes:
            _stack {DLinkedList} -- the stack container.
        
        Methods:
            __len__() -- return the number of elements in the stack
            __str__() -- overloading the built in print function to print items in the stack in single line
            push(item) -- append item at the end of the stack
            pop() -- delete and return item at the end of the stack 
            peek() -- print the top item of the stack
            reset() -- emptied the stack
        """
        self._stack = DLinkedList()
    
    def __len__(self):
        '''return the number of elements in the stack'''
        return len(self._stack)

    def __str__(self):
        """overloading the built in print function to print items in the stack in single line
        
        Returns:
            [string] -- return: string contains every item in the stack
        """
        string = "["
        for i in range(len(self)):
            if i < len(self)-1:
                string += str(self._stack[i]) + ", "
            else:
                string += str(self._stack[i])
        string += "]"
        return string

    def push(self, item):
        """append item at the end of the stack
        
        Arguments:
            item {python object} -- item to be pushed on the stack
        """
        self._stack.append(item)
    
    def pop(self):
        """delete and return item at the end of the stack 
        
        Returns:
            [python object] -- item to be popped from the stack
        """
        return self._stack.pop()
    
    def peek(self):
        '''print the top item of the stack'''
        print(self._stack[-1])

    def reset(self):
        '''emptied the stack'''
        self.__init__()
