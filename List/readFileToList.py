from DLinkedList import DLinkedList
def readFile(filename):
    """function to read file and append each line to ArrayList
    
    Arguments:
        filename {string} -- name of the path to the file
    
    Returns:
        [DLinkedList] -- List containing each line of the file
    """
    infile = open(filename, 'r')
    contents = infile.readlines()
    infile.close()
    array = DLinkedList()
    for line in contents:
        row = line.rstrip("\n")
        array.append(row)
    return array
