from ArrayList import ArrayList
from readFileToList import readFile

class TextEditor(object):
    """text editor from FIT1008Sem2_2017 assigment 2 Task4.

    Attributes:
        _list {ArrayList} -- a list of buffer for the txt file
    
    Methods:
        insert(index) -- keep inserting string line by line until KeyboardInterrupt is pressed.

        read(file) -- read a txt file line by line and append it to ArrayList buffer.
        
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
        """create a new ArrayList as a buffer for txt file
        and append empty string so that we can insert to the empty text"""
        self._list = ArrayList()
        self._commandDict = {
            "insert": self.insert,
            "read"  : self.read,
            "write" : self.write,
            "print" : self.print,
            "delete": self.delete,
            "search": self.search,            
            "quit"  : self.quit,
            "man"   : self.man,
            "help" : self.help
        }
        self._list.append("")

    def insert(self, index):
        """keep inserting string line by line until KeyboardInterrupt is pressed.

        
        Arguments:
            index {str} -- index of the line we want to insert before
                           index must be a string that can be casted
                           to integer 
        """
        print("Ctrl+C to exit insert")
        line = self._validLine(index) 
        while True:
            try:
                string = input()
                self._list.insert(line, string)
                # increment the line to keep the insert in order
                line += 1
            except KeyboardInterrupt:
                break
            except:
                pass

    def read(self, file):
        """read a txt file line by line and append it to ArrayList buffer.
        
        Arguments:
            file {str} -- path to txt document to be read
        """
        self._list = readFile(file)
        if len(self._list) == 0:
            self._list.append("")
    
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
        """write the buffer string from the list to a file with name == filename.
        
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

        Arguments:
            line {str} -- string of line number that can be casted to integer
        """
        if line:
            line = self._validLine(line)
            self._list.delete(line)
            if self._list._isempty():
                self._list.append("")
        else:
            self.__init__()
    
    def search(self, word):
        """search word and print the line numbers that contain the word.
        
        Arguments:
            word {str} -- words that we want to find
        """
        lowCase = word.lower()
        lowCaseTxt = self._lowerCase()
        occurences = ArrayList()
        for i in range(len(lowCaseTxt)):
            if lowCase in lowCaseTxt[i]:
                occurences.append(i)
        print(occurences)
            
    def _lowerCase(self):
        """
        convert all the string in the list to lower case.
        called by self.search() for word comparison

        Returns:
            [ArrayList] -- list containin the lowercase copy of txt string
        """
        lower = ArrayList()
        for item in self._list:
            lower.append(item.lower())
        
        return lower
    
    def quit(self, arg):
        """called when we want to exit the text editor.
        
        Arguments:
            arg {None} -- dummy argument which is not used
        """
        exit()

    def man(self, arg):
        """show the available commands of the text editor.
        
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
        
        Returns:
            [function] -- function call to the method refer by command and pass the arg to the method
        """
        return self._commandDict[command](*args)

    def command(self, inputCommand):
        """command line input of text editor command
        
        Arguments:
            inputCommand {str} -- command name and args for the text editor main commands
        """
        command = inputCommand.split()
        args = [None] if command[-1] == command[0] else command[1:]
        self.commandSelector(command[0], args)
    
    def main(self):
        """function to run the text editor application"""
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