import os
import sys


def root_dir():
    """ Returns root director for this project """
    print("Current file is {}".format(__file__))
    print("above current file is {}".format(__file__+'/..'))
    print("Real path of above folder is {}".format(os.path.realpath(__file__ + '/..')))
    print("Dirname path realpath is {}".format(os.path.dirname(os.path.realpath(__file__ + '/..'))))
    return os.path.dirname(os.path.realpath(__file__ + '/..'))
    
    
if __name__ == "__main__":
    retVal = root_dir()
    print(retVal)
    print(sys.path)
