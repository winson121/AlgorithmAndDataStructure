# from ArrayList import ArrayList
from DLinkedList import DLinkedList
from Stack import Stack
from readFileToList import readFile

class TextEditor(object):
    """text editor from FIT1008Sem2_2017 assigment 2 Task4.

    Attributes:
        _list {List} -- a list of buffer for the txt file
    
    Methods:
        insert(index) -- keep inserting string line by line until KeyboardInterrupt is pressed.

        read(file) -- read a txt file line by line and append it to List buffer.
        
        print(num1="", num2="") -- print the string at line num1 if only provided num1.
                                   if num1 and num2 is provided, it will print the string from num1
                                   to num2 provided that num1 < num2 and both are valid line number
        
        write(filename) -- "write the buffer string from the list to a file with name == filename.
        
        delete(line) -- delete the string at position line in txt file.
                        if the list is empty, it will append empty string
                        to enable insertion of new string.
    
        search(word) -- search word and print the line numbers that contain the word.
    
        quit(arg) -- called when we want to exit the text editor.

        man(arg) -- show the available commands of the text editor.

        help(arg) -- this function will print the docstring of the command.
                     if no parameter passed to the comand, it will return man page instead.
    """
    def __init__(self):
        """create a new List as a buffer for txt file
        and append empty string so that we can insert to the empty text"""
        self._list = DLinkedList()
        self._list.append("")
        self._undoable = ("read", "delete", "insert")
        self._undoList = Stack()
        self._commandDict = {
            "insert": self.insert,
            "read"  : self.read,
            "write" : self.write,
            "print" : self.print,
            "delete": self.delete,
            "search": self.search,
            "undo"  : self.undo,            
            "quit"  : self.quit,
            "man"   : self.man,
            "help" : self.help
        }
        self._undoDict = {
            "read"  : self.delete
        }
        
    def insert(self, index):
        """
        keep inserting string line by line until KeyboardInterrupt is pressed.

        
        Arguments:
            index {str} -- index of the line we want to insert before
                           index must be a string that can be casted
                           to integer 
        """
        print("Ctrl+C to exit insert")
        start = self._validLine(index) 
        end = start
        while True:
            try:
                string = input()
                self._list.insert(end, string)
                # increment the line to keep the insert in order
                end += 1
            except KeyboardInterrupt:
                insertArg = self._undoList.pop()
                insertArg.append(start)
                insertArg.append(end)
                self._undoList.push(insertArg)
                break

    def read(self, file):
        """read a txt file line by line and append it to List buffer.
        the contain currently in the list will be saved to stack for
        undo action

        Arguments:
            file {str} -- path to txt document to be read
        """
        self._saveState()
        self._list = readFile(file)
    
    def _saveState(self):
        """save current self._list and self._undoList to stack before overwriting
        self._list with content of txt file and resetting the self._undoList.
        used for when we want to undo reading and going back to the state before we read the new txt file
        """
        topStack = self._undoList.pop()
        topStack.append(self._list)
        self._undoList.push(topStack)

    def _validLine(self, index):
        """
        check whether the line argument is within the list index.
        if its within the list index, it will convert line to positive index.
        else raises IndexError

        Arguments:
            index {str} -- line number of the txt file. line must be castable to integer
        
        Raises:
            IndexError: raised when the index is out of txt line number range
        
        Returns:
            [int] -- return the converted index to valid line number
        """
        index = int(index)
        if not self._list._validIndex(index):
            raise IndexError("Index is out of range")
        line = index
        if line < 0:
            line = len(self._list) + line
        return line

    def print(self, num1="", num2=""):
        """
        print the string at line num1 if only provided num1.
        if num1 and num2 is provided, it will print the string from num1
        to num2 provided that num1 < num2 and both are valid line number
        
        Arguments:
            num1 {str} -- starting line number of the txt file that
                          we want to print.(default: {""})
            num2 {str} -- end line number of the txt file that
                          we want to print.(default: {""})
        
        Raises:
            IndexError: raised when num1 >= num2
        """
        if num1 and num2:
            validNum1 = self._validLine(num1)
            validNum2 = self._validLine(num2)
            if not(validNum1 < validNum2):
                raise IndexError("Index is out of range")
            for i in range(validNum1, validNum2+1):
                print(self._list[i])
        elif num1:
            num1 = self._validLine(num1)
            print(self._list[num1])
        elif not num1:
            print(self._list)
    
    def write(self, filename):
        """
        write the buffer string from the list to a file with name == filename.
        
        Arguments:
            filename {str} -- the path to the file. new file created
                              if it doesn't exist
        """
        file = open(filename, "w+")
        file.write("\n".join(self._list))
        file.close()
    
    def delete(self, line):
        """
        delete the string at position line in txt file.
        if the list is empty, it will append empty string
        to enable insertion of new string.
        the deleted line/s will be saved to stack for undo action.

        Arguments:
            line {str} -- string of line number that can be casted to integer
        """
        if line is not None:
            line = self._validLine(line)
            # save the line to be deleted to stack
            # topAction = self._undoList.pop()
            # topAction.append(line)
            # topAction.append(self._list[line])
            # self._undoList.push(topAction)
            # delete the line in the list
            self._list.delete(line)
            if self._list._isempty():
                self._list.append("")
        else:
            # save the entire list to stack when we reset the editor
            # self._saveState()
            # save undo action list and restore it after reset
            # tmpStack = self._undoList
            self.__init__()
            # self._undoList = tmpStack
    
    def search(self, word):
        """search word and print the line numbers that contain the word.
        
        Arguments:
            word {str} -- words that we want to find
        """
        lowCase = word.lower()
        lowCaseTxt = self._lowerCase()
        occurences = DLinkedList()
        for i in range(len(lowCaseTxt)):
            if lowCase in lowCaseTxt[i]:
                occurences.append(i)
        print(occurences)
            
    def _lowerCase(self):
        """
        convert all the string in the list to lower case.
        called by self.search() for word comparison

        Returns:
            [List] -- list containin the lowercase copy of txt string
        """
        lower = DLinkedList()
        for item in self._list:
            lower.append(item.lower())
        
        return lower
    
    def undo(self, arg=None):
        undoAction = list(self._undoList.pop())
        if undoAction[0] == "read":
            self._undoReset(undoAction[1])
        elif undoAction[0] == "insert":
            self._undoInsert(undoAction[1:])
        # elif undoAction[0] == "delete":
        #     self._undoDelete(undoAction[1:])
    
    # def _undoDelete(self, arg):
    #     if len(arg) == 1:
    #         self._undoReset(arg)
    #     elif len(arg) == 2:
    #         if arg[-1] == "" and arg[0] >= len(self._list):
    #             return
    #         # self._list.insert(*arg)

    def _undoInsert(self, arg):
        """undo the insert operation to the _list
        
        Arguments:
            arg {List} -- list containing the starting and ending line of insertion 
        """
        start, end = arg
        for _ in range(start, end):
            self.delete(start)

    def _undoReset(self, arg):
        """reset the _list and restore the contents of _list with the value
        of _list before we read the txt file or delete the previous _list
        
        Arguments:
            arg {List} -- List containing the previous content before we overwrite it
        """
        tmpStack = self._undoList
        self.delete(None)
        self._list = arg
        self._undoList = tmpStack

    def quit(self, arg):
        """
        called when we want to exit the text editor.
        
        Arguments:
            arg {None} -- dummy argument which is not used
        """
        raise SystemExit

    def man(self, arg):
        """
        show the available commands of the text editor.
        
        Arguments:
            arg {None} -- dummy argument
        """
        print(self.__doc__)

    def help(self, command):
        """
        this function will print the docstring of the command.
        if no parameter passed to the comand, it will return man page instead.

        Arguments:
            command {function} -- the method of the text editor.
        """
        if command is None:
            self.man(command)
        else:
            print(self._commandDict[command].__doc__)

    def commandSelector(self, command, args):
        """
        dispatch table containing the list of command exposed by the 
        text editor interface to the user
        
        Arguments:
            command {str} -- key of the text editor command
            args {str} -- parameters of the command from stdin
        
        Raises:
            Exception: raised when number of arguments is invalid to the called function

        Returns:
            [function] -- function call to the method refer by command and pass the arg to the method
        """
        try:
            return self._commandDict[command](*args)
        except SystemExit:
            exit()
        except:
            # remove the latest command from the stack if the execution is incomplete
            self._undoList.pop()
            raise Exception

    def command(self, inputCommand):
        """command line input of text editor command
        
        Arguments:
            inputCommand {str} -- command name and args for the text editor main commands
        """
        command = inputCommand.split()
        args = [None] if command[-1] == command[0] else command[1:]
        if command[0] in self._undoable:
            self._undoList.push([command[0]]) 
            print(self._undoList)
        self.commandSelector(command[0], args)
    
    def main(self):
        """function to run the text editor application"""
        print("Welcome to my text editor!\nthis text editor can only edit .txt file")
        while True:
            print(">>",end="")
            option = input()
            try:
                self.command(option)
            except Exception:
                print("?")

if __name__ == "__main__":
    editor = TextEditor()
    editor.main()