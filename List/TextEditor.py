from ArrayList import ArrayList
from readFileToList import readFile

class TextEditor(object):
    def __init__(self):
        self._list = ArrayList()
        self._list.append("")

    # def _listToString(self, strList):
    #     string = ""
    #     for i in range(len(strList)):
    #         string += strList[i]
    #     return string

    def insert(self, index):
        print("Ctrl+C to exit insert")
        line = self._validLine(int(index)) 
        while True:
            try:
                string = input()
                self._list.insert(line, string)
                line += 1
            except KeyboardInterrupt:
                break
            except:
                pass

    # def insert(self, lineIndex, strList):
    #     lineIndex = int(lineIndex)
    #     string = self._listToString(strList)
    #     self._list.insert(lineIndex, string)
    
    def read(self, file):
        self._list = readFile(file)
        if len(self._list) == 0:
            self._list.append("")
    
    def _validLine(self, index):
        if not self._list._validIndex(index):
            raise IndexError("Index is out of range")
        line = index
        if line < 0:
            line = len(self._list) + line
        return line

    def print(self, num1=False, num2=False):
        if num1 and num2:
            num1, num2 = int(num1), int(num2)
            validNum1 = self._validLine(num1)
            validNum2 = self._validLine(num2)
            if not(validNum1 < validNum2):
                raise IndexError("Index is out of range")
            for i in range(num1, num2+1):
                print(self._list[i])
        elif num1:
            num1 = int(num1)
            print(self._list[num1])
        elif not num1:
            print(self._list)
    
    def write(self, filename):
        file = open(filename, "w+")
        file.write("\n".join(self._list))
        file.close()
    
    def delete(self, line):
        if len(self._list) == 1:
            raise IndexError("Can't delete anymore")
        if line:
            self._list.delete(int(line))
        else:
            self.__init__()
    
    def search(self, word):
        lowCase = word.lower()
        lowCaseTxt = self._lowerCase()
        occurences = ArrayList()
        for i in range(len(lowCaseTxt)):
            if lowCase in lowCaseTxt[i]:
                occurences.append(i)
        return occurences
            
    def _lowerCase(self):
        lower = ArrayList()
        for item in self._list:
            lower.append(item.lower())
        
        return lower
    
    def quit(self, arg):
        exit()

    def commandSelector(self, command, args):
        commandDict = {
            "insert": self.insert,
            "read"  : self.read,
            "write" : self.write,
            "print" : self.print,
            "delete": self.delete,
            "search": self.search,            
            "quit"  : self.quit
        }
        return commandDict[command](*args)

    def command2(self, inputCommand):
        command = inputCommand.split()
        args = [None] if command[-1] == command[0] else command[1:]
        self.commandSelector(command[0], args)
    
    def main(self):
        while True:
            print(">>",end="")
            option = input()
            try:
                self.command2(option)
            except Exception:
                print("?")

if __name__ == "__main__":
    editor = TextEditor()
    editor.main()