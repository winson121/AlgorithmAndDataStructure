import ctypes 
def build_array(size):
    """function to create array of references to Python Objects.
    
    Arguments:
        size {int} -- positive integer, the size of the array
    
    Returns:
        array -- array of python references with the given size.
    """
    assert size > 0; ValueError("Size must be positive!")
    assert isinstance(size, int); ValueError("Size must be integer!")
    array = (size * ctypes.py_object)()
    array[:] = size * [None]    # set each array index to None
    return array
