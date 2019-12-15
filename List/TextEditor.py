# from ArrayList import ArrayList
from DLinkedList import DLinkedList
from Stack import Stack
from readFileToList import readFile

class TextEditor(object):
    """
    text editor from FIT1008Sem2_2017 assigment 2 Task4.
    The line of document in the editor starts from 0.
    when you want to insert a string after the last line,
    you can use: insert #lines or insert -1 command to the editor

    Attributes:
        _list {List} -- a list of buffer for the txt file
        _undoable {tuple} -- tuple containing command that can be undone
        _undoList {Stack} -- Stack containing the the list of command to be undone
        _undoDict {dict} -- dictionary containing the key to the undo function
        __commandDict {dict} -- dictionary containing keys to the command
        _lines {int} -- number of lines in the document
    
    Methods:
        insert(index) -- keep inserting string to the position before index until KeyboardInterrupt is pressed.

        read(file) -- read a txt file line by line and append it to List buffer.
        
        print(num1="", num2="") -- print the string at line num1 if only provided num1.
                                   if num1 and num2 is provided, it will print the string from num1
                                   to num2 provided that num1 < num2 and both are valid line number
        
        write(filename) -- "write the buffer string from the list to a file with name == filename.
        
        delete(line) -- delete the string at position line in txt file.
                        if the list is empty, it will append empty string
                        to enable insertion of new string.
    
        search(word) -- search word and print the line numbers that contain the word.

        undo(None) -- undo insert, delete, and read command

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
        self._lines = 0
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
            "read"  : self._undoReset,
            "insert": self._undoInsert,
            "delete": self._undoDelete
        }
    
    def __len__(self):
        '''number of lines in current document'''
        return self._lines

    def _incrementLines(self, count=1):
        '''increment lines after insertion'''
        self._lines += count
    
    def _decrementLine(self, count=1):
        '''decrement line after delete'''
        self._lines -= count

    def insert(self, index):
        """
        keep inserting string to the position before index until KeyboardInterrupt is pressed.

        
        Arguments:
            index {str} -- index of the line we want to insert before
                           index must be a string that can be casted
                           to integer 
        """
        print("Ctrl+C to exit insert")
        start = self._validLine(index, True) 
        end = start
        flag = True
        while flag:
            try:
                string = input()
                self._list.insert(end, string)
                # increment the line to keep the insert in order
                end += 1
            except KeyboardInterrupt:
                flag = False
                if start == end:
                    self._undoList.pop()
                else:
                    self._incrementLines(end-start)
                    insertArg = self._undoList.pop()
                    insertArg.append(start)
                    insertArg.append(end)
                    self._undoList.push(insertArg)

    def read(self, file):
        """read a txt file line by line and append it to List buffer.
        the contain currently in the list will be saved to stack for
        undo action

        Arguments:
            file {str} -- path to txt document to be read
        """
        self._saveState()
        self._list = readFile(file)
        # added the last line for insertion when the document is empty
        self._list.append("")
        # store the number of lines of document
        self._lines = len(self._list)-1
    
    def _saveState(self):
        """save current self._list and self._undoList to stack before overwriting
        self._list with content of txt file and resetting the self._undoList.
        used for when we want to undo reading and going back to the state before we read the new txt file
        """
        topStack = self._undoList.pop()
        topStack.append(self._lines)
        topStack.append(self._list)
        self._undoList.push(topStack)

    def _calculateValidIndex(self, index, lenOfLines):
        """function to calculate the valid line number of argument given to TextEditor command

        the valid index for insertion will need to use the len(self._list) as lenOfLines due to
        the last index in self._list is used for insertion while the document is empty.
        
        as for deletion, the valid index for deletion will need to use self._lines for the 
        lenOfLines argument so that the last item in self._list won't be deleted to enable insertion
        for empty document.
        
        Arguments:
            index {int} -- the line number given by the editor command argument
            lenOfLines {int} -- the number of lines in accessible depend on the command type.
        
        Returns:
            [int] -- adjusted index to refer to the document line
        """
        line = index
        if line < 0:
            line += lenOfLines
        return line

    def _validLine(self, index, insert=False):
        """
        check whether the line argument is within the list index.
        if its within the list index, it will convert line to positive index.
        else raises IndexError

        Arguments:
            index {str} -- line number of the txt file. line must be castable to integer
            insert {bool} -- if insert is True, _validLine will evaluate the index based on
                            len(self._list) as the index range instead of number of lines in
                            document(self._lines) (default: {False})
        Raises:
            IndexError: raised when the index is out of txt line number range
        
        Returns:
            [int] -- return the converted index to valid line number
        """
        lenOfLines = self._lines if insert is False else len(self._list)
        index = int(index)
        if not ((0 <= index < lenOfLines) or (-lenOfLines <= index < 0)):
            raise IndexError("Index is out of range")
        return self._calculateValidIndex(index, lenOfLines)

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
    
    def delete(self, line, isUndo=False):
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
            # save the line to be deleted to stack if delete is not called by undo
            if not isUndo:
                topAction = self._undoList.pop()
                topAction.append(line)
                topAction.append(self._list[line])
                self._undoList.push(topAction)
            # delete the line in the list
            self._list.delete(line)
            self._decrementLine()
        else:
            # save the entire list to stack when we reset the editor
            if not isUndo:
                self._saveState()
            # save undo action list and restore it after reset
            tmpStack = self._undoList
            self.__init__()
            self._undoList = tmpStack
    
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
        for i in range(len(self)):
            lower.append(self._list[i].lower())
        
        return lower
    
    def undo(self, arg=None):
        """
        undo insert, delete, and read command
        
        Keyword Arguments:
            arg {None} -- if arg is give, exception is raised(default: {None})
        
        Returns:
            [function] -- function call to the function refer by the top command in undo stack
        
        Raises:
            IndexError: raised argument is given to undo command
        """
        if arg:
            raise ValueError
        undoAction = list(self._undoList.pop())
        return self._undoDict[undoAction[0]](*undoAction[1:])
    
    def _undoDelete(self, line, buffer):
        """undo the deletion from the position at line
        and replace it with the string/list before deletion 
        
        Arguments:
            line {int} -- the line that has been deleted 
            buffer {str,List} -- string/list that we want to insert/overwrite
        """
        if type(buffer) == str:
            self._list.insert(line, buffer)
            self._incrementLines()
        else:
            self._undoReset(line, buffer)

    def _undoInsert(self, start, end):
        """undo the insert operation to the _list
        
        Arguments:
            start {int} -- start line of insert
            end {int} -- end line of insert 
        """
        for _ in range(start, end):
            self.delete(start, True)

    def _undoReset(self, line, buffer):
        """reset the _list and restore the contents of _list with the value
        of _list before we read the txt file or delete the previous _list
        
        Arguments:
            line {int} -- the number of lines prior to resetting the document
            buffer{List} -- the list containing the document prior to reset
        """
        tmpStack = self._undoList
        self.delete(None, True)
        self._lines = line
        self._list = buffer
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
        except KeyError:
            raise KeyError
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
        print("Welcome to my text editor!\nbelow is the manual for the editor\n", self.__doc__)
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