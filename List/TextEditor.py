from ArrayList import ArrayList
from readFileToList import readFile

class TextEditor(object):
    def __init__(self):
        self._list = None
    
    def _listToString(self, list):
        string = ""
        for item in list:
            string += item
        return string

    def insert(self, index, str):
        string = self._listToString(list):
        self._list.insert(index, string)
    
    def read(self, file):
        self._list = readFile(file)
    
    def _print_list(self, num1=None, num2=None):
        if num1 and num2:
            for i in range(num1, num2+1):
                print(self._list[i])
        elif num1:
            print(self._list[num1])
        elif not num1:
            self._list.print()
    
    def write(self, file):
        file = open(filename, "w+")
        file.write("\n".join(self._list()))
        file.close()
    
    def delete(self, line=None):
        if line:
            self._list.remove(line)
        else:
            self._list = ""
    
    def search(self, word):
        lowCase = word.lower()
        lowCaseTxt = self._lowerCase()
        occurences = ArrayList()
        for i in range(len(lowCaseTxt)):
            if word in lowCaseTxt[i]:
                occurences.append(i)
        return occurences
            
    def _lowerCase(self):
        lower = ArrayList()
        for item in self._list:
            lower.append(item.lower())
        
        return lower
    
    def command(self, inputCommand):
        command = inputCommand.split()
        if command:
            if command[0] == "insert":
                