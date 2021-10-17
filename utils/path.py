import os
import sys




def this_file():
    current_path = os.getcwd()
    python_path = '/'.join(sys.argv[0].split('/')[:-1])
    return os.path.join(current_path, python_path).rstrip('/')