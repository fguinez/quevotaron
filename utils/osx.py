import os
import sys




def this_file():
    current_path = os.getcwd()
    python_path = '/'.join(sys.argv[0].split('/')[:-1])
    return os.path.join(current_path, python_path).rstrip('/')

def create_file(path):
    dirs = path.strip('/').split('/')[:-1]
    for i in range(len(dirs)):
        semipath = '/'+'/'.join(dirs[:i+1])
        if not os.path.exists(semipath):
            os.mkdir(semipath)
    open(path, 'a').close()