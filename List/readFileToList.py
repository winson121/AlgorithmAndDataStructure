from ArrayList import ArrayList
def readFile(filename):
    """function to read file and append each line to ArrayList
    
    Arguments:
        filename {string} -- name of the path to the file
    
    Returns:
        [ArrayList] -- List containing each line of the file
    """
    infile = open(filename, 'r')
    contents = infile.readlines()
    infile.close()
    array = ArrayList()
    for line in contents:
        row = line.rstrip("\n")
        array.append(row)
    return array
