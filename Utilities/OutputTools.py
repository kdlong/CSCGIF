import os
import errno
def makeDirectory(path):
    '''
    Make a directory, don't crash
    '''
    path = os.path.expanduser(path)
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: 
            raise
